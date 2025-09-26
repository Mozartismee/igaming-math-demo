# Constraints Component (Guardrails & Projections)

## Linear bands (invariants)
Let RTP/Hit bands be
\[
L_\mu \le \mu(p) = \sum_i r_i p_i \le U_\mu,\qquad
L_h \le h(p) = \sum_i w_i p_i \le U_h.
\]
Also \(p \in \Delta^k\) (simplex), and any legal caps are encoded by \(r\).

## Feasibility
A banded feasible set
\[
\mathcal{C}=\Big\{p\in\Delta^k \mid L_\mu \le \sum_i r_i p_i \le U_\mu, \; L_h \le \sum_i w_i p_i \le U_h\Big\}
\]
is nonempty if the bands intersect the convex hull of \(\{(r_i, w_i)\}\) under convex combinations. Practical check: ensure \( [L_\mu, U_\mu] \) intersects \([\min_i r_i, \max_i r_i]\) and \( [L_h, U_h] \subset [0,1]\), then verify via LP.

## KL/Bregman projection
Given \(q \in \Delta^k\), project to \(\mathcal{C}\) by
\[
\min_{x \in \mathcal{C}} D_{\mathrm{KL}}(x\|q).
\]
The KKT system leads to
\[
x_i \propto q_i \exp(-\lambda_0 - \lambda_\mu r_i - \lambda_h w_i).
\]
Solve for \(\lambda\) to satisfy the bands (with clamping if only one side is violated).

## Priority
If both bands cannot be met simultaneously within \(\delta\)-small change, prioritize **hard legal bounds** first (e.g., RTP lower bound), then pick the nearest feasible hit-rate.

## Inputs / Outputs / Tests
- **Inputs:** \(r, w\), bands \([L_\mu,U_\mu],[L_h,U_h]\), current \(q\).
- **Outputs:** projected \(x\), multipliers \(\lambda\).
- **Tests:** feasibility flag; post-projection \(x \in \mathcal{C}\); minimality \(D_{\mathrm{KL}}(x\|q)\) decreased.
