解 令 $\sqrt{2x-1} = t$, $x = \frac{1+t^2}{2}$, $dx = t \, dt$, 则

$$\int_{1}^{5} \frac{x-1}{1+\sqrt{2x-1}} \, dx = \int_{1}^{\sqrt{9}} \frac{\frac{1+t^2}{2}-1}{1+t} \cdot t \, dt = \frac{1}{2} \int_{1}^{3} (t^2 - t) \, dt = \frac{1}{2} \left[ \frac{1}{3} t^3 - \frac{1}{2} t^2 \right]_{1}^{3} = \frac{7}{3}.$$

### 【502】求 $\int_{\ln 2}^{\ln 4} \frac{dx}{\sqrt{e^x - 1}}$.

解 令 $\sqrt{e^x - 1} = t$, 故 $x = \ln(t^2 + 1)$. 当 $x = \ln 2$ 时, $t = 1$; 当 $x = \ln 4$ 时, $t = \sqrt{3}$. 故

$$\int_{\ln 2}^{\ln 4} \frac{dx}{\sqrt{e^x - 1}} = \int_{1}^{\sqrt{3}} \frac{2t}{t^2 + 1} \, dt = 2 \int_{1}^{\sqrt{3}} \frac{1}{t^2 + 1} \, dt = 2 \arctan t \bigg|_{1}^{\sqrt{3}} = 2 \left( \frac{\pi}{3} - \frac{\pi}{4} \right) = \frac{\pi}{6}.$$