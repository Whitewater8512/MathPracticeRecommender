import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

os.environ["TORCH_DEVICE"] = "cuda"
os.environ["WORKERS"] = "1"
os.environ["MARKER_VRAM_PER_GPU"] = "6"

import chromadb
from chromadb.utils import embedding_functions

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

# ================= 配置区域 =================
DATA_FOLDER = "datas"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "math_textbooks"
# ===========================================


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"已创建 {DATA_FOLDER} 文件夹，请将 PDF 放入其中。")

client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"description": "数学题库知识库"}
)

def load_pdfs_to_vector_db():
    """使用 marker-pdf 1.x 将 PDF 解析为高质量 Markdown 并存入向量库"""
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
    
    if not pdf_files:
        return

    # === 修改 1：查询数据库中已经处理过的文件列表 ===
    try:
        # 获取库中所有的元数据
        existing_data = collection.get(include=["metadatas"])
        existing_metadatas = existing_data.get("metadatas", [])
        # 提取出所有已存在的文件名
        processed_files = {meta["source"] for meta in existing_metadatas if meta and "source" in meta}
    except Exception as e:
        print(f"获取已处理文件列表失败: {e}")
        processed_files = set()

    # 过滤出还没处理的文件
    pending_files = [f for f in pdf_files if f not in processed_files]

    if not pending_files:
        print("所有 PDF 文件均已存在于知识库中，跳过。")
        return

    print(f"🚀 发现 {len(pending_files)} 个新文件等待处理。正在加载深度学习模型...")
    
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )

    for pdf_file in pending_files:
        pdf_path = os.path.join(DATA_FOLDER, pdf_file)
        print(f"📄 正在深度解析: {pdf_file}")
        
        # 每次循环初始化当前文件的存储列表
        documents = []
        metadatas = []
        ids = []
        
        try:
            # 1. 转换文档获取 rendered 对象
            rendered = converter(pdf_path)
            
            # 2. 从 rendered 对象中提取 Markdown 文本
            rendered_output = text_from_rendered(rendered)
            full_text = rendered_output[0] if isinstance(rendered_output, tuple) else rendered_output
            
            if not full_text:
                print(f"⚠️ {pdf_file} 提取的内容为空，跳过。")
                continue

            # 按固定长度切块 (Chunking)
            chunks = [full_text[i:i+1000] for i in range(0, len(full_text), 800)]
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({"source": pdf_file, "chunk_index": i})
                ids.append(f"{pdf_file}_{i}")
                
            # === 修改 2：每解析完一个文件，立刻写入数据库 (落盘) ===
            if documents:
                collection.add(documents=documents, metadatas=metadatas, ids=ids)
                print(f"✅ {pdf_file} 解析完成！成功写入 {len(documents)} 个文本块。")
                
        except Exception as e:
            print(f"❌ 解析 {pdf_file} 失败: {e}")

    print("🎉 所有新文件处理完毕！")

def retrieve_relevant_context(query: str, top_k: int = 2) -> str:
    """根据知识点检索相关的上下文"""
    if collection.count() == 0:
        return ""
        
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    context_list = results['documents'][0] if results['documents'] else []
    return "\n---\n".join(context_list)

def get_knowledge_base_stats() -> dict:
    """获取向量知识库的统计信息"""
    if collection is None:
        return {"total_chunks": 0, "total_files": 0, "files": []}
        
    try:
        # 1. 获取所有的文本块 (Chunks) 总数
        total_chunks = collection.count()
        
        if total_chunks == 0:
             return {"total_chunks": 0, "total_files": 0, "files": []}
             
        # 2. 获取所有的元数据以统计独立的 PDF 文件数
        existing_data = collection.get(include=["metadatas"])
        metadatas = existing_data.get("metadatas", [])
        
        # 使用集合 (set) 去重，提取所有不重复的文件名
        unique_files = {meta["source"] for meta in metadatas if meta and "source" in meta}
        
        return {
            "total_chunks": total_chunks,
            "total_files": len(unique_files),
            "files": sorted(list(unique_files))
        }
    except Exception as e:
        print(f"统计数据获取失败: {e}")
        return {"total_chunks": 0, "total_files": 0, "files": []}

# 自动运行知识库加载
load_pdfs_to_vector_db()