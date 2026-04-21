import os
import pandas as pd
import streamlit as st
import database as db
import llm_api as llm_api
import rag as rag
import rec_model
import json

# 初始化数据库（首次运行会重建表结构，插入新例题）
db.init_db()

# --- 页面全局配置 ---
st.set_page_config(page_title="智能数学推题系统", page_icon="📐", layout="wide")

# --- Session State 全局状态管理（兼容原有逻辑，新增题型相关状态）---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_kp' not in st.session_state:
    st.session_state.current_kp = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'page' not in st.session_state:
    st.session_state.page = "login" # 页面路由：login, main, report
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False # 控制提交后状态

# --- 页面跳转回调函数 ---
def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.page = "login"
    st.session_state.answer_submitted = False

def go_to_report():
    st.session_state.page = "report"
    st.session_state.answer_submitted = False

def go_to_main():
    st.session_state.page = "main"
    st.session_state.current_q = None 
    st.session_state.answer_submitted = False

def load_new_question(force_ai=False):
    """使用推荐引擎加载题目，支持强制 AI 模式"""
    if st.session_state.current_kp:
        # 统一调用 rec_model
        source, q = rec_model.recommend_next_step(
            st.session_state.user_id, 
            st.session_state.current_kp, 
            force_ai=force_ai
        )
        st.session_state.current_q = q
        st.session_state.q_source = source
    st.session_state.answer_submitted = False

# --- 界面渲染核心逻辑 ---

