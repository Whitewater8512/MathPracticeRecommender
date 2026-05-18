$= \left[ x^2 (e^x - 1) \right] = 2x(e^x - 1) + 2x^3 e^x, \quad -\infty < x < +\infty$

利用幂级数的和函数求数项级数的和

【1121】 $\sum_{n=1}^{\infty} n \left( \frac{1}{2} \right)^{n-1} = \underline{\hspace{1cm}}.$

解 记 $S(x)=\sum_{n=1}^{\infty} nx^{n-1}$

$$\int_{0}^{x} S(x)dx = \int_{0}^{x} \left( \sum_{n=1}^{\infty} nx^{n-1} \right)dx = \sum_{n=1}^{\infty} \left( \int_{0}^{x} nx^{n-1} dx \right) = \sum_{n=1}^{\infty} x^n = \frac{x}{1-x}, \quad |x| < 1$$

所以 $S(x) = \left( \frac{x}{1-x} \right)' = \frac{1}{(1-x)^2}, \quad |x| < 1$

当 $x = \frac{1}{2}$ 时, $S\left( \frac{1}{2} \right) = \left( \frac{1}{1 - \frac{1}{2}} \right)^2 = 4$. 所以 $\sum_{n=1}^{\infty} n \left( \frac{1}{2} \right)^{n-1} = S\left( \frac{1}{2} \right) = 4$.

故应填 4.