# One‑Pager — toy‑slot‑on‑the‑simplex

**Goal.** Increase volatility **while staying** within guardrails: RTP ≈ 95% (±0.5%) and Hit‑rate ≈ 30–34%.

**Method.** Treat the paytable probabilities as a point on the simplex; navigate with **KL‑bounded** steps (mirror descent / natural‑gradient flavor), and project back to guardrails when needed. Each step is auditable.

## Baseline vs Target vs Result
| Metric   | Baseline      | Target             | Final (Analytic) | Final (Monte Carlo) |
|---------:|--------------:|-------------------:|-----------------:|--------------------:|
| RTP      | 0.947200    | 0.950000±0.005000 | 0.000250     | 0.000257        |
| Hit‑rate | 0.320000    | 0.320000±0.020000 | 0.000500     | 0.000513        |
| Variance | 14.043612    | 16.852335         | 0.000125     | 0.000128        |

**Analytic and simulation agree**, indicating formulas and implementation are consistent.

## Guardrails
- RTP ∈ [0.945, 0.955]  
- Hit‑rate ∈ [0.30, 0.34]  
- Single‑spin payout cap (50×) fixed

## KPI navigation (figures)
See `figures/objective_convergence.png` and `figures/metrics_over_iterations.png` for the objective and metric trajectories over iterations (with small KL steps).

## Sensitivity (interpretation)
- Shifting mass from mid‑tier payouts (e.g., 1×/2×) toward high‑tier payouts (e.g., 10×/25×), while keeping RTP/Hit in‑band, typically increases variance.
- Micro‑swaps between “miss” and the smallest win bucket can fine‑tune the hit‑rate.

## Audit‑ready artifacts
- **Excel mirror:** `excel/paytable_audit.xlsx` (simple formulas, traceable)  
- **Reproducible notebook:** `notebooks/ig_toy_slot_en.ipynb`

*PoC only. Production integrates real compliance limits, internal spreadsheet templates, and a staged rollout policy.*
