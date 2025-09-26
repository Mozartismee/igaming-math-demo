# Simulator Component (Monte Carlo & Confidence)

## Setup
Draw \(X \in \{r_i\}\) with \(\mathbb{P}[X=r_i]=p_i\). For \(N\) i.i.d. spins \(X_1,\dots,X_N\):
\[
\hat{\mu}_N = \frac1N\sum_{j=1}^N X_j, \quad
\widehat{\mathrm{Var}}_N = \frac1N\sum_{j=1}^N X_j^2 - \hat{\mu}_N^2, \quad
\widehat{h}_N = \frac1N \sum_{j=1}^N \mathbf{1}[X_j>0].
\]

## Confidence intervals (normal approx.)
By CLT, approximately
\[
\hat{\mu}_N \sim \mathcal{N}\!\big(\mu,\, \sigma_\mu^2/N\big), \quad \sigma_\mu^2=\mathrm{Var}(X).
\]
For hit-rate \(h\) (Bernoulli with \(p=h\)),
\[
\widehat{h}_N \sim \mathcal{N}\!\big(h,\, h(1-h)/N\big).
\]
A two-sided \(1-\alpha\) CI:
\[
\hat{\theta}_N \pm z_{1-\alpha/2}\,\sqrt{\widehat{\mathrm{Var}}(\hat{\theta}_N)}.
\]

## Sample size guidance
To achieve margin \(\varepsilon\) for \(\mu\):
\[
N \gtrsim z_{1-\alpha/2}^2\, \sigma_\mu^2 / \varepsilon^2,\quad \sigma_\mu^2 \approx \widehat{\mathrm{Var}}_N.
\]
Use pilot runs to estimate \(\sigma_\mu^2\).

## Goodness-of-fit
Optionally test simulated category frequencies against \(p\) via \(\chi^2\) or exact multinomial tests.

## Inputs / Outputs / Tests
- **Inputs:** \(r,p,N,\) seed.
- **Outputs:** estimates \(\hat{\mu}_N,\widehat{\mathrm{Var}}_N,\widehat{h}_N\) and CIs; raw draws (optional).
- **Tests:** analytic values fall within CIs at declared level; reproducibility with fixed seed.
