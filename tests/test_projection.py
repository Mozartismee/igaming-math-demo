import numpy as np
from igsimplex.core import affine_exponentiated_projection, kpis, normalize

def test_projection_hits_bands():
    r = np.array([0,1,2,10], float)
    p = normalize(np.array([0.75,0.2,0.04,0.01], float))
    p2 = affine_exponentiated_projection(p, r, rtp_band=(0.05,0.15), hit_band=(0.10,0.40))
    rtp, hit, _ = kpis(p2, r)
    assert 0.05 <= rtp <= 0.15
    assert 0.10 <= hit <= 0.40
