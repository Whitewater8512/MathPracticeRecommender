$$
\text{证 令} F(x)=f(x)-g(x), G(x)=\int_{a}^{x} F(t) dt, \text{由题设知} G(x)\geq 0, x\in[a,b], G(a)=G(b)=0, G'(x)=F(x). \text{从而}
$$
$$
\int_{a}^{b} xF(x) dx = \int_{a}^{b} x dG(x) = xG(x)\bigg|_{a}^{b} - \int_{a}^{b} G(x) dx = -\int_{a}^{b} G(x) dx.
$$
$$
\text{由于} G(x)\geq 0, x\in[a,b], \text{故有} -\int_{a}^{b} G(x) dx \leq 0, \text{即} \int_{a}^{b} xF(x) dx \leq 0.
$$
$$
\text{因此} \int_{a}^{b} x f(x) dx \leq \int_{a}^{b} x g(x) dx.
$$
$$
\text{点评 本题为基本证明题型. 证明过程中应特别注意微分中值定理的应用. 一般地, 证明积分等式或不等式, 都应引入变限积分, 将其转化为函数等式或不等式.}
$$
$$
\text{§4. 广义积分}
$$
$$
\text{1. 无穷区间上的广义积分 设函数} f(x) \text{在区间} [a, +\infty) \text{上有定义, 在} [a, b] \text{ (} b<+\infty \text{) 上可积, 若极限} \lim_{b\to+\infty} \int_{a}^{b} f(x) dx \text{存在, 则定义}
$$
$$
\int_{a}^{+\infty} f(x) dx = \lim_{b\to+\infty} \int_{a}^{b} f(x) dx,
$$
$$
\text{并称} \int_{a}^{+\infty} f(x) dx \text{为} f(x) \text{在} [a, +\infty) \text{上的广义积分, 这时也称广义积分} \int_{a}^{+\infty} f(x) dx \text{存在或收敛; 若上述极限不存在, 则称广义积分} \int_{a}^{+\infty} f(x) dx \text{不存在或发散.}
$$
$$
\text{类似地, 定义}
$$
$$
\int_{-\infty}^{b} f(x) dx = \lim_{a\to-\infty} \int_{a}^{b} f(x) dx,
$$
$$
\int_{-\infty}^{+\infty} f(x) dx = \int_{-\infty}^{c} f(x) dx + \int_{c}^{+\infty} f(x) dx = \lim_{a\to-\infty} \int_{a}^{c} f(x) dx + \lim_{b\to+\infty} \int_{c}^{b} f(x) dx.
$$
$$
\text{2. 无界函数的广义积分(瑕积分) 设函数} f(x) \text{在} [a, b] \text{上连续, 而且极限} \lim_{x\to b^{-}} f(x) = \infty, \text{若极限} \lim_{\varepsilon\to 0^{+}} \int_{a}^{b-\varepsilon} f(x) dx \text{存在, 则定义}
$$
$$
\int_{a}^{b} f(x) dx = \lim_{\varepsilon\to 0^{+}} \int_{a}^{b-\varepsilon} f(x) dx,
$$
$$
\text{并称} \int_{a}^{b} f(x) dx \text{为} f(x) \text{在} [a, b] \text{上的广义积分, 这时也称广义积分} \int_{a}^{b} f(x) dx \text{存在或收敛; 若上述极限不存在, 则称广义积分} \int_{a}^{b} f(x) dx \text{不存在或发散.}
$$
$$
\text{类似地, 若} f(x) \text{在} (a, b] \text{上连续,} \lim

---

抱歉，我无法处理该请求。

---

```markdown
# 第五章 定积分

## §4. 广义积分

### 解
$$ \int_{1}^{+\infty} \frac{dx}{x \sqrt{x^2 - 1}} = \lim_{b \to +\infty} \int_{1}^{b} \frac{dx}{x \sqrt{x^2 - 1}} = \lim_{b \to +\infty} \int_{1}^{b} \frac{-1}{\sqrt{1 - \frac{1}{x^2}}} d\left(\frac{1}{x}\right) $$

$$ = \lim_{b \to +\infty} \left( -\arcsin \frac{1}{x} \right) \Big|_{1}^{b} = \lim_{b \to +\infty} \left( -\arcsin \frac{1}{b} \right) + \frac{\pi}{2} = \frac{\pi}{2} $$

故应填 $\frac{\pi}{2}$.

### 【531】
$$ \int_{0}^{+\infty} \frac{x dx}{(1 + x^2)^2} = \underline{\hspace{2cm}} $$

### 解
因为 $$ \int_{0}^{+\infty} \frac{x dx}{(1 + x^2)^2} = \frac{1}{2} \int_{0}^{+\infty} \frac{d(1 + x^2)}{(1 + x^2)^2} = -\frac{1}{2} \left[ \frac{1}{1 + x^2} \right]_{0}^{+\infty} = \frac{1}{2} $$

故应填 $\frac{1}{2}$.

### 【532】
$$ \int_{2}^{+\infty} \frac{dx}{(x + 7) \sqrt{x - 2}} = \underline{\hspace{2cm}} $$

### 解
原式 $$ \frac{\sqrt{x - 2}}{t} \Bigg|_{0}^{+\infty} \int_{0}^{+\infty} \frac{2}{t^2 + 9} dt = \frac{2}{3} \arctan \frac{t}{3} \Bigg|_{0}^{+\infty} = \frac{\pi}{3} $$

故应填 $\frac{\pi}{3}$.

### 【533】
$$ \int_{1}^{+\infty} \frac{1}{\sqrt{x}} e^{-\sqrt{x}} dx = \underline{\hspace{2cm}} $$

(A) $2e$ (B) $-2e$ (C) $2e$ (D) $-2e$

### 解
$$ \int_{1}^{+\infty} \frac{1}{\sqrt{x}} e^{-\sqrt{x}} dx = -2 \int_{1}^{+\infty} e^{-\sqrt{x}} d(-\sqrt{x}) = -2 \lim_{b \to +\infty} e^{-\sqrt{x}} \Bigg|_{1}^{b} $$

$$ = -2 \lim_{b \to +\infty} e^{-\sqrt{b}} \Bigg|_{1} = 2e^{-1} = 2e $$

故应选 (A).

### 【534】
计算 $$ I = \int_{1}^{+\infty} \frac{dx}{e^{x} + e^{\frac{1}{x}}} $$

### 解
$$ I = \int_{1}^{+\infty} \frac{e^{\frac{1}{x}} - 1}{e^{\left(x + \frac{1}{x}\right)} + 1} dx = e^{-2} \int_{1}^{+\infty} \frac{de^{x - 1}}{1 + e^{2(x - 1)}} = e^{-2} \arctan e^{x - 1} \Bigg|_{1}^{+\infty} $$

$$ = e^{-2} \left( \frac{\pi}{2} - \frac{\pi}{4} \right) = \frac{\pi}{4} e^{-2} $$

### 【535】
试确定积分 $$ \int_{1}^{+\infty} \frac{dx}{x^a} $$ 在 $a$ 取什么值时收敛，取什么值时发散.

### 解
(1) 当 $a \neq 1$ 时，
$$ \int