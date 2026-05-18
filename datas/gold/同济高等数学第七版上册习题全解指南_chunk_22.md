解 (1) 错误。如对数列 $\left\{\left(-1\right)^n + \frac{1}{n}\right\}, a = 1$。对任给的 $\varepsilon > 0$（设 $\varepsilon < 1$），存在 $N = \left\lfloor \frac{1}{\varepsilon} \right\rfloor$，当 $n > N$ 时，$\left(-1\right)^n + \frac{1}{n} - 1 \leq \frac{1}{n} < \varepsilon$，但 $\left\{\left(-1\right)^n + \frac{1}{n}\right\}$ 的极限不存在。

(2) 错误。如对数列
$$x_n = \begin{cases} 
n, & n = 2k - 1, \\
1 - \frac{1}{n}, & n = 2k, 
\end{cases} \quad k \in \mathbb{N}_+, \quad a = 1.$$

对任给的 $\varepsilon > 0$（设 $\varepsilon < 1$），存在 $N = \left\lfloor \frac{1}{\varepsilon} \right\rfloor$，当 $n > N$ 且 $n$ 为偶数时，$|x_n - a| = \frac{1}{n} < \varepsilon$ 成立，但 $\{x_n\}$ 的极限不存在。