import numpy as np
import pytest
from scripts.model3_compressed_outcross import outcross_tucker
from scripts.model3_island.tensor_density import make_tensor_grid,tensor_births
from scripts.model3_island.density import FactorizedMatrix
from scripts.run_model3_full_mutation import config


def full(core,factors):
    return np.einsum('abc,ia,jb,kc->ijk',core,*factors).ravel()


@pytest.mark.parametrize('rate',[0.,.01])
@pytest.mark.parametrize('scheme',['jump','heat_fv'])
@pytest.mark.parametrize('orthogonalize',[False,True])
def test_outcross_equals_original_joint_operator(rate,scheme,orthogonalize):
    axes = ([0,.5,1],[0,.2,.7,1],[0,1])
    grid = make_tensor_grid(axes)
    rng = np.random.default_rng(172)
    dc = rng.random((2,3,1)); rc = rng.random((1,2,2))
    df = [rng.random((len(a)*(len(a)+1)//2,r)) for a,r in zip(axes,dc.shape)]
    rf = [rng.random((len(a)*(len(a)+1)//2,r)) for a,r in zip(axes,rc.shape)]
    donor = full(dc,df); recipient = full(rc,rf)
    # Signed factors/cores are legitimate representations of positive densities.
    df[0][:,0] *= -1; dc[0,:,:] *= -1
    core,factors = outcross_tucker(dc,df,rc,rf,axes,rate,.05,scheme,orthogonalize=orthogonalize)
    got = full(core,factors)
    expected = tensor_births(grid,FactorizedMatrix(donor[:,None],recipient[:,None]),
        np.zeros_like(donor),config('assurance_cost',rate),(True,True,True),scheme)
    np.testing.assert_allclose(got,expected,atol=1e-11,rtol=0)
    assert got.sum() == pytest.approx(donor.sum()*recipient.sum(),abs=1e-10)


def test_output_budget_rejected_before_allocation():
    c = np.ones((2,2,2)); f = [np.ones((3,2))]*3
    with pytest.raises(MemoryError):
        outcross_tucker(c,f,c,f,([0,1],)*3,0,.05,max_output_values=1)


def test_opposite_homozygotes_make_heterozygote():
    c = np.ones((1,1,1))
    donor = [np.array([[1.],[0.],[0.]])]*3
    recipient = [np.array([[0.],[0.],[1.]])]*3
    core,factors = outcross_tucker(c,donor,c,recipient,([0,1],)*3,0,.05)
    expected = np.zeros((3,3,3)); expected[1,1,1]=1
    np.testing.assert_allclose(full(core,factors),expected.ravel(),atol=1e-14)


def test_qr_avoids_expanded_core_without_truncation():
    rng = np.random.default_rng(13)
    c = rng.random((4,4,4))*.01
    f = [rng.random((3,4)) for _ in range(3)]
    with pytest.raises(MemoryError):
        outcross_tucker(c,f,c,f,([0,1],)*3,0,.05,max_output_values=100)
    expected = full(*outcross_tucker(c,f,c,f,([0,1],)*3,0,.05))
    result = outcross_tucker(c,f,c,f,([0,1],)*3,0,.05,
        max_output_values=100,orthogonalize=True)
    assert result[0].shape == (3,3,3)
    np.testing.assert_allclose(full(*result),expected,atol=1e-11,rtol=0)


def test_qr_rejects_oversized_contraction_intermediate():
    c = np.ones((2,2,2)); f = [np.ones((3,2))]*3
    with pytest.raises(MemoryError,match='intermediate'):
        outcross_tucker(c,f,c,f,([0,1],)*3,0,.05,
            orthogonalize=True,max_intermediate_values=1)
