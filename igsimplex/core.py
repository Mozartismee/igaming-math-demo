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
    p'(i) ∝ p(i) * exp(μ h_i), 且 E[h] 對 μ 單調遞增。
    side='upper'：把命中率壓到 target（≤ target），μ ≤ 0；
    side='lower'：把命中率拉到 target（≥ target），μ ≥ 0。
    """
    p = normalize(p)
    h = np.asarray(mask01, dtype=float)
    cur = _hit(p, h)

    if side == "upper":
        # 目標：E[h] ≤ target。若已滿足，直接回傳。
        if cur <= target + tol:
            return p
        # 夾住區間 [lo, hi]，使 f(lo) ≤ target ≤ f(hi)；f(μ) = E[h] 單調↑
        lo, hi = -1.0, 0.0
        while _hit(_tilt(p, lo * h), h) > target and lo > -1e12:
            lo *= 2.0  # 更負，命中率會更低
        f_lo = _hit(_tilt(p, lo * h), h)
        f_hi = _hit(_tilt(p, hi * h), h)  # = cur
        # 二分
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            f_mid = _hit(_tilt(p, mid * h), h)
            if f_mid <= target:
                lo = mid  # 保持 f(lo) ≤ target
            else:
                hi = mid  # 保持 f(hi) ≥ target
        return _tilt(p, lo * h)  # lo 對應 ≤ target 的邊界

    else:  # side == "lower"
        # 目標：E[h] ≥ target。若已滿足，直接回傳。
        if cur >= target - tol:
            return p
        # 夾住區間 [lo, hi]，使 f(lo) ≤ target ≤ f(hi)
        lo, hi = 0.0, 1.0
        while _hit(_tilt(p, hi * h), h) < target and hi < 1e12:
            hi *= 2.0  # 更正，命中率會更高
        f_lo = _hit(_tilt(p, lo * h), h)  # = cur
        f_hi = _hit(_tilt(p, hi * h), h)
        # 二分
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            f_mid = _hit(_tilt(p, mid * h), h)
            if f_mid >= target:
                hi = mid  # 保持 f(hi) ≥ target
            else:
                lo = mid  # 保持 f(lo) ≤ target
        return _tilt(p, hi * h)  # hi 對應 ≥ target 的邊界

# ---------- Public API ----------

def affine_exponentiated_projection(
    p: np.ndarray,
    r: np.ndarray,
    rtp_band: tuple[float, float] | None,
    hit_band: tuple[float, float] | None,
    max_iter: int = 10,
    tol: float = 1e-8
) -> np.ndarray:
    """
    KL-minimal alternating projection with **RTP as hard constraint** and
    **Hit as soft (best-effort)**. We first enforce RTP into its band; then we
    try to enforce Hit. If enforcing Hit would violate RTP, we revert and stop.
    This matches cases where bands may be infeasible jointly.
    """
    p = normalize(p)
    r = np.asarray(r, dtype=float)
    h = (r > 0.0).astype(float)

    for _ in range(max_iter):
        # --- Step 1: enforce RTP (hard) ---
        rtp, hit, _ = kpis(p, r)
        if rtp_band is not None:
            low_rtp, high_rtp = rtp_band
            if rtp > high_rtp + tol:
                p = _project_rtp_kl(p, r, high_rtp, side="upper", tol=tol)
            elif rtp < low_rtp - tol:
                p = _project_rtp_kl(p, r, low_rtp, side="lower", tol=tol)

        rtp, hit, _ = kpis(p, r)
        ok_rtp = (rtp_band is None) or (rtp >= rtp_band[0] - tol and rtp <= rtp_band[1] + tol)

        # --- Step 2: try to enforce Hit (soft, do-not-break RTP) ---
        if hit_band is not None and ok_rtp:
            low_hit, high_hit = hit_band
            q = p
            if hit > high_hit + tol:
                q = _project_hit_kl(p, h, high_hit, side="upper", tol=tol)
            elif hit < low_hit - tol:
                q = _project_hit_kl(p, h, low_hit, side="lower", tol=tol)

            # accept only if RTP stays in band
            rtp_q, hit_q, _ = kpis(q, r)
            if rtp_band is None or (rtp_q >= rtp_band[0] - tol and rtp_q <= rtp_band[1] + tol):
                p = q
                rtp, hit = rtp_q, hit_q
            else:
                # cannot satisfy both; keep RTP-feasible p and stop
                return normalize(p)

        # stop if RTP satisfied (always hard), and Hit either satisfied or not requested
        ok_hit = (hit_band is None) or (hit >= hit_band[0] - tol and hit <= hit_band[1] + tol)
        if ok_rtp and ok_hit:
            return normalize(p)

    return normalize(p)

