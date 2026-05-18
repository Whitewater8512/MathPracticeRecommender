import os
import re
import json
import time
import base64
import fitz  # PyMuPDF，极其轻量的 PDF 处理库
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# 载入环境变量
load_dotenv()

# 初始化智谱 API 客户端
DS_CLIENT = OpenAI(
    api_key=os.getenv("CLOUD_MODEL_API_KEY"), 
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

# 模型配置
VISION_MODEL = "glm-4v-plus"  # 用于看图写 Markdown 的视觉模型
KG_MODEL = "glm-5.1"          # 用于抽图谱关系的纯文本逻辑大模型

# 定义路径规范
RAW_PDF_DIR = "datas/raw_pdfs"
SILVER_DIR = "datas/silver"
GOLD_DIR = "datas/gold"
KG_MODEL_PATH = "knowledge_graph_model.json"

# 确保输出目录存在
for d in [RAW_PDF_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(d, exist_ok=True)

# ==========================================
# Phase 1: 视觉大模型处理 PDF -> Markdown (Silver)
# ==========================================
def pdf_page_to_base64(page) -> str:
    """将单页 PDF 渲染为高清图片并转为 base64"""
    # 放大系数，提高分辨率以保证下标和积分号的清晰度
    zoom_matrix = fitz.Matrix(2.0, 2.0) 
    pix = page.get_pixmap(matrix=zoom_matrix)
    img_data = pix.tobytes("png")
    return base64.b64encode(img_data).decode('utf-8')

def extract_markdown_from_vision_model(base64_img: str, max_retries=3) -> str:
    """调用云端视觉大模型解析单页内容"""
    system_prompt = """你是一个专业的学术文档排版专家。请仔细阅读图片中的考研数学内容，并将其转换为包含完整 LaTeX 公式的 Markdown 格式。
规则：
1. 绝对不要遗漏任何文字、定理和公式。
2. 独立公式使用 $$...$$，行内公式使用 $...$。
3. 请直接输出 Markdown 纯文本，不要包含 ```markdown 等代码块包裹符。"""

    for attempt in range(max_retries):
        try:
            response = DS_CLIENT.chat.completions.create(
                model=VISION_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
                        ]
                    }
                ],
                timeout=60
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"   ⚠️ 视觉解析失败 (重试 {attempt+1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)
    return ""

def process_pdfs_to_silver():
    """将 raw_pdfs 目录下的 PDF 全部转换为 Markdown"""
    print("\n👁️ [Phase 1] 启动云端视觉解析 (PDF -> Markdown)...")
    pdf_files = [f for f in os.listdir(RAW_PDF_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"   ⚠️ 在 {RAW_PDF_DIR} 未找到 PDF。")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(RAW_PDF_DIR, pdf_file)
        base_name = pdf_file.replace(".pdf", "")
        silver_path = os.path.join(SILVER_DIR, f"{base_name}.md")
        
        if os.path.exists(silver_path):
            print(f"   ⏭️ {pdf_file} 已存在 Markdown 缓存，跳过解析。")
            continue
            
        print(f"   📄 正在解析: {pdf_file}")
        doc = fitz.open(pdf_path)
        full_markdown = []
        
        for page_num in range(len(doc)):
            print(f"      - 处理第 {page_num + 1}/{len(doc)} 页...")
            b64_img = pdf_page_to_base64(doc[page_num])
            md_text = extract_markdown_from_vision_model(b64_img)
            full_markdown.append(md_text)
            
        # 落盘 Silver 数据
        with open(silver_path, "w", encoding="utf-8") as f:
            f.write("\n\n---\n\n".join(full_markdown))
        print(f"   ✅ 解析完成，输出至: {silver_path}")
        doc.close()

# ==========================================
# Phase 2 & 3: 语义切块与图谱抽取 (Gold & KG)
# ==========================================
def semantic_math_chunking(text: str, max_chunk_size: int = 800) -> List[str]:
    chunks = []
    current_chunk = ""
    paragraphs = re.split(r'\n\n+', text)
    
    def is_math_environment_closed(s: str) -> bool:
        display_math_count = len(re.findall(r'\$\$', s))
        begin_count = len(re.findall(r'\\begin\{.*?\}', s))
        end_count = len(re.findall(r'\\end\{.*?\}', s))
        return (display_math_count % 2 == 0) and (begin_count == end_count)

    for para in paragraphs:
        para = para.strip()
        if not para: continue
            
        proposed_chunk = current_chunk + "\n\n" + para if current_chunk else para
        
        if len(proposed_chunk) > max_chunk_size and current_chunk and is_math_environment_closed(current_chunk):
            chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk = proposed_chunk
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def extract_kg_relations_with_retry(chunk_text: str, max_retries: int = 3) -> List[Dict]:
    system_prompt = """你是一个考研数学知识图谱构建专家。
请分析输入的文本，提取其中的数学知识点，并判断它们之间的**前置依赖关系**。
输出格式必须是严格的 JSON 对象，包含一个 "relations" 数组。
字段说明：
- source: 前置知识点
- target: 后继知识点
- weight: 依赖强度 (0.0 到 1.0 的浮点数)

示例：
{
  "relations": [
    {"source": "极限概念", "target": "连续性", "weight": 0.9},
    {"source": "导数", "target": "泰勒展开", "weight": 0.85}
  ]
}
如果文本中没有明显的依赖关系，请返回 {"relations": []}。"""

    for attempt in range(max_retries):
        try:
            completion = DS_CLIENT.chat.completions.create(
                model=KG_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": chunk_text}
                ],
                response_format={"type": "json_object"},
                timeout=30 
            )
            raw_text = completion.choices[0].message.content
            result_json = json.loads(raw_text)
            return result_json.get("relations", [])
            
        except Exception as e:
            print(f"   ⚠️ 抽取关系失败 (重试 {attempt + 1}/{max_retries}): {e}")
            time.sleep(2 ** attempt) 
            
    return []

