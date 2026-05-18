(2) \([\varphi(x)]^2\) 必有间断点；

(3) \(f[\varphi(x)]\) 必有间断点；

(4) \(\frac{\varphi(x)}{f(x)}\) 必有间断点。

解 (1) 错。例如，\(\varphi(x) = \text{sgn}(x) f(x) = e^x\)，\(\varphi[f(x)] = 1\) 在 \(\mathbb{R}\) 上处处连续。

(2) 错。例如，\(\varphi(x) = \begin{cases} 1, & x \in \mathbb{Q} \\ -1, & x \in \mathbb{R} \setminus \mathbb{Q} \end{cases}\)，\([\varphi(x)]^2 = 1\) 在 \(\mathbb{R}\) 上处处连续。

(3) 对。例如，\(\varphi(x)\) 同 (2)，\(f(x) = |x| + 1\)，\(f[\varphi(x)] = 2\) 在 \(\mathbb{R}\) 上处处连续。

(4) 对。因为，若 \(F(x) = \frac{\varphi(x)}{f(x)}\) 在 \(\mathbb{R}\) 上处处连续，则 \(\varphi(x) = F(x) \cdot f(x)\) 也在 \(\mathbb{R}\) 上处处连续，这与已知条件矛盾。

## 6. 设函数

\[ f(x) = \begin{cases} e^x, & x < 0 \\ a + x, & x \geq 0 \end{cases} \]

应当怎样选择数 \(a\)，才能使得 \(f(x)\) 成为在 \((-\infty, +\infty)\) 内的连续函数。