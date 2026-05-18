（2）因为 $\frac{1}{x} \to 0 (x \to \infty)$，$|\arctan x| < \frac{\pi}{2}$，所以

$$\lim_{x \to \infty} \frac{\arctan x}{x} = 0.$$

---

```markdown
# 高等数学（第七版）上册习题全解

## 4. 设 $\{a_n\}$, $\{b_n\}$, $\{c_n\}$ 均为非负数列，且 $\lim_{n \to \infty} a_n = 0$, $\lim_{n \to \infty} b_n = 1$, $\lim_{n \to \infty} c_n = \infty$，下列陈述中哪些是对的，哪些是错的？如果是对的，说明理由；如果是错的，试给出一个反例。

(1) $a_n < b_n, n \in \mathbb{N}_+$；  
(2) $b_n < c_n, n \in \mathbb{N}_+$；  
(3) $\lim_{n \to \infty} a_n c_n$ 不存在；  
(4) $\lim_{n \to \infty} b_n c_n$ 不存在。

解 (1) 错。例如 $a_n = \frac{1}{n}, b_n = \frac{n}{n+1}, n \in \mathbb{N}_+$，当 $n=1$ 时，$a_1 = 1 > \frac{1}{2} = b_1$，故对任意 $n \in \mathbb{N}_+$，$a_n < b_n$ 不成立。

(2) 错。例如 $b_n = \frac{n}{n+1}, c_n = (-1)^n n, n \in \mathbb{N}_+$，当 $n$ 为奇数时，$b_n < c_n$ 不成立。