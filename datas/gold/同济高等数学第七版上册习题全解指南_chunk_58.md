\[ f(x) = \begin{cases} 
1, & x \geq 0, \\
-1, & x < 0. 
\end{cases} \]

则 \( |f(x)| \) 在 \( x = 0 \) 处连续，而 \( f(x) \) 在 \( x = 0 \) 处不连续。

#### 6. 证明：若函数 \( f(x) \) 在点 \( x_0 \) 连续且 \( f(x_0) \neq 0 \)，则存在 \( x_0 \) 的某一邻域 \( U(x_0) \)，当 \( x \in U(x_0) \) 时，\( f(x) \neq 0 \)。

**证**

若 \( f(x_0) > 0 \)，因为 \( f(x) \) 在 \( x_0 \) 连续，所以取 \( \varepsilon = \frac{1}{2} f(x_0) > 0 \)，\(\exists \delta > 0\)，当 \( x \in U(x_0, \delta) \) 时，有 \( |f(x) - f(x_0)| < \frac{1}{2} f(x_0) \)，即

\[ 0 < \frac{1}{2} f(x_0) < f(x) < \frac{3}{2} f(x_0). \]
```

---

# 第一章 函数与极限

## 7. 设

$$
f(x) = \begin{cases} 
x, & x \in \mathbb{Q}, \\
0, & x \in \mathbb{R} \setminus \mathbb{Q}.
\end{cases}
$$

证明：
1. \( f(x) \) 在 \( x = 0 \) 连续；
2. \( f(x) \) 在非零的 \( x \) 处都不连续。