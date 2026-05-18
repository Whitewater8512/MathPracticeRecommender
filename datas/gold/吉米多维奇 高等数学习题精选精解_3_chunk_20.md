$$
x_1 = \frac{1}{2}, \quad y_1 = \frac{1}{4}, \quad x_2 = \frac{11}{8}, \quad y_2 = -\frac{5}{8}
$$

显然，当$(x_1, y_1), (x_2, y_2)$中至少有一个移向无穷远处时，$d \to +\infty$，故$d$的最小值在有限点处达到，从而在点$\left(\frac{1}{2}, \frac{1}{4}\right), \left(\frac{11}{8}, -\frac{5}{8}\right)$处，取得最短距离$d = \frac{7}{8}\sqrt{2}$。

## 【815】

在已给的椭球面$\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1$内一切内接的长方体(各边分别平行坐标轴)中，求其体积最大者。

解 设$x, y, z$为长方体在第一卦限中的顶点坐标，则长方体的体积为 $V = 8xyz$。

因为$(x, y, z)$在椭球面上，所以它满足方程

$$
\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1
$$

问题是求函数$V = 8xyz$在满足条件$\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1$下的最大值，为此，引入下面的拉格朗日函数

$$
F(x, y, z, \lambda) = 8xyz + \lambda \left(\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} - 1\right)
$$

由