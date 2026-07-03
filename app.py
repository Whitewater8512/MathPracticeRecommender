import os
os.environ["CHROMA_TELEMETRY"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "false"

import re
import json
import numpy as np
import sympy
import pandas as pd
import streamlit as st
import extra_streamlit_components as stx

import graph_rag
import database as db
import llm_api
import rag
import rec_model
import evaluation
from graph_kt import ConceptGraphKT

# 初始化数据库
db.init_db()

# 初始化 Cookie 管理器
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# --- 页面全局配置 ---
st.set_page_config(page_title="智能数学推题系统", page_icon="📐", layout="wide")

# ==========================================
# Session State 全局状态管理
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.page = "login"

# --- 终极保活方案：优先 URL 参数（瞬间生效），备用 Cookie ---
cached_user_id = st.query_params.get("user_id") 
if not cached_user_id:
    cached_user_id = cookie_manager.get("user_id")

if not st.session_state.logged_in and cached_user_id:
    st.session_state.logged_in = True
    st.session_state.user_id = int(cached_user_id)
    st.session_state.page = "main"
    st.query_params["user_id"] = str(cached_user_id) 
    st.rerun()

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_kp' not in st.session_state:
    st.session_state.current_kp = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False
if 'answered_q_id' not in st.session_state:
    st.session_state.answered_q_id = None
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = None

# 全局模型与熟练度引擎初始化
kg_engine_global = rec_model.get_kg_engine()
records_global = db.get_user_records(st.session_state.user_id) if st.session_state.user_id else []
graph_kt_global = ConceptGraphKT(kg_engine_global.kg)
global_scores = graph_kt_global.update_user_state(records_global)

# 评估引擎
eval_engine = evaluation

# --- 页面跳转回调函数 ---
def logout():
    cookie_manager.delete("user_id")
    if "user_id" in st.query_params:
        del st.query_params["user_id"]
    st.session_state.clear()
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
    """使用推荐引擎加载题目"""
    if 'path_logs' in st.session_state:
        del st.session_state.path_logs
    if 'recommended_kp' in st.session_state:
        del st.session_state.recommended_kp

    if st.session_state.current_kp:
        source, q = rec_model.recommend_next_step(
            st.session_state.user_id, 
            st.session_state.current_kp, 
            force_ai=force_ai
        )
        st.session_state.current_q = q
        st.session_state.q_source = source
    st.session_state.answer_submitted = False
    st.session_state.answered_q_id = None
    st.session_state.is_correct = None

# ==========================================
# 1. 登录/注册页面
# ==========================================
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
                
                # 双写备份：写 Cookie + 写 URL 参数
                cookie_manager.set("user_id", str(user_id), max_age=3*24*60*60)
                st.query_params["user_id"] = str(user_id)
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

# ==========================================
# 2. 登录后的主应用页面
# ==========================================
else:
    if 'page' not in st.session_state:
        st.session_state.page = "main"
        
    # --- 侧边栏 ---
    with st.sidebar:
        st.markdown(f"### 👤 用户ID：{st.session_state.user_id}")
        st.divider()

        kps = db.get_all_knowledge_points()
        
        st.subheader("📚 知识点熟练度")
        st.caption("点击下方对应章节即可切换练习目标")

        if not kps:
            st.warning("题库暂无知识点，请先初始化数据库")
        else:
            # 确保初次登录时有默认选中的知识点
            if not st.session_state.current_kp:
                st.session_state.current_kp = kps[0]

            # 遍历渲染：按钮 + 贴地进度条
            with st.expander("👇 点击展开/收起全部知识点", expanded=True):
                for kp in kps:
                    prof = min(max(int(global_scores.get(kp, 15.0)), 0), 100)
                    
                    # 动态决定颜色
                    if prof < 40: bar_color = "#FF4B4B"
                    elif prof < 70: bar_color = "#FFAA00"
                    else: bar_color = "#00CC96"
                        
                    # 当前选中的知识点给出特殊高亮标识
                    is_current = (kp == st.session_state.current_kp)
                    prefix = "🎯" if is_current else "📓"
                    
                    # 1. 渲染 Streamlit 原生按钮（作为点击触发器）
                    if st.button(f"{prefix} {kp} ({prof}%)", key=f"nav_{kp}", width='stretch'):
                        if st.session_state.current_kp != kp:
                            st.session_state.current_kp = kp
                            with st.spinner(f"正在为您加载【{kp}】的专属题目，请稍候..."):
                                load_new_question()
                            st.rerun()

                    # 2. 渲染 HTML 进度条（利用负边距紧紧贴在按钮下方）
                    st.markdown(f"""
                    <div style="width: 100%; background-color: #444444; border-radius: 4px; height: 6px; margin-top: -14px; margin-bottom: 12px;">
                        <div style="width: {prof}%; background-color: {bar_color}; height: 6px; border-radius: 4px; transition: width 0.5s;"></div>
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        if st.button("📊 查看知识点答题报告", use_container_width=True):
            go_to_report()
            st.rerun()

        if st.button("📈 评估中心", use_container_width=True):
            st.session_state.page = "evaluation"
            st.rerun()
        
        st.divider()
        st.subheader("🎯 弱项突破建议")
        weaks = db.get_user_weak_points(st.session_state.user_id)
        if weaks:
            for wk in weaks:
                if st.button(f"强化练习：{wk}", key=f"weak_{wk}"):
                    st.session_state.current_kp = wk
                    with st.spinner(f"正在为您加载【{wk}】的专属题目，请稍候..."):
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
        acc, total_count = db.get_raw_stats(st.session_state.user_id, st.session_state.current_kp)
        score = round(global_scores.get(st.session_state.current_kp, 15.0), 1)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("知识点熟练度", f"{score} 分")
        col2.metric("累计答题数", f"{total_count} 题")
        col3.metric("正确率", f"{acc}%" if total_count > 0 else "0%")
            
        st.markdown("---")
        st.subheader("📝 最近答题记录")
        history_df = db.get_history(st.session_state.user_id, st.session_state.current_kp)
        
        if not history_df.empty:
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

    # B. 底层数据预览
    elif st.session_state.page == "db_manager":
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
            st.write(f"当前共有 **{len(all_qs)}** 道题目。")
            df = pd.DataFrame(all_qs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("结构化数据库目前是空的。")

        st.divider()
        if st.button("🔙 返回首页", type="primary"):
            st.session_state.page = "main"
            st.rerun()

    # C. 评估中心
    elif st.session_state.page == "evaluation":
        st.header("📊 评估中心")
        st.markdown("---")

        metrics = eval_engine.compute_all_metrics(st.session_state.user_id)

        if not metrics['summary']['sufficient_data']:
            st.warning(f"📭 答题数据不足（当前仅 {metrics['summary']['total_records']} 条记录），至少需要 5 条才能生成评估报告。请多刷几道题后再来查看。")

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔙 返回刷题", use_container_width=True):
                    go_to_main()
                    st.rerun()
        else:
            comp = metrics['summary']['composite']
            m4 = metrics['kt_validity']['kp_mastery_radar']
            m7 = metrics['learning']['correctness_trend']
            m5 = metrics['coverage']['kp_coverage']

            # ── 顶部概览仪表盘 ──
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("综合学习指数", f"{comp['score']}分", delta=f"等级 {comp['grade']}")
            col2.metric("平均掌握度", f"{m4['avg_mastery']}%")
            col3.metric("总体正确率", f"{m7.get('overall_accuracy', 0)}%")
            col4.metric("知识覆盖熵", f"{m5.get('normalized_entropy', 0):.2f}")

            st.caption(f"📋 基于 **{metrics['summary']['total_records']}** 条答题记录生成")
            st.markdown("---")

            # ── 4 个 Tab 页 ──
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 推荐准确性", "🧠 认知诊断有效性",
                "🌐 覆盖度与多样性", "📈 学习成效"
            ])

            # ── Tab 1: 推荐准确性 ──
            with tab1:
                st.subheader("M1: 难度适配分析")
                m1 = metrics['recommendation']['difficulty_fitness']
                if m1.get('status') != 'insufficient_data':
                    brackets = m1['bracket_breakdown']
                    bracket_labels = list(brackets.keys())
                    chart_data = pd.DataFrame({
                        '适配 (fits)': [brackets[b]['fits'] for b in bracket_labels],
                        '偏难 (too hard)': [brackets[b]['too_hard'] for b in bracket_labels],
                        '偏易 (too easy)': [brackets[b]['too_easy'] for b in bracket_labels],
                    }, index=bracket_labels)
                    st.bar_chart(chart_data, stack=True)
                    st.caption(f"总体适配率: **{m1['fitness_rate']}%** | 偏难: {m1['too_hard_rate']}% | 偏易: {m1['too_easy_rate']}%")
                else:
                    st.info("数据不足，无法计算")

            # ── Tab 2: 认知诊断有效性 ──
            with tab2:
                col_left, col_right = st.columns(2)

                with col_left:
                    st.subheader("M3: 掌握度-正确率一致性")
                    m3 = metrics['kt_validity']['mastery_alignment']
                    if m3.get('status') != 'insufficient_data':
                        bracket_data = m3['bracket_breakdown']
                        chart_df = pd.DataFrame({
                            '正确率 (%)': [bracket_data[b]['correct_rate'] for b in bracket_data],
                        }, index=list(bracket_data.keys()))
                        st.bar_chart(chart_df)
                        r_val = m3['correlation']
                        interp = m3['interpretation']
                        st.caption(f"Pearson r = **{r_val}** ({interp})")
                    else:
                        st.info("数据不足，无法计算")

                with col_right:
                    st.subheader("M4: 知识点掌握雷达")
                    if m4:
                        fig = eval_engine.plot_radar_chart(m4['mastery_scores'])
                        st.pyplot(fig)
                    else:
                        st.info("数据不足，无法计算")

            # ── Tab 3: 覆盖度与多样性 ──
            with tab3:
                col_left, col_right = st.columns(2)

                with col_left:
                    st.subheader("M5: 知识点覆盖均衡度")
                    if m5.get('status') != 'insufficient_data':
                        kp_counts = m5['kp_counts']
                        sorted_kps = sorted(kp_counts.items(), key=lambda x: x[1], reverse=True)
                        chart_df = pd.DataFrame({
                            '答题次数': [v for _, v in sorted_kps],
                        }, index=[k for k, _ in sorted_kps])
                        st.bar_chart(chart_df, horizontal=True)
                        st.caption(f"已练习 **{m5['unique_kps_practiced']}/{m5['total_kps']}** 个知识点 | 归一化熵: **{m5['normalized_entropy']:.3f}**")
                    else:
                        st.info("数据不足，无法计算")

                with col_right:
                    st.subheader("M6: 难度分布合理性")
                    m6 = metrics['coverage']['difficulty_distribution']
                    if m6.get('status') != 'insufficient_data':
                        dist = m6['distribution']
                        chart_df = pd.DataFrame({
                            '题目数量': [dist.get(d, {}).get('count', 0) for d in [1, 2, 3, 4]],
                        }, index=['难度1', '难度2', '难度3', '难度4'])
                        st.bar_chart(chart_df)
                        st.caption(f"平均难度: **{m6['avg_difficulty']:.2f}**")
                    else:
                        st.info("数据不足，无法计算")

            # ── Tab 4: 学习成效 ──
            with tab4:
                col_left, col_right = st.columns(2)

                with col_left:
                    st.subheader("M7: 正确率时间趋势")
                    if m7.get('status') != 'insufficient_data':
                        rates = m7['rolling_rates']
                        chart_df = pd.DataFrame({
                            '滑动窗口正确率': rates,
                        })
                        chart_df['趋势线'] = np.polyval(
                            np.polyfit(range(len(rates)), rates, 1),
                            range(len(rates))
                        )
                        st.line_chart(chart_df)
                        trend_dir = "上升" if m7['trend_slope'] > 0 else "下降"
                        st.caption(f"趋势: **{trend_dir}** (每10题变化 {m7['trend_per_10']}%) | 初始: {m7['start_rate']}% → 最终: {m7['end_rate']}%")
                    else:
                        st.info("数据不足，无法计算")

                with col_right:
                    st.subheader("M8: 综合指数分解")
                    if comp.get('status') != 'insufficient_data':
                        components = comp['components']
                        comp_df = pd.DataFrame({
                            '得分': [
                                components['avg_mastery'],
                                components['recent_accuracy'],
                                components['kp_coverage'],
                                components['mastery_growth']
                            ],
                        }, index=['平均掌握度', '近期正确率', '知识覆盖熵', '掌握增长斜率'])
                        st.bar_chart(comp_df)

                        # 等级展示
                        grade_color = {
                            'A': '#00CC96', 'B': '#636EFA', 'C': '#FFAA00',
                            'D': '#FF6B6B', 'E': '#FF4B4B'
                        }
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 20px;">
                            <span style="font-size: 72px; font-weight: bold; color: {grade_color.get(comp['grade'], '#888')};">{comp['grade']}</span>
                            <p style="font-size: 18px; color: #888;">综合等级评定</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("数据不足，无法计算")

            # ── 底部操作栏 ──
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 刷新评估", use_container_width=True):
                    st.rerun()
            with col2:
                report_md = eval_engine.generate_report_markdown(metrics)
                st.download_button(
                    label="📄 导出评估报告",
                    data=report_md,
                    file_name="evaluation_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col3:
                if st.button("🔙 返回刷题页面", use_container_width=True):
                    go_to_main()
                    st.rerun()

    # D. 核心刷题页面
    else:
        st.header(f"✏️ 知识点练习：{st.session_state.current_kp}")
        st.markdown("---")

        if st.session_state.current_q is None:
            with st.spinner(f"正在为您准备题目，请稍候..."):
                load_new_question()

        if st.session_state.current_q is not None:
            q = st.session_state.current_q
            q_type = q['question_type']

            with st.expander("💡 为什么推荐这道题？点击查看 AI 动态图谱路由"):
                # kg_vis = graph_rag.GraphRAG()
                kg_vis = kg_engine_global
                
                if 'path_logs' in st.session_state and 'recommended_kp' in st.session_state:
                    st.info(f"🔍 诊断报告：检测到您当前对“{st.session_state.current_kp}”的掌握度较低，AI 已为您自动规划最优降维路径。")
                    kg_vis.render_routing_visualization(
                        target_kp=st.session_state.current_kp, 
                        recommended_kp=st.session_state.recommended_kp, 
                        path_logs=st.session_state.path_logs
                    )
                else:
                    st.success("🎯 诊断报告：当前知识点掌握度良好，或处于自主强化模式。下方为您展示该知识点的上下游全景体系：")
                    kg_vis.render_local_map(
                        target_kp=st.session_state.current_kp, 
                        user_bkt_scores=global_scores
                    )   
                    st.caption("💡 图例说明：【大圆圈】为当前练习题；子节点部分，【绿色】 代表您已掌握（≥70%），【黄色】 代表及格（40-70%），【红色】 代表薄弱（<40%）。")

            st.subheader("📄 题目")
            st.markdown(f"### {q['content']}")
            st.caption(f"难度：{'⭐'*q['difficulty']} | 题型：{'选择题' if q_type=='choice' else '填空题'}")
            st.divider()
            
            q_id = q['q_id']
            is_disabled = (st.session_state.answer_submitted and st.session_state.answered_q_id == q_id)
            
            st.subheader("✍️ 你的答案")
            with st.form("answer_form", clear_on_submit=False):
                user_answer = None
                
                if q_type == "choice":
                    options = json.loads(q['options'])
                    option_list = [f"{key}. {value}" for key, value in options.items()]
                    option_list.append("🤷‍♂️ 我不知道 (直接看解析)")
                    
                    user_selected = st.radio(
                        "请选择正确选项",
                        options=option_list,
                        disabled=is_disabled, 
                        label_visibility="collapsed"
                    )
                    if user_selected:
                        user_answer = "我不知道" if "我不知道" in user_selected else user_selected.split(".")[0]
                        
                elif q_type == "blank":
                    user_answer = st.text_input(
                        "请输入最终数字答案（仅支持输入纯数字和/符号）",
                        disabled=is_disabled,
                        label_visibility="collapsed"
                    )
                    st.caption("💡 如果不会做，可以直接点击提交查看解析。")
                
                submitted = st.form_submit_button(
                    "提交答案", 
                    type="primary", 
                    use_container_width=True,
                    disabled=is_disabled
                )
                
                if submitted:
                    if not is_disabled:
                        # --- 输入合法性校验 ---
                        valid_submission = True
                        
                        if q_type == "blank":
                            user_input_str = str(user_answer).strip()
                            
                            # 1. 拦截空答案
                            if not user_input_str:
                                st.warning("⚠️ 答案不能为空，请填写计算结果后再提交！")
                                valid_submission = False
                                
                            # 2. 拦截非法字符（仅允许数字、负号、小数点、分数线和空格）
                            elif not re.match(r'^[-0-9/\s]+$', user_input_str):  # 正则里的 . 没了！
                                st.warning("⚠️ 格式错误！系统已限制为严谨的数学表达，请仅使用数字、负号（-）或分数线（/），禁止输入小数或字母。")
                                valid_submission = False

                        # 只有通过了校验，才会进入真实判题和存库流程
                        if valid_submission:
                            st.session_state.answer_submitted = True
                            st.session_state.answered_q_id = q_id
                            
                            correct_answer = q['answer'].strip()
                            is_correct = False
                            
                            if q_type == "choice":
                                is_correct = False if user_answer == "我不知道" else (user_answer == correct_answer)

                            elif q_type == "blank":
                                try:
                                    def clean_math(expr_str):
                                        s = str(expr_str).replace('$', '').strip()
                                        s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
                                        return s

                                    cleaned_user = clean_math(user_input_str)
                                    cleaned_correct = clean_math(correct_answer)
                                    
                                    user_expr = sympy.sympify(cleaned_user)
                                    correct_expr = sympy.sympify(cleaned_correct)
                                    
                                    is_correct = (sympy.simplify(user_expr - correct_expr) == 0)
                                except Exception:
                                    fallback_user = str(user_answer).replace(' ', '').replace('$', '')
                                    fallback_correct = correct_answer.replace(' ', '').replace('$', '')
                                    is_correct = (fallback_user == fallback_correct)
                            
                            st.session_state.is_correct = is_correct
                            db.save_answer(st.session_state.user_id, q_id, is_correct)
                            st.rerun()
            
            # --- 答题后的正负强化反馈 ---
            if is_disabled:
                if st.session_state.is_correct:
                    st.success("🎉 回答正确！太棒了，继续保持！")
                else:
                    st.error("❌ 回答错误。没关系，看看下方的解析补齐知识盲区吧！")

            if is_disabled and q.get('explanation'):
                clean_exp = q['explanation'].replace('\\n', '\n').replace('\\\\n', '\n')
                st.info(f"💡 **AI 深度解析**:\n\n{clean_exp}")
            
            # --- 结果展示与下一题控制区 ---
            col1 = st.empty()
            with col1:
                if st.button("下一题 (AI生成) ➡️", type="primary", disabled=not is_disabled):
                    with st.spinner("正在获取题目..."):
                        src, new_q = rec_model.recommend_next_step(
                            st.session_state.user_id, 
                            st.session_state.current_kp, 
                            force_ai=True
                        )
                        
                        if new_q:
                            st.session_state.current_q = new_q
                            st.session_state.q_source = src
                            st.session_state.answer_submitted = False
                            st.session_state.answered_q_id = None
                            st.session_state.is_correct = None
                            st.session_state.show_toast = True
                            st.rerun()
                        else:
                            st.error("题目获取失败，请重试")
        else:
            st.error("题目加载失败 😔")
            st.info("""
            **诊断信息：**
            系统尝试为您（或者使用 AI）寻找或生成一道专属题目，但遇到了网络拥堵。
            
            **建议：**
            1. 点击左侧侧边栏切换一下知识点。
            2. 如果您是管理员，请检查终端后台是否有 API 报错日志。
            """)
            
            if st.button("🔄 重新尝试生成"):
                with st.spinner("正在重新生成题目..."):
                    load_new_question(force_ai=True)
                st.rerun()

if st.session_state.get('show_toast', False):
    st.toast('✨ AI 题目生成成功！', icon='🎉')
    st.session_state.show_toast = False