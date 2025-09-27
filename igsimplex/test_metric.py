import numpy as np
from igsimplex.core import kpis, normalize

def test_kpis_basic():
    r = np.array([0,1,2,10], float)
    p = normalize(np.array([0.7,0.2,0.09,0.01], float))
    rtp, hit, var = kpis(p, r)
    assert 0.0 <= hit <= 1.0
    assert abs(p.sum() - 1.0) < 1e-12
    assert var >= 0.0
