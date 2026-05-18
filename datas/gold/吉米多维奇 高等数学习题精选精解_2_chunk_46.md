原式 = \(\int_{\frac{3}{2}}^{1} \frac{dx}{\sqrt{x - x^2}} + \int_{1}^{\frac{3}{2}} \frac{dx}{\sqrt{x^2 - x}}.\)

$$\int_{\frac{3}{2}}^{1} \frac{dx}{\sqrt{x - x^2}} = \lim_{\epsilon \to 0^{+}} \int_{\frac{3}{2}}^{1} \frac{dx}{\sqrt{4 - (x - \frac{1}{2})^2}} = \lim_{\epsilon \to 0^{+}} \arcsin(2x - 1) \bigg|_{\frac{3}{2}}^{\epsilon} = \frac{\pi}{2}.$$

$$\int_{1}^{\frac{3}{2}} \frac{dx}{\sqrt{x^2 - x}} = \lim_{\epsilon_2 \to +\infty} \int_{1}^{\epsilon_2} \frac{dx}{\sqrt{(x - \frac{1}{2})^2 - \frac{1}{4}}} = \lim_{\epsilon_2 \to +\infty} \ln \left[ (x - \frac{1}{2}) + \sqrt{(x - \frac{1}{2})^2 - \frac{1}{4}} \right] \bigg|_{1}^{\epsilon_2} = \ln(2 + \sqrt{3}).$$

因此 \(\int_{\frac{3}{2}}^{\frac{3}{2}} \frac{dx}{\sqrt{|x - x^2|}} = \frac{\pi}{2} + \ln(2 + \sqrt{3}).\)

### 点评