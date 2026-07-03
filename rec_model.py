import database as db
import rag
from graph_rag import GraphRAG
from graph_kt import ConceptGraphKT
import llm_api
import random
import pandas as pd
import streamlit as st
import redis
import threading
import json

# 初始化新的知识图谱引擎
# kg_engine = GraphRAG(db_path=db.DB_FILE)
@st.cache_resource(show_spinner="正在初始化知识图谱与向量引擎...")
def get_kg_engine():
    print("\n🚀 [系统初始化] 正在加载 GraphRAG 引擎...")
    return GraphRAG(db_path=db.DB_FILE)

# 初始化 Redis 客户端 (设置 decode_responses=True 确保拿到的直接是字符串)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True,
                           socket_timeout=3, socket_connect_timeout=3)
POOL_MAX_SIZE = 3  # 缓存池最大容量
POOL_THRESHOLD = 2 # 缓存池安全水位

def async_fill_pool(user_id, target_kp, difficulty, q_type, count=1):
    pool_key = f"q_pool:{user_id}:{target_kp}:{difficulty}"
    lock_key = f"lock:{pool_key}" 
    
    # 【优化1】将锁的过期时间从 30 秒延长到 120 秒，防止大模型生成慢导致锁提前失效、引发并发拥堵
    if not redis_client.set(lock_key, "1", ex=120, nx=True):
        print(f"🔒 [跳过任务] 队列 {pool_key} 正在补货中，避免并发重复请求...")
        return
        
    try:
        for _ in range(count):
            print(f"🔄 [异步预生成] 正在为 User:{user_id} 补给 {target_kp} ...")
            context = rag.retrieve_relevant_context(target_kp)
            new_q = llm_api.generate_math_question(
                knowledge_point=target_kp, difficulty=difficulty,
                question_type=q_type, rag_context=context, use_cloud=True
            )
            if new_q:
                # 存入数据库
                new_id = db.insert_ai_question(
                    content=new_q['content'], kp=target_kp, diff=difficulty,
                    q_type=q_type, options=new_q['options'],
                    answer=new_q['answer'], explanation=new_q.get('explanation', '')
                )
                
                full_q = {
                    "q_id": new_id, 
                    "content": new_q['content'],
                    "knowledge_point": target_kp,
                    "difficulty": difficulty,
                    "question_type": q_type,
                    "options": new_q['options'],
                    "answer": new_q['answer'],
                    "explanation": new_q.get('explanation', '')
                }
                
                # 推入 Redis 队列
                redis_client.rpush(pool_key, json.dumps(full_q))
                print(f"✅ [异步预生成] 完成！当前池容量: {redis_client.llen(pool_key)}")
            else:
                print("⚠️ [异步预生成] 单次生成失败，可能触发了API限流。")
    finally:
        # 任务完成，释放锁
        redis_client.delete(lock_key)

