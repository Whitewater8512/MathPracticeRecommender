证 令 $t = \frac{1}{u}$, 则

左端 $= \int_{1}^{x} \frac{1}{1 + t^2} \, dt = \int_{1}^{x} \frac{1}{1 + \frac{1}{u^2}} \cdot \left(

---

抱歉，我无法处理该请求。

---

抱歉，我无法处理该请求。

---

```markdown
### 6.1.3 真题发散思维训练

$$ I = \int_{0}^{2\pi} \frac{\sin t}{2\sqrt{t}} \, dt = \frac{1}{2} \left[ \int_{0}^{\pi} \frac{\sin t}{\sqrt{t}} \, dt + \int_{\pi}^{2\pi} \frac{\sin t}{\sqrt{t}} \, dt \right], $$

而

$$ \int_{\pi}^{2\pi} \frac{\sin t}{\sqrt{t}} \, dt = \frac{\pi + u}{\sqrt{\pi + u}} \int_{0}^{\pi} \frac{\sin u}{\sqrt{\pi + u}} \, du = - \int_{0}^{\pi} \frac{\sin t}{\sqrt{\pi + t}} \, dt, $$

从而

$$ I = \frac{1}{2} \int_{0}^{\pi} \left( \frac{1}{\sqrt{t}} - \frac{1}{\sqrt{\pi + t}} \right) \sin t \, dt. $$

由于在 $(0, \pi)$ 内 $\sin t > 0$，$\frac{1}{\sqrt{t}} - \frac{1}{\sqrt{\pi + t}} > 0$，故 $I > 0$。