【813】在椭圆 $$x^2 + 4y^2 = 4$$ 上求一点, 使其到直线 2x + 3y - 6 = 0 的距离最短.
解 设 P(x, y) 为椭圆 $$x^2 + 4y^2 = 4$$ 上任意一点, 则 P 到直线 2x + 3y - 6 = 0 的距离
$$d = \frac{|2x + 3y - 6|}{\sqrt{13}}$$
求 d 的最小值点即求 $$d^2$$ 的最小值点. 作
$$F(x, y, \lambda) = \frac{1}{13}(2x + 3y - 6)^2 + \lambda(x^2 + 4y^2 - 4)$$
由拉格朗日乘数法, 有
$$\frac{\partial F}{\partial x} = 0,$$ $$\frac{\partial F}{\partial y} = 0,$$ $$\frac{\partial F}{\partial \lambda} = 0$$
即
$$\begin{cases}
\frac{4}{13}(2x + 3y - 6) + 2\lambda x = 0 \\
\frac{6}{13}(2x + 3y - 6) + 8\lambda y = 0 \\
x^2 + 4y^2 - 4 = 0
\end{cases}$$
解之得
$$x_1 = \frac{8}{5}, \quad y_1 = \frac{3}{5}; \quad x_2 = -\frac{8}{5}, \quad y_2 = -\frac{3}{5}$$
于是
$$d \mid_{(x_1, y_1)} = \frac{1}{\sqrt{13}}, \quad d \mid_{(x_2, y_2)} = \frac{11}{\sqrt{13}}$$
由问题的实际意义知最短距离是存在的. 因此 $$\left(-\frac{8}{5}, -\frac{3}{5}\right)$$ 即为所求的点.