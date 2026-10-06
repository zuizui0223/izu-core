import numpy as np
import pytest
from scripts.model3_child_factor_bound import reduce_child_factors


def result(dc,rc,fs):
    transforms=[f.reshape(f.shape[0],dc.shape[k],rc.shape[k]) for k,f in enumerate(fs)]
    return np.einsum('abc,def,iad,jbe,kcf->ijk',dc,rc,*transforms,optimize=True)


@pytest.mark.parametrize('signed',[False,True])
def test_spectral_bound_controls_actual_child_error(signed):
    rng=np.random.default_rng(53);dc=rng.random((2,2,2));rc=rng.random((2,2,2))
    fs=[np.outer(rng.random(12),rng.random(4))+1e-12*rng.random((12,4)) for _ in range(3)]
    if signed:dc[0]*=-1;fs[0][:,:2]*=-1
    q,r,receipt=reduce_child_factors(dc,rc,fs,absolute_l1=1e-6)
    expected=result(dc,rc,fs);actual=result(dc,rc,[a@b for a,b in zip(q,r)])
    assert np.abs(expected-actual).sum()<=receipt['absolute_l1_bound']+1e-10
    assert receipt['absolute_l1_bound']<=1e-6
    assert receipt['ranks']==[1,1,1]


def test_zero_operator():
    core=np.ones((2,2,2));fs=[np.ones((5,4))]*2+[np.zeros((5,4))]
    q,r,receipt=reduce_child_factors(core,core,fs,absolute_l1=1e-8)
    assert np.count_nonzero(result(core,core,[a@b for a,b in zip(q,r)]))==0
    assert receipt['absolute_l1_bound']==0


def test_tight_bound_keeps_necessary_directions():
    core=np.ones((2,2,2));fs=[np.eye(4)]*3
    q,r,receipt=reduce_child_factors(core,core,fs,absolute_l1=1e-12)
    assert receipt['ranks']==[4,4,4]


@pytest.mark.parametrize('budget',[0,-1,np.nan])
def test_invalid_error_budget(budget):
    with pytest.raises(ValueError):
        reduce_child_factors(np.ones((1,1,1)),np.ones((1,1,1)),[np.ones((2,1))]*3,absolute_l1=budget)


def test_factor_dimension_mismatch():
    with pytest.raises(ValueError,match='shape'):
        reduce_child_factors(np.ones((2,2,2)),np.ones((2,2,2)),[np.ones((3,3))]*3,absolute_l1=1e-8)


def test_input_resource_limit():
    with pytest.raises(MemoryError):
        reduce_child_factors(np.ones((2,2,2)),np.ones((2,2,2)),[np.ones((3,4))]*3,absolute_l1=1e-8,max_values=1)
