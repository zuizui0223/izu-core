import numpy as np
import pytest
from dataclasses import replace
from scripts.model3_birth_marginal_reference import exact_next_marginals
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.density import density_step
from scripts.run_model3_full_mutation import config
from scripts.audit_model3_unified_reduction import _visitors,_empty_state

@pytest.mark.parametrize('setting',['assurance_cost','prior_selfing'])
@pytest.mark.parametrize('scheme',['jump','heat_fv'])
@pytest.mark.parametrize('present',[False,True])
def test_exact_marginal_reference_matches_full_joint_births(setting,scheme,present):
    rng=np.random.default_rng(332);counts=rng.random((6,6,6));counts*=48/counts.sum()
    state=(counts,[np.eye(6)]*3);axes=([0,.5,1],)*3
    cfg=replace(config(setting,.01),survival=.35);visitors=_visitors([.2,.8] if present else [])
    expected,_=density_step(counts.ravel(),make_tensor_grid(axes),visitors,_empty_state(1),cfg,mutation_scheme=scheme,inheritance_backend='tensor')
    actual=exact_next_marginals(state,axes,visitors,cfg,scheme=scheme)
    expected=expected.reshape(6,6,6)
    for k in range(3):np.testing.assert_allclose(actual[k],expected.sum(axis=tuple(i for i in range(3) if i!=k)),atol=1e-11,rtol=0)
