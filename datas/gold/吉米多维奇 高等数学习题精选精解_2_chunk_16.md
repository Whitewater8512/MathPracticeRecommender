解：
\[
\int \frac{\ln \sin x}{\sin^2 x} dx = -\int \ln \sin x \, d(\cot x) = -\cot x \ln \sin x + \int \cot x \cdot \frac{\cos x}{\sin x} dx
\]
\[
= -\cot x \ln \sin x + \int (\csc^2 x - 1) dx = -\cot x \ln \sin x - \cot x - x + C.
\]

故应填 \(-\cot x \ln \sin x - \cot x - x + C\)。

点评 因为 \(\frac{1}{\sin^2 x} dx = -d(\cot x)\)，故采用分部积分公式计算。

一般地，对形如 \(\int \frac{f(x)}{\varphi(x)} dx\) 的积分可考虑转化为 \(\int f(x) d(g(x))\)，然后使用分部积分公式计算，其中 \(g'(x) = \frac{1}{\varphi(x)}\)。

先作代换，再使用分部积分公式计算。

## [424] 设 \(f'(x^2) = \ln x\) (\(x > 0\))，求 \(f(x)\)。