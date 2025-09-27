import numpy as np
from .core import normalize, kpis, kl, affine_exponentiated_projection

def variance_grad(p: np.ndarray, r: np.ndarray):
    """∂Var/∂p_i = r_i^2 − 2*RTP*r_i (under simplex coordinates)."""
    p = normalize(p)
    rtp, _, _ = kpis(p, r)
    return r**2 - 2.0 * rtp * r

def exponentiated_step(p: np.ndarray, grad: np.ndarray, eta: float):
    """Exponentiated gradient update on simplex: p' ∝ p * exp(eta * grad)."""
    logits = np.log(np.maximum(p, 1e-300)) + eta * grad
    p_new = np.exp(logits - logits.max())
    return p_new / p_new.sum()

def kl_bounded_step(p: np.ndarray, grad: np.ndarray, max_kl: float):
    """
    Choose eta by binary search so that KL(p_new || p) <= max_kl.
    """
    lo, hi = 0.0, 100.0  # wide bracket
    p_new = p.copy()
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        cand = exponentiated_step(p, grad, mid)
        d = kl(cand, p)
        if d > max_kl:
            hi = mid
        else:
            lo = mid
            p_new = cand
    return p_new, lo  # return chosen eta

def run_optimization(p0: np.ndarray, r: np.ndarray, rtp_band, hit_band,
                     max_kl_per_step=5e-4, max_iters=200, project_every_step=True):
    """
    Maximize Variance with KL-bounded exponentiated steps and guardrail projection.
    Returns history dict with p_list, kpis_list, kl_list, eta_list.
    """
    p = normalize(p0)
    hist = {"p": [p.copy()], "rtp": [], "hit": [], "var": [], "kl": [], "eta": []}

    rtp, hit, var = kpis(p, r)
    hist["rtp"].append(rtp); hist["hit"].append(hit); hist["var"].append(var)
    hist["kl"].append(0.0);  hist["eta"].append(0.0)

    for _ in range(max_iters):
        g = variance_grad(p, r)
        p_step, eta = kl_bounded_step(p, g, max_kl_per_step)
        if project_every_step:
            p_step = affine_exponentiated_projection(p_step, r, rtp_band, hit_band)

        dkl = kl(p_step, p)
        p = p_step

        rtp, hit, var = kpis(p, r)
        hist["p"].append(p.copy())
        hist["rtp"].append(rtp); hist["hit"].append(hit); hist["var"].append(var)
        hist["kl"].append(dkl);   hist["eta"].append(eta)

        # crude stop: tiny movement and var plateaus
        if dkl < 1e-7:
            break

    return hist
