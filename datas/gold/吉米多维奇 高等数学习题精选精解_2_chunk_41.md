$$ I = \int_{2}^{4} \frac{\sqrt{\ln(9 - x)}}{\sqrt{\ln(9 - x)} + \sqrt{\ln(x + 3)}} \, dx = \int_{2}^{4} \frac{9 - x = t + 3}{\sqrt{\ln(t + 3)} + \sqrt{\ln(9 - t)}} (-dt) $$

$$ = \int_{2}^{4} \frac{\sqrt{\ln(x + 3)}}{\sqrt{\ln(9 - x)} + \sqrt{\ln(x + 3)}} \, dx. $$

所以 $2I = \int_{2}^{4} dx = 2,$ 即 $I = 1.$

#### 【515】计算 $I = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \frac{e^x \sin^4 x}{1 + e^x} \, dx.$

解

$$ I = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \frac{e^x \sin^4 x}{1 + e^x} \, dx = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \frac{e^{-t} \sin^4 (-t)}{1 + e^{-t}} \, dt = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \frac{\sin^4 t}{1 + e^t} \, dt = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}

---

```markdown
# 第五章 定积分

## §3. 定积分的换元法和分部积分法

### 【517】
计算 $\int_{1}^{2} x(\ln x)^2 dx$.

解 用分部积分法计算：
$$
\int_{1}^{2} x(\ln x)^2 dx = \left[ \frac{x^2}{2} (\ln x)^2 \right]_{1}^{2} - \int_{1}^{2} \frac{x^2}{2} \cdot \frac{2\ln x}{x} dx
$$
$$
= 2(\ln 2)^2 - \int_{1}^{2} \ln x dx = 2\ln^2 2 - \left[ \frac{x^2}{2} \ln x \right]_{1}^{2} + \frac{1}{2} \int_{1}^{2} x dx
$$
$$
= 2\ln^2 2 - 2\ln 2 + \frac{x^2}{4} \bigg|_{1}^{2} = 2\ln^2 2 - 2\ln 2 + \frac{3}{4}.