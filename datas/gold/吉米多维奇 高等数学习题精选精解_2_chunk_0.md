# 第四章 不定积分

## §1. 不定积分的概念与性质

1. **原函数与不定积分的定义**

设函数 \( F(x) \) 与 \( f(x) \) 在区间 \((a, b)\) 内有定义，若对于任意 \( x \in (a, b) \) 有

\[
   F'(x) = f(x) \quad \text{或} \quad \mathrm{d}F(x) = f(x) \mathrm{d}x
   \]

则称 \( F(x) \) 是 \( f(x) \) 在 \((a, b)\) 上的一个原函数。

函数 \( f(x) \) 的全体原函数称为 \( f(x) \) 的不定积分，记为 \(\int f(x) \mathrm{d}x\)。设 \( F(x) \) 是 \( f(x) \) 的一个原函数，则 \(\int f(x) \mathrm{d}x = F(x) + C\)，\( C \) 为任意常数。

2. **不定积分的基本性质**

\[
   (1) \int f'(x) \mathrm{d}x = f(x) + C;
   \]
   \[
   (2) \frac{\mathrm{d}}{\mathrm{d}x} \left[ \int f(x) \mathrm{d}x \right] = f(x);
   \]
   \[
   (3) \int [k_1 f(x) \pm k_2 g(x)] \mathrm{d}x = k_1 \int f(x) \mathrm{d}x \pm k_2 \int g(x) \mathrm{d}x \quad (k_1, k_2 \text{不同时为零}).
   \]

3. **基本公式**