import numpy as np
import pytest
from scripts.model3_core_rounding import rounded


def full(state):
    c,f=state
    return np.einsum('abc,ia,jb,kc->ijk',c,*f)


def test_rank_reduction_bound_and_mass():
    rng=np.random.default_rng(701)
    factors=[rng.random((9,3)) for _ in range(3)]
    core=np.zeros((3,3,3));core[0,0,0]=1;core[1,1,1]=1e-12;core[2,2,2]=2e-12
    source=(core,factors)
    target,receipt=rounded(source,relative_l1=1e-7)
    before=full(source);after=full(target)
    assert np.abs(before-after).sum() <= receipt['absolute_l1_bound']+1e-11
    assert after.sum()==pytest.approx(before.sum(),abs=1e-11)
    assert target[0].size<core.size
    assert receipt['absolute_l1_bound']<=1e-7*before.sum()


def test_correlated_signed_basis_is_preserved():
    rng=np.random.default_rng(718)
    factors=[rng.random((7,3)) for _ in range(3)]
    core=rng.random((3,3,3))
    factors[0][:,0]*=-1;core[0,:,:]*=-1
    source=(core,factors);target,receipt=rounded(source)
    np.testing.assert_allclose(full(target),full(source),atol=1e-10,rtol=0)
    assert receipt['absolute_l1_bound']<=1e-8*full(source).sum()


def test_exact_zero():
    source=(np.zeros((2,2,2)),[np.ones((5,2))]*3)
    target,receipt=rounded(source)
    assert np.count_nonzero(full(target))==0
    assert receipt['absolute_l1_bound']==0


@pytest.mark.parametrize('epsilon',[0,-1,np.nan,1])
def test_bad_tolerance(epsilon):
    with pytest.raises(ValueError):
        rounded((np.ones((1,1,1)),[np.ones((2,1))]*3),relative_l1=epsilon)
