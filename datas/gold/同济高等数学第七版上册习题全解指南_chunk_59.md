证：
1. \(\forall \varepsilon > 0\)，取 \(\delta = \varepsilon\)，则当 \(|x - 0| = |x| < \delta\) 时，
   $$
   |f(x) - f(0)| = |f(x)| \leq |x| < \varepsilon,
   $$
   故 \(\lim_{x \to 0} f(x) = f(0)\)，即 \( f(x) \) 在 \( x = 0 \) 连续。

2. 我们证明：\(\forall x_0 \neq 0\)，\( f(x) \) 在 \( x_0 \) 不连续。

若 \( x_0 = r \neq 0\)，\( r \in \mathbb{Q} \)，则 \( f(x_0) = f(r) = r \)。

分别取一有理数列 \(\{r_n\}\)：\( r_n \to r \)（\( n \to \infty \)），\( r_n \neq r \)；取一无理数列 \(\{s_n\}\)：\( s_n \to r \)（\( n \to \infty \)），则
   $$
   \lim_{n \to \infty} f(r_n) = \lim_{n \to \infty} r_n = r, \quad \lim_{n \to \infty} f(s_n) = \lim_{n \to \infty} 0 = 0,
   $$
   而 \( r \neq 0 \)，由函数极限与数列极限的关系知 \(\lim_{x \to r} f(x)\) 不存在，故 \( f(x) \) 在 \( r \) 处不连续。