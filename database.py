import json
import sqlite3
import pandas as pd
from datetime import datetime
import json
import os

# 数据库文件名 (确保路径稳定)
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'tutor.db')
# 简化处理：直接放在当前运行目录
DB_FILE = 'tutor.db'

def init_db():
    """安全初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 1. 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT)''')

    # 2. 检查 questions 表是否存在且结构正确
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions'")
    table_exists = c.fetchone()
    
    if not table_exists:
        # 如果表不存在，创建新表
        c.execute('''CREATE TABLE questions
                     (q_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      content TEXT,
                      knowledge_point TEXT,
                      difficulty INTEGER,
                      question_type TEXT,
                      options TEXT,
                      answer TEXT)''')
        # 插入初始数据
        _insert_sample_data(c)
    else:
        # 简单的兼容性检查：如果表存在但没有 question_type 列，说明是旧版本
        try:
            c.execute("SELECT question_type FROM questions LIMIT 1")
        except sqlite3.OperationalError:
            # 旧版本 detected，强制重建
            print("检测到旧版本数据库，正在重建...")
            c.execute("DROP TABLE questions")
            c.execute('''CREATE TABLE questions
                         (q_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          content TEXT,
                          knowledge_point TEXT,
                          difficulty INTEGER,
                          question_type TEXT,
                          options TEXT,
                          answer TEXT)''')
            _insert_sample_data(c)

    # 3. 答题记录表
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  q_id INTEGER,
                  is_correct INTEGER,
                  timestamp DATETIME)''')

    conn.commit()
    conn.close()


def _insert_sample_data(c):
    """辅助函数：插入覆盖考研高数细分标签的样例题"""
    
    sample_questions = [
        # ================= 1. 函数极限 =================
        (
            "求极限 $\\lim_{x \\to 0} \\frac{\\sin 3x}{x}$ 的值（ ）",
            "函数极限", 1, "choice",
            json.dumps({"A": "0", "B": "1", "C": "3", "D": "不存在"}), "C"
        ),
        (
            "已知 $\\lim_{x \\to \\infty} (1+\\frac{k}{x})^x = e^2$，则实数 $k=$____",
            "函数极限", 2, "blank", "", "2"
        ),
        (
            "下列极限中计算结果为 $e$ 的是（ ）",
            "函数极限", 2, "choice",
            json.dumps({
                "A": "$\\lim_{x \\to 0}(1+x)^x$", 
                "B": "$\\lim_{x \\to \\infty}(1+\\frac{1}{x})^x$", 
                "C": "$\\lim_{x \\to 0}(1+\\frac{1}{x})^x$", 
                "D": "$\\lim_{x \\to \\infty}(1+x)^{\\frac{1}{x}}$"
            }), "B"
        ),

        # ================= 2. 数列极限 =================
        (
            "求极限 $\\lim_{n \\to \\infty} \\frac{3n^2+1}{2n^2-n}$ 的值（ ）",
            "数列极限", 1, "choice",
            json.dumps({"A": "0", "B": "1.5", "C": "$\\infty$", "D": "不存在"}), "B"
        ),
        (
            "计算 $\\lim_{n \\to \\infty} (\\sqrt{n^2+n} - n) =$____（填小数）",
            "数列极限", 3, "blank", "", "0.5"
        ),
        (
            "设数列 $x_n = \\frac{(-1)^n}{n}$，则该数列（ ）",
            "数列极限", 1, "choice",
            json.dumps({"A": "发散", "B": "收敛于0", "C": "收敛于1", "D": "无界"}), "B"
        ),

        # ================= 3. 连续、间断与导数 =================
        (
            "函数 $f(x) = \\frac{x^2-1}{x-1}$ 在 $x=1$ 处的间断点类型为（ ）",
            "连续、间断与导数", 2, "choice",
            json.dumps({"A": "跳跃间断点", "B": "无穷间断点", "C": "振荡间断点", "D": "可去间断点"}), "D"
        ),
        (
            "设 $f(x) = |x|$，则 $f(x)$ 在区间 $(-1, 1)$ 内不可导的点的个数为____",
            "连续、间断与导数", 1, "blank", "", "1"
        ),
        (
            "已知 $y = \\sin(x^2)$，则导数 $y'$ 为（ ）",
            "连续、间断与导数", 2, "choice",
            json.dumps({"A": "$\\cos(x^2)$", "B": "$2x\\cos(x^2)$", "C": "$-2x\\cos(x^2)$", "D": "$\\sin(2x)$"}), "B"
        ),

        # ================= 4. 中值定理 =================
        (
            "若函数 $f(x)$ 在 $[a,b]$ 上连续，在 $(a,b)$ 内可导，且 $f(a)=f(b)$，则使得 $f'(\\xi)=0$ 成立的定理是（ ）",
            "中值定理", 1, "choice",
            json.dumps({"A": "罗尔定理", "B": "拉格朗日中值定理", "C": "柯西中值定理", "D": "泰勒定理"}), "A"
        ),
        (
            "对函数 $f(x) = x^2$ 在区间 $[0, 2]$ 上应用拉格朗日中值定理，得到的中值 $\\xi =$____",
            "中值定理", 2, "blank", "", "1"
        ),
        (
            "下列函数中，在区间 $[-1, 1]$ 上满足罗尔定理条件的是（ ）",
            "中值定理", 3, "choice",
            json.dumps({"A": "$f(x)=|x|$", "B": "$f(x)=\\frac{1}{x}$", "C": "$f(x)=1-x^2$", "D": "$f(x)=x^3$"}), "C"
        ),

        # ================= 5. 导数应用 =================
        (
            "函数 $y = x^3 - 3x$ 的单调递减区间是（ ）",
            "导数应用", 2, "choice",
            json.dumps({"A": "$(-\\infty, -1)$", "B": "$(-1, 1)$", "C": "$(1, +\\infty)$", "D": "$(-1, +\\infty)$"}), "B"
        ),
        (
            "函数 $f(x) = x e^{-x}$ 的最大值为____（保留三位小数）",
            "导数应用", 3, "blank", "", "0.368"  # 1/e 约等于 0.368
        ),
        (
            "曲线 $y = x^4 - 6x^2 + 5$ 的拐点个数为（ ）",
            "导数应用", 2, "choice",
            json.dumps({"A": "0个", "B": "1个", "C": "2个", "D": "3个"}), "C"
        ),

        # ================= 6. 导数证明 =================
        (
            "证明不等式 $e^x > 1+x \\ (x>0)$ 时，常构造辅助函数 $f(x) = e^x - 1 - x$，并利用（ ）证明其单调性。",
            "导数证明", 2, "choice",
            json.dumps({"A": "零点定理", "B": "导数的符号", "C": "积分法", "D": "柯西中值定理"}), "B"
        ),
        (
            "证明方程 $x^3 + x - 1 = 0$ 只有一个实根。设 $f(x)=x^3+x-1$，计算 $f'(0)=$____",
            "导数证明", 1, "blank", "", "1"
        ),
        (
            "若要证明方程 $f(x)=0$ 在 $(a,b)$ 内至少存在一个根，通常首选的定理是（ ）",
            "导数证明", 1, "choice",
            json.dumps({"A": "罗尔定理", "B": "零点定理", "C": "费马引理", "D": "极值第一充分条件"}), "B"
        ),

        # ================= 7. 积分 =================
        (
            "不定积分 $\\int x e^x dx$ 的结果为（ ）",
            "积分", 2, "choice",
            json.dumps({"A": "$e^x + C$", "B": "$x e^x - e^x + C$", "C": "$x e^x + C$", "D": "$\\frac{1}{2}x^2 e^x + C$"}), "B"
        ),
        (
            "定积分 $\\int_{0}^{2} 3x^2 dx$ 的值为____",
            "积分", 1, "blank", "", "8"
        ),
        (
            "计算 $\\int \\frac{1}{1+x^2} dx$，其原函数是（ ）",
            "积分", 1, "choice",
            json.dumps({"A": "$\\arcsin x + C$", "B": "$\\ln|1+x^2| + C$", "C": "$\\arctan x + C$", "D": "$\\tan x + C$"}), "C"
        ),

        # ================= 8. 积分应用 =================
        (
            "由曲线 $y = x^2$ 与直线 $y = x$ 所围成的平面图形的面积 $A$ 为（ ）",
            "积分应用", 2, "choice",
            json.dumps({"A": "$\\frac{1}{2}$", "B": "$\\frac{1}{3}$", "C": "$\\frac{1}{6}$", "D": "1"}), "C"
        ),
        (
            "曲线 $y = \\sqrt{x}$ 在区间 $[0, 1]$ 上的部分绕横轴旋转一周所得旋转体的体积为 $V$，则 $V/\\pi =$____",
            "积分应用", 3, "blank", "", "0.5"
        ),
        (
            "若曲线方程为参数方程 $x=x(t), y=y(t) \\ (\\alpha \\le t \\le \\beta)$，则求该曲线弧长的积分公式为（ ）",
            "积分应用", 2, "choice",
            json.dumps({
                "A": "$\\int_{\\alpha}^{\\beta} \\sqrt{x^2(t)+y^2(t)} dt$", 
                "B": "$\\int_{\\alpha}^{\\beta} \\sqrt{(x'(t))^2+(y'(t))^2} dt$", 
                "C": "$\\int_{\\alpha}^{\\beta} |x'(t)+y'(t)| dt$", 
                "D": "$\\int_{\\alpha}^{\\beta} x(t)y'(t) dt$"
            }), "B"
        ),

        # ================= 9. 重积分 =================
        (
            "二次积分 $\\int_{0}^{1} dx \\int_{0}^{x} f(x,y) dy$ 交换积分次序后为（ ）",
            "重积分", 3, "choice",
            json.dumps({
                "A": "$\\int_{0}^{1} dy \\int_{y}^{1} f(x,y) dx$", 
                "B": "$\\int_{0}^{1} dy \\int_{0}^{y} f(x,y) dx$", 
                "C": "$\\int_{0}^{x} dy \\int_{0}^{1} f(x,y) dx$", 
                "D": "$\\int_{0}^{1} dy \\int_{0}^{x} f(x,y) dx$"
            }), "A"
        ),
        (
            "设区域 $D$ 为单位圆 $x^2+y^2 \\le 1$，计算二重积分 $\\iint_{D} 3 dx dy =$____（填包含 $\\pi$ 的数值，用3.1416近似）",
            "重积分", 2, "blank", "", "9.4248" # 3 * pi
        ),
        (
            "在极坐标系下，二重积分的面积元素 $d\\sigma$ 为（ ）",
            "重积分", 1, "choice",
            json.dumps({"A": "$dr d\\theta$", "B": "$r dr d\\theta$", "C": "$r^2 dr d\\theta$", "D": "$d(r\\cos\\theta) d(r\\sin\\theta)$"}), "B"
        ),

        # ================= 10. 多元微分概念 =================
        (
            "关于二元函数 $f(x,y)$，下列命题正确的是（ ）",
            "多元微分概念", 3, "choice",
            json.dumps({
                "A": "偏导数连续则函数必定可微", 
                "B": "函数连续则偏导数必定存在", 
                "C": "偏导数存在则函数必定连续", 
                "D": "函数可微则偏导数必定连续"
            }), "A"
        ),
        (
            "设函数 $z = x^2 y + y^3$，则该函数在点 $(1, 2)$ 处对 $x$ 的偏导数 $\\frac{\\partial z}{\\partial x} =$____",
            "多元微分概念", 2, "blank", "", "4"
        ),
        (
            "函数在某一点处的方向导数取得最大值的方向是该点的（ ）",
            "多元微分概念", 1, "choice",
            json.dumps({"A": "切线方向", "B": "法线方向", "C": "梯度方向", "D": "等值线方向"}), "C"
        ),

        # ================= 11. 多元微分计算 =================
        (
            "设 $z = u^2 + v^2$，而 $u=x+y, v=x-y$，则 $\\frac{\\partial z}{\\partial x}$ 为（ ）",
            "多元微分计算", 2, "choice",
            json.dumps({"A": "$2x$", "B": "$4x$", "C": "$4y$", "D": "$2u+2v$"}), "B"
        ),
        (
            "求由方程 $x^2 + y^2 + z^2 - 3xyz = 0$ 确定的隐函数 $z=z(x,y)$ 在点 $(1,1,1)$ 处的偏导数 $\\frac{\\partial z}{\\partial x} =$____",
            "多元微分计算", 4, "blank", "", "-1"
        ),
        (
            "函数 $z = f(x,y)$ 的全微分 $dz$ 公式为（ ）",
            "多元微分计算", 1, "choice",
            json.dumps({
                "A": "$dz = f'_x dx + f'_y dy$", 
                "B": "$dz = f'_x + f'_y$", 
                "C": "$dz = f(x+dx, y+dy) - f(x,y)$", 
                "D": "$dz = f'_y dx + f'_x dy$"
            }), "A"
        ),

        # ================= 12. 微分方程 =================
        (
            "微分方程 $y'' + 2y' + y = 0$ 的特征方程为（ ）",
            "微分方程", 1, "choice",
            json.dumps({"A": "$r+1=0$", "B": "$r^2+2r+1=0$", "C": "$r^2+1=0$", "D": "$r^2-2r+1=0$"}), "B"
        ),
        (
            "已知一阶线性微分方程 $y' - y = 0$ 的通解形式为 $y=C e^x$。若满足初始条件 $y(0)=5$，则常数 $C =$____",
            "微分方程", 2, "blank", "", "5"
        ),
        (
            "下列微分方程中，属于可分离变量的微分方程是（ ）",
            "微分方程", 2, "choice",
            json.dumps({"A": "$y' = x+y$", "B": "$y' = xy$", "C": "$y' + xy = x^2$", "D": "$y'' + y = 0$"}), "B"
        ),

        # ================= 13. 曲线积分 =================
        (
            "平面内第二类曲线积分 $\\int_{L} P dx + Q dy$ 与路径无关的充分必要条件是（在单连通域内）（ ）",
            "曲线积分", 2, "choice",
            json.dumps({
                "A": "$\\frac{\\partial P}{\\partial x} = \\frac{\\partial Q}{\\partial y}$", 
                "B": "$\\frac{\\partial P}{\\partial y} = \\frac{\\partial Q}{\\partial x}$", 
                "C": "$\\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} > 0$", 
                "D": "$P=Q$"
            }), "B"
        ),
        (
            "应用格林公式计算，闭曲线积分 $\\oint_{L} x dy - y dx$ 的值，其中 $L$ 为圆周 $x^2+y^2=1$（逆时针）。结果除以 $\\pi$ 为____",
            "曲线积分", 3, "blank", "", "2"
        ),
        (
            "第一类曲线积分 $\\int_{L} f(x,y) ds$ 的几何意义当 $f(x,y) \\equiv 1$ 时代表曲线 $L$ 的（ ）",
            "曲线积分", 1, "choice",
            json.dumps({"A": "面积", "B": "质量", "C": "弧长", "D": "体积"}), "C"
        ),

        # ================= 14. 曲面积分 =================
        (
            "高斯公式（Gauss Divergence Theorem）建立了哪两种积分之间的联系？（ ）",
            "曲面积分", 2, "choice",
            json.dumps({
                "A": "第一类曲线积分与二重积分", 
                "B": "第二类曲线积分与二重积分", 
                "C": "第二类曲面积分与三重积分", 
                "D": "第一类曲面积分与第二类曲面积分"
            }), "C"
        ),
        (
            "向量场 $\\vec{F} = (x, y, z)$ 穿过单位球面 $x^2+y^2+z^2=1$ 的外侧的通量为 $A\\pi$，则 $A=$____",
            "曲面积分", 4, "blank", "", "4"
        ),
        (
            "斯托克斯公式（Stokes' Theorem）的核心在于将空间闭曲线上的线积分转化为该曲线所围成的（ ）上的面积分。",
            "曲面积分", 2, "choice",
            json.dumps({"A": "任意曲面", "B": "平面", "C": "球面", "D": "柱面"}), "A"
        ),

        # ================= 15. 级数判敛 =================
        (
            "关于 $p$ 级数 $\\sum_{n=1}^{\\infty} \\frac{1}{n^p}$ 的敛散性，下列说法正确的是（ ）",
            "级数判敛", 1, "choice",
            json.dumps({"A": "当 $p>1$ 时收敛", "B": "当 $p \\ge 1$ 时收敛", "C": "当 $p<1$ 时收敛", "D": "对任意 $p$ 均发散"}), "A"
        ),
        (
            "应用比值判别法（达朗贝尔判别法）考察级数 $\\sum_{n=1}^{\\infty} \\frac{2^n}{n!}$ 时，计算得出的极限 $\\rho = \\lim_{n \\to \\infty} \\frac{u_{n+1}}{u_n} =$____",
            "级数判敛", 2, "blank", "", "0"
        ),
        (
            "莱布尼茨判别法用于判定下列哪种级数的敛散性？（ ）",
            "级数判敛", 1, "choice",
            json.dumps({"A": "正项级数", "B": "交错级数", "C": "任意项级数", "D": "函数项级数"}), "B"
        ),

        # ================= 16. 幂级数 =================
        (
            "幂级数 $\\sum_{n=1}^{\\infty} \\frac{x^n}{n}$ 的收敛区间为（ ）",
            "幂级数", 3, "choice",
            json.dumps({"A": "$(-1, 1)$", "B": "$[-1, 1)$", "C": "$(-1, 1]$", "D": "$[-1, 1]$"}), "B"
        ),
        (
            "求幂级数 $\\sum_{n=0}^{\\infty} \\frac{x^n}{2^n}$ 的收敛半径 $R=$____",
            "幂级数", 2, "blank", "", "2"
        ),
        (
            "函数 $f(x) = e^x$ 展开为麦克劳林级数（Maclaurin series）时，含 $x^3$ 项的系数为（ ）",
            "幂级数", 2, "choice",
            json.dumps({"A": "$1$", "B": "$\\frac{1}{2}$", "C": "$\\frac{1}{6}$", "D": "$\\frac{1}{24}$"}), "C"
        )
    ]

    c.executemany('''INSERT INTO questions 
                    (content, knowledge_point, difficulty, question_type, options, answer) 
                    VALUES (?, ?, ?, ?, ?, ?)''', sample_questions)

def login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def register_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_questions():
    """获取题库中的所有题目，用于全量重打标或查看"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM questions", conn)
    conn.close()
    return df.to_dict('records')

