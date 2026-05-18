---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

```markdown
# 第五章 定积分

## §5. 综合提高题型

### 解析

$$\int_{1}^{+\infty} \frac{dx}{x(x+1)} = \left( \ln \left| \frac{x}{x+1} \right| \right) \bigg|_{1}^{+\infty} = \ln 2, \text{积分收敛.}$$

$$\int_{0}^{1} \frac{dx}{x(x+1)} = \lim_{\epsilon \to 0^{+}} \int_{\epsilon}^{1} \frac{dx}{x(x+1)} = \lim_{\epsilon \to 0^{+}} \left( \ln \left| \frac{x}{x+1} \right| \right) \bigg|_{\epsilon}^{1} = +\infty, \text{积分发散.}$$

故应选 (D).

### 点评

由于被积函数中含有绝对值，故应先将其分段表示为

$$|x - x^2| = \begin{cases} 
x - x^2, & 0 \leq x \leq 1 \\
x^2 - x, & x < 0 \text{ 或 } x > 1 
\end{cases}$$

应用积分的可加性化为两个广义积分，分别进行计算.

### [548] 计算积分

$$\int_{\frac{3}{2}}^{\frac{3}{2}} \frac{dx}{\sqrt{|x - x^2|}}.$$

### 解析

注意到被积函数含有绝对值符号且 \(x = 1\) 是其无穷间断点，故