import os
os.environ["IF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["OMP_NUM_THREADS"] = "4"

import database as db
import rag
import llm_api
import random
import pandas as pd
from datetime import datetime

def recommend_next_step(user_id, current_kp, force_ai=False):
    """
    决策中心：增加 force_ai 参数，并实现 AI 题目持久化
    """
    # 1. 只有在不强制 AI 且 随机概率未命中时，才尝试从本地找题
    local_q = None
    if not force_ai and random.random() > 0.2:
        local_q = db.get_recommended_question(user_id, current_kp)

    # 2. 如果本地没题，或命中 AI 逻辑，或强制 AI
    if local_q is None or force_ai:
        context = rag.retrieve_relevant_context(current_kp)

        # 根据熟练度动态决定难度
        acc, _, rec_coef = db.calculate_proficiency(user_id, current_kp)
        difficulty = 1
        if rec_coef > 85: difficulty = 4
        elif rec_coef > 65: difficulty = 3
        elif rec_coef > 40: difficulty = 2

        q_type = random.choice(["choice", "blank"])

        # 调用 LLM 生成题目
        new_q = llm_api.generate_math_question(
            knowledge_point=current_kp,
            difficulty=difficulty,
            question_type=q_type,
            rag_context=context
        )

        if new_q:
            new_id = db.insert_ai_question(
                content=new_q['content'],
                kp=current_kp,
                diff=difficulty,
                q_type=q_type,
                options=new_q['options'],
                answer=new_q['answer']
            )
    
            ai_q = {
                "q_id": new_id, 
                "content": new_q['content'],
                "knowledge_point": current_kp,
                "difficulty": difficulty,
                "question_type": q_type,
                "options": new_q['options'],
                "answer": new_q['answer']
            }
            return "ai", ai_q

    return "local", local_q

def batch_auto_tag_database(force_all=False):
    """
    自动扫描并打标
    :param force_all: 是否强制对所有题目重新打标
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 启动 AI 自动打标程序...")
    
    # 根据参数选择是“只打未分类”还是“全部重打”
    if force_all:
        questions_to_tag = db.get_all_questions()
        print(f"模式：强制全量重打标 (共 {len(questions_to_tag)} 道题)")
    else:
        questions_to_tag = db.get_untagged_questions()
        print(f"模式：仅处理未分类题目 (共 {len(questions_to_tag)} 道题)")

    if not questions_to_tag:
        print("💡 题库中没有符合条件的题目，任务结束。")
        return
        
    success_count = 0
    for i, q in enumerate(questions_to_tag):
        print(f"[{i+1}/{len(questions_to_tag)}] 正在处理题目 ID: {q['q_id']} ... ", end="")
        
        # 提取题干的前 20 个字符作为日志显示
        short_content = q['content'][:20].replace('\n', '') + "..."
        
        new_tag = llm_api.auto_tag_question(q['content'])
        
        if new_tag and new_tag != "未分类":
            db.update_question_tag(q['q_id'], new_tag)
            print(f"✅ 成功! 标签更新为: 【{new_tag}】")
            success_count += 1
        else:
            print(f"❌ 失败 (AI 未给出有效标签)")

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✨ 打标任务完成！共成功处理 {success_count} 道题。")
    
    # 结束后展示数据库现状
    print("\n" + "="*50)
    print("📊 当前题库数据预览：")
    all_data = db.get_all_questions()
    if all_data:
        df = pd.DataFrame(all_data)
        # 仅显示 ID、内容摘要和标签
        df['content_preview'] = df['content'].str.slice(0, 30) + "..."
        print(df[['q_id', 'knowledge_point', 'content_preview']].to_string(index=False))
    print("="*50)

if __name__ == "__main__":
    print("准备开始 AI 自动打标")
    db.init_db()
    batch_auto_tag_database(force_all=True)
    print("AI 自动打标完成")
    print("现在你可以使用streamlit run app.py 来查看推荐结果")
