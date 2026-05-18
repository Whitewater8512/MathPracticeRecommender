---

抱歉，我无法处理该请求。

---

```markdown
$$ I = \pi e^{\pi} \int_{0}^{\pi} e^{-t} \sin t \, dt. $$

记 \( A = \int_{0}^{\pi} e^{-t} \sin t \, dt \),

则

$$ A = - \int_{0}^{\pi} \sin t \, de^{-t} = \left[ e^{-t} \sin t \right]_{0}^{\pi} - \int_{0}^{\pi} e^{-t} \cos t \, dt $$

$$ = - \int_{0}^{\pi} \cos t \, de^{-t} = \left[ e^{-t} \cos t \right]_{0}^{\pi} + \int_{0}^{\pi} e^{-t} \sin t \, dt = e^{-\pi} + 1 - A. $$

因此 \( A = \frac{1}{2} (1 + e^{-\pi}) \), \( I = \frac{\pi e^{\pi}}{2} (1 + e^{-\pi}) = \frac{\pi}{2} (1 + e^{\pi}). $$

【874】计算二重积分 \(\iint_{D} y \, dx \, dy\)，其中 \( D \) 是由直线 \( x = -2 \), \( y = 0 \), \( y = 2 \) 以及曲线 \( x = -\sqrt{2y - y^3} \) 所围成的平面区域.

解法一

区域 \( D \) 和 \( D_1 \) 如图 874 所示，有

$$ \iint_{D} y \, dx \, dy = \iint_{D+D_1} y \, dx \, dy - \iint_{D_1} y \, dx \, dy, $$

$$ \iint_{D+D_1} y \, dx \, dy = \int_{-2}^{0} dx \int_{0}^{2} y \, dy = 4. $$

在极坐标系下，有 \( D_1 = \{ (r, \theta) \mid \frac{\pi}{2} \leq \theta \leq \pi, 0 \leq r \leq 2\sin\theta \} \)，因此

$$ \iint_{D_1} y \, dx \, dy = \int_{\frac{\pi}{2}}^{\pi} d\theta \int_{0}^{2\sin\theta} r \sin\theta \cdot r \, dr = \frac{8}{3} \int_{\frac{\pi}{2}}^{\pi} \sin^4 \theta \, d\theta $$

$$ = \frac{8}{3} \times 4 \int_{\frac{\pi}{2}}^{\pi} \left[ 1 - 2\cos2\theta + \frac{1 + \cos4\theta}{2} \right] d\theta = \frac{\pi}{2} $$

于是

$$ \iint_{D} y \, dx \, dy = 4 - \frac{\pi}{2}. $$

解法二

如图 874 所示，\( D = \{ (x, y) \mid -2 \leq x \leq -\sqrt{2y - y^3}, 0 \leq y \leq 2 \} \).

$$ \iint_{D} y \, dx \, dy = \int_{0}^{2} y \, dy \int_{-2}^{-\sqrt{2y - y^3}} dx = 2 \int_{0}^{2} y \, dy - \int_{0}^{2} y \sqrt{2y - y^3} \, dy $$

$$ = 4 - \int_{0}^{2} y \sqrt{2y - y^3} \, dy. $$

令 \( y - 1 = \sin t \)，有 \( dy = \cos t \, dt \)，则

$$ \int_{0}^{2} y \sqrt{1 - (y - 1)^2} \, dy = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} (1 + \sin t) \cos^2 t \, dt = \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \cos^2 t \, dt + \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} \cos^