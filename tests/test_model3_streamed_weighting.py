import numpy as np
import pytest
from scripts.model3_streamed_weighting import bounded_weighted

def full(s):return np.einsum('abc,ia,jb,kc->ijk',s[0],*s[1],optimize=True)

def test_output_larger_than_budget_matches_correlated_signed_reference():
 rng=np.random.default_rng(552)
 core=np.einsum('ar,br,cr->abc',*[rng.normal(size=(6,2)) for _ in range(3)])
 state=(core,[rng.normal(size=(12,6)) for _ in range(3)])
 xy=rng.random((12,2))@rng.random((2,12));a=rng.random(12)
 actual,receipt=bounded_weighted(state,xy,a,(np.arange(12),)*2,absolute_l1=1e-5,budget=500)
 error=np.abs(full(actual)-full(state)*xy[:,:,None]*a[None,None,:]).sum()
 assert error<=receipt['absolute_l1_bound']+1e-9
 assert receipt['absolute_l1_bound']<=1e-5
 assert actual[0].size<=500
 assert receipt['streamed']


def test_uncompressible_output_is_rejected_without_relaxing_error():
 rng=np.random.default_rng(552)
 state=(rng.normal(size=(6,6,6)),[rng.normal(size=(12,6)) for _ in range(3)])
 xy=rng.random((12,2))@rng.random((2,12));a=rng.random(12)
 with pytest.raises(MemoryError):
  bounded_weighted(state,xy,a,(np.arange(12),)*2,absolute_l1=1e-5,budget=500)
