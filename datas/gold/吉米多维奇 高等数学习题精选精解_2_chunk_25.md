\[
\lim_{n \to \infty} \frac{1}{n} \sum_{i=1}^{n} f\left(\frac{i}{n}\right) = \int_{0}^{1} f(x) \, dx \quad (\text{此时 } a = 0, b = 1)
\]

使用以上两个公式可计算某些和式的极限。

2. **定积分的基本性质**

(1) 定积分的结果与积分变量无关，即

\[
\int_{a}^{b} f(x) \, dx = \int_{a}^{b} f(t) \, dt
\]

(2) \(\int_{a}^{a} f(x) \, dx = 0\);

(3) \(\int_{a}^{b} f(x) \, dx = -\int_{b}^{a} f(x) \, dx\);

(4) 若 \( f(x) \) 在 \([a, b]\) 上可积，\( k \) 为任一常数，则

\[
\int_{a}^{b} kf(x) \, dx = k \int_{a}^{b} f(x) \, dx
\]

(5) 若 \( f(x), g(x) \) 在 \([a, b]\) 上都可积，则

\[
\int_{a}^{b} [f(x) \pm g(x)] \, dx = \int_{a}^{b} f(x) \, dx \pm \int_{a}^{b} g(x) \, dx
\]

(6) 设函数 \( f(x) \) 在 \([a, c]\), \([c, b]\), \([a, b]\) 上都可积，则

\[
\int_{a}^{b} f(x) \, dx = \int_{a}^{c} f(x) \, dx + \int_{c}^{b} f(x) \, dx
\]

当 \( c \) 点在 \([a, b]\) 外时，结论仍成立；