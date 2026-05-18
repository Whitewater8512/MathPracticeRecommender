$\lim_{x \to 0} \frac{f(x,0) - f(0,0)}{x} = \lim_{x \to 0} x \sin \frac{1}{\sqrt{x^2}} = 0$

即偏导数 $\frac{\partial f(0,0)}{\partial x}$ 存在, 且 $\frac{\partial f(0,0)}{\partial x} = 0$.

同理 $\frac{\partial f(0,0)}{\partial y}$ 也存在, 其值为零.

(3) 由 (2) 知, $\frac{\partial f(0,0)}{\partial x} = \frac{\partial f(0,0)}{\partial y} = 0$,

故 $\Delta x - [\frac{\partial f(0,0)}{\partial x} \cdot \Delta x + \frac{\partial f(0,0)}{\partial y} \cdot \Delta y] = f(\Delta x, \Delta y) - f(0,0) - [0 \cdot \Delta x + 0 \cdot \Delta y]$

$= [(\Delta x)^2 + (\Delta y)^2] \sin \frac{1}{\sqrt{(\Delta x)^2 + (\Delta y)^2}}$