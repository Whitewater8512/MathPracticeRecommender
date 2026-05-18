而 $\Delta x - [f_{x}^{\prime}(0,0) \cdot \Delta x + f_{y}^{\prime}(0,0) \cdot \Delta y] = \frac{\Delta x \cdot \Delta y}{\sqrt{(\Delta x)^2 + (\Delta y)^2}}$, 如果考虑点 $P(\Delta x, \Delta y)$ 沿着直线 $y = x$ 趋近于 $(0,0)$, 则 $\frac{\Delta x \cdot \Delta y}{\sqrt{(\Delta x)^2 + (\Delta y)^2}} = \frac{\Delta x \cdot \Delta x}{(\Delta x)^2 + (\Delta x)^2} = \frac{1}{2}$, 说明它不能随 $\rho \to 0$ 而趋于 0, 故函数在点 $(0,0)$ 处不可微.

【748】讨论函数 $z = f(x, y) = \begin{cases} (x^2 + y^2) \sin \frac{1}{\sqrt{x^2 + y^2}}, & x^2 + y^2 \neq 0 \\ 0, & x^2 + y^2 = 0 \end{cases}$ 在坐标原点处

(1) 是否连续; (2) 偏导数是否存在; (3) 是否可微; (4) 偏导数是否连续.

解 (1) 当 $(x, y) \neq (0,0)$ 时, $|f(x, y)| \leq x^2 + y^2$, 故 $\lim_{(x, y) \to (0,0)} f(x, y) = 0$, 所以函数在原点连续.

(2) 在 $(0,0)$ 点, $f(x,0) - f(0,0) = \frac{x^2 \sin \frac{1}{\sqrt{x^2}}}{x}$, 所以