import numpy as np
import pytest
from scripts.model3_compressed_selfing import local_selfing, selfed_factors
from scripts.model3_island.tensor_density import make_tensor_grid, tensor_births
from scripts.model3_island.density import FactorizedMatrix
from scripts.run_model3_full_mutation import config


def reconstruct(core, factors):
    return np.einsum('abc,ia,jb,kc->ijk',core,*factors)


@pytest.mark.parametrize('rate',[0.,.01])
@pytest.mark.parametrize('scheme',['jump','heat_fv'])
def test_exact_joint_selfing_against_frozen_birth_operator(rate,scheme):
    axes = ([0,.5,1],[0,.2,.7,1],[0,1])
    grid = make_tensor_grid(axes)
    rng = np.random.default_rng(481)
    factors = [rng.random((len(a)*(len(a)+1)//2,2)) for a in axes]
    # Two correlated joint components, not a product of three marginals.
    core = np.zeros((2,2,2)); core[0,0,0]=1.2;core[1,1,1]=.7
    weights = reconstruct(core,factors).ravel()
    transitions = [local_selfing(a,rate,.05,scheme) for a in axes]
    transformed = selfed_factors(factors,transitions)
    got = reconstruct(core,transformed).ravel()
    no_outcross = FactorizedMatrix(np.zeros((weights.size,0)),np.zeros((weights.size,0)))
    expected = tensor_births(grid,no_outcross,weights,config('assurance_cost',rate),(True,True,True),scheme)
    np.testing.assert_allclose(got,expected,atol=1e-11,rtol=0)
    assert got.sum() == pytest.approx(weights.sum(),abs=1e-11)
    assert all(a.shape==b.shape for a,b in zip(factors,transformed))
    # A signed basis change must not change the represented biology.
    factors[0][:,0] *= -1; core[0,:,:] *= -1
    signed = reconstruct(core,selfed_factors(factors,transitions)).ravel()
    np.testing.assert_allclose(signed,expected,atol=1e-11,rtol=0)


def test_mendelian_heterozygote_without_mutation():
    np.testing.assert_allclose(local_selfing([0,1],0,.05,'jump'),
        [[1,0,0],[.25,.5,.25],[0,0,1]],atol=1e-14)


def test_rejects_nonstochastic_transition():
    with pytest.raises(ValueError):
        selfed_factors([np.ones((2,1))]*3,[np.eye(2)*2]*3)


def test_rejects_missing_trait():
    with pytest.raises(ValueError):
        selfed_factors([np.ones((2,1))]*2,[np.eye(2)]*2)
