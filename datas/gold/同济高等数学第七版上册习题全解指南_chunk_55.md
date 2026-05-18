$$
f_1(x) = \begin{cases} 
\frac{x}{\tan x}, & x \neq k\pi, k\pi + \frac{\pi}{2}, \\
1, & x = 0
\end{cases} \quad (k \in \mathbb{Z}),
$$

则 \( f_1(x) \) 在 \( x = 0 \) 处连续。

对 \( x = k\pi (k = \pm 1, \pm 2, \ldots) \)，因为 \(\lim_{x \to k\pi} \frac{x}{\tan x} = \infty\)，所以 \( x = k\pi (k = \pm 1, \pm 2, \ldots) \) 为第二类间断点（无穷间断点）。

对 \( x = k\pi + \frac{\pi}{2} (k \in \mathbb{Z}) \)，因为 \(\lim_{x \to k\pi + \frac{\pi}{2}} \tan x = 0\)，而函数在 \( k\pi + \frac{\pi}{2} \) 处无定义，所以 \( x = k\pi + \frac{\pi}{2} (k \in \mathbb{Z}) \) 为第一类间断点（可去间断点），重新定义函数：

$$
f_2(x) = \begin{cases} 
\frac{x}{\tan x}, & x \neq k\pi, k\pi + \frac{\pi}{2}, \\
0, & x = k\pi + \frac{\pi}{2}
\end{cases} \quad (k \in \mathbb{Z}),
$$

则 \( f_2(x) \) 在 \( x = k\pi + \frac{\pi}{2} (k \in \mathbb{Z}) \) 处连续。

#### (3) 对 \( x = 0 \)