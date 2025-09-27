# Industry Value Note — igaming-math-demo (Day-2 Learning Demo)

**Scope.** This is a 2-day learning demo. It is **not** production. It shows a controllable way to tune a slot paytable under strict guardrails and to audit every change end-to-end.

## What problem this solves
- **Guardrails drift**: Small parameter tweaks can push RTP/Hit out of legal or internal limits.
- **Untraceable changes**: “Why did we change this number?” is hard to answer months later.
- **Iteration cost**: Pure trial-and-error or large MC sweeps are slow and compute-heavy.

## What this method does (non-math)
- Treat the **paytable** as a point on a probability simplex (the “parameter space”).
- Update in **small, KL-bounded steps** (trust-region). If a step hits limits, **project back** into the RTP / Hit bands.
- After convergence, run a **Monte Carlo check** to confirm analytic KPIs and attach a 95% CI.
- Everything is logged: per-step KPIs, cumulative KL distance, final summary, and an **Excel audit mirror**.

## Why it matters to the business
- **Risk control**: Every step is inside an explicit trust-region and guardrails; drift is mechanically prevented.
- **Auditability**: Each run produces `metrics_history.csv`, `summary.json`, and an Excel mirror. Decisions are explainable.
- **Efficiency**: Analytic KPIs make iterations fast; **MC is only used at the end** for a statistical safety check.
- **Transferability**: The shell (trust-region + projection + MC backstop) is reusable when objectives change.

## What we measured in a run (example)
*(Replace with your latest run numbers; do not hardcode. Pull from `runs/<timestamp>/summary.json`.)*
- **Target bands**: RTP in `[0.945, 0.955]`, Hit in `[0.30, 0.34]`.
- **Outcome**: Final distribution stays within bands; variance increased vs baseline.
- **MC validation**: Analytic RTP / Hit / Var within **95% CI** of a `N = 1e6` Monte Carlo check (seeded, reproducible).
- **Artifacts**: `runs/<ts>/metrics_history.csv`, `runs/<ts>/summary.json`, `runs/<ts>/paytable_audit.xlsx`.

## What this demo does **not** claim
- No reels/line-pays/bonus/jackpot mechanics yet (this is a **paytable layer** demo).
- No production deployment; no real player logs; no A/B evidence of behavioral lift (yet).
- Not a guarantee that “higher variance is always better.” It is a **controlled way** to explore that direction.

## Where this scales next (practical roadmap)
1. **Mechanics realism**: add reels/line-pays RTP approximator (DP or sampling) under the same shell.
2. **Multi-objective**: Pareto view (Variance↑, Tail-risk↓, RTP/Hit in-band) with decision guidance.
3. **Behavioral link**: plug a retention/ARPU proxy; if black-box, use sampling gradients but **keep** the KL shell.
4. **Release safety**: shadow → canary → auto-rollback hooks; auto-generated change log.

## How to read the outputs (quick)
- `metrics_history.csv`: per-step RTP/Hit/Var, per-step KL; expect small KL steps and in-band KPIs.
- `summary.json`: final analytic vs MC numbers with 95% CI; seed included for reproduction.
- `paytable_audit.xlsx`: Excel mirror of the math so non-engineers can audit calculations.

*Contact:* This is a learning prototype built in 2 days. Feedback on mechanics priorities and KPI objectives is welcome.
