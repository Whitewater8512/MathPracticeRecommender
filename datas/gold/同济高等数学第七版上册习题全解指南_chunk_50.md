## 5. 利用等价无穷小的性质，求下列极限：
(1) $\lim_{x \to 0} \frac{\tan 3x}{2x}$;
(2) $\lim_{x \to 0} \frac{\sin (x^n)}{(\sin x)^m}$ (n, m 为正整数);
(3) $\lim_{x \to 0} \frac{\tan x - \sin x}{\sin^3 x}$;
(4) $\lim_{x \to 0} \frac{\sin x - \tan x}{(\sqrt{1 + x^2} - 1)(\sqrt{1 + \sin x} - 1)}$.

解：
(1) $\lim_{x \to 0} \frac{\tan 3x}{2x} = \lim_{x \to 0} \frac{3x}{2x} = \frac{3}{2}$.
(2) $\lim_{x \to 0} \frac{\sin (x^n)}{(\sin x)^m} = \lim_{x \to 0} \frac{x^n}{x^m} = \begin{cases} 0, & n > m, \\ 1, & n = m, \\ \infty, & n < m. \end{cases}$
```

---

# 第一章 函数与极限

## 31

(3) \(\lim_{x \to 0} \frac{\tan x - \sin x}{\sin^3 x} = \lim_{x \to 0} \frac{\sec x - 1}{\sin^2 x} = \lim_{x \to 0} \frac{x^2}{x^2} = \frac{1}{2}.\)