# Paytable Component

## Purpose
Define the outcome multipliers (payout vector) and their probabilities as objects on the probability simplex, which forms the **state** optimized by the method.

## Objects and Domain
- **Payout vector:** \( r \in \mathbb{R}^{k+1}_{\ge 0} \), e.g. \(r = (0, 0.5, 1, 2, 5, 10, 25, 50)\).
- **Probability vector:** \( p \in \Delta^k \), where the (k-simplex)
  \[
    \Delta^k := \Big\{\, p \in \mathbb{R}^{k+1}_{\ge 0} \;\Big|\; \sum_{i=0}^{k} p_i = 1 \Big\}.
  \]
- **Win-mask:** \( w_i := \mathbf{1}[r_i > 0] \), so hit-rate \(= \sum_i w_i p_i\).

## Invariants (Guardrails)
Let target bands be \( \text{RTP} \in [L_\mu, U_\mu] \) and \( \text{Hit} \in [L_h, U_h] \). Define
\[
  \mu(p) := \sum_{i} r_i p_i, \qquad h(p) := \sum_{i} w_i p_i.
\]
Guardrails require \( \mu(p) \in [L_\mu, U_\mu] \) and \( h(p) \in [L_h, U_h] \). The hard cap on single-spin payout is encoded by the support of \(r\).

## Inputs / Outputs
- **Inputs:** payout vector \(r\), initial \(p^{(0)} \in \Delta^k\), guardrail bands, and caps.
- **Outputs:** updated \(p^{(t)} \in \Delta^k\) staying inside guardrails (or projected back).

## Tests
- `sum(p) == 1` and `all(p_i >= 0)`
- `mu(p) in [L_mu, U_mu]` and `h(p) in [L_h, U_h]` (post-projection)
- Non-regression on index order: \(r\) and \(p\) must be aligned by index.
