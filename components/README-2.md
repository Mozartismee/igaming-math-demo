# Components Overview

This directory documents the **building blocks** of the demo so teams can swap or extend parts without breaking the pipeline.

- `paytable.md` — payout vector \(r\) (multipliers) and probability vector \(p\); domain set \(\Delta^k\); invariants.
- `metrics.md` — formal KPI definitions (RTP/Hit/Variance), analytic formulas, and test obligations.
- `optimizer.md` — KL-bounded mirror-descent update rule on the simplex; step size; stopping; trust region.
- `constraints.md` — guardrails as linear constraints; KL/Bregman projection; feasibility and priority.
- `simulator.md` — Monte Carlo estimators and confidence intervals; sample-size guidance.
- `audit.md` — Excel mirror, one-pager, and notebook reproducibility rules.
- `data_schema.md` — `spins_log` fields, aggregates, and data-quality checks.
- `config.md` — targets, tolerances, seeds, file paths; recommended YAML layout.

**Design principle:** stable interfaces. Each component states **Inputs / Outputs / Invariants / Tests** so internals can evolve without changing contracts.
