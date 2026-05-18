```markdown
# 第八章 多元函数微分法及其应用

## §5. 隐函数的求导法则

### 【765】设函数 \( u = f(x, y, z) \) 具有连续的二阶偏导数，则 \(\frac{\partial^2 u}{\partial x \partial y} = \underline{\hspace{2cm}}\)。

**解** 令 \( v = xy \), \( w = xz \)，则 \( u = f(x, v, w) \)，于是

\[
\frac{\partial u}{\partial x} = f_x + f_v \cdot v_x + f_w \cdot w_x = f_x + yf_v + zf_w,
\]

\[
\frac{\partial^2 u}{\partial x \partial y} = (f_x' \cdot v_y + f_v' \cdot w_y) + y(f_v' \cdot v_y + f_{vv}' \cdot w_y) + z(f_w' \cdot v_y + f_{vw}' \cdot w_y) + f_{wv}' \cdot w_y
\]

\[
= xf_{xx} + xyf_{vx} + xzf_{wx} + yf_v + zf_w.
\]

故应填 \( xf_{xx} + xyf_{vx} + xzf_{wx} + yf_v + zf_w \)。

**点评** 对于中间变量或自变量多于两个的情况，复合函数求导法则可进行相应推广。原则为：函数对某个自变量求偏导数时，必须通过一切有关的中间变量，有几个中间变量，公式中就应有几项相加。其中每一项都应是函数对某个中间变量的偏导数与这个中间变量对该自变量偏导数的乘积，此法则也称为链式法则。

### 一元隐函数求导法则