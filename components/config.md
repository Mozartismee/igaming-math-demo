# Config Component

## Recommended YAML keys
```yaml
targets:
  rtp: 0.95
  rtp_tolerance: 0.005
  hit: 0.32
  hit_tolerance: 0.02
variance:
  multiplier: 1.2   # aim Var >= 1.2 * baseline Var
optimizer:
  lr: 0.4
  kl_cap: 0.001
  max_iters: 600
projection:
  priority: ["rtp", "hit"]   # prioritize legal bounds first
simulator:
  draws: 1000000
  seed: 42
artifacts:
  out_dir: artifacts/
  save_figures: true
```

## Contracts
- Every run must serialize the **config used** beside outputs.
- Downstream jobs read KPIs and per-step KL from a stable CSV/JSON contract.