def process_md_to_graph():
    print("\n🧠 [Phase 2] 启动语义切块与图谱抽取...")
    
    global_kg = []
    if os.path.exists(KG_MODEL_PATH):
        try:
            with open(KG_MODEL_PATH, "r", encoding="utf-8") as f:
                global_kg = json.load(f)
            print(f"   ✅ 载入现有图谱数据，边数: {len(global_kg)}")
        except Exception:
            print("   ⚠️ 现有图谱数据解析失败，将重新构建。")

    silver_files = [f for f in os.listdir(SILVER_DIR) if f.endswith(".md")]
    
    for file_name in silver_files:
        silver_path = os.path.join(SILVER_DIR, file_name)
        base_name = file_name.replace(".md", "")
        
        with open(silver_path, "r", encoding="utf-8") as f:
            full_text = f.read()
            
        chunks = semantic_math_chunking(full_text)
        print(f"   📄 文件 {file_name} 切分为 {len(chunks)} 个 Chunk。")
        
        for i, chunk in enumerate(chunks):
            gold_filename = f"{base_name}_chunk_{i}.md"
            gold_path = os.path.join(GOLD_DIR, gold_filename)
            
            if os.path.exists(gold_path):
                continue
                
            with open(gold_path, "w", encoding="utf-8") as gf:
                gf.write(chunk)
                
            print(f"      🔍 正在抽取关系: {gold_filename}...")
            relations = extract_kg_relations_with_retry(chunk)
            if relations:
                global_kg.extend(relations)
                
                with open(KG_MODEL_PATH, "w", encoding="utf-8") as kg_f:
                    json.dump(global_kg, kg_f, ensure_ascii=False, indent=2)

    print("\n🧹 [Phase 3] 清洗并合并图谱重复边...")
    unique_edges = {}
    for edge in global_kg:
        key = f"{edge['source']}->{edge['target']}"
        if key not in unique_edges:
            unique_edges[key] = edge
        else:
            unique_edges[key]['weight'] = max(unique_edges[key]['weight'], edge['weight'])

    with open(KG_MODEL_PATH, "w", encoding="utf-8") as f:
        json.dump(list(unique_edges.values()), f, ensure_ascii=False, indent=2)
        
    print(f"🎉 流水线全链路执行完毕！最终图谱包含 {len(unique_edges)} 条依赖边。")

if __name__ == "__main__":
    # 执行流：先搞定视觉，再搞定逻辑
    process_pdfs_to_silver()
    process_md_to_graph()