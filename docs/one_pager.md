# One-Pager — toy-slot-on-the-simplex

**Goal.** Increase volatility (Variance ↑) while staying within guardrails: RTP ≈ 95% (±0.5%) and Hit-rate ≈ 30–34%.

**Method.** Treat the paytable probabilities as a point on the probability simplex; navigate with **KL-bounded steps** (mirror descent / natural-gradient flavor), and **project back to guardrails** (KL/Bregman projection onto linear RTP/Hit bands) when needed. Each step is auditable.

## Baseline vs Target vs Result

| Metric    | Baseline  | Target (band)     | Final (Analytic) | Final (MC) | Δ to Target (Analytic) | Δ to Target (MC) |
|:---------:|:---------:|:------------------:|:----------------:|:----------:|:----------------------:|:----------------:|
| RTP       | 0.947200  | 0.9500 ± 0.0050   | 0.949800         | 0.949812   | −0.000200              | −0.000188        |
| Hit-rate  | 0.320000  | 0.3200 ± 0.0200   | 0.321000         | 0.321013   | +0.001000              | +0.001013        |
| Variance  | 14.043612 | maximize in-band  | 16.852335        | 16.848900  | +2.808723              | +2.805288        |

**MC agreement.** 95% CI (config-dependent) keeps Analytic and MC within tolerance.

## Guardrails

- RTP ∈ [0.945, 0.955]
- Hit-rate ∈ [0.30, 0.34]
- Single-spin payout cap fixed at 50×

**Trust region.** `max_kl_per_step = 5e-4` (configurable).

## KPI navigation (figures)

See `figures/objective_convergence.png` and `figures/metrics_over_iterations.png` for objective and metric trajectories over iterations (KL-bounded steps with guardrail projection).

## Sensitivity (interpretation)

- Shifting probability mass from mid-tier payouts (1×/2×) toward high-tier payouts (10×/25×), while keeping RTP/Hit in-band, typically increases variance.
- Micro-swaps between “miss” and the smallest win bucket can fine-tune the hit-rate.

## Audit-ready artifacts

- **Excel mirror:** `excel/paytable_audit.xlsx` (formulas; step-by-step trace)
- **Reproducible notebook:** `notebooks/ig_toy_slot_en.ipynb`

> **PoC only.** Production integrates real compliance limits, internal spreadsheet templates, and staged rollout (shadow → canary → full).
