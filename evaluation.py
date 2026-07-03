import sqlite3
import pandas as pd
import numpy as np

from graph_kt import ConceptGraphKT
from graph_rag import GraphRAG
import database as db

# ── matplotlib 中文字体配置 ──
import matplotlib
import matplotlib.font_manager as fm
matplotlib.rcParams['axes.unicode_minus'] = False

# 按优先级查找可用中文字体
_cjk_candidates = ['Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei',
                   'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Source Han Sans SC',
                   'PingFang SC', 'Heiti SC', 'STHeiti', 'SimSun', 'FangSong']
_available_fonts = {f.name for f in fm.fontManager.ttflist}
_chosen_font = None
for _font in _cjk_candidates:
    if _font in _available_fonts:
        _chosen_font = _font
        break

if _chosen_font:
    matplotlib.rcParams['font.sans-serif'] = [_chosen_font, 'DejaVu Sans']
else:
    # 兜底：扫描所有字体找含 CJK 字符的
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
    print("⚠️ 未找到中文字体，图表中文可能显示为方框。请安装 Microsoft YaHei 或 SimHei。")

try:
    from scipy.stats import pearsonr
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _get_user_records_with_details(user_id):
    conn = sqlite3.connect(db.DB_FILE)
    df = pd.read_sql_query("""
        SELECT r.record_id, r.q_id, r.is_correct, r.timestamp,
               q.knowledge_point, q.difficulty, q.question_type
        FROM records r JOIN questions q ON r.q_id = q.q_id
        WHERE r.user_id = ?
        ORDER BY r.timestamp ASC
    """, conn, params=(user_id,))
    conn.close()
    return df


def _mastery_to_expected_diff(m):
    if m > 85: return 4
    elif m > 65: return 3
    elif m > 40: return 2
    else: return 1


def _reconstruct_mastery_timeline(records_df):
    kg_engine = GraphRAG(db_path=db.DB_FILE)
    kt = ConceptGraphKT(kg_engine.kg)

    timeline = []
    accumulated_records = []

    for _, row in records_df.iterrows():
        scores = kt.update_user_state(accumulated_records)
        mastery_before = scores.get(row['knowledge_point'], 15.0)

        timeline.append({
            'kp': row['knowledge_point'],
            'mastery_before': mastery_before,
            'is_correct': int(row['is_correct']),
            'difficulty': int(row['difficulty']),
            'timestamp': row['timestamp'],
            'q_id': int(row['q_id'])
        })

        accumulated_records.append([row['knowledge_point'], int(row['is_correct'])])

    return timeline


