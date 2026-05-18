```markdown
【1000】设 \( u(x, y, z) \) 在闭区域 \(\Omega\) 上具有二阶连续偏导数，\(\Sigma\) 为 \(\Omega\) 的边界，\(\frac{\partial u}{\partial n}\) 为 \( u(x, y, z) \) 沿 \(\Sigma\) 的外法线方向导数，并引用拉普拉斯算子 \(\Delta = \left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right)\)，证明
$$
\oint_{\Sigma} u \frac{\partial u}{\partial n} \, dS = \iiint_{\Omega} \left[ -\left( \frac{\partial u}{\partial x} \right)^2 + \left( \frac{\partial u}{\partial y} \right)^2 + \left( \frac{\partial u}{\partial z} \right)^2 \right] \, dx \, dy \, dz + \iiint_{\Omega} u \Delta u \, dx \, dy \, dz.
$$

分析 本例左端是沿闭曲面 \(\Sigma\) 外侧的对面积的曲面积分，而右端则是在 \(\Sigma\) 所围区域 \(\Omega\) 上的三重积分，只有以对坐标的曲面积分为桥梁，才能把它们联系起来。因此，解题时应先用两种类型曲面积分之间的关系把左边的曲面积分化为对坐标的曲面积分，然后利用高斯公式使之化为三重积分。