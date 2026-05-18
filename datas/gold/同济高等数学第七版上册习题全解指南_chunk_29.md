(2) 因为 $\left| \frac{\sin x}{\sqrt{x}} - 0 \right| \leq \frac{1}{\sqrt{x}}$, 要使 $\left| \frac{\sin x}{\sqrt{x}} - 0 \right| < \varepsilon$, 只要 $\frac{1}{\sqrt{x}} < \varepsilon$, 即 $x > \frac{1}{\varepsilon^2}$, 所以 $\forall \varepsilon > 0$, 取 $X = \frac{1}{\varepsilon^2}$, 则当 $x > X$ 时, 就有 $\left| \frac{\sin x}{\sqrt{x}} - 0 \right| < \varepsilon$, 即 $\lim_{x \to \infty} \frac{\sin x}{\sqrt{x}} = 0$.

## 3. 习题 7

当 $x \to 2$ 时, $y = x^2 \to 4$. 问 $\delta$ 等于多少, 使得当 $|x - 2| < \delta$ 时, $|y - 4| < 0.001$?

解 由于 $x \to 2$, $|x - 2| \to 0$, 不妨设 $|x - 2| < 1$, 即 $1 < x < 3$.

要使 $|x^2 - 4| = |x + 2||x - 2| < 5|x - 2| < 0.001$, 只要

$|x - 2| < \frac{0.001}{5} = 0.0002$,

取 $\delta = 0.0002$, 则当 $0 < |x - 2| < \delta$ 时, 就有 $|x^2 - 4| < 0.001$.