$$g[f(x)] = e^{f(x)} = \begin{cases} e, & |x| < 1, \\ 1, & |x| = 1, \\ e^{-1}, & |x| > 1. \end{cases}$$

$f[g(x)]$ 与 $g[f(x)]$ 的图形依次如图 1-2, 图 1-3 所示.

![](https://i.imgur.com/8j4k7Z8.png)

图 1-2

![](https://i.imgur.com/8j4k7Z8.png)

图 1-3

## 例 14

已知水渠的横断面为等腰梯形, 斜角 $\varphi = 40^\circ$ (图 1-4). 当过水断面 $ABCD$ 的面积为定值 $S_0$ 时, 求湿周 $L$ ($L = AB + BC + CD$) 与水深 $h$ 之间的函数关系式, 并指明其定义域.

![](https://i.imgur.com/8j4k7Z8.png)

图 1-4

解 $AB = CD = \frac{h}{\sin 40^\circ}$, 又

$$S_0 = \frac{1}{2} h \left[ BC + (BC + 2 \cot 40^\circ \cdot h) \right],$$

得

$$BC = \frac{S_0}{h} - \cot 40^\circ \cdot h,$$

所以

$$L = \frac{S_0}{h} + \frac{2 - \cos 40^\circ}{\sin 40^\circ} h,$$

而 $h > 0$ 且 $\frac{S_0}{h} - \cot 40^\circ \cdot h > 0$, 因此湿周函数的定义域为 $(0, \sqrt{S_0 \tan 40^\circ})$.

## 例 15