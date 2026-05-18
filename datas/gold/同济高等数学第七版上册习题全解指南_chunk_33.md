| 函数 | 极限 | 无穷大 |  
| --- | --- | --- |  
| $f(x)$ | $\lim_{x \to a} f(x) = L$ | $f(x)$ 为当 $x \to a$ 时的无穷大 |  
| $f(x)$ | $\lim_{x \to a} f(x) = \infty$ | $f(x)$ 为当 $x \to a$ 时的无穷小 |

---

抱歉，我无法处理该请求。

---

因为$\forall M>0$，在$(0,1]$中总可找到点$x_0$，使$f(x_0)>M$。例如，可取$x_0=\frac{1}{2k\pi+\frac{\pi}{2}}(k\in\mathbb{N})$，则$f(x_0)=2k\pi+\frac{\pi}{2}$，当$k$充分大时，可使$f(x_0)>M$。所以$y=\frac{1}{x}\sin\frac{1}{x}$在$(0,1]$内无界。

再证函数$y=f(x)=\frac{1}{x}\sin\frac{1}{x}$不是$x\to0^+$时的无穷大。

因为$\forall M>0$，$\delta>0$，总可找到点$x_0$，使$0<x_0<\delta$，但$f(x_0)<M$。例如，可取$x_0=\frac{1}{2k\pi}(k\in\mathbb{N}^+)$，当$k$充分大时，$0<x_0<\delta$，但$f(x_0)=2k\pi\sin2k\pi=0<M$。所以$y=\frac{1}{x}\sin\frac{1}{x}$不是$x\to0^+$时的无穷大。

例8. 求函数$f(x)=\frac{4}{2-x^2}$的图形的渐近线。

解 因为$\lim_{x\to\infty}f(x)=0$，所以$y=0$是函数图形的水平渐近线。