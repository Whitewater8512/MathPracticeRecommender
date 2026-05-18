$$
f(x) = \frac{x^3 + 3x^2 - x - 3}{x^2 + x - 6} = \frac{(x^2 - 1)(x + 3)}{(x + 3)(x - 2)} = \frac{x^2 - 1}{x - 2},
$$

所以

$$
\lim_{x \to 0} f(x) = \frac{1}{2}, \quad \lim_{x \to -3} f(x) = -\frac{8}{5}, \quad \lim_{x \to 2} f(x) = \infty.
$$

### 2. 设函数 $f(x)$ 与 $g(x)$ 在点 $x_0$ 连续，证明函数
$$
\varphi(x) = \max \{f(x), g(x)\}, \quad \psi(x) = \min \{f(x), g(x)\}
$$
在点 $x_0$ 也连续。

证 $\varphi(x) = \max \{f(x), g(x)\} = \frac{1}{2}[f(x) + g(x) + |f(x) - g(x)|]$,

$\psi(x) = \min \{f(x), g(x)\} = \frac{1}{2}[f(x) + g(x) - |f(x) - g(x)|]$.

又若 $f(x)$ 在点 $x_0$ 连续，则 $|f(x)|$ 在点 $x_0$ 也连续；由连续函数的和、差仍连续，故 $\varphi(x), \psi(x)$ 在点 $x_0$ 也连续.

### 3. 求下列极限：

(1) $\lim_{x \to 0} \sqrt{x^2 - 2x + 5}$;

(2) $\lim_{\alpha \to \frac{\pi}{4}} (\sin 2\alpha)^3$;

(3) $\lim_{x \to \frac{\pi}{6}} \ln(2\cos 2x)$;