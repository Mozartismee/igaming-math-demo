# Methodology: KL-Bounded Navigation on a Statistical Manifold

## What problem are we solving?
Design slot math that **feels more exciting** (higher volatility) while staying within **guardrails**:
- RTP ≈ 95% (±0.5%)
- Hit-rate ≈ 30–34%
- Compliance/Responsible Gaming caps (e.g., max single-spin payout)

Traditional tuning often relies on grid search + heuristics. It lacks a **common coordinate system**, so updates can fix one KPI and break another, documentation drifts, and audits are expensive.

## Core idea (unified coordinates + guardrails)
- Treat the paytable probabilities `p` as a point on the **probability simplex** (a statistical manifold).
- Define **invariants/guardrails** as constraints (RTP/Hit within bands; payout caps).
- Move in **small, KL-bounded steps** (mirror-descent / natural-gradient flavor) so each update has a measured **distance** and **direction**, and **project back** to the constraint set when needed.
- Every step is **audit-ready** (Excel mirror + one-pager + reproducible notebook).

## KPIs (bet = 1)
- RTP = Σ p_i · r_i
- Hit-rate = Σ_{r_i > 0} p_i
- Variance = Σ p_i · r_i² − RTP²  (proxy for volatility)

`r` is the payout vector (multipliers). `p` is the probability vector.

## Update rule (intuitive)
We adjust `p` to increase variance **without** leaving the RTP/Hit bands. Each step:
1) Take a small “mirror-descent” move on the simplex (KL-bounded).
2) If RTP/Hit drift out of band, **project back** (minimal correction).
3) Log the step’s KL distance and KPI deltas.

This is a **trust-region** view: many small, safe steps > few large risky jumps.

## Why this beats blind search
- **Coupling aware:** One coordinate system for multiple KPIs; you see trade-offs as geometry, not trial-and-error.
- **Safer:** KL trust-region keeps changes small and auditable; guardrails prevent breaking constraints.
- **Cheaper audits:** Formulas are analytic; Monte Carlo cross-checks are scripted; Excel mirrors are traceable.

## Extensibility
- **Bonus mixing:** Effective distribution p_eff = (1 − b)·p_base + b·p_bonus with a cost cap. Same guardrails apply.
- **Business mapping:** Changes in `p` map to LTV/retention proxies; once the manifold exists, downstream models read the same coordinates.

## Validation & governance
- **Analytic vs Monte Carlo** must agree (± CI).
- **Guardrails** satisfied at every step.
- **Artifacts per step:** one-pager (assumptions, metrics, CI), Excel mirror (SUMPRODUCT-level formulas), notebook (seeded, reproducible).

## Limitations / failure modes
- Non-stationary behavior → use rolling windows + canary rollout.
- Poor data quality → add consistency checks and missing-data handling.
- Unrealistic targets → multi-objective trade-offs need re-weighting or harder constraints.

*Bottom line:* We turn game math from **craft** into an **auditable production line** with a common geometric language.
