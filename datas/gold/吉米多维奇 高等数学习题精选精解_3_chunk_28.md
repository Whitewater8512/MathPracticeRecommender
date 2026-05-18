解
$$
\iiint_{\Omega} [-e^3 \tan(x^2 y^3) + 3] \, dV = \iiint_{\Omega} e^3 \tan(x^2 y^3) \

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

```markdown
# 第九章 重积分

## §4 综合提高题型

### 从而
$$ A = \iint_{B} \sqrt{1 - x^2 - y^2} \, dx \, dy - A $$

### 所以
$$ 2A = \int_{0}^{\frac{\pi}{2}} d\theta \int_{0}^{\sin\theta} \sqrt{1 - r^2} \cdot r \, dr $$

$$ = \frac{1}{3} \int_{0}^{\frac{\pi}{2}} (1 - \cos^3\theta) \, d\theta = \frac{1}{3} \left( \frac{\pi}{2} - \frac{2}{3} \right) $$

### 故
$$ A = \frac{1}{6} \left( \frac{\pi}{2} - \frac{2}{3} \right) $$

### 于是
$$ f(x, y) = \sqrt{1 - x^2 - y^2} - \frac{4}{3\pi} \left( \frac{\pi}{2} - \frac{2}{3} \right) $$

### 点评
由二重积分的定义知 $\iint_{B} f(u, v) \, du \, dv$ 是常数，且 $\iint_{B} f(x, y) \, dx \, dy = \iint_{B} f(u, v) \, du \, dv$，这样就把求 $f(x, y)$ 的问题转化为求 $\iint_{B} f(x, y) \, dx \, dy$ 的问题。

### 一般地，若连续函数 $f(x, y)$ 满足
$$ f(x, y) = g(x, y) + h(x, y) \iint_{B} f(u, v) \, du \, dv $$

又 $g(x, y), h(x, y)$ 为已知，则可令 $A = \iint_{B} f(u, v) \, du \, dv$，从而有
$$ \iint_{B} f(x, y) \, dx \, dy = \iint_{B} g(x, y) \, dx \, dy + \iint_{B} h(x, y) \, dx \, dy \cdot \iint_{B} f(u, v) \, du \, dv $$

即 $A = \iint_{B} g(x, y) \, dx \, dy + A \cdot \iint_{B} h(x, y) \, dx \, dy$，可解得 $A$。

### 【921】求
$$ \iint_{D} (\sqrt{x^2 + y^2} + y) \, d\sigma $$

其中 $D$ 是由圆 $x^2 + y^2 = 4$ 和 $(x + 1)^2 + y^2 = 1$ 所围成的平面区域（如图 921(1) 所示）。

### 解法一
$$ \iint_{D} (\sqrt{x^2 + y^2} + y) \, d\sigma $$

$$ = \iint_{D_{\text{大圆}}} (\sqrt{x^2 + y^2} + y) \, d\sigma - \iint_{D_{\text{小圆}}} (\sqrt{x^2 + y^2} + y) \, d\sigma $$

$$ = \iint_{D_{\text{大圆}}} (\sqrt{x^2 + y^2} + y) \, d\sigma - \iint_{D_{\text{小圆}}} (\sqrt{x^2 + y^2} + y) \, d\sigma $$

$$ = \iint_{D_{\text{大圆}}} \sqrt{x^2 + y^2} \, d\sigma + \iint_{D_{\text{大圆}}} y \, d\sigma - \iint_{D_{\text{小圆}}} \sqrt{x^2 + y^2} \, d\sigma - \iint_{D_{\text{小圆}}} y \, d\sigma $$

$$ = \int_{0}^{2\pi} d\theta \int_{0}^{2} r^2 \, dr + 0 = \frac{16}{3} \pi $$

$$ \iint_{D_{\text{小圆}}} (\sqrt{x^2 + y^2} + y) \, d\sigma = \iint_{D_{\text{小圆