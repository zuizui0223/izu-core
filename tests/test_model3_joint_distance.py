import numpy as np
import pytest
from scripts.model3_joint_distance import joint_distance

def full(state):return np.einsum('abc,ia,jb,kc->ijk',state[0],*state[1],optimize=True)

def test_joint_distance_bounds_full_l1_for_correlated_signed_states():
    rng=np.random.default_rng(741)
    a=(rng.normal(size=(2,3,2)),[rng.normal(size=(7,k)) for k in [2,3,2]])
    b=(rng.normal(size=(3,2,3)),[rng.normal(size=(7,k)) for k in [3,2,3]])
    delta=full(a)-full(b);r=joint_distance(a,b,budget=10000)
    assert abs(r['frobenius']-np.linalg.norm(delta))<1e-11
    assert np.abs(delta).sum()<=r['l1_upper']+1e-10

def test_nearly_equal_states_keep_small_difference_without_squared_norm_subtraction():
    rng=np.random.default_rng(12);f=[np.linalg.qr(rng.normal(size=(20,3)))[0] for _ in range(3)]
    core=rng.normal(size=(3,3,3));changed=core.copy();changed[1,2,0]+=1e-10
    r=joint_distance((core,f),(changed,f),budget=10000)
    assert 9.99e-11<r['frobenius']<1.001e-10

def test_resource_cap_rejects_factor_concatenation():
    state=(np.ones((2,2,2)),[np.ones((100,2))]*3)
    with pytest.raises(MemoryError):joint_distance(state,state,budget=300)


def test_equal_locus_marginals_do_not_hide_joint_difference():
    a=np.ones((2,2,2));v=np.array([-1.,1.]);b=a+.2*np.einsum('i,j,k->ijk',v,v,v)
    for k in range(3):np.testing.assert_allclose(a.sum(axis=tuple(j for j in range(3) if j!=k)),b.sum(axis=tuple(j for j in range(3) if j!=k)))
    r=joint_distance((a,[np.eye(2)]*3),(b,[np.eye(2)]*3))
    assert abs(r['frobenius']-.2*np.sqrt(8))<1e-12
    assert r['l1_upper']>=np.abs(a-b).sum()-1e-12
