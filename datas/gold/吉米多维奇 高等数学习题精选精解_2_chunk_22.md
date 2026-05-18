解法二：设 $x = \tan t$，则 $dx = \sec^2 t \, dt$，于是
$$
\int x^3 \sqrt{1+x^2} \, dx = \int \tan^3 t \cdot \sec^3 t \, dt = \int \sec^2 t \tan^2 t \, d(\sec t)
$$
$$
= \int (\sec^4 t - \sec^2 t) \, d(\sec t) = \frac{1}{5} \sec^5 t - \frac{1}{3} \sec^3 t + C
$$
$$
= \frac{1}{5}(1+x^2)^{5/2} - \frac{1}{3}(1+x^2)^{3/2}

---

```markdown
$$\int \frac{\arctan u}{1+u^2} du = \int \arctan u d(\arctan u) = \frac{1}{2} (\arctan u)^2 + C.$$

因此，就要设法利用这一积分公式.

解法一 利用第一换元法计算：

$$\int \frac{\arctan \frac{1}{x}}{1+\left(\frac{1}{x}\right)^2} \frac{dx}{x^2} = \int \frac{\arctan \frac{1}{x}}{1+\left(\frac{1}{x}\right)^2} d\left(\arctan \frac{1}{x}\right) = -\frac{1}{2} \left(\arctan \frac{1}{x}\right)^2 + C.$$

解法二 利用分部积分法计算：

$$\int \frac{\arctan \frac{1}{x}}{1+\left(\frac{1}{x}\right)^2} \frac{dx}{x^2} = \int \arctan \frac{1}{x} d\left(\arctan \frac{1}{x}\right)$$

$$= \arctan \frac{1}{x} \cdot \arctan x - \int \arctan x \frac{1}{1+\left(\frac{1}{x}\right)^2} \left(-\frac{1}{x^2}\right) dx$$

$$= \arctan \frac{1}{x} \cdot \arctan x + \int \frac{\arctan x}{1+x^2} dx$$

$$= \arctan \frac{1}{x} \cdot \arctan x + \int \arctan x d(\arctan x)$$

$$= \arctan \frac{1}{x} \cdot \arctan x + \frac{1}{2} (\arctan x)^2 + C.$$

【444】求 $$\int \frac{dx}{\sin(2x) + 2\sin x}$$

解：

$$\int \frac{dx}{\sin(2x) + 2\sin x} = \int \frac{dx}{2\sin x (\cos x + 1)} = \frac{1}{4} \int \frac{d\left(\frac{x}{2}\right)}{\sin \frac{x}{2} \cos^3 \frac{x}{2}} = \frac{1}{4} \int \frac{d\left(\tan \frac{x}{2}\right)}{\tan \frac{x}{2} \cos^2 \frac{x}{2}}$$

$$= \frac{1}{4} \frac{1 + \tan^2 \frac{x}{2}}{\tan \frac{x}{2}} d\left(\tan \frac{x}{2}\right) = -\frac{1}{8} \tan^2 \frac{x}{2} + \frac{1}{4} \ln \left| \tan \frac{x}{2} \right| + C.$$

利用分部积分公式计算不定积分

【445】计算 $$\int \frac{x^2 e^x}{(x+2)^2} dx.$$

分析 可以用分部积分法计算. 如何选择 $u(x)$ 与 $dv(x)$ 呢？若选 $u(x) = -\frac{x^2}{(x+2)^2}$，则

$$e^x dx = dv(x) = d(e^x), \quad v(x) = e^x, \quad du(x) = \frac{4x}{(x+2)^3} dx$$

$$\int \frac{x^2 e^x}{(x+2)^2} dx = \frac{x^2}{(x+2)^2} e^x - \int \frac{4x}{(x+2)^3} e^x dx,$$

右边的积分并不容易求，因此，采用如下解法：

解 取 $u(x) = x^2 e^x, \quad \frac{1}{(x+2)^2} dx = d\left(-\frac{1}{x+2}\right) = dv(x)$

$$\int \frac{x^2 e^x}{(x+2)^2} dx = \int x^2 e^x d\left(-\frac{1}{x+2}\right) = -\frac{x^2 e^x}{x+2} - \int \left(-\frac{1