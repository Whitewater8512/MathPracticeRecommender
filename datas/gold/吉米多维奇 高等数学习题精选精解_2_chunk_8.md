分析：函数的原函数图形即为该函数的积分曲线。由题意，本题是求函数 \(\frac{1}{x}\) 的通过点 \((e^2, 3)\) 的那条积分曲线。

解：设该曲线的方程为 \(y = f(x)\)。由题意知 \(y' = f'(x) = \frac{1}{x}\)，从而
\[
y = \int \frac{1}{x} \, dx = \ln |x| + C
\]
又曲线过点 \((e^2, 3)\)，所以 \(3 = \ln e^2 + C = 2 + C\)，即得 \(C = 1\)。因此该曲线方程为 \(y = \ln |x| + 1\)。

## §2. 换元积分法

1. **第一换元法（凑微分法）** 设 \(\int f(u) \, du = F(u) + C\)，且 \(u = \varphi(x)\) 可微，则
\[
\int f[\varphi(x)] \varphi'(x) \, dx = \int f[\varphi(x)] \, d[\varphi(x)] = F[\varphi(x)] + C
\]

2. **第二换元法** 设 \(x = \varphi(t)\) 严格单调并可微，且 \(\varphi'(t) \neq 0\)，若 \(\int f[\varphi(t)] \varphi'(t) \, dt = \Phi(t) + C\)，则
\[
\int f(x) \, dx = \Phi[\varphi^{-1}(x)] + C
\]
```

---

# 基本题型

## 使用第一换元法求不定积分