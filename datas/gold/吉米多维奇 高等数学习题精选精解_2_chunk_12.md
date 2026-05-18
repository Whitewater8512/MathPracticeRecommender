---

# 考研数学复习指导

## 一、基本题型

### 使用分部积分公式求不定积分

#### [416] 求 $\int \ln(x + \sqrt{x^2 + 1}) \, dx$

解：
$$
\int \ln(x + \sqrt{x^2 + 1}) \, dx = x \ln(x + \sqrt{x^2 + 1}) - \int x \cdot \frac{1}{\sqrt{x^2 + 1}} \left(1 + \frac{x}{\sqrt{x^2 + 1}}\right) \, dx
$$
$$
= x \ln(x + \sqrt{x^2 + 1}) - \int \frac{x}{\sqrt{x^2 + 1}} \, dx = x \ln(x + \sqrt{x^2 + 1}) - \sqrt{x^2 + 1} + C.
$$

#### [417] 计算 $\int \frac{x + \ln^2 x}{(x \ln x)^2} \, dx$