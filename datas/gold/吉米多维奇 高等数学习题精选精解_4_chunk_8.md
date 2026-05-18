点评 本题中把级数 $\sum_{n=1}^{\infty} u_n$ 视为幂级数 $\sum_{n=1}^{\infty} a_n x^n$ 在 $x = x_0$ 时所得的数项级数, 通过求幂级数 $\sum_{n=1}^{\infty} a_n x^n$ 的和函数 $S(x)$, 可得 $\sum_{n=1}^{\infty} u_n = S(x_0)$, 这是求数项级数和函数的常用方法.

【1122】求级数 $\sum_{n=0}^{\infty} (-1)^n \frac{(2n-n+1)}{2^n}$ 的和.

解 $\sum_{n=0}^{\infty} (-1)^n \frac{(2n-n+1)}{2^n} = \sum_{n=0}^{\infty} n(n-1) \left( -\frac{1}{2} \right)^n + \sum_{n=0}^{\infty} \left( -\frac{1}{2} \right)^n$,

其中 $\sum_{n=0}^{\infty} \left( -\frac{1}{2} \right)^n = \frac{1}{1 + \frac{1}{2}} = \frac{2}{3}$.

设

---

```markdown
# 4.3 级数求和问题

$$
\sum_{n=0}^{\infty} n(n-1)x^n = \frac{2x^2}{(1-x)^3}, \quad x \in (-1,1).
$$

$$
\sum_{n=0}^{\infty} n(n-1)\left(-\frac{1}{2}\right)^n = \frac{4}{27}.
$$

所以