# ═══════════════════════════════════════════
# M1: 难度适配准确率
# ═══════════════════════════════════════════
def metric_difficulty_fitness(user_id):
    df = _get_user_records_with_details(user_id)
    if len(df) < 5:
        return {'status': 'insufficient_data'}

    timeline = _reconstruct_mastery_timeline(df)

    fits = 0; too_hard = 0; too_easy = 0
    bracket_results = {i: {'fits': 0, 'too_hard': 0, 'too_easy': 0, 'total': 0} for i in range(5)}

    for entry in timeline:
        expected = _mastery_to_expected_diff(entry['mastery_before'])
        actual = entry['difficulty']
        bracket = min(int(entry['mastery_before'] // 20), 4)
        bracket_results[bracket]['total'] += 1

        if abs(actual - expected) <= 1:
            fits += 1
            bracket_results[bracket]['fits'] += 1
        elif actual > expected:
            too_hard += 1
            bracket_results[bracket]['too_hard'] += 1
        else:
            too_easy += 1
            bracket_results[bracket]['too_easy'] += 1

    total = len(timeline)
    return {
        'fitness_rate': round(fits / total * 100, 1),
        'too_hard_rate': round(too_hard / total * 100, 1),
        'too_easy_rate': round(too_easy / total * 100, 1),
        'total_answers': total,
        'bracket_breakdown': {
            f"{i*20}-{(i+1)*20}%": {
                'fits': bracket_results[i]['fits'],
                'too_hard': bracket_results[i]['too_hard'],
                'too_easy': bracket_results[i]['too_easy'],
                'total': bracket_results[i]['total']
            } for i in range(5)
        }
    }


# ═══════════════════════════════════════════
# M2: 掌握度-正确率一致性
# ═══════════════════════════════════════════
def metric_mastery_correctness_alignment(user_id):
    df = _get_user_records_with_details(user_id)
    if len(df) < 5:
        return {'status': 'insufficient_data'}

    timeline = _reconstruct_mastery_timeline(df)

    brackets = {i: {'correct': 0, 'total': 0} for i in range(5)}
    all_masteries = []
    all_correct = []

    for entry in timeline:
        bracket = min(int(entry['mastery_before'] // 20), 4)
        brackets[bracket]['total'] += 1
        if entry['is_correct']:
            brackets[bracket]['correct'] += 1
        all_masteries.append(entry['mastery_before'])
        all_correct.append(entry['is_correct'])

    bracket_rates = {}
    for i in range(5):
        b = brackets[i]
        bracket_rates[f"{i*20}-{(i+1)*20}%"] = {
            'correct_rate': round(b['correct'] / b['total'] * 100, 1) if b['total'] > 0 else 0,
            'sample_count': b['total']
        }

    if len(all_masteries) > 2:
        if HAS_SCIPY:
            corr, p_value = pearsonr(all_masteries, all_correct)
        else:
            # numpy fallback
            corr = np.corrcoef(all_masteries, all_correct)[0, 1]
            p_value = float('nan')
    else:
        corr, p_value = 0, 1

    if corr > 0.5: interpretation = '强相关'
    elif corr > 0.3: interpretation = '中等相关'
    else: interpretation = '弱相关'

    return {
        'correlation': round(corr, 3),
        'p_value': round(p_value, 4) if not np.isnan(p_value) else None,
        'bracket_breakdown': bracket_rates,
        'interpretation': interpretation
    }


# ═══════════════════════════════════════════
# M4: 知识点掌握雷达
# ═══════════════════════════════════════════
def metric_kp_mastery_radar(user_id):
    records = db.get_user_records(user_id)
    kg_engine = GraphRAG(db_path=db.DB_FILE)
    kt = ConceptGraphKT(kg_engine.kg)
    scores = kt.update_user_state(records)

    core_kps = db.get_all_knowledge_points()
    core_scores = {kp: round(scores.get(kp, 15.0), 1) for kp in core_kps}

    sorted_kps = sorted(core_scores.items(), key=lambda x: x[1], reverse=True)
    return {
        'mastery_scores': core_scores,
        'avg_mastery': round(np.mean(list(core_scores.values())), 1),
        'max_kp': sorted_kps[0][0] if sorted_kps else '',
        'max_score': sorted_kps[0][1] if sorted_kps else 0,
        'min_kp': sorted_kps[-1][0] if sorted_kps else '',
        'min_score': sorted_kps[-1][1] if sorted_kps else 0,
    }


# ═══════════════════════════════════════════
# M5: 知识点覆盖均衡度
# ═══════════════════════════════════════════
def metric_kp_coverage(user_id):
    df = _get_user_records_with_details(user_id)
    if len(df) < 5:
        return {'status': 'insufficient_data'}

    kp_counts = df['knowledge_point'].value_counts().to_dict()
    total = sum(kp_counts.values())

    probs = [c / total for c in kp_counts.values()]
    entropy = -sum(p * np.log(p) for p in probs)
    n = len(kp_counts)
    max_entropy = np.log(n) if n > 1 else 1
    normalized_entropy = round(entropy / max_entropy, 3) if max_entropy > 0 else 0

    all_kps = db.get_all_knowledge_points()
    return {
        'kp_counts': kp_counts,
        'unique_kps_practiced': len(kp_counts),
        'total_kps': len(all_kps),
        'entropy': round(entropy, 3),
        'normalized_entropy': normalized_entropy,
        'coverage_rate': round(len(kp_counts) / max(len(all_kps), 1) * 100, 1)
    }


# ═══════════════════════════════════════════
# M6: 难度分布合理性
# ═══════════════════════════════════════════
def metric_difficulty_distribution(user_id):
    df = _get_user_records_with_details(user_id)
    if len(df) < 5:
        return {'status': 'insufficient_data'}

    diff_counts = df['difficulty'].value_counts().sort_index().to_dict()
    total = len(df)

    return {
        'distribution': {int(k): {'count': int(v), 'rate': round(v / total * 100, 1)}
                         for k, v in diff_counts.items()},
        'avg_difficulty': round(df['difficulty'].mean(), 2),
        'total': total
    }


# ═══════════════════════════════════════════
# M7: 正确率时间趋势
# ═══════════════════════════════════════════
def metric_correctness_trend(user_id):
    df = _get_user_records_with_details(user_id)
    if len(df) < 5:
        return {'status': 'insufficient_data'}

    window = max(5, len(df) // 5)
    rolling_rates = df['is_correct'].rolling(window=window, min_periods=3).mean().dropna()

    if len(rolling_rates) < 2:
        return {'status': 'insufficient_data'}

    x = np.arange(len(rolling_rates))
    y = rolling_rates.values
    slope, intercept = np.polyfit(x, y, 1)

    return {
        'rolling_rates': [round(v, 3) for v in rolling_rates.tolist()],
        'window_size': window,
        'trend_slope': round(slope, 5),
        'trend_per_10': round(slope * 10 * 100, 1),
        'start_rate': round(rolling_rates.iloc[0] * 100, 1),
        'end_rate': round(rolling_rates.iloc[-1] * 100, 1),
        'overall_accuracy': round(df['is_correct'].mean() * 100, 1)
    }


# ═══════════════════════════════════════════
# M8: 综合学习指数
# ═══════════════════════════════════════════
def metric_composite_score(user_id):
    m4 = metric_kp_mastery_radar(user_id)
    m5 = metric_kp_coverage(user_id)
    m7 = metric_correctness_trend(user_id)

    if m5.get('status') == 'insufficient_data' or m7.get('status') == 'insufficient_data':
        return {'status': 'insufficient_data'}

    avg_mastery = m4['avg_mastery'] / 100.0
    recent_acc = m7['end_rate'] / 100.0
    coverage = m5['normalized_entropy']
    growth = max(0.0, min(1.0, m7['trend_slope'] * 100 + 0.5))

    composite = (0.35 * avg_mastery + 0.25 * recent_acc +
                 0.20 * coverage + 0.20 * growth) * 100

    if composite >= 85: grade = 'A'
    elif composite >= 70: grade = 'B'
    elif composite >= 55: grade = 'C'
    elif composite >= 40: grade = 'D'
    else: grade = 'E'

    return {
        'score': round(composite, 1),
        'grade': grade,
        'components': {
            'avg_mastery': round(avg_mastery * 100, 1),
            'recent_accuracy': round(recent_acc * 100, 1),
            'kp_coverage': round(coverage * 100, 1),
            'mastery_growth': round(growth * 100, 1)
        }
    }


# ═══════════════════════════════════════════
# 主入口: 计算全部指标
# ═══════════════════════════════════════════
def compute_all_metrics(user_id):
    df = _get_user_records_with_details(user_id)
    sufficient = len(df) >= 5

    result = {
        'summary': {
            'total_records': len(df),
            'sufficient_data': sufficient,
        },
        'recommendation': {},
        'kt_validity': {},
        'coverage': {},
        'learning': {}
    }

    if sufficient:
        result['summary']['composite'] = metric_composite_score(user_id)
        result['recommendation']['difficulty_fitness'] = metric_difficulty_fitness(user_id)
        result['kt_validity']['mastery_alignment'] = metric_mastery_correctness_alignment(user_id)
        result['kt_validity']['kp_mastery_radar'] = metric_kp_mastery_radar(user_id)
        result['coverage']['kp_coverage'] = metric_kp_coverage(user_id)
        result['coverage']['difficulty_distribution'] = metric_difficulty_distribution(user_id)
        result['learning']['correctness_trend'] = metric_correctness_trend(user_id)
        result['learning']['composite_score'] = result['summary']['composite']

    return result


# ═══════════════════════════════════════════
# 可视化: 雷达图
# ═══════════════════════════════════════════
def plot_radar_chart(mastery_scores, title="知识点掌握雷达图"):
    import matplotlib.pyplot as plt

    kps = list(mastery_scores.keys())
    values = list(mastery_scores.values())
    N = len(kps)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_closed = values + values[:1]
    angles_closed = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    ax.fill(angles_closed, values_closed, alpha=0.25, color='#1f77b4')
    ax.plot(angles_closed, values_closed, color='#1f77b4', linewidth=2)

    # 理想参考线 (100 分)
    ideal = [100] * N + [100]
    ax.plot(angles_closed, ideal, color='#d3d3d3', linewidth=1, linestyle='--', alpha=0.7)

    ax.set_xticks(angles)
    ax.set_xticklabels(kps, size=7)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=7)
    ax.set_title(title, size=14, pad=25)
    ax.grid(True, alpha=0.3)

    return fig


# ═══════════════════════════════════════════
# 生成评估报告 Markdown
# ═══════════════════════════════════════════
def generate_report_markdown(metrics, username=""):
    s = metrics['summary']
    comp = s.get('composite', {})

    md = f"""# 📊 智能推题系统 — 评估报告

**用户**: {username} | **答题总数**: {s['total_records']} 条

---

## 🏆 综合学习指数

| 指标 | 数值 |
|------|------|
| 综合指数 | **{comp.get('score', 'N/A')} 分** (等级 {comp.get('grade', 'N/A')}) |
"""

    if 'components' in comp:
        c = comp['components']
        md += f"""| 平均掌握度 | {c['avg_mastery']}% |
| 近期正确率 | {c['recent_accuracy']}% |
| 知识覆盖熵 | {c['kp_coverage']}% |
| 掌握度增长 | {c['mastery_growth']}% |
"""

    md += "\n---\n\n## 🎯 推荐准确性\n\n"

    rec = metrics.get('recommendation', {})
    m1 = rec.get('difficulty_fitness', {})
    if m1 and m1.get('status') != 'insufficient_data':
        md += f"""### M1: 难度适配准确率
- 适配率: **{m1['fitness_rate']}%**
- 偏难率: {m1['too_hard_rate']}%
- 偏易率: {m1['too_easy_rate']}%
"""

    md += "\n---\n\n## 🧠 认知诊断有效性\n\n"

    kt = metrics.get('kt_validity', {})
    m3 = kt.get('mastery_alignment', {})
    if m3 and m3.get('status') != 'insufficient_data':
        md += f"""### M3: 掌握度-正确率一致性
- Pearson r = **{m3['correlation']}** ({m3['interpretation']})
"""

    m4 = kt.get('kp_mastery_radar', {})
    if m4:
        md += f"""### M4: 知识点掌握雷达
- 平均掌握度: **{m4['avg_mastery']}%**
- 最擅长: {m4.get('max_kp', '')} ({m4.get('max_score', 0)}%)
- 最薄弱: {m4.get('min_kp', '')} ({m4.get('min_score', 0)}%)
"""

    md += "\n---\n\n## 🌐 覆盖度与多样性\n\n"

    cov = metrics.get('coverage', {})
    m5 = cov.get('kp_coverage', {})
    if m5 and m5.get('status') != 'insufficient_data':
        md += f"""### M5: 知识点覆盖均衡度
- 已练习知识点: {m5['unique_kps_practiced']}/{m5['total_kps']}
- 归一化熵: **{m5['normalized_entropy']}** (覆盖均衡度)
"""

    m6 = cov.get('difficulty_distribution', {})
    if m6 and m6.get('status') != 'insufficient_data':
        md += f"""### M6: 难度分布
- 平均难度: **{m6['avg_difficulty']}**
"""

    md += "\n---\n\n## 📈 学习成效\n\n"

    lrn = metrics.get('learning', {})
    m7 = lrn.get('correctness_trend', {})
    if m7 and m7.get('status') != 'insufficient_data':
        md += f"""### M7: 正确率趋势
- 初始正确率: {m7['start_rate']}%
- 最终正确率: {m7['end_rate']}%
- 趋势: 每 10 题变化 **{m7['trend_per_10']}%**
- 总体正确率: {m7['overall_accuracy']}%
"""

    md += "\n---\n\n> 📅 报告由智能推题系统评估中心自动生成\n"

    return md
