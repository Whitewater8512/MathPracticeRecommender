$$
2n(x^2 + y^2) = 2(x^2 + y^2), \text{因此} n = 1
$$

$$
du = \frac{(x - y)dx + (x + y)dy}{x^2 + y^2} = \frac{x dx + y dy - y dx + x dy}{x^2 + y^2}
$$

$$
= \frac{d\left(\frac{x^2 + y^2}{2}\right)}{x^2 + y^2} + x^2 d\left(\frac{y}{x}\right) = \frac{1}{2} \frac{d(x^2 + y^2)}{x^2 + y^2} + \frac{d\left(\frac{y}{x}\right)}{1 + \left(\frac{y}{x}\right)^2}
$$

$$
u(x, y) = \frac{1}{2} \ln(x^2 + y^2) + \arctan \frac{y}{x} + C
$$

$$
P = \frac{x + ay}{(x + y)^2}, \quad Q = \frac{y}{(x + y)^2}
$$

$$
\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x} \text{得} a = 2
$$

$$
\iint_{\Sigma} f(x, y, z) dS = \lim_{\lambda \to 0} \sum_{i=1}^{n} f(\xi_i, \eta_i, \zeta_i) \Delta S_i
$$