def get_all_knowledge_points():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT DISTINCT knowledge_point FROM questions", conn)
    conn.close()
    return df['knowledge_point'].tolist()

def get_question_by_kp(kp, user_id):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("""
        SELECT * FROM questions 
        WHERE knowledge_point = ?
        AND q_id NOT IN (
            SELECT q_id FROM records WHERE user_id = ? AND is_correct = 1
        )
        ORDER BY RANDOM() LIMIT 1
    """, conn, params=(kp, user_id))
    if df.empty:
        df = pd.read_sql_query("SELECT * FROM questions WHERE knowledge_point = ? ORDER BY RANDOM() LIMIT 1", conn, params=(kp,))
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None

def save_answer(user_id, q_id, is_correct):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO records (user_id, q_id, is_correct, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, q_id, int(is_correct), datetime.now()))
    conn.commit()
    conn.close()

def calculate_proficiency(user_id, kp):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("""
        SELECT r.is_correct, q.question_type FROM records r
        JOIN questions q ON r.q_id = q.q_id
        WHERE r.user_id = ? AND q.knowledge_point = ?
    """, conn, params=(user_id, kp))
    conn.close()

    tot = len(df)
    if tot == 0:
        return 0.0, 0, 25.0  # 对应P(L0)=0.4，25分

    # ========== 1. 基础正确率计算 ==========
    correct_count = df['is_correct'].sum()
    raw_acc = df['is_correct'].mean() * 100

    # ========== 2. BKT模型核心参数配置 ==========
    P_L0 = 0.4    # 初始掌握概率
    P_T = 0.05    # 学习转移概率
    P_S = 0.1     # 失误概率
    P_G_default = 0.25  # 默认猜测概率（4选1选择题）

    # 初始化当前掌握概率
    current_mastery = P_L0

    for _, row in df.iterrows():
        is_correct = row['is_correct']
        q_type = row['question_type']
        
        # 适配题型的猜测概率：填空题几乎无法蒙对，猜测概率极低
        P_G = 0.05 if q_type == 'blank' else P_G_default

        # 步骤1：根据本次答题结果，计算观测后的后验掌握概率
        if is_correct == 1:
            # 答对的情况：贝叶斯公式更新
            numerator = current_mastery * (1 - P_S)
            denominator = numerator + (1 - current_mastery) * P_G
            posterior_mastery = numerator / denominator if denominator != 0 else current_mastery
        else:
            # 答错的情况：贝叶斯公式更新
            numerator = current_mastery * P_S
            denominator = numerator + (1 - current_mastery) * (1 - P_G)
            posterior_mastery = numerator / denominator if denominator != 0 else current_mastery

        # 步骤2：更新下一次答题前的掌握概率（考虑学习效应）
        current_mastery = posterior_mastery + (1 - posterior_mastery) * P_T

        # 步骤3：限制掌握概率在 [0, 1] 范围内
        current_mastery = max(0, min(1, current_mastery))

    # 计算最终推荐系数
    final_rec_coef = current_mastery * 100
    return round(raw_acc, 1), tot, round(final_rec_coef, 1)

