# 第一章 函数与极限

## (3) \( x_{n+1} = \sqrt{2 + x_n} \) (\( n \in \mathbb{N}_+ \)), \( x_1 = \sqrt{2} \).

先证数列 \( \{x_n\} \) 有界：

\( n = 1 \) 时, \( x_1 = \sqrt{2} < 2 \); 假定 \( n = k \) 时, \( x_k < 2 \). 当 \( n = k + 1 \) 时, \( x_{k+1} = \sqrt{2 + x_k} < \sqrt{2 + 2} = 2 \). 故 \( x_n < 2 \) (\( n \in \mathbb{N}_+ \)).

再证数列 \( \{x_n\} \) 单调增加：

因

$$
x_{n+1} - x_n = \frac{2 + x_n - x_n^2}{\sqrt{2 + x_n} + x_n} = -\frac{(x_n - 2)(x_n + 1)}{\sqrt{2 + x_n} + x_n},
$$

由 \( 0 < x_n < 2 \), 得 \( x_{n+1} - x_n > 0 \), 即 \( x_{n+1} > x_n \) (\( n \in \mathbb{N}_+ \)).

由单调有界准则, 即知 \(\lim_{n \to \infty} x_n\) 存在.

记 \(\lim_{n \to \infty} x_n = a\). 由 \( x_{n+1} = \sqrt{2 + x_n} \), 得 \( a^2 = 2 + a \). 两端同时取极限得

$$
a^2 = 2 + a \implies a^2 - a - 2 = 0 \implies a_1 = 2, a_2 = -1 \, (\text{舍去}).
$$