def recommend_next_step(user_id, current_kp, force_ai=False):
    local_q = None
    target_kp = current_kp
    kg_engine = get_kg_engine()

    records = db.get_user_records(user_id)
    graph_kt = ConceptGraphKT(kg_engine.kg)
    user_graph_scores = graph_kt.update_user_state(records)
    
    acc, total = db.get_raw_stats(user_id, current_kp)
    rec_coef = user_graph_scores.get(current_kp, 15.0)
    
    if rec_coef < 30 and not force_ai:
        recommended_kp, path_logs = kg_engine.dynamic_attention_routing(current_kp, user_graph_scores)
        if recommended_kp != current_kp:
            target_kp = recommended_kp
            st.session_state.path_logs = path_logs 
            st.session_state.recommended_kp = recommended_kp
            print(f"💡 触发图谱降维：推荐前置节点 {target_kp}")

    difficulty = 1
    if rec_coef > 85: difficulty = 4
    elif rec_coef > 65: difficulty = 3
    elif rec_coef > 40: difficulty = 2

    # 查找本地题目
    if not force_ai:
        conn = db.sqlite3.connect(db.DB_FILE)
        df_candidates = pd.read_sql_query("""
            SELECT * FROM questions 
            WHERE knowledge_point = ? 
            AND difficulty <= ?
            AND q_id NOT IN (SELECT q_id FROM records WHERE user_id = ? AND is_correct = 1)
            ORDER BY ABS(difficulty - ?) ASC LIMIT 1
        """, conn, params=(target_kp, difficulty + 1, user_id, difficulty))
        conn.close()

        if not df_candidates.empty:
            local_q = df_candidates.iloc[0].to_dict()

    # 3. LLM 实时生成兜底 (接入 Redis)
    if local_q is None or force_ai:
        q_type = random.choice(["choice", "blank"])
        pool_key = f"q_pool:{user_id}:{target_kp}:{difficulty}"
        
        print(f"\n☁️ 尝试从 Redis 缓存池获取: {pool_key}")
        
        # [核心] 从池中取题
        cached_q_str = redis_client.lpop(pool_key)
        
        if cached_q_str:
            ai_q = json.loads(cached_q_str)
            print("⚡ [缓存命中] 秒级返回预生成题目！")
            
            # 获取被拿走一题后的当前剩余量
            current_len = redis_client.llen(pool_key)
            if current_len < POOL_THRESHOLD:
                fill_count = POOL_MAX_SIZE - current_len
                print(f"📉 [水位告警] 当前剩余 {current_len} 题，启动后台补充 {fill_count} 题...")
                threading.Thread(target=async_fill_pool, args=(user_id, target_kp, difficulty, q_type, fill_count)).start()
                
            return "ai (cached)", ai_q
            
        else:
            print(f"⏳ [缓存未命中] 难度 {difficulty} 的题库为空！启动后台补给...")
            # 1. 马上让后台去补充满目标难度的题
            threading.Thread(target=async_fill_pool, args=(user_id, target_kp, difficulty, q_type, POOL_MAX_SIZE)).start()
            
            # 2. 尝试从相邻难度 (先找低一档，再找高一档) 借题应急，拒绝让用户死等
            fallback_diffs = [difficulty - 1, difficulty + 1]
            for fb_diff in fallback_diffs:
                if 1 <= fb_diff <= 5: # 确保难度在合理范围内
                    fb_pool_key = f"q_pool:{user_id}:{target_kp}:{fb_diff}"
                    fb_cached = redis_client.lpop(fb_pool_key)
                    if fb_cached:
                        print(f"🔀 [丝滑降级] 从相邻难度 {fb_diff} 借到题目，实现 0 秒等待！")
                        return "ai (cached_fallback)", json.loads(fb_cached)
            
            # 3. 兜底中的兜底：如果连相邻难度的池子都被榨干了，才被迫同步生成
            print("⚠️ [彻底没题] 所有相邻缓存均为空，被迫触发最终同步生成...")
            context = rag.retrieve_relevant_context(target_kp)
            new_q = llm_api.generate_math_question(
                knowledge_point=target_kp, difficulty=difficulty, question_type=q_type, rag_context=context, use_cloud=True
            )
            
            if new_q:
                print(f"✅ [系统日志] 云端大模型同步出题成功！")
                new_id = db.insert_ai_question(
                    content=new_q['content'], kp=target_kp, diff=difficulty,
                    q_type=q_type, options=new_q['options'], answer=new_q['answer'], explanation=new_q.get('explanation', '')
                )
                ai_q = {
                    "q_id": new_id, "content": new_q['content'], "knowledge_point": target_kp,
                    "difficulty": difficulty, "question_type": q_type, "options": new_q['options'],
                    "answer": new_q['answer'], "explanation": new_q.get('explanation', '')
                }
                return "ai", ai_q
            else:
                print("❌ [致命错误] LLM出题失败。请检查 API_KEY 或网络限制。")
                return "ai", None

    return "local", local_q