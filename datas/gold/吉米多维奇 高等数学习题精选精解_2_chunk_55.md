## [747]
设 \( f(x, y) = \begin{cases} \frac{xy}{\sqrt{x^2 + y^2}}, & x^2 + y^2 \neq 0, \\ 0, & x^2 + y^2 = 0 \end{cases} \)，讨论 \( f(x, y) \) 在 \((0, 0)\) 处是否可微。

**解：** 在点 \((0, 0)\) 处有
\[ f'_x(0, 0) = \lim_{\Delta x \to 0} \frac{f(0 + \Delta x, 0) - f(0, 0)}{\Delta x} = \lim_{\Delta x \to 0} \frac{\sqrt{(\Delta x)^2 + 0^2}}{\Delta x} = 0, \]
```

---

```markdown
第八章 多元函数微分法及其应用

$ f_{x}^{\prime}(0,0) = \lim_{\Delta y \to 0} \frac{f(0,0+\Delta y) - f(0,0)}{\Delta y} = \lim_{\Delta y \to 0} \frac{0 \cdot \Delta y}{\sqrt{0^2 + (\Delta y)^2}} = 0, $