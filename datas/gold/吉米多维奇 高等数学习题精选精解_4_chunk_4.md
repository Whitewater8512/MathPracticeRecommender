## 【1100】
已知级数 \(\sum_{n=1}^{\infty} (-1)^n \frac{x^n}{n} = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots\)，求收敛半径及收敛域。

### 解
\[
\rho = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = \lim_{n \to \infty} \frac{1}{n+1} = 1, \text{所以 } R = 1.
\]

当 \( x = 1 \) 时，\(\sum_{n=1}^{\infty} (-1)^n \frac{1}{n}\) 收敛；\( x = -1 \) 时，\(\sum_{n=1}^{\infty} (-1)^n \frac{(-1)^n}{n} = -\sum_{n=1}^{\infty} \frac{1}{n}\) 发散。

所以收敛半径为 1，收敛域为 \((-1, 1]\)。

## 【1101】
幂级数 \(\sum_{n=1}^{\infty} \frac{n}{2^n + (-3)^n} x^{2n-1}\) 的收敛半径 \( R = \)________。

### 解
\[
\lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = \lim_{n \to \infty} \left| \frac{\frac{n+1}{2^{n+1} + (-3)^{n+1}}}{\frac{n}{2^n + (-3)^n}} \right| = \lim_{n \to \infty} \frac{2^n + (-3)^n}{2^{n+1} + (-3)^{n+1}} = \frac{1}{3}.
\]