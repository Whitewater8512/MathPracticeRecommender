点评 本题考查多元函数的条件极值, 使用了拉格朗日乘数法求解.

【814】求抛物线 $$y = x^2$$ 和直线 $$x - y - 2 = 0$$ 之间的最短距离.
解 设 (x_1, y_1) 为抛物线 $$y = x^2$$ 上任意一点, 而 (x_2, y_2) 是直线 $$x - y - 2 = 0$$ 上的任意点, 求函数
$$d^2 = (x_2 - x_1)^2 + (y_2 - y_1)^2$$
在条件 $$y_1 = x_1^2, x_2 - y_2 - 2 = 0$$ 下的极值. 令
```

---

```markdown
# 高等数学（二）

## 解方程组

$$
F(x_1, x_2, y_1, y_2, \lambda_1, \lambda_2) = (x_2 - x_1)^2 + (y_2 - y_1)^2 + \lambda_1(y_1 - x_1^2) + \lambda_2(x_2 - y_2 - 2)
$$

解方程组

$$
\begin{cases}
\frac{\partial F}{\partial x_1} = -2(x_2 - x_1) - 2\lambda_1 x_1 = 0 \\
\frac{\partial F}{\partial x_2} = 2(x_2 - x_1) + \lambda_2 = 0 \\
\frac{\partial F}{\partial y_1} = -2(y_2 - y_1) + \lambda_1 = 0 \\
\frac{\partial F}{\partial y_2} = 2(y_2 - y_1) - \lambda_2 = 0 \\
y_1 = x_1^2 \\
x_2 - y_2 - 2 = 0
\end{cases}
$$

解此方程组得惟一解