设 \( f(x) \) 是定义在区间 \([a, b]\) 上的有界函数，任取分点 \( a = x_0 < x_1 < x_2 < \cdots < x_n = b \)，将 \([a, b]\) 分为 \( n \) 个子区间 \([x_{i-1}, x_i]\)，记 \(\Delta x_i = x_i - x_{i-1}\)（\(i = 1, 2, \cdots, n\)），又在每个子区间上任取一点 \(\xi_i \in [x_{i-1}, x_i]\)（\(i = 1, 2, \cdots, n\)），若不论对区间 \([a, b]\) 如何分法，也不论 \(\xi_i\) 在 \([x_{i-1}, x_i]\) 中如何取法，只要当 \(\lambda = \max \Delta x_i\) 趋于零时，和式 \(\sum_{i=1}^{n} f(\xi_i) \Delta x_i\) 的极限存在，则称此极限值为 \( f(x) \) 在 \([a, b]\) 上的定积分，记为

\[
\int_{a}^{b} f(x) \, dx = \lim_{\lambda \to 0} \sum_{i=1}^{n} f(\xi_i) \Delta x_i
\]

此时也称 \( f(x) \) 在 \([a, b]\) 上可积。

特别地，把区间 \([a, b]\) 分为 \( n \) 等份，\(\xi_i\) 取为每个小区间的右端点，则有

\[
\lim_{n \to \infty} \frac{b-a}{n} \sum_{i=1}^{n} f\left(a + \frac{b-a}{n}i\right) = \int_{a}^{b} f(x) \, dx
\]