解 原式 \(\lim_{x \to 0} \frac{\int_0^x f(t) \, dt - \int_0^x f(t) \, dt}{\int_0^x f(x - t) \, dt}\) 设 \(x - t = u\)，则 \(\lim_{x \to 0} \frac{\int_0^x f(t) \, dt - \int_0^x f(t) \, dt}{\int_0^x f(u) \, du}\)

\[
= \lim_{x \to 0} \frac{\int_0^x f(t) \, dt + x f(x) - x f(x)}{\int_0^x f(u) \, du + x f(x)} = \lim_{x \to 0} \frac{x f(\xi)}{x f(\xi) + x f(x)}
\]

\[
= \frac{f(0)}{f(0) + f(0)} = \frac{1}{2}, \text{其中} \xi \text{介于} 0 \text{与} x \text{之间}。

# 【488】设函数 \(f(x)\) 有导数，且 \(f(0) = 0\)，

\(F(x) = \int_0^x t^{n-1} f(x^n - t^n) \, dt\)，

证明：\(\lim_{x \to 0} \frac{F(x)}{x^{2n}} = 2n f'(0)\)。

证 令 \(u = x^n - t^n\)，则 \(F(x) = \frac{1}{n} \int_0^{x^n} f(u) \, du\)，有 \(F'(x) = x^{n-1} f(x^n)\)，