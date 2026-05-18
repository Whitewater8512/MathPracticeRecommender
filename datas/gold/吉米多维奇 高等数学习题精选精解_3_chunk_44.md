### 点评 (1) 中令 \( P = \frac{\varphi(y)}{2x^2 + y^4}, Q = \frac{2xy}{2x^2 + y^4} \)，利用格林公式
$$
\oint_{\mathrm{C}} \frac{\varphi(y) \, dx + 2xy \, dy}{2x^2 + y^4} = \iint_{\mathrm{D}} \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, d\sigma = 0.
$$

### (2) 中利用 (1) 和 \(\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}\)，且 \(\varphi(y)\) 中不含 \(x\) 得 \(\varphi(y) = -y^2\)。

### 曲线积分与路径无关的条件

### 【1017】设曲线积分 \(\int_{\mathrm{L}} [f(x) - e^x] \sin y \, dx - f(x) \cos y \, dy\) 与路径无关，其中 \(f(x)\) 具有一阶连续导数，且 \(f(0) = 0\)，则 \(f(x) = \frac{e^x - e^{-x}}{2}\)。

解 \( P = [f(x) - e^x] \sin y, Q = -f(x) \cos y \)。

由 \(\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}\) 得 \([f(x) - e^x] \cos y = -f'(x) \cos y\)。

即 \(f'(x) + f(x) = e^x\)，

---