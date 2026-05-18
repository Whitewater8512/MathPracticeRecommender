又 $f[\varphi(x)] = \ln \frac{\varphi(x)+1}{\varphi(x)-1} = \ln x$，从而 $\frac{\varphi(x)+1}{\varphi(x)-1} = x$，$\varphi(x) = \frac{x+1}{x-1}$。

于是
$$
\int \varphi(x) \, dx = \int \frac{x+1}{x-1} \, dx = 2 \ln (x-1) + x + C.
$$

#### [442] 求 $\int x^3 \sqrt{1+x^2} \, dx.$

解法一：
$$
\int x^3 \sqrt{1+x^2} \, dx = \frac{1}{2} \int x^2 \sqrt{1+x^2} \, dx^2 = \frac{1}{2} \int (1+x^2-1) \sqrt{1+x^2} \, d(1+x^2)
$$
$$
= \frac{1}{2} \int (1+x^2)^{3/2} \, d(1+x^2) - \frac{1}{2} \int (1+x^2)^{1/2} \, d(1+x^2)
$$
$$
= \frac{1}{5}(1+x^2)^{5/2} - \frac{1}{3}(1+x^2)^{3/2} + C = \frac{1}{15}(3x^4 + x^2 - 2) \sqrt{1+x^2} + C.
$$