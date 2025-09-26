# Metrics Component

## Definitions (bet = 1)
Given \( r \in \mathbb{R}^{k+1}_{\ge 0} \) and \( p \in \Delta^k \):
\[
\mathrm{RTP}(p) := \mu(p) = \sum_{i=0}^k r_i p_i, \qquad
\mathrm{Hit}(p) := h(p) = \sum_{i=0}^k \mathbf{1}[r_i>0]\; p_i.
\]
The variance of returns (proxy for volatility) is
\[
\mathrm{Var}(p) := \sum_{i=0}^k r_i^2 p_i \;-\; \mu(p)^2.
\]

## Differentials (for optimization)
For an infinitesimal change \(\delta p\) subject to \(\sum_i \delta p_i = 0\):
\[
\frac{\partial \mu}{\partial p_i} = r_i, \qquad 
\frac{\partial h}{\partial p_i} = \mathbf{1}[r_i>0], \qquad
\frac{\partial \,\mathrm{Var}}{\partial p_i} = r_i^2 - 2\,\mu(p)\, r_i.
\]

## Sanity checks
- Bounds: \(0 \le \mathrm{RTP}(p) \le \max_i r_i\), \(0 \le \mathrm{Hit}(p) \le 1\).
- If mass is shifted from mid-tier to high-tier payouts while preserving \(\mu\), \(\mathrm{Var}\) typically increases.

## Tests
- Analytic vs Monte Carlo: for \(N\) i.i.d. draws \(X_j \in \{r_i\}\) with \(\mathbb{P}[X=r_i]=p_i\),
  \[
  \hat{\mu}_N = \frac1N \sum_{j=1}^N X_j \xrightarrow[]{a.s.} \mu(p), \quad
  \widehat{\mathrm{Var}}_N \xrightarrow[]{a.s.} \mathrm{Var}(p).
  \]
- Confidence intervals (normal approximation) for \(\mu\) and \(\mathrm{Hit}\) must contain analytic values with the declared \(\alpha\).
