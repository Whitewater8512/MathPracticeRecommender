import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 本地 Qwen 部署
LOCAL_CLIENT = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")
LOCAL_MODEL = "/root/autodl-tmp/MPR/models/Qwen2.5-Math-7B-Instruct"

# 云端 大模型
CLOUD_CLIENT = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)
CLOUD_MODEL = "deepseek-v4-flash"

def clean_latex_markdown(text: str) -> str:
    if not text: return text
    text = text.replace('`', '')
    text = re.sub(r'\$\s+', '$', text)
    text = re.sub(r'\s+\$', '$', text)
    text = re.sub(r'\\underline\{\\hspace\{.*?\}\}', '______', text)
    text = text.replace('\\[', '$$').replace('\\]', '$$')
    text = text.replace('\\(', '$').replace('\\)', '$')
    return text

def generate_math_question(knowledge_point: str, difficulty: int = 2, question_type: str = "blank", rag_context: str = "", use_cloud: bool = True):
    system_prompt = """你是一个专业的高等数学出题专家。你的任务是根据用户提供的知识点生成一道高质量的数学题。
请严格遵守以下规则：
1. 【题干纯净】`content` 字段只能包含题目主体！**绝对禁止**在 `content` 中输出选项及其内容。
2. 【选项格式】选择题选项必须存放在 `options` 字段。**严厉警告：选项里的任何数字、字母、分数或公式，都必须严格使用 $ 包裹！**（例如：必须输出 "$0$" 或 "$\\frac{1}{2}$"，绝对不能只写 "0" 或 "\\frac{1}{2}"）。填空题 `options` 输出空字符串。
3. 【填空占位符】如果是填空题，题干中的待填空位置请严格使用 6 个纯文本下划线 `______` 表示（例如：“该极限的值为 ______”）。**绝对禁止**使用 `\\underline{\\hspace{...}}` 或 `\\fill` 等 LaTeX 占位指令！
4. 【公式规范】数学公式必须使用标准 LaTeX。
   - 在 JSON 字符串中，所有 LaTeX 反斜杠必须双写！例如：输出 "\\\\frac{1}{2}" 而不是 "\\frac{1}{2}"。
   - 独立公式使用 $$ 包裹，行内公式使用 $ 包裹。
   - 禁止转义下划线！直接输出 "_"，不要输出 "\\_"。
5. 【PoT 推理】在 `explanation` 字段中必须包含严密的【思路】和【推导】过程，然后再将最终答案填入 `answer` 字段。
6. 【强制输出 JSON】必须严格按照给定的格式输出 JSON。
7. 【填空题答案限制】填空题的 `answer` 必须且只能是具体的整数或分数（如 "1", "-2", "1/2"）。绝对禁止出现小数、e、\\pi 等无理数，也禁止包含任何变量字母。

---
【示例 1：选择题】
输入: 知识点: 函数极限, 难度: 2, 题型: choice
输出:
{
  "content": "求极限 $\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin 3x}{x}$ 的值（ ）",
  "explanation": "【思路】本题考察等价无穷小替换。\\\\n【推导】当 $x \\\\to 0$ 时，$\\\\sin 3x \\\\sim 3x$。因此原式 = $\\\\lim_{x \\\\to 0} \\\\frac{3x}{x} = 3$。选项 C 正确。",
  "answer": "C",
  "options": {
    "A": "0",
    "B": "1",
    "C": "3",
    "D": "不存在"
  }
}

【示例 2：填空题】
输入: 知识点: 导数计算, 难度: 1, 题型: blank
输出:
{
  "content": "已知函数 $f(x) = x^3 - 2x + 1$，则 $f'(1) = $ ______",
  "explanation": "【思路】先求导函数，再代入数值计算。\\\\n【推导】因为 $f'(x) = 3x^2 - 2$，所以 $f'(1) = 3(1)^2 - 2 = 1$。",
  "answer": "1",
  "options": ""
}
"""

    user_content = f"""
【输入】
知识点: {knowledge_point}
难度: {difficulty} (1-5)
题型: {'choice' if question_type == 'choice' else 'blank'}
参考上下文: {rag_context}
"""
    json_schema = {
        "name": "math_question",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "explanation": {"type": "string", "description": "必须包含详细推导过程"},
                "answer": {"type": "string"},
                "options": {
                    "type": "object",
                    "properties": {
                        "A": {"type": "string"}, "B": {"type": "string"},
                        "C": {"type": "string"}, "D": {"type": "string"}
                    }
                }
            },
            "required": ["content", "explanation", "answer"]
        }
    }

    try:
        # 动态路由：高难度题目 (diff >= 4) 或明确要求时，切换至云端大模型增强推理
        # if use_cloud or difficulty >= 4:
        #     completion = CLOUD_CLIENT.chat.completions.create(
        #         model=CLOUD_MODEL,
        #         messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
        #         response_format={"type": "json_object"}
        #     )
        # else:
        #     completion = LOCAL_CLIENT.chat.completions.create(
        #         model=LOCAL_MODEL,
        #         messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
        #         extra_body={"guided_json": json_schema['schema']}
        #     )
        completion = CLOUD_CLIENT.chat.completions.create(
            model=CLOUD_MODEL,
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )

        raw_text = completion.choices[0].message.content
        result_json = json.loads(raw_text)

        result_json['content'] = clean_latex_markdown(result_json.get('content', ''))
        
        if question_type == "blank":
            result_json['options'] = ""
        else:
            opts = result_json.get('options', {})
            result_json['options'] = json.dumps({k: clean_latex_markdown(v) for k, v in opts.items()}, ensure_ascii=False)

        return result_json
    except Exception as e:
        print(f"LLM 生成失败: {e}")
        return None