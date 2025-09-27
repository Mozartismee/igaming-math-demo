# toy-slot-on-the-simplex: KL-bounded tuning under RTP/Hit guardrails

**Tagline.** Treat the slot paytable as a point on the probability simplex. Increase volatility via **small, KL‑bounded steps** (mirror descent / natural gradient) **within RTP/Hit guardrails**. Every step is **audit‑ready** (Excel mirror + one‑pager + reproducible notebook).

> Note: This README uses plain text math for readability. The mathematical details live in `docs/info_geometry.md`.

## What this repo provides

- **Auditable tuning framework:** a unified coordinate system for RTP, Hit‑rate, and Variance with explicit guardrails.
- **Reproducibility:** an executable notebook, seeded Monte Carlo checks, and an Excel mirror for non‑engineers.
- **Executive‑readiness:** a one‑pager summarizing assumptions, metrics, and results in plain English.

## How it works (at a glance)

Paytable probabilities are treated as a vector `p = (p1, …, pn)` with all entries positive and `p1 + … + pn = 1` (the open probability simplex).  
Updates take **small, KL‑bounded steps** and are **projected back** to the RTP/Hit bands when needed. KPIs (RTP / Hit‑rate / Variance) are computed analytically and cross‑checked by Monte Carlo simulation. This yields **safe, explainable, traceable** parameter changes.

See **`docs/info_geometry.md`** for a minimal atlas:

- **Mixture coordinates:** `x = (p1, …, p_{n-1})`, with inverse `pn = 1 − sum(x_i)`.
- **Exponential coordinates:** `theta_i = log(pi / pn)`; inverse (softmax)  
  `pi = exp(theta_i) / (1 + sum_j exp(theta_j))`, `pn = 1 / (1 + sum_j exp(theta_j))`.
- **Fisher metric vs KL:** near interior points, the quadratic approximation of KL matches the Fisher metric, so KL‑bounded updates behave like short geodesic steps (natural‑gradient view).

## Quick start

```bash
pip install -r requirements.txt
# Run the demo:
# notebooks/ig_toy_slot_en.ipynb
```

Or browse pre‑generated artifacts:

- **Unified Quick Note:** `docs/QUICK_NOTE.md`
- **Excel mirror:** `excel/paytable_audit.xlsx`
- **One‑pager:** `docs/one_pager.md`
- **Methodology (overview):** `docs/methodology.md`
- **Information Geometry (atlas & charts):** `docs/info_geometry.md`
- **Figures:** `figures/objective_convergence.png`, `figures/metrics_over_iterations.png`
- **Sample data:** `data/spins_log_sample.csv`

## Methodology & components

- Conceptual framework (unified coordinates, guardrails, KL trust‑region): `docs/methodology.md`  
- Building blocks (`components/`):
  - `paytable.md` — payout/probability vectors; simplex domain; invariants  
  - `metrics.md` — RTP / Hit‑rate / Variance definitions and differentials  
  - `optimizer.md` — KL‑bounded mirror‑descent on the simplex; step control; stopping  
  - `constraints.md` — guardrails as linear bands; KL/Bregman projection  
  - `simulator.md` — Monte Carlo estimators and confidence intervals  
  - `audit.md` — Excel mirror, one‑pager, and notebook reproducibility rules  
  - `data_schema.md` — `spins_log` schema and data‑quality checks  
  - `config.md` — targets, tolerances, seeds, file paths (YAML suggestions)

## KPI definitions (bet = 1)

Let `p` be the probability vector and `r` the payout (multiplier) vector.

- **RTP:** `RTP = sum_i p[i] * r[i]`
- **Hit‑rate:** `Hit = sum of p[i] for which r[i] > 0`
- **Variance (volatility proxy):** `Var = sum_i p[i] * r[i]^2  −  RTP^2`

## Demo configuration (default)

- Baseline (analytic): `RTP ≈ 0.9472`, `Hit‑rate ≈ 0.3200`, `Var ≈ 14.0436`  
- Guardrails (bands): `RTP ≈ 0.9500 (±0.005)`, `Hit‑rate ≈ 0.3200 (±0.02)`  
- Goal: **increase Variance** while remaining within both bands  
- Validation: **Analytic vs Monte Carlo** (≥ `10^6` draws) agree within confidence intervals

> Targets and tolerances are configurable; see `components/config.md`.

## Folder layout

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── docs
│   ├── one_pager.md
│   ├── methodology.md
│   ├── QUICK_NOTE.md
│   ├── info_geometry.md
│   └── figures
│       └── atlas_coords.png
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

This is a **toy demo / PoC** showing: unified coordinates + guardrails + audit‑first delivery.  
A production setup would plug in real jurisdiction limits, internal spreadsheet templates, data pipelines, and staged rollout (shadow → canary → full).
