import numpy as np

def normalize(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 0.0, None)
    s = p.sum()
    if s <= 0:
        raise ValueError("Probability vector has non-positive sum.")
    return p / s

def kpis(p: np.ndarray, r: np.ndarray):
    """Compute RTP, Hit, Var (bet=1)."""
    p = normalize(p)
    r = np.asarray(r, dtype=float)
    rtp = float(np.dot(p, r))
    hit = float(p[r > 0.0].sum())
    var = float(np.dot(p, r**2) - rtp**2)
    return rtp, hit, var

def kl(p_new: np.ndarray, p_old: np.ndarray) -> float:
    """KL(p_new || p_old). Both must be prob. vectors."""
    p_new = normalize(p_new)
    p_old = normalize(p_old)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(p_new > 0, p_new / np.maximum(p_old, 1e-300), 1.0)
        term = np.where(p_new > 0, p_new * np.log(ratio), 0.0)
    return float(np.sum(term))

def mc_estimates(p: np.ndarray, r: np.ndarray, n: int, seed: int = 123):
    """Monte Carlo RTP/Hit/Var estimator."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(p), size=n, p=normalize(p))
    pay = r[idx]
    rtp = float(pay.mean())
    hit = float((pay > 0.0).mean())
    var = float(pay.var(ddof=0) - 0.0)  # bet=1
    return rtp, hit, var

def affine_exponentiated_projection(p: np.ndarray, r: np.ndarray,
                                    rtp_band: tuple[float, float],
                                    hit_band: tuple[float, float],
                                    max_iter: int = 50, tol: float = 5e-7):
    """
    KL (Bregman) projection of p onto linear bands of RTP and Hit.
    Uses multiplicative weights with two dual parameters (lambda, mu):
      p' ∝ p * exp(lambda * r + mu * I[r>0])
    and coordinate updates on (lambda, mu) until both constraints fall into bands.
    """
    p0 = normalize(p)
    r = np.asarray(r, dtype=float)
    mask_hit = (r > 0.0).astype(float)

    lam, mu = 0.0, 0.0
    for _ in range(max_iter):
        logits = np.log(np.maximum(p0, 1e-300)) + lam * r + mu * mask_hit
        p_new = np.exp(logits - logits.max())
        p_new = p_new / p_new.sum()

        rtp, hit, _ = kpis(p_new, r)

        # Adjust lam for RTP
        if rtp < rtp_band[0]:
            lam += 0.5
        elif rtp > rtp_band[1]:
            lam -= 0.5
        else:
            # small nudges to center
            lam += 0.1 * (0.5 * (rtp_band[0] + rtp_band[1]) - rtp)

        # Adjust mu for Hit
        if hit < hit_band[0]:
            mu += 0.5
        elif hit > hit_band[1]:
            mu -= 0.5
        else:
            mu += 0.1 * (0.5 * (hit_band[0] + hit_band[1]) - hit)

        # Check convergence (both in-band and stable)
        if (rtp_band[0] <= rtp <= rtp_band[1]) and (hit_band[0] <= hit <= hit_band[1]):
            # ensure small KL movement from previous projection step
            if kl(p_new, p0) < tol:
                return p_new
            # else keep refining a bit more with smaller nudges
    return p_new  # best-effort
