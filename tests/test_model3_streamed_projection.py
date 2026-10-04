import numpy as np
import pytest
from scripts.model3_streamed_projection import project_columns

def test_signed_correlated_low_rank_matrix_without_full_read():
    rng=np.random.default_rng(51);a=rng.normal(size=(40,3))@rng.normal(size=(3,200))
    calls=[]
    def block(start,stop):
        calls.append(stop-start);return a[:,start:stop]
    q,b,receipt=project_columns(block,a.shape,absolute_frobenius=1e-9,budget=3000,block_columns=11)
    assert max(calls)<=11
    assert b.size<=3000
    assert np.linalg.norm(a-q@b)<=receipt['residual_frobenius']+1e-12
    assert receipt['residual_frobenius']<=1e-9

def test_nonzero_residual_is_directly_measured():
    rng=np.random.default_rng(2);a=rng.normal(size=(30,2))@rng.normal(size=(2,80))+1e-7*rng.normal(size=(30,80))
    q,b,r=project_columns(lambda s,t:a[:,s:t],a.shape,absolute_frobenius=1e-4,budget=3000,block_columns=7)
    error=np.linalg.norm(a-q@b)
    assert error>1e-8
    assert abs(error-r['residual_frobenius'])<1e-12
    assert error<1e-4

def test_gram_budget_fails_before_reading():
    def forbidden(*args):raise AssertionError('must not read')
    with pytest.raises(MemoryError):project_columns(forbidden,(100,500),absolute_frobenius=1e-9,budget=1000)

def test_incompressible_output_fails_instead_of_relaxing_tolerance():
    a=np.random.default_rng(61).normal(size=(20,100))
    with pytest.raises(MemoryError):project_columns(lambda s,t:a[:,s:t],(20,100),absolute_frobenius=1e-9,budget=600)
