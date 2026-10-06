import numpy as np
import pytest
from scripts.model3_checked_gamete_factors import reduce_gamete_factors

def test_square_modes_skip_svd_and_keep_full_child_map(monkeypatch):
    rng=np.random.default_rng(38);n=5
    d=[np.linalg.qr(rng.normal(size=(n,n)))[0] for _ in range(3)]
    r=[np.linalg.qr(rng.normal(size=(n,n)))[0] for _ in range(3)]
    def forbidden(*a,**k):raise AssertionError('unnecessary SVD')
    monkeypatch.setattr(np.linalg,'svd',forbidden)
    q,t,info=reduce_gamete_factors(np.ones((n,n,n)),np.ones((n,n,n)),d,r,absolute_l1=1e-8,max_values=10000)
    from itertools import combinations_with_replacement
    pairs=np.array(list(combinations_with_replacement(range(n),2)));a,b=pairs.T
    for k in range(3):
        f=(d[k][a,:,None]*r[k][b,None,:]+(a!=b)[:,None,None]*d[k][b,:,None]*r[k][a,None,:]).reshape(len(pairs),-1)
        np.testing.assert_allclose(q[k]@t[k],f,atol=1e-14)
    assert info['exact_square_modes']==[0,1,2]
    assert info['absolute_l1_bound']==0.

def test_rectangular_modes_and_square_modes_reconstruct():
    rng=np.random.default_rng(80);n=5
    d=[np.linalg.qr(rng.normal(size=(n,w)))[0] for w in [5,3,2]]
    r=[np.linalg.qr(rng.normal(size=(n,w)))[0] for w in [5,2,3]]
    q,t,info=reduce_gamete_factors(rng.normal(size=(5,3,2)),rng.normal(size=(5,2,3)),d,r,absolute_l1=1e-12,max_values=10000)
    assert info['exact_square_modes']==[0]
    from itertools import combinations_with_replacement
    pairs=np.array(list(combinations_with_replacement(range(n),2)));a,b=pairs.T
    for k in range(3):
        f=(d[k][a,:,None]*r[k][b,None,:]+(a!=b)[:,None,None]*d[k][b,:,None]*r[k][a,None,:]).reshape(len(pairs),-1)
        np.testing.assert_allclose(q[k]@t[k],f,atol=2e-14)

def test_rejects_nonorthogonal_gamete_basis():
    fs=[np.eye(3) for _ in range(3)];fs[0]=fs[0]*2
    with pytest.raises(ValueError,match='orthonormal'):
        reduce_gamete_factors(np.ones((3,3,3)),np.ones((3,3,3)),fs,[np.eye(3)]*3,absolute_l1=1e-8)
