---

```markdown
# 【486】确定常数 \(a, b, c\) 的值，使 \(\lim_{x \to 0} \frac{a x - \sin x}{\int_b^x \ln(1 + t^3) \, dt} = c \)（\(c \neq 0\)）。

解 由于 \(x \to 0\) 时，\(a x - \sin x \to 0\)，且极限 \(c\) 不为零，所以当 \(x \to 0\) 时，\(\int_b^x \ln(1 + t^3) \, dt \to 0\)，故必有 \(b = 0\)。

由于 \(\lim_{x \to 0} \frac{a x - \sin x}{\int_0^x \ln(1 + t^3) \, dt} = \lim_{x \to 0} \frac{a - \cos x}{\ln(1 + x^3)} = \lim_{x \to 0} \frac{x(a - \cos x)}{\ln(1 + x^3)}\)

\[
= \lim_{x \to 0} x \frac{a - \cos x}{x^3} = \lim_{x \to 0} \frac{a - \cos x}{x^2} = c \quad (c \neq 0),
\]

故必有 \(a = 1\)，从而 \(c = \frac{1}{2}\)。

# 【487】设函数 \(f(x)\) 连续，且 \(f(0) \neq 0\)，求极限 \(\lim_{x \to 0} \frac{\int_0^x (x - t) f(t) \, dt}{\int_0^x f(x - t) \, dt}\)。