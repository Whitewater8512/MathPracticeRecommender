---

```markdown
# 5.3 不定积分的计算

## 使用基本积分公式计算不定积分

### 例题 398
求 \(\int \frac{1 + x + x^2}{x(1 + x^2)} \, dx\)

分析：基本积分表中没有这种类型的积分，我们可以先把被积函数变形，化为表中所示类型之后，再逐项积分。

解：
\[
\int \frac{1 + x + x^2}{x(1 + x^2)} \, dx = \int \frac{x + (1 + x^2)}{x(1 + x^2)} \, dx = \int \left( \frac{1}{1 + x^2} + \frac{1}{x} \right) \, dx = \int \frac{1}{1 + x^2} \, dx + \int \frac{1}{x} \, dx
\]
\[
= \arctan x + \ln |x| + C
\]

### 例题 399
求 \(\int \frac{1 + \sin^2 x}{1 - \cos 2x} \, dx\)

解：
\[
\int \frac{1 + \sin^2 x}{1 - \cos 2x} \, dx = \int \frac{1 + \sin^2 x}{1 - 2\sin^2 x} \, dx = \frac{1}{2} \int \left( \csc^2 x + 1 \right) \, dx = -\frac{1}{2} \cot x + \frac{1}{2} x + C
\]

### 求积分曲线

#### 例题 400
一曲线通过点 \((e^2, 3)\)，且在任一点处的切线斜率等于该点横坐标的倒数，求该积分曲线。