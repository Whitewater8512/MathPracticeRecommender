抱歉，我无法处理该请求。

---

$$\pi+\int_{0}^{\frac{\pi}{2}}2\sin^{2}\theta d\theta=\frac{3\pi}{2}.$$

故应填$\frac{3\pi}{2}$.

点评 用化为参数的定积分的方法计算对坐标的曲线积分时，首先要写出积分路径的参数表示式，特别要注意的是参数的起点对应曲线的起点，写成定积分表示式时积分的下限对应参数的起点，上限对应参数的终点，下限不一定小于上限，因为对坐标的曲线积分与方向有关.如果曲线方程是用直角坐标或极坐标表示时，可先化成参数方程然后再计算.

【947】计算曲线积分$I=\int_{L}(y+2xy)dx+(x^{2}+2x+y^{2})dy$,其中$L$是由点$A(4,0)$到点$O(0,0)$的上半圆周$y=\sqrt{4x-x^{2}}$.

解 曲线$L$的参数方程是$\begin{cases}x=2+2\cos t,\\y=2\sin t,\end{cases}t:0\rightarrow\pi,$

故

$$I=\int_{0}^{\pi}\left\{\left[2\sin t+2(2+2\cos t)\cdot2\sin t\right](-2\sin t)\right.$$

$$+\left[4(1+\cos t)^{2}+4(1+\cos t)+4\sin^{2}t]\cdot2\cos t\right\}dt$$

$$=\int_{0}^{\pi}\left(-20\sin^{2}t-16\sin^{2}t\cos t+24\cos t+24\cos^{2}t\right)dt=2\pi.$$