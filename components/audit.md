# Audit Component (Excel / One-Pager / Repro)

## Deliverables per change
1. **Excel mirror**: traceable formulas only (e.g., `SUMPRODUCT`, element‑wise squares).  
2. **One‑pager**: assumptions, baseline/target/final KPIs, CI table, two plots (objective; KPI trajectories), bullet recommendations.  
3. **Notebook checkpoint**: seeded, re-runnable; emits CSV of per-step KL and KPI deltas.

## Excel specs
Given columns `Payout (x)` and `Prob`:
\[
\texttt{RTP} = \mathrm{SUMPRODUCT}(\texttt{Prob}, \texttt{Payout}), \quad
\texttt{Var} = \mathrm{SUMPRODUCT}(\texttt{Prob}, \texttt{Payout}^2) - \texttt{RTP}^2, \quad
\texttt{Hit} = 1 - \texttt{Prob}_{\text{miss}}.
\]
Name ranges to prevent misalignment; lock the payout cap cells.

## Reproducibility
- Fix random seed; log versions of Python/Excel templates.
- Store per-step artifacts (KL, KPIs) and configs (targets, tolerances) alongside outputs.
- One-pager numbers must match Excel and notebook to the last printed precision.

## Inputs / Outputs / Tests
- **Inputs:** current \(p,r\), targets, tolerances.
- **Outputs:** XLSX, PDF/MD one-pager, notebook output.
- **Tests:** cross-check equality (Excel vs analytic vs simulation); file completeness checklist.
