import argparse, json, time, os, yaml, numpy as np, pandas as pd
from pathlib import Path
from .core import kpis, mc_estimates
from .opt import run_optimization

def _ts():
    return time.strftime("%Y%m%d_%H%M%S")

def run_from_config(cfg_path: str):
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    out_dir = Path(f"runs/run_{_ts()}")
    out_dir.mkdir(parents=True, exist_ok=True)

    seed = int(cfg.get("seed", 123))
    np.random.seed(seed)

    p_init = np.array(cfg["p_init"], float)
    r = np.array(cfg["r"], float)
    rtp_band = tuple(cfg["rtp_band"])
    hit_band = tuple(cfg["hit_band"])
    max_iters = int(cfg.get("max_iters", 120))
    max_kl = float(cfg.get("max_kl_per_step", 5e-4))
    project_every_step = bool(cfg.get("project_every_step", True))

    hist = run_optimization(p_init, r, rtp_band, hit_band,
                            max_kl_per_step=max_kl,
                            max_iters=max_iters,
                            project_every_step=project_every_step)

    # History dataframe
    df = pd.DataFrame({
        "iter": range(len(hist["rtp"])),
        "RTP": hist["rtp"],
        "Hit": hist["hit"],
        "Var": hist["var"],
        "KL": hist["kl"],
        "eta": hist["eta"],
    })
    df.to_csv(out_dir / "metrics_history.csv", index=False)

    # Final KPIs and MC check
    p_final = hist["p"][-1]
    rtp_f, hit_f, var_f = kpis(p_final, r)
    rtp_mc, hit_mc, var_mc = mc_estimates(p_final, r, n=1_000_000, seed=seed+1)

    summary = {
        "RTP": {"Analytic": rtp_f, "MC": rtp_mc},
        "Hit": {"Analytic": hit_f, "MC": hit_mc},
        "Var": {"Analytic": var_f, "MC": var_mc},
        "rtp_band": rtp_band, "hit_band": hit_band,
        "max_kl_per_step": max_kl, "iters": len(hist["rtp"])-1,
    }
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Minimal Excel mirror
    try:
        import openpyxl  # ensure engine
        df.to_excel(out_dir / "paytable_audit.xlsx", index=False)
    except Exception:
        pass

    print(f"[OK] Wrote results to: {out_dir}")
    return 0

def main():
    ap = argparse.ArgumentParser(prog="igsimplex", description="KL-bounded tuning under RTP/Hit guardrails")
    sub = ap.add_subparsers(dest="cmd", required=True)

    rp = sub.add_parser("run", help="Run optimization from YAML config")
    rp.add_argument("--config", "-c", required=True, help="Path to YAML config")

    args = ap.parse_args()
    if args.cmd == "run":
        return run_from_config(args.config)

if __name__ == "__main__":
    raise SystemExit(main())
