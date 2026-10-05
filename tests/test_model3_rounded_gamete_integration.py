import numpy as np
import pytest
from dataclasses import replace
from scripts.model3_rounded_gamete_integration import bounded_step
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


@pytest.mark.parametrize('scheme',['jump','heat_fv'])
def test_forced_streamed_child_matches_exact_outcross(scheme):
    from scripts.model3_rounded_gamete_child import streamed_outcross
    from scripts.model3_compressed_outcross import outcross_tucker
    rng=np.random.default_rng(519)
    donor=(rng.random((5,5,5)),[rng.random((6,5)) for _ in range(3)])
    recipient=(rng.random((5,5,5)),[rng.random((6,5)) for _ in range(3)])
    donor[0][:]*=48/full(donor).sum()
    recipient[0][:]/=full(recipient).sum()
    axes=([0,.5,1],)*3
    actual,receipt=streamed_outcross(donor,recipient,axes,.01,.05,scheme,relative_l1=1e-8,budget=10000,force_stream=True)
    expected=outcross_tucker(*donor,*recipient,axes,.01,.05,scheme)
    error=np.abs(full(actual)-full(expected)).sum()
    assert error<=receipt['absolute_l1_bound']+1e-9
    assert receipt['streamed']


def test_forced_sum_fallback_against_dense(monkeypatch):
    import scripts.model3_rounded_gamete_integration as model
    def blocked(*args,**kwargs):raise MemoryError('force bounded sum path')
    monkeypatch.setattr(model,'summed',blocked)
    rng=np.random.default_rng(781)
    state=(rng.random((2,2,2)),[rng.random((6,2)) for _ in range(3)])
    state[0][:]*=48/full(state).sum()
    axes=([0,.5,1],)*3;grid=make_tensor_grid(axes);cfg=config('assurance_cost',.01)
    visitors=exposure(76001,'near').visitors[0]
    expected,_=density_step(full(state),grid,visitors,_empty_state(1),cfg,mutation_scheme='jump',inheritance_backend='tensor')
    actual,receipts=model.bounded_step(state,axes,visitors,cfg)
    assert np.abs(full(actual)-expected).sum()/48<1e-6
    assert any(x['stage'].startswith('sum_projection:') for x in receipts)


def test_forced_streamed_sum_fallback(monkeypatch):
    import scripts.model3_rounded_gamete_integration as model
    def blocked(*args,**kwargs):raise MemoryError('force joint streamed sum path')
    monkeypatch.setattr(model,'bounded_sum',blocked)
    test_forced_sum_fallback_against_dense(monkeypatch)
