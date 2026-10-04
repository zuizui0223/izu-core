import json
from dataclasses import replace
from pathlib import Path
import numpy as np
import pytest
from scripts.model3_island.types import Config, VisitorState
from scripts.model3_island.selection import investment_invasion_terms
from scripts.audit_model3_joint_syndrome_vector import invasion_gradient

def config():
    return Config.from_dict(json.loads(Path("data/design/model3_ch2_bridge_20260927.json").read_text())["base_config"])

@pytest.mark.parametrize("timing,discount,cost", [("delayed",0,0),("prior",0,0),("delayed",1,0),("delayed",0,.5)])
@pytest.mark.parametrize("optima", [[],[.35,.45,.55,.65],[.1,.9]])
def test_investment_gradient_holds_residents_fixed(timing,discount,cost,optima):
    c=replace(config(),activity=.4,activity_mode="fixed",investment_cost=.5,assurance_mode="evolving",assurance_timing=timing,pollen_discount=discount,assurance_cost=cost,depression=.5)
    v=VisitorState(np.arange(len(optima)),np.array(optima),np.full(len(optima),.18),np.ones(len(optima)))
    for i in [.3,.5,.7]:
        r=np.array([.2,i,.5])
        got=investment_invasion_terms(r,v,c)
        expected=invasion_gradient(r,v,c,trait_index=1,step=1e-5)
        assert got["gradient"] == pytest.approx(expected,abs=2e-8)
        assert got["gradient"] == pytest.approx(got["benefit"]-got["cost"],abs=1e-12)

def test_population_derivative_is_not_invasion_selection():
    from scripts.audit_model3_analytic_syndrome_threshold import monomorphic_terms
    c=replace(config(),activity=.4,activity_mode="fixed",investment_cost=.5,pollen_discount=0,assurance_cost=0,depression=.5)
    v=VisitorState(np.arange(4),np.array([.35,.45,.55,.65]),np.full(4,.18),np.ones(4))
    assert monomorphic_terms(access=.2,visitor_optima=v.optima)["log_fitness_gradient"]>0
    assert investment_invasion_terms(np.array([.2,.5,.5]),v,c)["gradient"]==pytest.approx(-.1522648263,abs=1e-8)

def test_invasion_gradient_matches_density_low_frequency_limit():
    from scripts.model3_island.density import make_grid,density_step
    from scripts.model3_island.types import PlantState
    c=replace(config(),activity=.4,activity_mode="fixed",investment_cost=.5,assurance_mode="evolving",pollen_discount=0,assurance_cost=0,depression=.5)
    v=VisitorState(np.arange(4),np.array([.35,.45,.55,.65]),np.full(4,.18),np.ones(4))
    empty=PlantState(np.empty((0,3,2)),np.empty((0,3,2),dtype=np.int64),np.empty((0,3,2),dtype=bool),np.empty(0,dtype=np.int64),np.empty(0,dtype=np.int64))
    logs=[]
    h=1e-5
    for delta in [-h,h]:
        g=make_grid(([.2],sorted([.5,.5+delta]),[.5]))
        means=g.genotypes.mean(axis=2)
        ri=np.where(np.all(np.isclose(means,[.2,.5,.5],rtol=0,atol=1e-12),axis=1))[0][0]
        mi=np.where(np.all(np.isclose(means,[.2,.5+delta,.5],rtol=0,atol=1e-12),axis=1))[0][0]
        n=np.zeros(len(means));n[ri]=c.capacity*(1-1e-8);n[mi]=c.capacity*1e-8
        _,ledger=density_step(n,g,v,empty,c)
        w=.5*(ledger.maternal-ledger.self_viable)+.5*ledger.outcross.sum(axis=1)+ledger.self_viable
        logs.append(np.log(w[mi]/n[mi]))
    got=investment_invasion_terms([.2,.5,.5],v,c)["gradient"]
    assert got==pytest.approx((logs[1]-logs[0])/(2*h),abs=1e-7)

def test_batched_count_scaled_gradient_matches_scalar_invasion():
    c=replace(config(),assurance_mode="evolving",activity_mode="count_scaled",
              assurance_timing="prior",pollen_discount=.7,assurance_cost=.4)
    v=VisitorState(np.arange(3),np.array([.12,.48,.91]),np.array([.13,.19,.27]),np.array([.4,.8,1.]))
    states=np.random.default_rng(1904).uniform(.1,.9,size=(17,3))
    got=investment_invasion_terms(states,v,c)["gradient"]
    expected=[invasion_gradient(z,v,c,trait_index=1,step=1e-5) for z in states]
    np.testing.assert_allclose(got,expected,atol=2e-8,rtol=0)
