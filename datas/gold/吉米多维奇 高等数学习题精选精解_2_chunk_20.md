### [440] 求 $\int \frac{1}{\sqrt{1+x}+\sqrt[3]{1+x}} \, dx.$

分析：被积函数中出现两个根号 $\sqrt{f(x)}$ 与 $\sqrt[3]{f(x)}$，一般设 $t = \sqrt[3]{f(x)}$，其中 $c$ 为 $u, b$ 的最小公倍数。

解：令 $\sqrt[3]{1+x} = t, x = t^6 - 1, dx = 6t^5 \, dt$，则
$$
\int \frac{1}{\sqrt{1+x}+\sqrt[3]{1+x}} \, dx = \int \frac{1}{t^3+t} \cdot 6t^5 \, dt = 6 \int \frac{t^3}{t^3+t} \, dt = 6 \int \frac{t^3+1-1}{t^3+t} \, dt
$$
$$
= 6 \int \left( t^2 - t + 1 - \frac{1}{t+1} \right) \, dt = 2t^3 - 3t^2 + 6t - 6 \ln |t+1| + C
$$
$$
= 2 \sqrt{1+x} - 3 \sqrt[3]{1+x} + 6 \sqrt[3]{1+x} - 6 \ln |\sqrt[3]{1+x}+1| + C.
$$

### 作代换计算不定积分

#### [441] 设 $f(x^2-1) = \ln \frac{x^2}{x^2-2}$，且 $f[\varphi(x)] = \ln x$，求 $\int \varphi(x) \, dx.$

解：因为 $f(x^2-1) = \ln \frac{(x^2-1)+1}{(x^2-1)-1}$，所以 $f(x) = \ln \frac{x+1}{x-1}$。