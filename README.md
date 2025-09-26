# toy-slot-on-the-simplex — KL-bounded tuning under RTP/Hit guardrails

**Tagline.** Treat the slot paytable as a point on the probability simplex. Move in **small, KL-bounded steps** (mirror-descent / natural-gradient flavor) **inside RTP/Hit guardrails** to increase volatility. Every step is **audit-ready** (Excel mirror + one-pager + reproducible notebook).

## What this repo provides

- **Auditable tuning framework**: A unified coordinate system for RTP, Hit-rate, and volatility with explicit guardrails.
- **Reproducibility**: An executable notebook, seeded Monte Carlo checks, and an Excel mirror for non-engineers.
- **Executive-readiness**: A one-pager that summarizes assumptions, metrics, and results in plain English.

## How it works (at a glance)

We model the paytable probabilities \(p\) on the **probability simplex** and navigate with **small, KL-bounded updates**, projecting back to **RTP/Hit bands** when necessary. KPIs (RTP / Hit-rate / Variance) are analytic and cross-checked by Monte Carlo simulation. This yields **safe, explainable, and traceable** parameter changes.

## Quick start

```bash
pip install -r requirements.txt
# Run the demo:
# notebooks/ig_toy_slot_en.ipynb
```

Or browse pre-generated artifacts:

- **Excel mirror**: `excel/paytable_audit.xlsx`
- **One-pager**: `docs/one_pager.md`
- **Methodology (conceptual overview)**: `docs/methodology.md`
- **Figures**: `figures/objective_convergence.png`, `figures/metrics_over_iterations.png`
- **Sample data**: `data/spins_log_sample.csv`

## Methodology & components

- Conceptual framework (unified coordinates, guardrails, KL trust-region): `docs/methodology.md`  
- Building blocks (`components/`):
  - `paytable.md` — payout/probability vectors; simplex domain; invariants  
  - `metrics.md` — RTP / Hit-rate / Variance definitions and differentials  
  - `optimizer.md` — KL-bounded mirror-descent on the simplex; step control; stopping  
  - `constraints.md` — guardrails as linear bands; KL/Bregman projection  
  - `simulator.md` — Monte Carlo estimators and confidence intervals  
  - `audit.md` — Excel mirror, one-pager, and notebook reproducibility rules  
  - `data_schema.md` — `spins_log` schema and data-quality checks  
  - `config.md` — targets, tolerances, seeds, file paths (YAML suggestions)

## KPI definitions (bet = 1)

- **RTP**: \( \text{RTP}(p) = \sum_i p_i\, r_i \)  
- **Hit-rate**: \( \text{Hit}(p) = \sum_{r_i>0} p_i \)  
- **Variance (volatility proxy)**: \( \text{Var}(p) = \sum_i p_i\, r_i^2 - \text{RTP}(p)^2 \)  
  Where `r` is the **payout vector** (multipliers) and `p` the corresponding probability vector.

## Demo configuration (default)

- Baseline metrics (analytic): RTP ≈ 0.9472, Hit ≈ 0.3200, Var ≈ 14.0436  
- Guardrails (bands): RTP ≈ 0.9500 (±0.005), Hit ≈ 0.3200 (±0.02)  
- Goal: **increase variance** while staying inside the bands  
- Validation: **Analytic vs Monte Carlo** (1e6 draws) agree within confidence intervals  

> Targets and tolerances can be adapted; see `components/config.md`.

## Folder layout

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── docs
│   ├── one_pager.md
│   └── methodology.md
├── components
│   ├── paytable.pdf
│   ├── metrics.pdf
│   ├── optimizer.pdf
│   ├── constraints.pdf
│   ├── simulator.pdf
│   ├── audit.pdf
│   ├── data_schema.pdf
│   └── config.md
├── notebooks
│   └── ig_toy_slot_en.ipynb
├── excel
│   └── paytable_audit.xlsx
├── figures
│   ├── objective_convergence.png
│   └── metrics_over_iterations.png
└── data
    └── spins_log_sample.csv
```

## Scope & notes

This is a **toy demo / PoC** showing: unified coordinates + guardrails + audit-first delivery.  
A production setup would plug in real jurisdiction limits, internal spreadsheet templates, data pipelines, and staged rollout (shadow → canary → full).
