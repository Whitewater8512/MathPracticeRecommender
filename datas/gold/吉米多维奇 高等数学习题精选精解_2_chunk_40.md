### 某些不易求出原函数的定积分的计算

#### 【513】计算 $I = \int_{0}^{\frac{\pi}{2}} \frac{dx}{1 + (\tan x)^{\sqrt{3}}}.$

解

$$ I = \int_{0}^{\frac{\pi}{2}} \frac{dx}{1 + (\tan x)^{\sqrt{3}}} = \int_{0}^{\frac{\pi}{2}} \frac{(\cos x)^{\sqrt{3}}}{(\cos x)^{\sqrt{3}} + (\sin x)^{\sqrt{3}}} \, dx $$

$$ x = \frac{\pi}{2} - t, \quad \int_{0}^{\frac{\pi}{2}} \frac{(\sin t)^{\sqrt{3}}}{(\sin t)^{\sqrt{3}} + (\cos t)^{\sqrt{3}}} \, dt = \int_{0}^{\frac{\pi}{2}} \frac{(\sin x)^{\sqrt{3}}}{(\sin x)^{\sqrt{3}} + (\cos x)^{\sqrt{3}}} \, dx. $$

所以 $2I = \int_{0}^{\frac{\pi}{2}} dx = \frac{\pi}{2},$ 即 $I = \frac{\pi}{4}.$

#### 【514】计算 $I = \int_{2}^{4} \frac{\sqrt{\ln(9 - x)}}{\sqrt{\ln(9 - x)} + \sqrt{\ln(x + 3)}} \, dx.$

解