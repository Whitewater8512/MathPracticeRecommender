$$dZ = \frac{u^v}{x^2 + y^2} \left[\frac{xy}{u} - y \ln u\right] dx + \left[\frac{yx}{u} + x \ln u\right] dy.$$

点评 若 z = z(x, y), 则

$$dz = \frac{\partial z}{\partial x} dx + \frac{\partial z}{\partial y} dy.$$

本题在求 \frac{\partial z}{\partial x}, \frac{\partial z}{\partial y} 时, 使用了多元复合函数

---

```markdown
# 隐函数的全微分

## [744]
设 \( z = f(x, y) \) 是由方程 \( z - y - x + xe^{z-y-x} = 0 \) 所确定的二元函数，求 \( dz \)。

**解：** 把方程两端微分，得
\[ dz - dy - dx + e^{z-y-x} dx + xe^{z-y-x} (dz - dy - dx) = 0. \]
整理得 \((1 + xe^{z-y-x}) dz = (1 + xe^{z-y-x} - e^{z-y-x}) dx + (1 + xe^{z-y-x}) dy.\)
由此得
\[ dz = \frac{1 + (x-1) e^{z-y-x}}{1 + xe^{z-y-x}} dx + dy. \]

## [745]
由方程 \( xz + \sqrt{x^2 + y^2 + z^2} = \sqrt{2} \) 所确定的函数 \( z = z(x, y) \) 在点 (1, 0, -1) 处的全微分 \( dz = \)。