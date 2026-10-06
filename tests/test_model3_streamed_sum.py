import numpy as np
from scripts.model3_streamed_sum import streamed_sum

def dense(state):return np.einsum('abc,ia,jb,kc->ijk',state[0],*state[1],optimize=True)

def test_joint_sum_projected_before_full_allocation():
 rng=np.random.default_rng(941);fs=[np.linalg.qr(rng.normal(size=(16,4)))[0] for _ in range(3)]
 states=[(rng.normal(size=(4,4,4)),fs),(rng.normal(size=(4,4,4)),fs)]
 result,receipt=streamed_sum(states,absolute_l1=1e-7,budget=400,initial_rank=4)
 assert np.abs(dense(result)-sum(dense(s) for s in states)).sum()<=receipt['absolute_l1_bound']+1e-11
 assert result[0].size<=400
