设函数 \( z = f(x, y) \) 具有连续的一阶偏导数，则函数 \( z \) 在 \( P(x, y) \) 处的梯度是一个向量，记为

\[ \nabla f = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right) \]

```

---

```markdown
gradz，它在 \(x, y\) 坐标轴上的投影分别为在该点处的偏导数 \(\frac{\partial z}{\partial x}\) 与 \(\frac{\partial z}{\partial y}\)，即

\[
gradz = \frac{\partial z}{\partial x}i + \frac{\partial z}{\partial y}j
\]

函数 \(z = f(x, y)\) 在点 \(P(x, y)\) 处沿 \(l\) 方向上的方向导数 \(\frac{\partial z}{\partial l}\)，等于函数在该点处的梯度 gradz 在 \(l\) 方向上的投影，即

\[
\frac{\partial z}{\partial l} = gradz \cdot l^*
\]

其中，\(l^*\) 是射线 \(l\) 方向上的单位向量。

函数 \(z = f(x, y)\) 在点 \(P\) 处的梯度 gradz 的模是函数 \(z\) 在该点处方向导数的最大值，它的方向与函数 \(z\) 在点 \(P\) 处取最大方向导数的方向一致。

同样，三元函数 \(u = f(x, y, z)\) 具有连续的一阶偏导数时，函数 \(u\) 在点 \(P(x, y, z)\) 处的梯度为