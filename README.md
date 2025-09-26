# toy-slot-on-the-simplex — KL-bounded updates under RTP/Hit guardrails (Day‑1 Demo)

**Tagline:** Treat the slot paytable as a point on the probability simplex. Move in **small, KL‑bounded steps** (mirror descent / natural-gradient flavor) **inside RTP/Hit guardrails** to increase volatility. Every step is **audit‑ready** (Excel mirror + one‑pager + reproducible notebook).

## Why this repo
- **Business goal:** Make the game feel more exciting (higher volatility) **without** breaking player feel or compliance targets: RTP ≈ 95%, Hit‑rate ≈ 30–34%.
- **Core method:** A **unified coordinate system** (statistical manifold) + **invariants/guardrails** (RTP/Hit) + **KL trust‑region** for safe navigation.
- **Audit by design:** Excel mirror (for non-engineers and compliance), a one‑pager (executive/PM‑friendly), and a notebook (fully reproducible).

## Quick start
```bash
pip install -r requirements.txt
# Open and run the full demo:
# notebooks/ig_toy_slot_en.ipynb
```

Or browse pre-generated artifacts:
- Excel mirror: `excel/paytable_audit.xlsx`
- One‑pager: `docs/one_pager.md`
- Figures: `figures/objective_convergence.png`, `figures/metrics_over_iterations.png`
- Sample data: `data/spins_log_sample.csv`

## KPI definitions (bet = 1)
- RTP = Σ p_i · r_i  
- Hit‑rate = Σ{r_i>0} p_i  
- Variance = Σ p_i · r_i² − RTP²

Where `r` is the **payout vector** (multipliers), and `p` is the corresponding probability vector.

## Day‑1 scope
- Baseline (given): RTP ≈ 0.9472, Hit ≈ 0.3200, Var ≈ 14.0436
- Target guardrails: RTP ≈ 0.9500 (±0.005), Hit ≈ 0.3200 (±0.02), and **increase variance**
- Navigation: small **KL‑bounded** steps; log each step’s KL and KPI changes
- Validation: **Analytic vs Monte Carlo** (1e6 draws) must match closely

## Repo layout
```
.
├── README.md
├── requirements.txt
├── .gitignore
├── docs
│   └── one_pager.md
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

## Notes
This is a **toy demo / PoC** showing: unified coordinates + guardrails + audit‑first delivery. A production setup would plug in real jurisdiction limits, internal Excel templates, and a staged rollout (shadow → canary → full).
