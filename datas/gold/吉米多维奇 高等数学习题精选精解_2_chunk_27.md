解：
记 $\int_0^1 f(x) \, dx = a$，$\int_0^1 f(x) \, dx = b$，则 $f(x) = x^2 - ax + 2b$，分别代入前两式得，
$$
\int_0^1 (x^2 - ax + 2b) \, dx = a, \quad \int_0^1 (x^2 - ax + 2b) \, dx = b,
$$

积分得
$$
\left( \frac{1}{3}x^3 - \frac{1}{2}ax^2 + 2bx \right) \bigg|_0^1 = a, \quad \text{即} \quad 3a - 4b = \frac{8}{3},
$$
$$
\left( \frac{1}{3}x^3 - \frac{1}{2}ax^2 + 2bx \right) \bigg|_0^1 = b, \quad \text{即} \quad a - 2b = \frac{2}{3}.
$$

由①、②两式得 $a = \frac{4}{3}, b = \frac{1}{3}$，故 $f(x) = x^2 - \frac{4}{3}x + \frac{2}{3}$。

### 例3
设 $f(x) = x - \int_0^\pi f(x) \cos x \, dx$，求 $f(x)$。

解：
对 $f(x) = x - \int_0^\pi f(x) \cos x \, dx$ 两端同乘 $\cos x$ 并从 $0$ 到 $\pi$ 积分，得
$$
\int_0^\pi f(x) \cos x \, dx = \int_0^\pi x \cos x \, dx - \int_0^\pi f(x) \cos x \, dx \cdot \int_0^\pi \cos x \, dx = -2
$$