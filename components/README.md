# Components Overview


```
components/
├── README.md
├── paytable.md          # payout vector & probability vector; invariants
├── metrics.md           # RTP/Hit/Variance formulas & checks
├── optimizer.md         # KL-bounded (mirror-descent) step, step-size, stopping
├── constraints.md       # guardrails & projection strategies
├── simulator.md         # Monte Carlo spec & CI reporting
├── audit.md             # Excel mirror + one-pager artifacts
├── data_schema.md       # spins_log schema; aggregates; data quality checks
└── config.md            # targets, tolerances, seeds, file paths
```

This folder documents the **building blocks** of the demo so teams can swap or extend parts without breaking the pipeline.

- **paytable.md** — Defines the payout vector `r` (multipliers) and the probability vector `p`. Describes invariant bands (RTP/Hit) and any legal caps.
- **metrics.md** — Formal RTP/Hit/Variance definitions, analytic evaluation, and unit tests for metric consistency.
- **optimizer.md** — KL-bounded mirror-descent update rule, learning rate policy, trust-region thresholds, and stopping criteria.
- **constraints.md** — How guardrails are enforced (projection / Lagrange correction), priority when multiple constraints conflict.
- **simulator.md** — Monte Carlo procedure (sample size, seed, CI computation), reconciliation with analytic numbers.
- **audit.md** — What gets emitted each step: Excel mirror (traceable formulas), one-pager (assumptions, KPI deltas, CI), and notebook checkpoints.
- **data_schema.md** — `spins_log` fields, aggregations, and data quality checks (missingness, leakage, timestamp sanity).
- **config.md** — Targets, tolerances, seeds, run modes, and file paths (YAML suggested in production).

> Design principle: **stable interfaces**. Each component declares inputs/outputs so we can evolve internals without changing contracts.
