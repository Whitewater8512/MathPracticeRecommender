证
$$
\oint_{\Sigma} u \frac{\partial u}{\partial n} \, dS
$$
$$
= \oint_{\Sigma} u \left[ \frac{\partial u}{\partial x} \cos (n, x) + \frac{\partial u}{\partial y} \cos (n, y) + \frac{\partial u}{\partial z} \cos (n, z) \right] dS
$$
$$
= \oint_{\Sigma} \left[ u \frac{\partial u}{\partial x} \, dy \, dz + u \frac{\partial u}{\partial y} \, dz \, dx + u \frac{\partial u}{\partial z} \, dx \, dy \right]
$$
$$
= \iiint_{\Omega} \left[ \frac{\partial}{\partial x} \left( u \frac{\partial u}{\partial x} \right) + \frac{\partial}{\partial y} \left( u \frac{\partial u}{\partial y} \right) + \frac{\partial}{\partial z} \left( u \frac{\partial u}{\partial z} \right) \right] dx \, dy \, dz
$$
$$
= \iiint_{\Omega} \left[ \left( \frac{\partial u}{\partial x} \right)^2 + \left( \frac{\partial u}{\partial y} \right)^2 + \left( \frac{\partial u}{\partial z} \right)^2 \right] dx \, dy \, dz + \iiint_{\Omega} \left[ u \frac{\partial^2 u}{\partial x^2} + u \frac{\partial^2 u}{\partial y^2} + u \frac{\partial^2 u}{\partial z^2} \right] dx \, dy \, dz
$$
$$
= \iiint_{\Omega} \left[ \left( \frac{\partial u}{\partial x} \right)^2 + \left( \frac{\partial u}{\partial y} \right)^2 + \left( \frac{\partial u}{\partial z} \right)^2 \right] dx \, dy \, dz + \iiint_{\Omega} u \Delta u \, dx \, dy \, dz.

求通量及散度

【1001】设 \(\Sigma\) 是圆锥面 \( z = \sqrt{x^2 + y^2} \) 与平面 \( z = 2 \) 所围成封闭曲面的外侧，则向量场 \( \mathbf{A} = x \mathbf{i} + y \mathbf{j} + z \mathbf{k} \) 通过曲面 \(\Sigma\) 的通量 \(\Phi = \oint_{\Sigma} \mathbf{A} \cdot d\mathbf{S}\).

解
$$
\Phi = \oint_{\Sigma} \mathbf{A} \