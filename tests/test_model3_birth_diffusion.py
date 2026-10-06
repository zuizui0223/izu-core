from dataclasses import replace
import json
from pathlib import Path
import numpy as np
import pytest
from scripts.model3_island.density import mutation_matrix, birth_mutation_matrix, make_grid, density_step
from scripts.model3_island.types import Config
from scripts.model3_island.population import inherit
from scripts.audit_model3_unified_reduction import _founders, _visitors, _empty_state


def cfg():
    return Config.from_dict(json.loads(Path('data/design/model3_ch2_bridge_20260927.json').read_text())['base_config'])


def test_heat_kernel_is_positive_conservative_and_has_correct_end_cases():
    nodes=np.linspace(0,1,21)
    for u in [0,.01,1]:
        heat=birth_mutation_matrix(nodes,u,.05,'heat')
        assert np.min(heat)>=0
        np.testing.assert_allclose(heat.sum(axis=1),1,atol=1e-12)
        if u in [0,1]:
            np.testing.assert_allclose(heat,mutation_matrix(nodes,u,.05),atol=1e-12)
    with pytest.raises(ValueError):
        birth_mutation_matrix(nodes,.1,.05,'invalid')


def test_selected_locus_mutation_preserves_other_alleles_and_default_draws():
    c=replace(cfg(),mutation_rate=1,mutation_sd=.1)
    state=_founders(.5,[[.4,.4],[.4,.6],[.6,.6]])
    parents=np.arange(48)
    def run(mask=None):
        kw={} if mask is None else {'mutation_traits':mask}
        return inherit(state,parents,parents,c,segregation_rng=np.random.default_rng(9),mutation_rng=np.random.default_rng(10),year=1,**kw)
    np.testing.assert_array_equal(run().alleles,run((True,True,True)).alleles)
    limited=run((False,True,False))
    assert np.all(limited.alleles[:,[0,2],:]==.5)
    np.testing.assert_array_equal(limited.alleles[:,1],run().alleles[:,1])


def test_density_mutation_mask_permits_fixed_singleton_axes():
    from scripts.model3_island.density import project_state
    c=replace(cfg(),mutation_rate=.01,mutation_sd=.05)
    grid=make_grid(([.5],np.linspace(0,1,11),[.5]))
    _,counts=project_state(_founders(.5,[[.4,.4],[.4,.6],[.6,.6]]),grid)
    for scheme in ['jump','heat']:
        result,_=density_step(counts,grid,_visitors([.35,.45,.55,.65]),_empty_state(1),c,mutation_traits=(False,True,False),mutation_scheme=scheme)
        assert np.isfinite(result).all() and (result>=0).all()
        assert result.sum()<=c.capacity+1e-9
