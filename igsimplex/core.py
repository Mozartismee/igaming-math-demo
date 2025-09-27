import numpy as np

# ---------- Basics ----------

def normalize(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
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
        ratio = np.where(p_new > 0.0, p_new / np.maximum(p_old, 1e-300), 1.0)
        term = np.where(p_new > 0.0, p_new * np.log(ratio), 0.0)
    return float(np.sum(term))

def mc_estimates(p: np.ndarray, r: np.ndarray, n: int, seed: int = 123):
    """Monte Carlo RTP/Hit/Var estimator."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(p), size=n, p=normalize(p))
    pay = r[idx]
    rtp = float(pay.mean())
    hit = float((pay > 0.0).mean())
    var = float(pay.var(ddof=0))  # bet=1
    return rtp, hit, var

# ---------- KL projection helpers ----------

def _tilt(p: np.ndarray, a: np.ndarray) -> np.ndarray:
    """
    Exponential tilt: p' ∝ p * exp(a)
    Numerically stable via max-subtraction.
    """
    p = normalize(p)
    a = np.asarray(a, dtype=float)
    x = a - np.max(a)
    w = p * np.exp(x)
    s = w.sum()
    if not np.isfinite(s) or s <= 0:
        return p.copy()
    return w / s

def _rtp(p: np.ndarray, r: np.ndarray) -> float:
    return float(np.dot(normalize(p), np.asarray(r, dtype=float)))

def _hit(p: np.ndarray, mask01: np.ndarray) -> float:
    return float(np.dot(normalize(p), np.asarray(mask01, dtype=float)))

def _project_rtp_kl(p: np.ndarray,
                    r: np.ndarray,
                    target: float,
                    side: str,
                    tol: float = 1e-9,
                    max_iter: int = 80) -> np.ndarray:
    """
    Minimize KL(p'||p) s.t. E_{p'}[r] = target (hit equality analog below).
    When side='upper', enforce E[r] <= target by landing on boundary.
    When side='lower', enforce E[r] >= target by landing on boundary.
    Achieved by p'(i) ∝ p(i) * exp(-λ r_i) with bisection on λ.
    """
    p = normalize(p)
    r = np.asarray(r, dtype=float)
    cur = _rtp(p, r)

    if side == "upper":
        if cur <= target + tol:
            return p
        lo, hi = 0.0, 1.0
        # Expand hi until E_r <= target
        while _rtp(_tilt(p, -hi * r), r) > target and hi < 1e6:
            hi *= 2.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            pm = _tilt(p, -mid * r)
            val = _rtp(pm, r)
            if val <= target:
                hi = mid
            else:
                lo = mid
        return _tilt(p, -hi * r)

    else:  # side == "lower"
        if cur >= target - tol:
            return p
        lo, hi = 0.0, 1.0
        # Need to increase E[r] -> λ negative; search on -hi
        while _rtp(_tilt(p, +hi * r), r) < target and hi < 1e6:
            hi *= 2.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            pm = _tilt(p, +mid * r)
            val = _rtp(pm, r)
            if val >= target:
                hi = mid
            else:
                lo = mid
        return _tilt(p, +hi * r)

def _project_hit_kl(p: np.ndarray,
                    mask01: np.ndarray,
                    target: float,
                    side: str,
                    tol: float = 1e-9,
                    max_iter: int = 80) -> np.ndarray:
    """
    Minimize KL(p'||p) s.t. E_{p'}[h] = target for h∈{0,1}^n (hit-rate).
    Achieved by p'(i) ∝ p(i) * exp(μ h_i), bisection on μ.
    side='upper' enforces E[h] <= target; 'lower' enforces E[h] >= target.
    """
    p = normalize(p)
    h = np.asarray(mask01, dtype=float)
    cur = _hit(p, h)

    if side == "upper":
        if cur <= target + tol:
            return p
        lo, hi = 0.0, 1.0
        while _hit(_tilt(p, +hi * h), h) > target and hi < 1e6:
            hi *= 2.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            pm = _tilt(p, +mid * h)
            val = _hit(pm, h)
            if val <= target:
                hi = mid
            else:
                lo = mid
        return _tilt(p, +hi * h)

    else:  # side == "lower"
        if cur >= target - tol:
            return p
        lo, hi = 0.0, 1.0
        while _hit(_tilt(p, -hi * h), h) < target and hi < 1e6:
            hi *= 2.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            pm = _tilt(p, -mid * h)
            val = _hit(pm, h)
            if val >= target:
                hi = mid
            else:
                lo = mid
        return _tilt(p, -hi * h)

# ---------- Public API ----------

def affine_exponentiated_projection(
    p: np.ndarray,
    r: np.ndarray,
    rtp_band: tuple[float, float] | None,
    hit_band: tuple[float, float] | None,
    max_iter: int = 50,
    tol: float = 1e-8
) -> np.ndarray:
    """
    KL (Bregman) projection of p onto bands of RTP and Hit via alternating
    1D KL-minimal projections (exponential tilts). Stable and band-exact.

    Steps:
      1) If RTP is out of band, project to nearest boundary (I-projection).
      2) Recompute; if Hit is out of band, project similarly.
      3) Alternate up to max_iter or until both in-band (with tol).
    """
    p = normalize(p)
    r = np.asarray(r, dtype=float)
    h = (r > 0.0).astype(float)

    # Alternating projections
    for _ in range(max_iter):
        rtp, hit, _ = kpis(p, r)

        # RTP band
        if rtp_band is not None:
            low_rtp, high_rtp = rtp_band
            if rtp > high_rtp + tol:
                p = _project_rtp_kl(p, r, high_rtp, side="upper", tol=tol)
            elif rtp < low_rtp - tol:
                p = _project_rtp_kl(p, r, low_rtp, side="lower", tol=tol)

        # Recompute after RTP projection
        rtp, hit, _ = kpis(p, r)

        # Hit band
        if hit_band is not None:
            low_hit, high_hit = hit_band
            if hit > high_hit + tol:
                p = _project_hit_kl(p, h, high_hit, side="upper", tol=tol)
            elif hit < low_hit - tol:
                p = _project_hit_kl(p, h, low_hit, side="lower", tol=tol)

        # Check termination: both in bands
        rtp, hit, _ = kpis(p, r)
        ok_rtp = (rtp_band is None) or (rtp >= rtp_band[0] - tol and rtp <= rtp_band[1] + tol)
        ok_hit = (hit_band is None) or (hit >= hit_band[0] - tol and hit <= hit_band[1] + tol)
        if ok_rtp and ok_hit:
            return normalize(p)

    # Best effort if not converged within max_iter
    return normalize(p)