def get_history(user_id, kp):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("""
        SELECT q.content, q.question_type, r.is_correct, r.timestamp
        FROM records r JOIN questions q ON r.q_id = q.q_id
        WHERE r.user_id = ? AND q.knowledge_point = ?
        ORDER BY r.timestamp DESC LIMIT 10
    """, conn, params=(user_id, kp))
    conn.close()
    return df

def get_user_weak_points(user_id):
    """分析用户最近的答题记录，找出正确率最低的知识点"""
    conn = sqlite3.connect(DB_FILE)
    # 获取用户各知识点的错误次数排名前 3
    df = pd.read_sql_query("""
        SELECT q.knowledge_point, COUNT(*) as error_count
        FROM records r JOIN questions q ON r.q_id = q.q_id
        WHERE r.user_id = ? AND r.is_correct = 0
        GROUP BY q.knowledge_point
        ORDER BY error_count DESC LIMIT 3
    """, conn, params=(user_id,))
    conn.close()
    return df['knowledge_point'].tolist()

def get_recommended_question(user_id, current_kp):
    """
    智能推题核心逻辑：
    1. 优先找该知识点下用户没做过的题
    2. 根据用户该知识点的历史正确率匹配难度
    """
    conn = sqlite3.connect(DB_FILE)
    
    # 计算用户在该知识点的当前胜率
    acc, total, rec_coef = calculate_proficiency(user_id, current_kp)
    
    # 难度适配逻辑
    target_diff = 1
    if rec_coef > 85: target_diff = 4
    elif rec_coef > 65: target_diff = 3
    elif rec_coef > 40: target_diff = 2
    
    # 尝试从本地库找一道难度相近且没做对过的题
    df = pd.read_sql_query("""
        SELECT * FROM questions 
        WHERE knowledge_point = ? 
        AND difficulty BETWEEN ? AND ?
        AND q_id NOT IN (SELECT q_id FROM records WHERE user_id = ? AND is_correct = 1)
        ORDER BY RANDOM() LIMIT 1
    """, conn, params=(current_kp, target_diff-1, target_diff+1, user_id))
    
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None

def update_question_tag(q_id: int, new_tag: str):
    """更新题库中某道题的知识点标签"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE questions SET knowledge_point = ? WHERE q_id = ?", (new_tag, q_id))
    conn.commit()
    conn.close()

def get_untagged_questions():
    """获取所有知识点为 '未分类' 或太宽泛的题目（示例）"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT q_id, content FROM questions WHERE knowledge_point IN ('高等数学', '数学一', '未分类')", conn)
    conn.close()
    return df.to_dict('records')

def insert_ai_question(content, kp, diff, q_type, options, answer):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO questions (content, knowledge_point, difficulty, question_type, options, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (content, kp, diff, q_type, options, answer))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id