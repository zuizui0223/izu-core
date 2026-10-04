from dataclasses import replace
import numpy as np
import pytest
from scripts.model3_compressed_ecology import ecological_weights
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.density import density_step
from scripts.run_model3_full_mutation import config
from scripts.audit_model3_unified_reduction import _visitors,_empty_state


@pytest.mark.parametrize('setting',['assurance_cost','prior_selfing'])
@pytest.mark.parametrize('present',[False,True])
@pytest.mark.parametrize('mode',['fixed','evolving'])
def test_separated_ecological_weights_match_full_ledger(setting,present,mode):
    axes = ([0,.5,1],)*3
    grid = make_tensor_grid(axes)
    rng = np.random.default_rng(98)
    factors = [rng.random((6,2)) for _ in range(3)]
    core = rng.random((2,2,2))
    counts = np.einsum('abc,ia,jb,kc->ijk',core,*factors)
    core *= 48/counts.sum(); counts *= 48/counts.sum()
    c = replace(config(setting,.01),assurance_mode=mode,activity_mode='count_scaled')
    visitors = _visitors([.2,.8] if present else [])
    weights = ecological_weights(core,factors,axes,visitors,c)
    _,ledger = density_step(counts.ravel(),grid,visitors,_empty_state(1),c,inheritance_backend='tensor')
    i,j = weights['maps']
    def expand(name):
        xy=weights[name+'_xy'][i[:,None],j[None,:]]
        a=weights[name+'_a']
        if xy.ndim==3:
            return (counts[:,:,:,None]*xy[:,:,None,:]*a[None,None,:,None]).reshape(counts.size,-1)
        return (counts*xy[:,:,None]*a[None,None,:]).ravel()
    donor=expand('donor') if present else np.zeros((counts.size,0))
    recipient=expand('recipient') if present else np.zeros((counts.size,0))
    np.testing.assert_allclose(donor,ledger.outcross.donors,atol=1e-10,rtol=0)
    np.testing.assert_allclose(recipient,ledger.outcross.recipients,atol=1e-10,rtol=0)
    np.testing.assert_allclose(expand('self'),ledger.self_viable,atol=1e-10,rtol=0)
    assert weights['self_xy'].shape==(5,5)  # identical pair means grouped exactly
