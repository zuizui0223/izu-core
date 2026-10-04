import numpy as np
import pytest
from scripts.model3_bounded_sum import bounded_sum

def dense(state):
 c,f=state
 return np.einsum('abc,ia,jb,kc->ijk',c,*f,optimize=True)

def test_shared_signed_subspace_sum_bound():
 rng=np.random.default_rng(123);q=[np.linalg.qr(rng.normal(size=(12,3)))[0] for _ in range(3)]
 states=[(rng.normal(size=(3,3,3)),q),(rng.normal(size=(3,3,3)),q)]
 actual,receipt=bounded_sum(states,absolute_l1=1e-7,budget=1000)
 expected=sum(dense(s) for s in states)
 assert np.abs(dense(actual)-expected).sum()<=receipt['absolute_l1_bound']+1e-11
 assert actual[0].size<=27

def test_small_direction_removed_with_bound():
 fs=[np.eye(5)[:,:2] for _ in range(3)]
 states=[(np.ones((1,1,1)),[f[:,:1] for f in fs]),(np.ones((1,1,1))*1e-14,[f[:,1:] for f in fs])]
 actual,receipt=bounded_sum(states,absolute_l1=1e-8,budget=1000)
 assert np.abs(dense(actual)-sum(dense(s) for s in states)).sum()<=receipt['absolute_l1_bound']+1e-12

def test_invalid_tolerance():
 with pytest.raises(ValueError):bounded_sum([],absolute_l1=-1,budget=1000)
