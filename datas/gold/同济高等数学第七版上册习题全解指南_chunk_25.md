## 5. 根据函数极限的定义证明：
$$
\begin{aligned}
&\lim_{x \to 3} (3x - 1) = 8; \\
&\lim_{x \to -2} (5x + 2) = 12.
\end{aligned}
$$

---

```markdown
# 一、《高等数学》(第七版)上册习题全解

## 18

## (3) \(\lim_{x \to -2} \frac{x^2 - 4}{x + 2} = -4\)

## (4) \(\lim_{x \to -\frac{1}{2}} \frac{1 - 4x^2}{2x + 1} = 2\)

## 解

### (1) 因为

\[
| (3x - 1) - 8 | = | 3x - 9 | = 3 | x - 3 |
\]

要使 \( | (3x - 1) - 8 | < \varepsilon \)，只要 \( | x - 3 | < \frac{\varepsilon}{3} \)，所以 \(\forall \varepsilon > 0\)，取 \(\delta = \frac{\varepsilon}{3}\)，则当 \(0 < | x - 3 | < \delta\) 时，就有 \( | (3x - 1) - 8 | < \varepsilon \)，即 \(\lim_{x \to 3} (3x - 1) = 8\)。

### (2) 因为

\[
| (5x + 2) - 12 | = | 5x - 10 | = 5 | x - 2 |
\]