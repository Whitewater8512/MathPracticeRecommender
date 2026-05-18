$$
\begin{aligned}
&= \int \frac{\sin^2 t + \cos^2 t}{\sin^2 t \cos t} dt = \int \frac{\cos t}{\sin^2 t} dt + \int \frac{dt}{\cos t} \\
&= -\frac{1}{\sin t} + \ln \sec t + \tan t + C_1. \\
&\text{画一个直角三角形,使它的一个锐角为 } t, \text{斜边为 } x \text{ (如图 413),} \\
&\text{这时, } \sin t = \frac{\sqrt{x^2 - a^2}}{x}, \tan t = \frac{\sqrt{x^2 - a^2}}{a}, \text{于是所求积分为} \\
&\int \frac{x^2}{(x^2 - a^2)^2} dx = -\frac{x}{\sqrt{x^2 - a^2}} + \ln |x + \sqrt{x^2 - a^2}| + C. \\
&\text{其中 } C = C_1 - \ln a. \\
&\text{【414】求不定积分} \int \frac{dx}{x \sqrt{x^2 + 1}}. \\
&\text{解 令} \frac{1}{x} = t, \text{则} \\
&\text{原式} = \int \frac{1}{t \sqrt{1 + t^2}} dt = -\int \frac{1}{\sqrt{1 + t^2}} dt = -\ln (t + \sqrt{1 + t^2}) + C \\
&= -\ln \left( \frac{1}{x} + \sqrt{1 + \frac{1}{x^2}} \right) + C = -\ln \frac{1 + \sqrt{1 + x^2}}{x} + C. \\
&\text{【415】求} \int \frac{\sqrt{a^2 - x^2}}{x^4} dx. \\
&\text{解 设} x = \frac{1}{t}, \text{那么} dx = -\frac{dt}{t^2}, \text{于是} \\
&\int \frac{\sqrt{a^2 - x^2}}{x^4} dx = \int \frac{\sqrt{a^2 - \frac{1}{t^2}}}{\frac{1}{t^4}} \left( -\frac{dt}{t^2} \right) = -\int \frac{1}{t^4} \left( a^2 t^2 - 1 \right)^{\frac{1}{2}} dt, \\
&\text{当} x > 0 \text{时, 有} \\
&\int \frac{\sqrt{a^2 - x^2}}{x^4} dx = -\frac{1}{2a^2} \left( a^2 t^2 - 1 \right)^{\frac{1}{2}} d(a^2 t^2 - 1) = -\frac{(a^2 t^2 - 1)^{\frac{3}{2}}}{3a^2} + C \\
&= -\frac{(a^2 - x^2)^{\frac{3}{2}}}{3a^2 x^3} + C, \\
&\text{当} x < 0 \text{时, 有相同的结果.故无论何种情形,总有} \\
&\int \frac{\sqrt{a^2 - x^2}}{x^4} dx = \frac{(a^2 - x^2)^{\frac{3}{2}}}{3a^2 x^3} + C. \\
&\text{§3. 分部积分法} \\
&\text{分部积分法 若} u = u(x) \text{与} v = v(x) \text{可微,且} u'(x), v(x) \text{具有原函数,则有} \\
&\int u(x) v'(x) dx = u(x) v(x) - \int v(x) u'(x) dx
\end{aligned}
$$