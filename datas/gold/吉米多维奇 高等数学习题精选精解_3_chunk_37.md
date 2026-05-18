$$
\iint_{\Sigma} f(x, y, z) \, dS = \iint_{D} f(x, y, z(x, y)) \sqrt{1 + \left( \frac{\partial z}{\partial x} \right)^2 + \left( \frac{\partial z}{\partial y} \right)^2} \, dx \, dy.
$$

本题中 $D: x^2 + y^2 \leq 1, z = 4 - x - y, f(x, y, z) = y$,

因此 $\iint_{\Sigma} y \, dS = \iint_{D} y \sqrt{1 + 1 + 1} \, dx \, dy = \sqrt{3} \iint_{D} y \, dx \, dy = \sqrt{3} \int_{0}^{2\pi} \sin \theta \, d\theta \cdot \int_{0}^{1} r^2 \, dr = 0$.

故应选 (A).

【970】计算曲面积分 $\iint_{\Sigma} z \, dS$, 其中 $\Sigma$ 为锥面 $z = \sqrt{x^2 + y^2}$ 在柱体 $x^2 + y^2 \leq 2x$ 内的部分.

解 $\Sigma$ 在 $xOy$ 平面上的投影区域为 $D: x^2 + y^2 \leq 2x$.

$$
dS = \sqrt{1 + \left( \frac{\partial z}{\partial x} \right)^2 + \left( \frac{\partial z}{\partial y} \right)^2} \, d\sigma = \sqrt{2} \, d\sigma.
$$