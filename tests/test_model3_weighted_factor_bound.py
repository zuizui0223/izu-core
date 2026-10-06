import numpy as np
import pytest
from scripts.model3_weighted_factor_bound import bounded_weighted

def dense(state):
    return np.einsum('abc,ia,jb,kc->ijk',state[0],*state[1],optimize=True)

def test_correlated_signed_basis_matches_dense_within_bound():
    rng=np.random.default_rng(821)
    factors=[np.linalg.qr(rng.normal(size=(7,3)))[0] for _ in range(3)]
    state=(rng.normal(size=(3,3,3)),factors)
    xy=np.exp(rng.normal(size=(7,7)));a=np.linspace(.2,1,7);maps=(np.arange(7),np.arange(7))
    actual,receipt=bounded_weighted(state,xy,a,maps,absolute_l1=1e-7,budget=100000)
    expected=dense(state)*xy[:,:,None]*a[None,None,:]
    assert np.abs(dense(actual)-expected).sum()<=receipt['absolute_l1_bound']+1e-10
    assert receipt['absolute_l1_bound']<=1e-7

def test_large_physical_axes_preserve_sparse_correlated_support():
    rng=np.random.default_rng(31);n=101
    f=np.zeros((n,3));f[[0,50,100]]=np.eye(3)
    state=(rng.random((3,3,3)),[f]*3)
    xy=np.exp(-((np.linspace(0,1,n)[:,None]-np.linspace(0,1,n))**2));a=np.ones(n)
    actual,receipt=bounded_weighted(state,xy,a,(np.arange(n),np.arange(n)),absolute_l1=1e-7,budget=50000)
    assert actual[0].shape==(3,3,3)
    assert np.abs(dense(actual)-dense(state)*xy[:,:,None]).sum()<=receipt['absolute_l1_bound']+1e-9

def test_resource_guard_precedes_raw_factor_allocation():
    with pytest.raises(MemoryError):
        bounded_weighted((np.ones((2,2,2)),[np.ones((10,2))]*3),np.ones((10,10)),np.ones(10),(np.arange(10),np.arange(10)),absolute_l1=1e-6,budget=50)


def test_nonzero_truncation_error_is_covered():
    rng=np.random.default_rng(42);f=rng.random((8,2));state=(rng.random((2,2,2)),[f]*3)
    xy=np.ones((8,8))+1e-9*rng.random((8,8));a=np.ones(8)
    result,receipt=bounded_weighted(state,xy,a,(np.arange(8),np.arange(8)),absolute_l1=1e-3,budget=10000)
    error=np.abs(dense(result)-dense(state)*xy[:,:,None]).sum()
    assert error>1e-10
    assert error<=receipt['absolute_l1_bound']+1e-10
    assert receipt['absolute_l1_bound']<=1e-3


def test_weight_compression_precedes_large_raw_factor():
    rng=np.random.default_rng(71);n=129
    f=np.zeros((n,3));f[[0,64,128]]=np.eye(3)
    state=(rng.random((3,3,3)),[f]*3)
    xy=np.ones((n,n))+1e-12*rng.random((n,n))
    result,receipt=bounded_weighted(state,xy,np.ones(n),(np.arange(n),np.arange(n)),absolute_l1=1e-6,budget=20000)
    assert receipt['weight_rank']==1
    assert receipt['weight_l1_bound']>0
    error=np.abs(dense(result)-dense(state)*xy[:,:,None]).sum()
    assert error<=receipt['absolute_l1_bound']+1e-10
    assert receipt['absolute_l1_bound']<=1e-6