# 1. 登录/注册页面（无改动，兼容原有账号）
if not st.session_state.logged_in:
    st.title("📐 智能数学推题系统")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["账号登录", "新用户注册"])
    
    with tab1:
        username = st.text_input("用户名", key="login_username").strip()
        password = st.text_input("密码", type="password", key="login_password").strip()
        if st.button("登录", type="primary", use_container_width=True):
            user_id = db.login_user(username, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("用户名或密码错误，请重试")

    with tab2:
        new_username = st.text_input("设置用户名", key="reg_username")
        new_password = st.text_input("设置密码", type="password", key="reg_password")
        if st.button("注册账号", use_container_width=True):
            if not new_username or not new_password:
                st.warning("用户名和密码不能为空")
            elif db.register_user(new_username, new_password):
                st.success("注册成功！请切换到登录页登录")
            else:
                st.error("用户名已存在，请更换用户名")

# 2. 登录后的主应用页面
else:
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    # 侧边栏导航栏
    with st.sidebar:
        st.markdown(f"### 👤 用户ID：{st.session_state.user_id}")
        st.divider()
        
        # 知识点选择器
        kps = db.get_all_knowledge_points()
        if not kps:
            st.warning("题库暂无知识点，请先初始化数据库")
        else:
            default_index = 0
            if st.session_state.current_kp and st.session_state.current_kp in kps:
                default_index = kps.index(st.session_state.current_kp)
            selected_kp = st.selectbox("📚 选择练习知识点", kps, index=default_index)
            
            # 切换知识点时重置题目
            if selected_kp != st.session_state.current_kp:
                st.session_state.current_kp = selected_kp
                load_new_question()
        
        st.divider()
        if st.button("📊 查看知识点答题报告", use_container_width=True):
            go_to_report()
            st.rerun()
        
        st.divider()
        st.subheader("🎯 弱项突破建议")
        weaks = db.get_user_weak_points(st.session_state.user_id)
        if weaks:
            for wk in weaks:
                if st.button(f"强化练习：{wk}", key=f"weak_{wk}"):
                    st.session_state.current_kp = wk
                    load_new_question()
                    st.rerun()
        else:
            st.write("暂无记录，多做题我才能了解你哦~")

        st.divider()
        if st.button("🚪 退出登录", use_container_width=True):
            logout()
            st.rerun()
        
        if st.button("📁 题库数据查看器", use_container_width=True):
            st.session_state.page = "db_manager"
            st.rerun()

    # --- 主内容区 ---
    # A. 答题报告页面
    if st.session_state.page == "report":
        st.header(f"📊 知识点答题报告：{st.session_state.current_kp}")
        st.markdown("---")
        
        # 核心指标卡片
        score, total_count, _ = db.calculate_proficiency(st.session_state.user_id, st.session_state.current_kp)
        col1, col2, col3 = st.columns(3)
        col1.metric("知识点熟练度", f"{score} 分")
        col2.metric("累计答题数", f"{total_count} 题")
        col3.metric("正确率", f"{score}%" if total_count>0 else "0%")
        
        st.markdown("---")
        st.subheader("📝 最近答题记录")
        history_df = db.get_history(st.session_state.user_id, st.session_state.current_kp)
        
        if not history_df.empty:
            # 美化表格展示
            history_df['题型'] = history_df['question_type'].map({'choice': '选择题', 'blank': '填空题'})
            history_df['答题结果'] = history_df['is_correct'].apply(lambda x: "✅ 正确" if x else "❌ 错误")
            history_df['答题时间'] = history_df['timestamp']
            st.dataframe(history_df[['content', '题型', '答题结果', '答题时间']], use_container_width=True, hide_index=True)
        else:
            st.info("该知识点暂无答题记录，快去刷题吧~")
            
        st.divider()
        if st.button("🔙 返回刷题页面", type="primary"):
            go_to_main()
            st.rerun()

    # B. 核心刷题页面
    else:
        st.header(f"✏️ 知识点练习：{st.session_state.current_kp}")
        st.markdown("---")

        # 无题目时加载新题
        if st.session_state.current_q is None:
            load_new_question()

        # 渲染题目
        if st.session_state.current_q is not None:
            q = st.session_state.current_q
            q_type = q['question_type']
            
            # 题干展示
            st.subheader("📄 题目")
            st.markdown(f"### {q['content']}")
            st.caption(f"难度：{'⭐'*q['difficulty']} | 题型：{'选择题' if q_type=='choice' else '填空题'}")
            st.divider()
            
            # 答题区域（分题型渲染）
            st.subheader("✍️ 你的答案")
            with st.form("answer_form", clear_on_submit=False):
                user_answer = None
                # 选择题：渲染单选按钮，支持LaTeX选项
                if q_type == "choice":
                    options = json.loads(q['options'])
                    # 格式化选项为 ["A. xxx", "B. xxx"] 格式
                    option_list = [f"{key}. {value}" for key, value in options.items()]
                    user_selected = st.radio(
                        "请选择正确选项",
                        options=option_list,
                        disabled=st.session_state.answer_submitted,
                        label_visibility="collapsed"
                    )
                    # 提取用户选择的选项字母
                    if user_selected:
                        user_answer = user_selected.split(".")[0]
                
                # 填空题：强制数字输入，仅能输入数字，支持小数/整数
                elif q_type == "blank":
                    user_answer = st.number_input(
                        "请输入最终数字答案（支持小数）",
                        format="%.4f",
                        step=0.001,
                        disabled=st.session_state.answer_submitted,
                        label_visibility="collapsed"
                    )
                
                # 提交按钮
                submitted = st.form_submit_button(
                    "提交答案", 
                    type="primary", 
                    use_container_width=True,
                    disabled=st.session_state.answer_submitted
                )
                
                # 提交后的判题逻辑
                if submitted:
                    st.session_state.answer_submitted = True
                    correct_answer = q['answer']
                    is_correct = False
                    
                    # 选择题判题：字母完全匹配
                    if q_type == "choice":
                        is_correct = (user_answer == correct_answer)
                    
                    # 填空题判题：数值匹配，允许0.001的浮点误差
                    elif q_type == "blank":
                        try:
                            correct_num = float(correct_answer)
                            user_num = float(user_answer)
                            is_correct = abs(user_num - correct_num) < 0.001
                        except:
                            is_correct = False
                    
                    # 保存答题记录
                    db.save_answer(st.session_state.user_id, q['q_id'], is_correct)
                    
                    # 结果反馈
                    if is_correct:
                        st.success("🎉 回答正确！太棒了，继续加油~")
                    else:
                        st.error("❌ 答案错误")
                        # 展示正确答案
                        if q_type == "choice":
                            st.info(f"正确答案：{correct_answer}. {json.loads(q['options'])[correct_answer]}")
                        else:
                            st.info(f"正确答案：{correct_answer}")
            
            # 下一题按钮（提交后才显示）
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("下一题 (题库随机) ➡️"):
                    load_new_question()
                    st.rerun()
            with col2:
                if st.button("✨ AI 生成新题", type="primary"):
                    with st.spinner("AI 正在根据知识点精心出题..."):
                        # 只需这一行，逻辑全部在 rec_model 里
                        load_new_question(force_ai=True) 
                        if st.session_state.current_q:
                            st.success("AI 题目生成成功！")
                            st.rerun()
                        else:
                            st.error("生成失败，请检查配置")
        else:
            st.warning("该知识点暂无可用题目，请先在题库中添加题目~")

if st.session_state.page == "db_manager":
        st.header("📁 底层数据预览与统计")
        st.markdown("---")
        
        st.subheader("📚 RAG 向量知识库状态")
        rag_stats = rag.get_knowledge_base_stats()
        
        col1, col2 = st.columns(2)
        col1.metric(label="已入库 PDF 文件数", value=f"{rag_stats['total_files']} 个")
        col2.metric(label="向量化文本块 (Chunks)", value=f"{rag_stats['total_chunks']} 块")
        
        if rag_stats['files']:
            with st.expander("查看已入库的 PDF 文件列表"):
                for file_name in rag_stats['files']:
                    st.write(f"- {file_name}")
                    
        st.markdown("---")

        st.subheader("📝 结构化题库数据 (SQLite)")
        all_qs = db.get_all_questions()
        if all_qs:
            # 顺便在这里加上结构化题库的总量统计
            st.write(f"当前共有 **{len(all_qs)}** 道题目。")
            df = pd.DataFrame(all_qs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("结构化数据库目前是空的。")
            
        st.divider()
        if st.button("🔙 返回首页", type="primary"):
            st.session_state.page = "main"
            st.rerun()