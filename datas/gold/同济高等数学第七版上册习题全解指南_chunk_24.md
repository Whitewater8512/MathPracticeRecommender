## 4. 求 \( f(x) = \frac{x}{x} \), \( \varphi(x) = \frac{|x|}{x} \) 当 \( x \to 0 \) 时的左、右极限，并说明它们在 \( x \to 0 \) 时的极限是否存在.

解
$$
\begin{aligned}
&\lim_{x \to 0^-} f(x) = \lim_{x \to 0^-} \frac{x}{x} = \lim_{x \to 0^-} 1 = 1, \\
&\lim_{x \to 0^+} f(x) = \lim_{x \to 0^+} \frac{x}{x} = \lim_{x \to 0^+} 1 = 1, \\
&\text{因为} \lim_{x \to 0^-} f(x) = 1 = \lim_{x \to 0^+} f(x), \text{所以} \lim_{x \to 0} f(x) = 1.
\end{aligned}
$$

$$
\begin{aligned}
&\lim_{x \to 0^-} \varphi(x) = \lim_{x \to 0^-} \frac{|x|}{x} = \lim_{x \to 0^-} \frac{-x}{x} = -1, \\
&\lim_{x \to 0^+} \varphi(x) = \lim_{x \to 0^+} \frac{|x|}{x} = \lim_{x \to 0^+} \frac{x}{x} = 1, \\
&\text{因为} \lim_{x \to 0^-} \varphi(x) \neq \lim_{x \to 0^+} \varphi(x), \text{所以} \lim_{x \to 0} \varphi(x) \text{不存在}.
\end{aligned}
$$