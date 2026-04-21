import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ================= 配置区域 =================
API_KEY = "sk-84911bac3a264cbdb80f2ae0e0c34e40"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-math-plus" 
# ===========================================

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def clean_latex_markdown(text: str) -> str:
    """终极清洗函数：修复各种导致前端无法渲染的 LaTeX 格式问题"""
    if not text:
        return text
        
    text = text.replace('`', '')
    
    text = re.sub(r'\$\s+', '$', text) # 清理开头的空格
    text = re.sub(r'\s+\$', '$', text) # 清理结尾的空格
    
    text = text.replace('\\[', '$$').replace('\\]', '$$')
    text = text.replace('\\(', '$').replace('\\)', '$')
            
    return text


def generate_math_question(knowledge_point: str, difficulty: int = 2, question_type: str = "blank", rag_context: str = ""):
    """调用 Qwen 生成一道结构化的数学题"""

    system_prompt = """你是一个专业的高等数学出题专家。你的任务是根据用户提供的知识点生成一道高质量的数学题。
请严格遵守以下规则：
1. 【题干纯净】`content` 字段只能包含题目主体！**绝对禁止**在 `content` 中输出 A、B、C、D 选项及其内容。
2. 【选项格式】如果是选择题，选项内容必须存放在 `options` 字段中，且选项里的**数学公式必须用 $ 包裹**（例如 "$ \\frac{1}{2} $"）。如果是填空题，`options` 输出空字符串。
3. 【公式规范】数学公式请【必须且只能】使用 LaTeX 语法，用单个 $ 包裹内联公式，用 $$ 包裹块级公式。绝不能使用 Markdown 的反引号！
4. 【强制打草稿】你必须先在 explanation 字段中写出详尽的推导过程。经过严密计算后，再将最终结果填入 answer 字段。
5. 【强制输出JSON】必须严格按照给定的 JSON Schema 输出。
"""

    user_content = f"""
知识点: {knowledge_point}
难度: {difficulty} (1-5)
题型: {'选择题' if question_type == 'choice' else '填空题(答案为纯数字。尽量保持整数，如必须是小数，说明小数点后的位数)'}
"""

    if rag_context:
        user_content += f"\n以下是相关的参考资料，请参考其风格出题：\n{rag_context}\n"

    user_content += "\n请以 JSON 格式输出题目。"

    if question_type == "choice":
        options_schema = {
            "type": "object", 
            "description": "选择题的四个选项，选项中的数学公式必须被 $ 包裹",
            "properties": {
                "A": {"type": "string"},
                "B": {"type": "string"},
                "C": {"type": "string"},
                "D": {"type": "string"}
            },
            "required": ["A", "B", "C", "D"],
            "additionalProperties": False
        }
    else:
        options_schema = {
            "type": "string",
            "description": "这是填空题，此字段必须输出空字符串"
        }

    json_schema = {
        "name": "math_question_output",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string", 
                    "description": "题目的具体内容。绝对禁止在此字段中包含 A, B, C, D 选项文本！"
                },
                "explanation": {
                    "type": "string", 
                    "description": "详细的解题步骤和草稿过程"
                },
                "answer": {
                    "type": "string", 
                    "description": "最终正确答案。选择题填A/B/C/D，填空题填纯数字"
                },
                "options": options_schema
            },
            "required": ["content", "explanation", "answer", "options"],
            "additionalProperties": False
        }
    }

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            # 使用 JSON Schema 彻底锁死输出结构
            response_format={"type": "json_schema", "json_schema": json_schema}
        )

        raw_text = completion.choices[0].message.content
        print(f"【Debug】模型原始输出: {raw_text}") 

        result_json = json.loads(raw_text)

        # === 针对前端渲染的双重防御机制 ===
        
        # 1. 暴力清理题干：万一模型发疯在题干加了选项，直接用正则截断
        content_text = clean_latex_markdown(result_json.get('content', ''))
        content_text = re.sub(r'(\\n|\n)+[A-E]\..*$', '', content_text, flags=re.DOTALL)
        result_json['content'] = content_text

        # 2. 格式化选项
        if question_type == "blank":
            result_json['options'] = "" 
        else:
            opts = result_json.get('options', {})
            for key in ["A", "B", "C", "D"]:
                if key in opts:
                    opt_val = opts[key]
                    # 如果选项里有反斜杠 \ (比如 \frac) 但没有被 $ 包裹，强行给它穿上衣服
                    if '\\' in opt_val and '$' not in opt_val:
                        opt_val = f"${opt_val}$"
                    opts[key] = clean_latex_markdown(opt_val)
            result_json['options'] = json.dumps(opts, ensure_ascii=False)

        return result_json

    except Exception as e:
        print(f"调用 Qwen API 出错: {e}")
        return None

def auto_tag_question(question_content: str) -> str:
    # 保持原有逻辑不变
    system_prompt = """你是一个考研数学（高等数学）专家。
请根据用户提供的题目内容，将其归入最精确的细分知识点标签中。
常见的标签包括：
【函数极限，数列极限，连续、间断与导数，中值定理，导数应用，导数证明，积分，积分应用，重积分，多元微分概念，多元微分计算，微分方程，曲线积分，曲面积分，级数判敛，幂级数】
如果题目涉及多个知识点，请输出最核心的【一个】。
**严格要求**：只输出标签名称，不要带任何标点符号、前缀或解释，例如："函数极限"、"数列极限"、"连续、间断与导数"等。
"""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请为这道题打标：\n{question_content}"}
            ]
        )
        tag = completion.choices[0].message.content.strip()
        return tag
    except Exception as e:
        print(f"打标失败: {e}")
        return "未分类"
