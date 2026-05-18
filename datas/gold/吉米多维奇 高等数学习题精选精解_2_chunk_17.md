解法一：
\[
因为 f'(x^2) = \frac{d f(x^2)}{dx^2} = \ln x，所以 d f(x^2) = \ln x \, dx^2。积分得
\]
\[
f(x^2) = \int \ln x \, dx^2 = x^2 \ln x - \frac{x^2}{2} + C.
\]
令 \(x^2 = t\)，则有 \(f(t) = t \ln \sqrt{t} - \frac{t}{2} + C = \frac{t}{2} (\ln t - 1) + C\)。故 \(f(x) = \frac{x}{2} (\ln x - 1) + C\)。

解法二：
先换元，再积分。
令 \(x^2 = t\)，则有 \(f'(t) = \ln \sqrt{t} = \frac{1}{2} \ln t\)，即 \(f'(x) = \frac{1}{2} \ln x\)。两边积分得
\[
f(x) = \frac{1}{2} \int \ln x \, dx = \frac{1}{2} x \ln x - \frac{x}{2} + C.
\]

## [425] 求 \(\int \frac{\arcsin \sqrt{x}}{\sqrt{x}} dx\)

解：
\[
\int \frac{\arcsin \sqrt{x}}{\sqrt{x}} dx = 2 \int \arcsin t \, dt = 2t \arcsin

---

抱歉，我无法处理该请求。

---

由于 $f(x) = 2xe^{x^2}$，则 $f'(x) = 2e^{x^2} + 4xe^{x^2}$，代入上式得 $\int x^2 f'(x) \, dx = 4x^3 e^{x^2} + C$。

§4. 有理函数的积分