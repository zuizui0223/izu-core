import numpy as np
import pytest
from dataclasses import replace
from scripts.model3_compressed_step import weighted, summed, compressed_step
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.density import density_step
from scripts.run_model3_full_mutation import config,exposure
from scripts.audit_model3_unified_reduction import _visitors,_empty_state


def full(state):
    core,factors=state
    return np.einsum('abc,ia,jb,kc->ijk',core,*factors)


def initial():
    rng=np.random.default_rng(113)
    state=(rng.random((2,2,2)),[rng.random((6,2)) for _ in range(3)])
    state[0][:] *= 48/full(state).sum()
    return state


def test_exact_weight_and_sum():
    state=initial(); rng=np.random.default_rng(19)
    xy=rng.random((5,5)); a=rng.random(6); ix=np.array([0,1,2,2,3,4])
    result=weighted(state,xy,a,(ix,ix))
    expected=full(state)*xy[ix[:,None],ix[None,:]][:,:,None]*a
    np.testing.assert_allclose(full(result),expected,atol=1e-11,rtol=0)
    np.testing.assert_allclose(full(summed([state,result])),full(state)+expected,atol=1e-11,rtol=0)


@pytest.mark.parametrize('setting',['assurance_cost','prior_selfing'])
@pytest.mark.parametrize('scheme',['jump','heat_fv'])
@pytest.mark.parametrize('present',[False,True])
def test_complete_step_matches_original(setting,scheme,present):
    state=initial(); axes=([0,.5,1],)*3
    c=config(setting,.01); visitors=_visitors([.2,.8] if present else [])
    actual=compressed_step(state,axes,visitors,c,scheme=scheme)
    grid=make_tensor_grid(axes)
    expected,_=density_step(full(state).ravel(),grid,visitors,_empty_state(1),c,
        mutation_scheme=scheme,inheritance_backend='tensor')
    np.testing.assert_allclose(full(actual).ravel(),expected,atol=1e-9,rtol=0)


def test_weight_budget_rejected():
    with pytest.raises(MemoryError):
        weighted(initial(),np.ones((6,6)),np.ones(6),(np.arange(6),)*2,budget=1)


@pytest.mark.parametrize('scheme',['jump','heat_fv'])
@pytest.mark.parametrize('setting',['assurance_cost','prior_selfing'])
def test_repeated_steps_and_adult_survival(setting,scheme):
    axes=([0,.5,1],)*3; grid=make_tensor_grid(axes)
    c=replace(config(setting,.01),survival=.4)
    state=initial(); baseline=full(state).ravel()
    history=exposure(76001,'far')
    for t in range(12):
        state=compressed_step(state,axes,history.visitors[t],c,scheme=scheme)
        baseline,_=density_step(baseline,grid,history.visitors[t],_empty_state(1),c,
            mutation_scheme=scheme,inheritance_backend='tensor')
        np.testing.assert_allclose(full(state).ravel(),baseline,atol=1e-9,rtol=0)


def test_fixed_assurance_is_explicitly_outside_this_integration_scope():
    with pytest.raises(ValueError,match='evolving'):
        compressed_step(initial(),([0,.5,1],)*3,_visitors([]),
            replace(config('assurance_cost',.01),assurance_mode='fixed'))


def test_rounding_inside_full_step_matches_reference_and_records_error():
    from scripts.model3_core_rounding import rounded
    records=[]
    def reduce(state,stage):
        result,info=rounded(state)
        records.append((stage,info))
        return result
    state=initial();axes=([0,.5,1],)*3;c=config('prior_selfing',.01)
    visitors=_visitors([.2,.8]);grid=make_tensor_grid(axes)
    expected,_=density_step(full(state).ravel(),grid,visitors,_empty_state(1),c,
        inheritance_backend='tensor')
    result=compressed_step(state,axes,visitors,c,rounding=reduce)
    actual=full(result).ravel()
    assert records
    assert np.abs(actual-expected).sum()/48<1e-7
    assert -actual[actual<0].sum()/48<1e-10
