from dataclasses import replace
import numpy as np
import pytest
import json
from pathlib import Path
from scripts.model3_island.types import Config

def config():
    return Config.from_dict(json.loads(Path("data/design/model3_ch2_bridge_20260927.json").read_text())["base_config"])
from scripts.audit_model3_joint_syndrome_vector import invasion_gradient
from scripts.model3_island.types import VisitorState
from scripts.model3_island.selection import syndrome_thresholds

@pytest.mark.parametrize('timing', ['delayed','prior'])
@pytest.mark.parametrize('empty', [False,True])
def test_joint_thresholds_match_independent_mutant_gradient(timing,empty):
    c=replace(config(), assurance_mode='evolving', assurance_timing=timing,
              assurance_cost=.4, pollen_discount=.7)
    optima=np.array([] if empty else [.2,.5,.8])
    v=VisitorState(np.arange(len(optima)),optima,np.full(len(optima),.18),np.ones(len(optima)))
    for a in [.2,.5,.8]:
        z=np.array([.5,.5,a])
        got=syndrome_thresholds(z,v,c)
        expected=invasion_gradient(z,v,c,trait_index=2,step=1e-5)
        assert got['assurance_gradient']==pytest.approx(expected,abs=2e-8)
        assert bool(c.assurance_cost<got['assurance_cost_threshold']) == bool(expected>0)
        assert bool(c.investment_cost>got['investment_cost_threshold']) == bool(got['investment_gradient']<0)
        for key,field,trait in [('assurance_cost_threshold','assurance_cost',2),('investment_cost_threshold','investment_cost',1)]:
            threshold=float(got[key])
            if threshold>=0:
                at=replace(c,**{field:threshold})
                assert invasion_gradient(z,v,at,trait_index=trait,step=1e-5)==pytest.approx(0,abs=2e-8)
