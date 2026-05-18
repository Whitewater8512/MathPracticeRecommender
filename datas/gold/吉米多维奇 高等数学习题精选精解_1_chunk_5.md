$f_2(x) = f[f_1(x)] = \frac{f_1(x)}{\sqrt{1 + f_1^2(x)}} = \frac{x}{\sqrt{1 + 3x^2}}$,

一般地，可用数学归纳法证明

$f_n(x) = f[f_{n-1}(x)] = \frac{x}{\sqrt{1 + (n+1)x^2}} \quad (n = 2, 3, 4, \ldots)$

故应填 $\frac{x}{\sqrt{1 + (n+1)x^2}}$.

【10】设 $a_0 + a_1x + a_2x^2 + \cdots + a_8x^8 = (2x - 1)^8$, 求 $a_1 + a_2 + \cdots + a_7$.

解 设 $f(x) = a_0 + a_1x + a_2x^2 + \cdots + a_8x^8 = (2x - 1)^8$, 则

$f(0) = a_0 = 1$, $f(1) = a_0 + a_1 + \cdots + a_8 = 1$.

比较两边 $x^8$ 的系数 $a_8 = 2^8$.

故 $a_1 + a_2 + \cdots + a_7 = 1 - a_0 - a_8 = -256$.

【11】设 $f(x)$ 满足 $f^2(\ln x) - 2xf(\ln x) + x^2\ln x = 0$, 且 $f(0) = 0$, 求 $f(x)$.

解 令 $t = \ln x$, 即 $x = e^t$, 则有 $f^2(t) - 2ef(t) + te^t = 0$,

由此可解得 $f(t) = e^t \pm \sqrt{e^{2t} - te^t} = e^t(1 \pm \sqrt{1 - t})$.