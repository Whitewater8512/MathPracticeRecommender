## 基本题型

### 使用定积分的换元法计算定积分

**例 [494]**  
设 \( f(x) = \begin{cases} 
x e^x, & -\frac{1}{2} \leq x < \frac{1}{2}; \\
-1, & x \geq \frac{1}{2}.
\end{cases} \)  
则 \(\int_{-\frac{1}{2}}^{\frac{1}{2}} f(x-1) \, dx = \underline{\hspace{2cm}}.\)

**解**  
\[
\int_{-\frac{1}{2}}^{\frac{1}{2}} f(x-1) \, dx = \int_{-\frac{1}{2}}^{\frac{1}{2}} f(t) \, dt = \int_{-\frac{1}{2}}^{\frac{1}{2}} t e^t \, dt + \int_{\frac{1}{2}}^{\frac{1}{2}} (-1) \, dt = -\frac{1}{2}.
\]

故应填 \(-\frac{1}{2}.\)

**例 [495]**  
设 \(\int_1^2 f(t) \, dt = \frac{2^4}{2}\)，则 \(\int_1^{\sqrt{2}} \frac{1}{\sqrt{x}} f(\sqrt{x}) \, dx = \underline{\hspace{2cm}}.\)

(A) 2  
(B) 7  
(C) 12  
(D)

---

```markdown
# 考研数学试题解析