3. **常用公式**  
   设 \( f(x) \) 为连续函数：
   \[
   (1) \int_{-a}^a f(x) \, dx = \int_0^a \left[ f(x) + f(-x) \right] \, dx;
   \]
   \[
   (2) \int_{-a}^a f(x) \, dx = \begin{cases} 
   2 \int_0^a f(x) \, dx, & \text{若 } f(x) \text{ 是偶函数}; \\
   0, & \text{若 } f(x) \text{ 是奇函数}.
   \end{cases}
   \]
   \[
   (3) \int_0^{\frac{\pi}{2}} f(\sin x) \, dx = \int_0^{\frac{\pi}{2}} f(\cos x) \, dx;
   \]
   \[
   (4) \int_0^{\pi} x f(\sin x) \, dx = \frac{\pi}{2} \int_0^{\pi} f(\sin x) \, dx;
   \]
   \[
   (5) f(x+L) = f(x), \quad (L > 0), \text{ 则 } \int_0^L f(x) \, dx = \frac{1}{2} \int_0^{2L} f(x) \, dx = \int_a^{a+L} f(x) \, dx;
   \]
   \[
   (6) \int_0^{\frac{\pi}{2}} (\sin x)^n \, dx = \int_0^{\frac{\pi}{2}} (\cos x)^n \, dx = \begin{cases} 
   \frac{(n-1)!! \cdot \pi}{n!!}, & \text{当 } n \text{ 为偶数时}; \\
   \frac{(n-1)!!}{n!!}, & \text{当 } n \text{ 为奇数时}.
   \end{cases}
   \]
   此公式在定积分计算中十分有用，应记住。当 \( n \) 为偶数时，\( n!! \) 表示所有偶数（不大于 \( n \)）连乘积；当 \( n \) 为奇数时，\( n!! \) 表示所有奇数（不大于 \( n \)）连乘积。