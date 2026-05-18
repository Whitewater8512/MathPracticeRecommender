### 【503】已知 $\int_{0}^{\ln a} e^x \cdot \sqrt{3 - 2e^x} \, dx = \frac{1}{3}$, 求 $a$ 的值.

解 $\int_{0}^{\ln a} e^x \cdot \sqrt{3 - 2e^x} \, dx = -\frac{1}{2} \int_{0}^{\ln a} \sqrt{3 - 2e^x} \, d(3 - 2e^x)$.

令 $3 - 2e^x = t$, 所以

$$\int_{0}^{\ln a} e^x \cdot \sqrt{3 - 2e^x} \, dx = -\frac{1}{2} \int_{3}^{3 - 2a} \sqrt{t} \, dt = -\frac{1}{2} \cdot \frac{2}{3} t^{\frac{3}{2}} \bigg|_{3}^{3 - 2a} = -\frac{1}{3} \cdot \left[ \sqrt{(3 - 2a)^3} - 1 \right],$$

由 $\int_{0}^{\ln a} e^x \cdot \sqrt{3 - 2e^x} \, dx = \frac{1}{3}$, 故 $-\frac{1}{3} \cdot \left[ \sqrt{(3 - 2a)^3} - 1 \right] = \frac{1}{3}$.

即 $\sqrt{(3 - 2a)^3} = 0$, 也即 $3 - 2a = 0$.

所以 $a = \frac{3}{2}$.

### 利用定积分的换元法证明等式

#### 【504】当 $x > 0$ 时, 证明: $\int_{1}^{x} \frac{1}{1 + t^2} \, dt = \int_{1}^{x} \frac{1}{1 + u^2} \, du$.