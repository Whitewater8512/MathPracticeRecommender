解：
利用分部积分法，注意到 $d(\arctan \sqrt{x}) = \frac{1}{1 + x} \, d\sqrt{x}$，
$$
\int \arctan \sqrt{x} \, dx = x \cdot \arctan \sqrt{x} - \int x \, d(\arctan \sqrt{x}) = x \cdot \arctan \sqrt{x} - \int \frac{x}{1 + x} \, d(\sqrt{x})
$$
$$
= x \cdot \arctan \sqrt{x} - \sqrt{x} + \arctan \sqrt{x} + C = (x + 1) \cdot \arctan \sqrt{x} - \sqrt{x} + C.
$$
故应填 $(x + 1) \cdot \arctan \sqrt{x} - \sqrt{x} + C.$

#### [420] 求 $\int (\arcsin x)^2 \, dx$

解：
$$
\int (\arcsin x)^2 \, dx = x (\arcsin x)^2 - \int \frac{2x \arcsin x}{\sqrt{1 - x^2}} \, dx
$$
$$
= x (\arcsin x)^2 + \int \frac{\arcsin x}{\sqrt{1 - x^2}} \, d(1 - x^2)
$$
$$
= x (\arcsin x)^2 + 2 \sqrt{1 - x^2} \arcsin x - \int 2 \, dx
$$
$$
= x (\arcsin x)^2 + 2 \sqrt{1 - x^2} \arcsin x - 2x + C.
$$

---

```markdown
# 第四章 不定积分

## §3. 分部积分法