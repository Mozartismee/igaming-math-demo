### Minimal atlas on the open simplex

Let
\[
\Delta_{+}^{n-1}=\{\,p\in\mathbb{R}^n \mid p_i>0,\ \sum_{i=1}^n p_i=1\,\}.
\]

- (Mixture chart)  \(\varphi_m: \Delta_{+}^{n-1}\to\mathbb{R}^{n-1}\),  
  \(\varphi_m(p) = (p_1,\dots,p_{n-1})\);  
  \(\varphi_m^{-1}(x)=\bigl(x_1,\dots,x_{n-1},\,1-\sum_{i=1}^{n-1}x_i\bigr)\).

- (Exponential chart)  \(\varphi_e: \Delta_{+}^{n-1}\to\mathbb{R}^{n-1}\),  
  \(\varphi_e(p) = (\log(p_1/p_n),\dots,\log(p_{n-1}/p_n))\);  
  inverse (softmax with \( \theta_n\equiv 0\)):
  \[
  p_i=\frac{e^{\theta_i}}{1+\sum_{j=1}^{n-1}e^{\theta_j}},\quad
  p_n=\frac{1}{1+\sum_{j=1}^{n-1}e^{\theta_j}}.
  \]

- Fisher information gives the Riemannian metric; KL 的二階展開在內點近似該度量。  
  KL-bounded updates ≈ 在此度量下的短步（自然梯度風味）。
