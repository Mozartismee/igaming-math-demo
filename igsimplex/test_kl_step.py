import numpy as np
from igsimplex.opt import variance_grad, kl_bounded_step
from igsimplex.core import normalize, kl

def test_kl_bound_respected():
    r = np.array([0,1,2,10], float)
    p = normalize(np.array([0.7,0.2,0.09,0.01], float))
    g = variance_grad(p, r)
    p2, eta = kl_bounded_step(p, g, max_kl=1e-4)
    assert kl(p2, p) <= 1.0001e-4  # small numerical slack
    assert eta > 0.0
