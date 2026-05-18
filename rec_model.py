import database as db
import rag
from graph_rag import GraphRAG
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
POOL_THRESHOLD = 3 # 缓存池安全水位

def async_fill_pool(user_id, target_kp, difficulty, q_type, count=1):
    pool_key = f"q_pool:{user_id}:{target_kp}:{difficulty}"
    lock_key = f"lock:{pool_key}" # 🌟 新增：线程锁
    
    # 【优化】利用 Redis 的 SETNX 实现简单的并发锁，防止重复启动补货线程
    # 如果该队列已经在补货中，直接放弃本次线程启动
    if not redis_client.set(lock_key, "1", ex=30, nx=True):
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
                pool_key = f"q_pool:{user_id}:{target_kp}:{difficulty}"
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

    # 1. 画像诊断
    acc, _, rec_coef = db.calculate_proficiency(user_id, current_kp)
    
    # 2. 知识图谱自适应降维
    if rec_coef < 30 and not force_ai:
        # user_bkt_scores = {node: db.calculate_proficiency(user_id, node)[2] for node in kg_engine.kg.nodes}
        user_bkt_scores = db.get_all_bkt_scores(user_id, kg_engine.kg.nodes)
        recommended_kp, path_logs = kg_engine.dynamic_attention_routing(current_kp, user_bkt_scores)

        if recommended_kp != current_kp:
            target_kp = recommended_kp
            st.session_state.path_logs = path_logs 
            st.session_state.recommended_kp = recommended_kp
            print(f"💡 触发图谱降维：推荐前置节点 {target_kp}")

    # 动态难度判定
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
            
            # 检查水位，低水位则后台补充
            if redis_client.llen(pool_key) < POOL_THRESHOLD:
                threading.Thread(target=async_fill_pool, args=(user_id, target_kp, difficulty, q_type, 2)).start()
                
            return "ai (cached)", ai_q
        else:
            print("⏳ [缓存未命中] 同步等待生成，并启动后台补给...")
            # 启动后台多生成几道备用
            threading.Thread(target=async_fill_pool, args=(user_id, target_kp, difficulty, q_type, POOL_THRESHOLD)).start()
            
            # 本次阻塞等待生成
            context = rag.retrieve_relevant_context(target_kp)
            new_q = llm_api.generate_math_question(
                knowledge_point=target_kp, difficulty=difficulty, question_type=q_type, rag_context=context, use_cloud=True
            )
            
            if new_q:
                print(f"✅ [系统日志] 云端大模型同步出题成功！")
                new_id = db.insert_ai_question(
                    content=new_q['content'],
                    kp=target_kp,
                    diff=difficulty,
                    q_type=q_type,
                    options=new_q['options'],
                    answer=new_q['answer'],
                    explanation=new_q.get('explanation', '')
                )
                ai_q = {
                    "q_id": new_id, 
                    "content": new_q['content'],
                    "knowledge_point": target_kp,
                    "difficulty": difficulty,
                    "question_type": q_type,
                    "options": new_q['options'],
                    "answer": new_q['answer'],
                    "explanation": new_q.get('explanation', '')
                }
                return "ai", ai_q
            else:
                print("❌ [致命错误] LLM出题失败。请检查 API_KEY 或网络限制。")
                return "ai", None # 安全地返回 None，UI 会正常显示“加载失败”提示

    return "local", local_q