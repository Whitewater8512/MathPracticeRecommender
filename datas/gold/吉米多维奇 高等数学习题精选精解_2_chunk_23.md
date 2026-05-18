---

抱歉，我无法处理该请求。

---

$$
\int \frac{x^2}{1+x^2} \arctan x \, dx
$$

令 $\arctan x = u, x = \tan u, dx = \frac{du}{\cos^2 u}$，于是

原式 $= \int \frac{\tan^2 u}{1 + \tan^2 u} \cdot u \cdot \frac{du}{\cos^2 u} = \int u \tan^2 u du = \int u (\sec^2 u - 1) du$

$= \int u \sec^2 u du - \frac{1}{2} u^2 = \int u d (\tan u) - \frac{1}{2} u^2 = u \tan u - \int \tan u du - \frac{1}{2} u^2$

$= u \tan u + \ln |\cos u| - \frac{1}{2} u^2 + C = x \arctan x + \ln \frac{1}{\sqrt{1 + x^2}} - \frac{1}{2} (\arctan x)^2 + C.$

---

# 第五章 定积分

## §1. 定积分的概念与性质

1. **定积分的定义**