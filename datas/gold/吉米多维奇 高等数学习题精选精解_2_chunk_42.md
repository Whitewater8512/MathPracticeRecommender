### 【518】
设 $f(2x-1) = \frac{\ln x}{\sqrt{x}}$, 求 $\int_{1}^{7} f(x) dx$.

解 令 $x = 2t - 1$, 则 $dx = 2 dt$,
$$
\int_{1}^{7} f(x) dx = 2 \int_{1}^{4} f(2t-1) dt = 2 \int_{1}^{4} f(2x-1) dx = 2 \int_{1}^{4} \frac{\ln x}{\sqrt{x}} dx = 4 \int_{1}^{4} \ln x d(\sqrt{x})
$$
$$
= 4(\sqrt{x} \ln x \bigg|_{1}^{4} - \int_{1}^{4} \sqrt{x} \cdot \frac{1}{x} dx) = 8(\ln 4 - \sqrt{x} \bigg|_{1}^{4}) = 8(\ln 4 - 1).

### 【519】
计算 $\int_{0}^{\ln 2} \sqrt{1 - e^{-2x}} dx$.

解 原式 $= \int_{0}^{\ln 2} e^{-x} \sqrt{e^{2x} - 1} dx = -e^{-x} \sqrt{e^{2x} - 1} \bigg|_{0}^{\ln 2} + \int_{0}^{\ln 2} \frac{e^{x} dx}{\sqrt{e^{2x} - 1}}$
$$
= -\frac{\sqrt{3}}{2} + \ln(e^x + \sqrt{e^{2x} - 1}) \bigg|_{0}^{\ln 2} = -\frac{\sqrt{3}}{2} + \ln(2 + \sqrt{3}).