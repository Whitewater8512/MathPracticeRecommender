$$\left|x \sin \frac{1}{x}\right| < \varepsilon,$$

即 $x \sin \frac{1}{x}$ 为当 $x \to 0$ 时的无穷小。

## 2. 无穷大量

### 例 3. 根据定义证明: 函数 $y = \frac{1 + 2x}{x}$ 为当 $x \to 0$ 时的无穷大. 问 $x$ 应满足什么条件, 能使 $|y| > 10^4$?

证 因为 $\left|\frac{1 + 2x}{x}\right| = \left|\frac{1}{x} + 2\right| \geq \left|\frac{1}{x}\right| - 2$, 要使 $\left|\frac{1 + 2x}{x}\right| > M$, 只要 $\left|\frac{1}{x}\right| - 2 > M$, 即 $|x| < \frac{1}{M + 2}$, 所以 $\forall M > 0$, 取 $\delta = \frac{1}{M + 2}$, 则当 $0 < |x - 0| < \delta$ 时, 就有 $\left|\frac{1 + 2x}{x}\right| > M$, 即 $\frac{1 + 2x}{x}$ 为当 $x \to 0$ 时的无穷大.

令 $M = 10^4$, 取 $\delta = \frac{1}{10^4 + 2}$, 当 $0 < |x - 0| < \frac{1}{10^4 + 2}$ 时, 就能使 $\left|\frac{1 + 2x}{x}\right| > 10^4$.