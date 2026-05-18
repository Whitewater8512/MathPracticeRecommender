因为 $\lim_{\rho \to 0} \frac{\Delta x - [\frac{\partial f(0,0)}{\partial x} \cdot \Delta x + \frac{\partial f(0,0)}{\partial y} \cdot \Delta y]}{\rho} = \lim_{\rho \to 0} \rho \sin \frac{1}{\rho} = 0$

故函数 $f(x, y)$ 在 $(0,0)$ 点可微, 且 $dz = 0 \cdot dx + 0 \cdot dy = 0$

(4) 当 $(x, y) \neq (0,0)$ 时

$\frac{\partial z}{\partial x} = 2x \sin \frac{1}{\sqrt{x^2 + y^2}} \sqrt{x^2 + y^2} \cos \frac{1}{\sqrt{x^2 + y^2}}$

$\frac{\partial z}{

---

$$\frac{\partial f(x,y)}{\partial x}$$在原点不连续，同样也可说明$$\frac{\partial f(x,y)}{\partial y}$$在原点不连续。

§4. 多元复合函数的求导法则

1. 复合函数的偏导数

设函数$$u=\varphi(x,y)$$，$$v=\psi(x,y)$$在点$$(x,y)$$处存在偏导数，又函数$$z=f(u,v)$$在对应点$$(u,v)$$处具有连续的一阶偏导数，则复合函数$$z=f[\varphi(x,y),\psi(x,y)]$$在点$$(x,y)$$处对$$x$$及$$y$$的偏导数均存在，且有