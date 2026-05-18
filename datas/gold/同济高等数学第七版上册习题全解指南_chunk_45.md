### 逐步推理
1. **题目 (4)**：
   \[
   \lim_{x \to \infty} \left(1 - \frac{1}{x}\right)^{kx} = \lim_{x \to \infty} \left[1 + \frac{1}{(-x)}\right]^{(-x)(-k)} = e^{-k}
   \]
   这里使用了指数函数的极限性质。

2. **题目 (3)**：
   根据夹逼准则，证明极限存在。
   - 条件 (1) 和 (2) 给出 \(g(x) \leq f(x) \leq h(x)\) 且 \(\lim_{x \to a} g(x) = \lim_{x \to a} h(x) = A\)。
   - 对于任意 \(\epsilon > 0\)，存在 \(\delta_1 > 0\) 和 \(\delta_2 > 0\)，使得 \(|g(x) - A| < \epsilon\) 和 \(|h(x) - A| < \epsilon\)。
   - 取 \(\delta = \min\{\delta_1, \delta_2\}\)，则当 \(0 < |x - a| < \delta\) 时，有 \(A - \epsilon < g(x) \leq f(x) \leq h(x) < A + \epsilon\)。
   - 因此，\(|f(x) - A| < \epsilon\)，即 \(\lim_{x \to a} f(x) = A\)。

3. **题目 (4)**：
   利用夹逼准则证明极限存在。
   - 对于 \(x \to \infty\) 的情形，利用极限的定义和夹逼准则，可以类似地证明相应的准则。

### 最终答案
通过上述推理，可以证明题目中的极限存在，并得出相应的结果。
```

---