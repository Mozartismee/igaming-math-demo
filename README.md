# toy-slot-on-the-simplex: KL-bounded tuning under RTP/Hit guardrails

**Tagline.** Treat the slot paytable as a point on the probability simplex. Increase volatility via **small, KL-bounded steps** (mirror descent / natural gradient) **within RTP/Hit guardrails**. Every step is **audit-ready** (Excel mirror + one-pager + reproducible notebook).

## What this repo provides

- **Auditable tuning framework:** a unified coordinate system for RTP, Hit-rate, and Variance with explicit guardrails.
- **Reproducibility:** an executable notebook, seeded Monte Carlo checks, and an Excel mirror for non-engineers.
- **Executive-readiness:** a one-pager summarizing assumptions, metrics, and results in plain English.

## How it works (at a glance)

Paytable probabilities \(p\) are modeled on the **open probability simplex** \(\Delta^{n-1}_{+}=\{\,p\in\mathbb{R}^n \mid p_i>0,\ \sum_i p_i=1\,\}\).
Updates take **small, KL-bounded steps** and are **projected back** to the RTP/Hit bands when needed. KPIs (RTP / Hit-rate / Variance) are analytic and cross-checked by Monte Carlo simulation. This yields **safe, explainable, traceable** parameter changes.

See **`docs/info_geometry.md`** for a minimal atlas:

- **Mixture coordinates** \(x=(p_1,\dots,p_{n-1})\) with inverse \(p_n=1-\sum_{i=1}^{n-1}x_i\).
- **Exponential coordinates** \(\theta_i=\log(p_i/p_n)\) with inverse softmax \(p_i=\frac{e^{\theta_i}}{1+\sum_{j=1}^{n-1}e^{\theta_j}},\ p_n=\frac{1}{1+\sum_{j=1}^{n-1}e^{\theta_j}}\).
- **Fisher information metric:** the quadratic approximation of KL at interior points equals the Fisher metric, so KL-bounded updates correspond to short geodesic steps (natural-gradient view).

## Quick start

```bash
pip install -r requirements.txt
# Run the demo:
# notebooks/ig_toy_slot_en.ipynb
```

Or browse pre-generated artifacts:

- **Unified Quick Note:** `docs/QUICK_NOTE.md`
- **Excel mirror:** `excel/paytable_audit.xlsx`
- **One-pager:** `docs/one_pager.md`
- **Methodology (overview):** `docs/methodology.md`
- **Information Geometry (atlas & charts):** `docs/info_geometry.md`
- **Figures:** `figures/objective_convergence.png`, `figures/metrics_over_iterations.png`
- **Sample data:** `data/spins_log_sample.csv`

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

Let \(p\in\Delta^{n-1}_{+}\) and payout vector \(r\ge 0\).

- **RTP:** \(\mathrm{RTP}(p)=\sum_i p_i r_i\)  
- **Hit-rate:** \(\mathrm{Hit}(p)=\sum_{r_i>0} p_i\)  
- **Variance (volatility proxy):** \(\mathrm{Var}(p)=\sum_i p_i r_i^2-\mathrm{RTP}(p)^2\)

## Demo configuration (default)

- Baseline (analytic): RTP ≈ 0.9472, Hit-rate ≈ 0.3200, Var ≈ 14.0436  
- Guardrails (bands): RTP ≈ 0.9500 (±0.005), Hit-rate ≈ 0.3200 (±0.02)  
- Goal: **increase Variance** while remaining within both bands  
- Validation: **Analytic vs Monte Carlo** (≥ \(10^6\) draws) agree within confidence intervals

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

This is a **toy demo / PoC** showing: unified coordinates + guardrails + audit-first delivery.  
A production setup would plug in real jurisdiction limits, internal spreadsheet templates, data pipelines, and staged rollout (shadow → canary → full).
