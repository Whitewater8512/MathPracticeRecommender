import os
os.environ["IF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["OMP_NUM_THREADS"] = "4"

import database as db
import rag
import json
import llm_api
import random
import pandas as pd
from datetime import datetime
import numpy as np
import streamlit as st

@st.cache_resource
def load_mkr_weights():
    try:
        user_emb = np.load('checkpoints/mkr_user_emb.npy')
        item_emb = np.load('checkpoints/mkr_item_emb.npy')
        return user_emb, item_emb, True
    except Exception as e:
        return None, None, False

@st.cache_resource
def load_id_maps():
    try:
        with open('checkpoints/user_map.json', 'r') as f:
            u_map = json.load(f)
        with open('checkpoints/item_map.json', 'r') as f:
            i_map = json.load(f)
        return u_map, i_map
    except Exception:
        return {}, {}

# 全局调用一次（利用缓存）
USER_EMB, ITEM_EMB, MKR_LOADED = load_mkr_weights()
USER_TO_IDX, ITEM_TO_IDX = load_id_maps()

def get_mkr_score(user_id, q_id):
    u_idx = USER_TO_IDX.get(str(user_id))
    i_idx = ITEM_TO_IDX.get(str(q_id))

    if u_idx is not None and i_idx is not None:
        u_vector = USER_EMB[u_idx]
        i_vector = ITEM_EMB[i_idx]
        return np.dot(u_vector, i_vector)
    print(f"⚠️ 无法计算 MKR 分数，缺失用户或题目索引 (user_id: {user_id}, q_id: {q_id})")
    return 0.0

def recommend_next_step(user_id, current_kp, force_ai=False):
    local_q = None
    
    # 1. 如果不强制使用 AI，我们优先从本地题库找题
    if not force_ai:
        # 获取该知识点下，用户还没做对过的所有候选题目
        conn = db.sqlite3.connect(db.DB_FILE)
        df_candidates = pd.read_sql_query("""
            SELECT * FROM questions 
            WHERE knowledge_point = ? 
            AND q_id NOT IN (SELECT q_id FROM records WHERE user_id = ? AND is_correct = 1)
        """, conn, params=(current_kp, user_id))
        conn.close()

        if not df_candidates.empty:
            if MKR_LOADED:
                best_score = -float('inf')
                best_row_index = 0
                
                # 获取用户的 Embedding 向量
                # 注意：这里假设 user_id 直接对应矩阵索引，实际需转换 u_idx = user_id2idx[str(user_id)]
                u_idx = user_id % USER_EMB.shape[0] 
                u_vector = USER_EMB[u_idx]

                # 遍历所有候选题目，计算推荐得分
                for idx, row in df_candidates.iterrows():
                    q_id = row['q_id']
                    # 注意：同样需要索引映射 i_idx = item_id2idx[str(q_id)]
                    i_idx = q_id % ITEM_EMB.shape[0]
                    i_vector = ITEM_EMB[i_idx]
                    
                    # 核心：内积打分 (Score = User Embedding · Item Embedding)
                    score = np.dot(u_vector, i_vector)
                    
                    if score > best_score:
                        best_score = score
                        best_row_index = idx
                
                # 选出 MKR 得分最高的题目
                local_q = df_candidates.iloc[best_row_index].to_dict()
            # === 👆 MKR 逻辑结束 👆 ===
            else:
                # 降级方案：如果 MKR 没跑通，走原来的随机或者基于 BKT 难度的策略
                local_q = db.get_recommended_question(user_id, current_kp)

    # 2. 如果本地实在没题了，或者用户强行点了 "✨ AI 生成新题"，触发 RAG + LLM 逻辑
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
