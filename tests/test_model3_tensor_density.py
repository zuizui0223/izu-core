from dataclasses import replace
import json
from pathlib import Path
import numpy as np
import pytest
from scripts.model3_island.density import make_grid,density_step
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.types import Config
from scripts.audit_model3_unified_reduction import _empty_state,_visitors

@pytest.mark.parametrize('scheme',['jump','heat','heat_fv'])
@pytest.mark.parametrize('timing',['prior','delayed'])
@pytest.mark.parametrize('rate',[0,.01])
def test_tensor_preserves_full_sexual_operator(scheme,timing,rate):
    c=Config.from_dict(json.loads(Path('data/design/model3_ch2_bridge_20260927.json').read_text())['base_config'])
    c=replace(c,assurance_mode='evolving',assurance_timing=timing,assurance_cost=.5,mutation_rate=rate,mutation_sd=.05)
    axes=([0,.5,1],)*3
    dense=make_grid(axes);sparse=make_tensor_grid(axes)
    np.testing.assert_array_equal(dense.genotypes,sparse.genotypes)
    r=np.random.default_rng(20104).dirichlet(np.ones(len(dense.genotypes)))*48
    v=_visitors([.2,.4,.6,.8])
    expected,_=density_step(r,dense,v,_empty_state(1),c,mutation_scheme=scheme)
    got,_=density_step(r,sparse,v,_empty_state(1),c,mutation_scheme=scheme,inheritance_backend='tensor')
    np.testing.assert_allclose(got,expected,atol=1e-10,rtol=0)
