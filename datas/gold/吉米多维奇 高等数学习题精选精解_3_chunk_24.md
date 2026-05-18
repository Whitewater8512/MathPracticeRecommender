而 \( \cos x \cdot \sin y \) 对 \( y \) 是奇函数，对 \( x \) 是偶函数，故有

\[ \iint_{D_3 + D_4} \cos x \cdot \sin y \, dx \, dy = 0 \quad \text{和} \quad \iint_{D_1 + D_2} \cos x \cdot \sin y \, dx \, dy = 2 \iint_{D_1} \cos x \cdot \sin y \, dx \, dy, \]

故 \( I_2 = 2 \iint_{D_1} \cos x \cdot \sin y \, dx \, dy \).

从而

\[ \iint_{D} (xy + \cos x \cdot \sin y) \, dx \, dy = 2 \iint_{D_1} \cos x \cdot \sin y \, dx \, dy \]

故应选 (A).

点评 在利用积分区域的对称性进行计算时，要同时考虑被积函数的奇偶性，通常有：

(1) 设 \( D \) 对称于 \( y \) 轴，\( D_1 \) 是 \( D \) 的右半部分，

若 \( f(-x, y) = -f(x, y) \)，则 \(\iint_{D} f(x, y) \, dx = 0\);

若 \( f(-x, y) = f(x, y) \)，则 \(\iint_{D} f(x, y) \, dx = 2 \iint_{D_1} f(x, y) \, dx\).

(2) 设 \( D \) 对称于 \( x \) 轴，\( D_1 \) 是 \( D \) 的上半部分，

若 \( f(x, -y) = -f(x, y) \)，则 \(\iint_{D} f(x, y) \, dx = 0\);