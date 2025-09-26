# Optimizer Component (KL-Bounded Mirror Descent)

## Objective (example)
We increase variance while keeping RTP/Hit near targets via a weighted objective
\[
\mathcal{L}(p) \;=\; \lambda_\mu\big(\mu(p)-\mu^\star\big)^2 + \lambda_h\big(h(p)-h^\star\big)^2 + \lambda_v\big(\mathrm{Var}(p)-v^\star\big)^2.
\]
Guardrails are still enforced explicitly (projection), so \(\lambda_\mu,\lambda_h\) emphasize *preference* around the targets.

## Mirror map and update
Use the entropic mirror map (negative entropy): \( \psi(p) = \sum_i p_i \log p_i \). The mirror-descent update with step size \(\eta>0\) is
\[
p_i^{+} \;\propto\; p_i \exp\big(-\eta\, g_i\big), \qquad \text{where } g_i = \frac{\partial \mathcal{L}}{\partial p_i}.
\]
Then renormalize to ensure \(\sum_i p_i^{+} = 1\).

## Trust-region (KL bound)
Require the forward KL to be small at each step:
\[
D_{\mathrm{KL}}\!\big(p^{+}\,\|\,p\big) \;=\; \sum_i p_i^{+}\,\log\frac{p_i^{+}}{p_i} \;\le\; \delta.
\]
This yields **small, auditable steps** that preserve player feel and reduce risk.

## Projection to guardrails
If \(p^{+}\) violates bands, project back by solving the Bregman projection:
\[
\min_{x \in \Delta^k} \; D_{\mathrm{KL}}(x \,\|\, p^{+}) \quad \text{s.t.}\quad
L_\mu \le \sum_i r_i x_i \le U_\mu,\;\;
L_h \le \sum_i w_i x_i \le U_h.
\]
KKT conditions imply an exponential-family form
\[
x_i \;\propto\; p_i^{+}\; \exp\big(-\lambda_0 - \lambda_\mu r_i - \lambda_h w_i\big),
\]
with multipliers \(\lambda\) chosen to meet the constraints (solve 2–3 scalar equations).

## Stopping criteria
- KL step \( \le \varepsilon\),
- no appreciable change in \(\mathrm{Var}(p)\) over \(M\) iterations,
- guardrails satisfied for the last \(M\) steps.

## Inputs / Outputs / Tests
- **Inputs:** \(r\), \(p^{(0)}\), \(\mu^\star,h^\star,v^\star\), \(\delta\), \(\eta\).
- **Outputs:** trajectory \(\{p^{(t)}\}\), per-step KL and KPI deltas.
- **Tests:** monotone decrease of \(\mathcal{L}\) (for fixed projection), KL cap respected; post-projection guardrails met.
