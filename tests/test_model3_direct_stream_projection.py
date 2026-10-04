import numpy as np
import pytest
from scripts.model3_direct_stream_projection import project_columns

def test_ill_conditioned_signed_matrix_retains_small_modes():
    rng=np.random.default_rng(128)
    u=np.linalg.qr(rng.normal(size=(40,5)))[0];v=np.linalg.qr(rng.normal(size=(200,5)))[0]
    a=(u*np.array([1.,1e-3,1e-6,1e-9,1e-12]))@v.T
    q,b,r=project_columns(lambda s,t:a[:,s:t],a.shape,absolute_frobenius=1e-13,budget=3000,block_columns=11)
    assert np.linalg.norm(a-q@b)<=1e-13
    assert abs(np.linalg.norm(a-q@b)-r['residual_frobenius'])<1e-15
    assert b.size<=3000

def test_nonzero_residual_and_repeatability():
    rng=np.random.default_rng(82);a=rng.normal(size=(30,2))@rng.normal(size=(2,80))+1e-7*rng.normal(size=(30,80))
    results=[project_columns(lambda s,t:a[:,s:t],a.shape,absolute_frobenius=1e-4,budget=3000,block_columns=7) for _ in range(2)]
    q,b,r=results[0];error=np.linalg.norm(a-q@b)
    assert 1e-8<error<=1e-4
    assert abs(error-r['residual_frobenius'])<1e-12
    np.testing.assert_array_equal(b,results[1][1])

def test_budget_rejection_before_read():
    def forbidden(*args):raise AssertionError('must not read')
    with pytest.raises(MemoryError):project_columns(forbidden,(100,500),absolute_frobenius=1e-9,budget=100)
