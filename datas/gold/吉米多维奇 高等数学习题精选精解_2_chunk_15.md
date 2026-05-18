## [421] 求 \(\int \frac{1}{\arctan e^x} dx\)

解：
\[
\int \frac{1}{\arctan e^x} dx = -\frac{1}{2} \int \arctan e^x \, d(e^{-2x}) = -\frac{1}{2} \left[ e^{-2x} \arctan e^x - \int \frac{de^x}{e^{2x}(1 + e^{2x})} \right]
\]
\[
= -\frac{1}{2} \left( e^{-2x} \arctan e^x + e^{-x} + \arctan e^x \right) + C.
\]

点评 本题也可设 \(e^x = t\)，利用换元法求解。

## [422] 求 \(\int e^{2x} (\tan x + 1)^2 dx\)

解：
\[
\int e^{2x} (\tan x + 1)^2 dx = \int e^{2x} \sec^2 x dx + 2 \int e^{2x} \tan x dx = \int e^{2x} d(\tan x) + 2 \int e^{2x} \tan x dx
\]
\[
= e^{2x} \tan x - 2 \int e^{2x} \tan x dx + 2 \int e^{2x} \tan x dx = e^{2x} \tan x + C.
\]

## [423] 求 \(\int \frac{\ln \sin x}{\sin^2 x} dx\)