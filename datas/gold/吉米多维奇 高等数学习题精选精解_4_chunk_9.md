$$
\sum_{n=0}^{\infty} (-1)^n(n^2-n+1) = \frac{4}{27} + \frac{2}{3} = \frac{22}{27}.
$$

## [1123] 设 \( I_n = \int_0^{\frac{\pi}{4}} \sin^n x \cos x \, dx \), \( n = 0,1,2,\ldots \), 求 \(\sum_{n=0}^{\infty} I_n\).

解 由 \( I_n = \int_0^{\frac{\pi}{4}} \sin^n x d(\sin x) = \frac{1}{n+1} (\sin x)^{n+1} \bigg|_0^{\frac{\pi}{4}} = \frac{1}{n+1} \left(\frac{\sqrt{2}}{2}\right)^{n+1} \), 有

$$
\sum_{n=0}^{\infty} I_n = \sum_{n=0}^{\infty} \frac{1}{n+1} \left(\frac{\sqrt{2}}{2}\right)^{n+1}.
$$

令 \( S(x) = \sum_{n=0}^{\infty} \frac{1}{n+1} x^{n+1} \), 则其收敛半径 \( R = 1 \), 在 \( (-1,1) \) 内有

$$
S'(x) = \sum_{n=0}^{\infty} x^n = \frac{1}{1-x},
$$

于是 \( S(x) = \int_0^x \frac{1}{1-t} \, dt = -\ln|1-x|. \)

令 \( x = \frac{\sqrt{2}}{2} \in (-1,1) \), 则