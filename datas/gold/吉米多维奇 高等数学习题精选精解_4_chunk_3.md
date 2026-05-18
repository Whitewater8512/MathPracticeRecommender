【1098】若 $\sum_{n=1}^{\infty} a_n x^n$ 在 $x = 3$ 处发散，则级数 $\sum_{n=1}^{\infty} a_n \left(x - \frac{1}{2}\right)^n$ 在 $x = -3$ 处 ______.

(A) 条件收敛 (B) 绝对收敛 (C) 发散 (D) 敛散性不变

解 根据阿贝尔引理，因为 $\left|-3 - \frac{1}{2}\right| > |3|$，所以级数在 $x = -3$ 处发散.

故应选 (C).

### 求幂级数的收敛半径及收敛区间

【1099】幂级数 $\sum_{n=1}^{\infty} \frac{x^n}{n}$ 的收敛域为 ______.

解 由

$$
\lim_{n \to \infty} \left| \frac{u_{n+1}}{u_n} \right| = \lim_{n \to \infty} \left| \frac{n+1}{n} \right| = \lim_{n \to \infty} \frac{n}{n+1} = 1,
$$

得级数的收敛半径 $R = 1$，收敛区间为 $(-1, 1)$.

当 $x = 1$ 时，所给幂级数成为调和级数 $\sum_{n=1}^{\infty} \frac{1}{n}$，是发散的；

---

```markdown
# 高等数学复习题讲解

## 当 \( x = -1 \) 时，所给幂级数成为交错级数 \(\sum_{n=1}^{\infty} \frac{(-1)^n}{n}\)，由莱布尼兹定理知是收敛的。所以幂级数 \(\sum_{n=1}^{\infty} \frac{x^n}{n}\) 的收敛域是 \([-1, 1)\)。