注 在作等价无穷小的代换求极限时，可以对分子或分母中的一个或若干个因子作代换，但不能对分子或分母中的某个加项作代换。例如，本题中若将分子中的 \(\tan x\)、\(\sin x\) 均换成 \(x\)，那么分子成为 0，得出极限为 0，这就导致错误的结果。

(4) \(\lim_{x \to 0} \frac{\sin x - \tan x}{(\sqrt{1 + x^2} - 1)(\sqrt{1 + \sin x} - 1)} = \lim_{x \to 0} \frac{\sin x(1 - \sec x)}{1 \cdot x^2 \cdot \frac{1}{2} \sin x}\)

\(= \lim_{x \to 0} \frac{-1 - x^2}{6 - x^2} = -3.\)

## 6. 证明无穷小的等价关系具有下列性质：

(1) \(\alpha \sim \alpha\) (自反性)；

(2) 若 \(\alpha \sim \beta\)，则 \(\beta \sim \alpha\) (对称性)；

(3) 若 \(\alpha \sim \beta\)，\(\beta \sim \gamma\)，则 \(\alpha \sim \gamma\) (传递性).

证 (1) 因为 \(\lim_{x \to a} \frac{\alpha}{\alpha} = 1\)，所以 \(\alpha \sim \alpha\)；

(2) 因为 \(\alpha \sim \beta\)，即 \(\lim_{x \to a} \frac{\alpha}{\beta} = 1\)，所以 \(\lim_{x \to a} \frac{\beta}{\alpha} = 1\)，即 \(\beta \sim \alpha\)；