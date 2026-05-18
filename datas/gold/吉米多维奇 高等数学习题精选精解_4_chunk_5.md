所以 \(|x^2| < 3\) 时级数收敛，从而 \( R = \sqrt{3} \)。

## 【1102】
求 \(\sum_{n=0}^{\infty} \frac{x^{2n}}{(2n)!} = 1 + \frac{x^2}{2!} + \frac{x^4}{4!} + \cdots + \frac{x^{2n}}{(2n)!} + \cdots\) 的收敛区间。

### 解
令 \( x^2 = y \)，从而 \(\sum_{n=0}^{\infty} \frac{x^{2n}}{(2n)!} = \sum_{n=0}^{\infty} \frac{y^n}{(2n)!}\)。

\[
\lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = \lim_{n \to \infty} \frac{(2n+2)!}{(2n)!} = \lim_{n \to \infty} \frac{1}{(2n+1)(2n+2)} = 0.
\]

所以 \( R = +\infty \)，所以 \(\sum_{n=0}^{\infty} \frac{y^n}{(2n)!}\) 收敛区间为 \((- \infty, +\infty)\)，\(|y| = |x^2| < +\infty\)，所以 \(|x| < +\infty\)。

从而原级数收敛区间为 \((- \infty, +\infty)\)。

## 【1103】
\(\sum_{n=0}^{\infty} a_n (x - x_0)^n\)，求其收敛半径。

### 解
令 \( z = x - x_0 \) 得级数 \(\sum_{n=0}^{\infty} a_n z^n\)，其收敛半径为 \( R \)，即 \(|z| < R\)。