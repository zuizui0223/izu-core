import numpy as np
import pytest
from dataclasses import replace
from scripts.model3_bounded_integration import bounded_step
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.density import density_step
from scripts.run_model3_full_mutation import config,exposure
from scripts.audit_model3_unified_reduction import _visitors,_empty_state

def full(state):return np.einsum('abc,ia,jb,kc->ijk',state[0],*state[1],optimize=True).ravel()

@pytest.mark.parametrize('setting',['assurance_cost','prior_selfing'])
@pytest.mark.parametrize('scheme',['jump','heat_fv'])
@pytest.mark.parametrize('survival',[0.,.4])
def test_integrated_bounded_reproduction_against_dense(setting,scheme,survival):
    rng=np.random.default_rng(13);state=(rng.random((2,2,2)),[rng.random((6,2)) for _ in range(3)])
    state[0][:]*=48/full(state).sum();axes=([0,.5,1],)*3;grid=make_tensor_grid(axes)
    cfg=replace(config(setting,.01),survival=survival);baseline=full(state)
    history=exposure(76001,'far')
    for t in range(12):
        visitors=history.visitors[t] if t<9 else _visitors([])
        state,receipts=bounded_step(state,axes,visitors,cfg,scheme=scheme)
        baseline,_=density_step(baseline,grid,visitors,_empty_state(1),cfg,mutation_scheme=scheme,inheritance_backend='tensor')
        actual=full(state)
        assert np.abs(actual-baseline).sum()/48<1e-6
        assert -actual[actual<0].sum()/48<1e-10
        assert any(x['stage'].startswith('weight:') for x in receipts)
        assert all(x['absolute_l1_bound']>=0 for x in receipts)
