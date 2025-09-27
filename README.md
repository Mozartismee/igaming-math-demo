# toy-slot-on-the-simplex — KL-bounded tuning under RTP/Hit guardrails

**Tagline.** Treat the slot paytable as a point on the probability simplex. Increase volatility via **small, KL-bounded steps** (mirror descent / natural gradient) **within RTP/Hit guardrails**. Every step is **audit-ready** (Excel mirror + one-pager + reproducible notebook + CLI outputs).

> Note: This README uses plain text math for readability. Mathematical details live in `docs/info_geometry.md`.

**Python:** 3.9–3.12

---

## Quickstart 

```bash
# 0) clone
git clone <repo-url> && cd igaming-math-demo

# 1) virtualenv
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# 2) install (package + test deps)
pip install -U pip
pip install -e '.[dev]'      # 注意 zsh 需要引號；PowerShell 用 ".[dev]"

# 3) run tests — expect "3 passed"
pytest -q

# 4) run a reproducible demo
python -m igsimplex --config configs/var_only.yaml --seed 42
```

**Artifacts** are saved under `runs/<timestamp>/`:

- `summary.json` — analytic vs MC, guardrails, KL trust-region  
- `metrics_history.csv` — RTP/Hit/Var/KL per iteration  
- `paytable_audit.xlsx` — Excel mirror for non-engineers

> Alt: if you prefer notebooks  
> `pip install -r requirements.txt && jupyter notebook notebooks/ig_toy_slot_en.ipynb`

### Troubleshooting

- **`zsh: no matches found: .[dev]`** → 用 `pip install -e '.[dev]'`（加引號）。  
- **`ModuleNotFoundError: igsimplex`** → 確認你已啟用 venv 並成功執行 `pip install -e '.[dev]'`。  
- **Windows** 不需要 `make`：本專案已採用標準 Python 安裝流程。

---

## What this repo provides

- **Auditable tuning framework:** a unified coordinate system for RTP, Hit-rate, and Variance with explicit guardrails.
- **Reproducibility:** an executable notebook, seeded Monte Carlo checks, Excel mirror, and reproducible CLI runs.
- **Executive-readiness:** a one-pager (`docs/one_pager.md`) and Excel outputs for non-engineers.
- **Engine module:** `igsimplex/` — a small Python package implementing KL-bounded updates, guardrail projection, and metrics.

---

## How it works (at a glance)

Paytable probabilities are treated as a vector `p = (p1, …, pn)` with all entries positive and `p1 + … + pn = 1` (the open probability simplex).  
Updates take **small, KL-bounded steps** and are **projected back** to the RTP/Hit bands when needed. KPIs (RTP / Hit-rate / Variance) are computed analytically and cross-checked by Monte Carlo simulation. This yields **safe, explainable, traceable** parameter changes.

See **`docs/info_geometry.md`** for a minimal atlas:

- **Mixture coordinates:** `x = (p1, …, p_{n-1})`, with inverse `pn = 1 − sum(x_i)`.
- **Exponential coordinates:** `theta_i = log(pi / pn)`; inverse (softmax)  
  `pi = exp(theta_i) / (1 + sum_j exp(theta_j))`, `pn = 1 / (1 + sum_j exp(theta_j))`.
- **Fisher metric vs KL:** near interior points, the quadratic approximation of KL matches the Fisher metric, so KL-bounded updates behave like short geodesic steps (natural-gradient view).

---

## Artifacts (pre-generated)

- **Unified Quick Note:** `docs/QUICK_NOTE.md`  
- **Excel mirror:** `excel/paytable_audit.xlsx`  
- **One-pager:** `docs/one_pager.md`  
- **Methodology (overview):** `docs/methodology.md`  
- **Information Geometry (atlas & charts):** `docs/info_geometry.md`  
- **Figures:** `figures/objective_convergence.png`, `figures/metrics_over_iterations.png`  
- **Sample data:** `data/spins_log_sample.csv`

---

## Methodology & components

- Conceptual framework (unified coordinates, guardrails, KL trust-region): `docs/methodology.md`  
- Building blocks (`components/`):
  - `paytable.pdf` — payout/probability vectors; simplex domain; invariants  
  - `metrics.pdf` — RTP / Hit-rate / Variance definitions and differentials  
  - `optimizer.pdf` — KL-bounded mirror-descent on the simplex; step control; stopping  
  - `constraints.pdf` — guardrails as linear bands; KL/Bregman projection  
  - `simulator.pdf` — Monte Carlo estimators and confidence intervals  
  - `audit.pdf` — Excel mirror, one-pager, and notebook reproducibility rules  
  - `data_schema.pdf` — `spins_log` schema and data-quality checks  
  - `config.md` — targets, tolerances, seeds, file paths (YAML suggestions)

---

## KPI definitions (bet = 1)

Let `p` be the probability vector and `r` the payout (multiplier) vector.

- **RTP:** `RTP = sum_i p[i] * r[i]`  
- **Hit-rate:** `Hit = sum of p[i] for which r[i] > 0`  
- **Variance (volatility proxy):** `Var = sum_i p[i] * r[i]^2  −  RTP^2`

---

## Demo configuration (default)

- Baseline (analytic): `RTP ≈ 0.9472`, `Hit-rate ≈ 0.3200`, `Var ≈ 14.0436`  
- Guardrails (bands): `RTP ≈ 0.9500 (±0.005)`, `Hit-rate ≈ 0.3200 (±0.02)`  
- Goal: **increase Variance** while remaining within both bands  
- Validation: **Analytic vs Monte Carlo** (`≥ 10^6` draws) agree within confidence intervals

> Targets and tolerances are configurable; see `configs/*.yaml` and `components/config.md`.

---

## Folder layout

```
.
├── README.md
├── pyproject.toml
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
├── igsimplex
│   ├── core.py
│   ├── opt.py
│   ├── cli.py
│   └── __main__.py
├── configs
│   └── var_only.yaml
├── tests
│   ├── test_metrics.py
│   ├── test_projection.py
│   └── test_kl_step.py
├── notebooks
│   └── ig_toy_slot_en.ipynb
├── excel
│   └── paytable_audit.xlsx
├── figures
│   ├── objective_convergence.png
│   └── metrics_over_iterations.png
├── runs/               # auto-generated experiment outputs
└── compliance
    └── change_log.md   # template for audit & rollback
```

---

## Scope & notes

This is a **toy demo / PoC** showing:  

- unified coordinates + guardrails + audit-first delivery, and  
- an engine (`igsimplex/`) with CLI, tests, and compliance hooks.  

A production setup would plug in real jurisdiction limits, internal spreadsheet templates, data pipelines, and staged rollout (shadow → canary → full).  
Outputs under `runs/` plus `compliance/change_log.md` are designed as **audit / rollback artifacts**.
