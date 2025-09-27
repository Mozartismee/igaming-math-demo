# igaming-math-demo · Unified Quick Note

[Context] Increase payout variance with minimal, auditable steps while keeping RTP/Hit and compliance intact. Supports product pacing and risk control.

## Problem
Increase payout variance (Var) while keeping RTP and Hit within guardrails.

## Setup (toy model)
Payout vector r, e.g. [0, 0.5, 1, 2, 5, 10, 25, 50]; probabilities p ∈ Δ^{n−1}.  
RTP = ⟨p, r⟩; Hit = ∑_{r_i>0} p_i; Var = ⟨p, r²⟩ − RTP².  
Baseline example: RTP ≈ 0.9472, Hit ≈ 0.3200, Var ≈ 14.04.

## Guardrails
RTP ≈ 0.950 ± 0.005; Hit ∈ [0.30, 0.34]. Optional hard caps such as a max single payout.

## Objective (choose one)
1) Constrained maximization of Var; or  
2) Penalized objective L = w_μ(RTP − μ*)² + w_h(Hit − h*)² − w_v Var.

## Method (information geometry)
Operate on the statistical manifold with KL as a trust region.  
Mirror descent / natural gradient: p⁺ ∝ p ⊙ exp(−η ∇_p L), then normalize into Δ^{n−1}.  
On any violation of guardrails, project back to the feasible set.

### Projection (practical shortcut)
Hit off-range: move a tiny probability mass between miss ↔ smallest win.  
RTP off-range: move a tiny mass between small wins ↔ high wins.  
Normalize after each transfer.

## Pipeline (6 steps)
1) Initialize r, p₀; set μ*, h*, weights, η; compute baseline KPIs.  
2) Iterate: compute ∇L, apply exponentiated update to get p⁺.  
3) Check guardrails; project if needed.  
4) Log history: RTP, Hit, Var, KL, L.  
5) Stopping criterion: diminishing Var gains or max steps; obtain p*.  
6) Monte Carlo validation: simulate with p* for N ≥ 10⁶ and compare to analytics.

## Observations
A. RTP/Hit respond strongly to mass transfers. Hit is controlled on miss ↔ smallest win; RTP/Var on mid ↔ tail.  
B. With RTP fixed, pushing mid mass to tail grows Var faster; tune Hit along the miss line.  
C. KL trust region yields robust, auditable updates on Δ^{n−1}, superior to Euclidean steps.

## Defects (current)
Heuristic projection; config not in YAML; no real spins log; empirical step size and stopping; no Pareto map for multi-objectives.

## Improvements (roadmap)
Convex projection within a KL radius or QP; Fisher natural gradient with adaptive step sizing; YAML + CI; integrate reels and real logs with shadow → canary rollout; Var–Retention–RTP Pareto mapping.

## Results (example)
p* stays within guardrails: RTP ≈ 0.950 ± 0.0003, Hit ≈ 0.321 ± 0.001, Var ≈ 16.8 (~ +20%).  
Monte Carlo with N ≥ 10⁶ aligns with analytics within ~1e−4.  
Deliverables: one-pager, convergence plots, Excel audit mirror, final p* and KPIs.

## Mnemonic
Small KL steps on Δ^{n−1}; keep RTP/Hit inside rails; push tail to grow Var; project on violation; validate by simulation.
