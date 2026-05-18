解 设 \(\sqrt{x} = t\), 则 \(x = t^2\). 当 \(x = 0\) 时, \(t = 0\); 当 \(x = 4\) 时, \(t = 2\). 且 \(x = t^2\) 在 \([0, 2]\) 上单调, 故有
\[ \int_0^4 \frac{\sqrt{x}}{1 + \sqrt{x}} \, dx = \int_0^2 \frac{t^2}{1 + t} \, dt = 2 \int_0^2 \frac{t}{1 + t} \, dt = 2 \int_0^2 \left(t - 1 + \frac{1}{1 + t}\right) \, dt \]
\[ = 2 \left[ \frac{t^2}{2} - t + \ln(1 + t) \right]_0^2 = 2 \left[ \frac{4}{2} - 2 + \ln(1 + 2) - \ln 1 \right] = 2 \ln 3. \]

## 【498】
计算 \(\int_0^1 x(1 - x^4)^{\frac{3}{2}} \, dx\).

解 设 \(x^2 = \sin t\). 则 \(x = 0\) 时, \(t = 0\); \(x = 1\) 时, \(t = \frac{\pi}{2}\).
\[ \int_0^1 x(1 - x^4)^{\frac{3}{2}} \, dx = \frac{1}{2} \int_0^{\frac{\pi}{2}} \cos^4 t \, dt = \frac{1}{2} \cdot \frac{3 \pi}{4 \cdot 2 \cdot 2} = \frac{3 \pi}{32}. \]