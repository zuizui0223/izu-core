from pathlib import Path
import importlib.util
import math
import pytest

P=Path(__file__).resolve().parents[1]/'scripts'/'audit_chapter2_clock_power_envelope_20261013.py'
spec=importlib.util.spec_from_file_location('clock_power_envelope',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

@pytest.mark.parametrize('sigma,expected',[(.05,512),(.10,512),(.15,512),(.20,896),(.25,None)])
def test_confirm_n_determined_by_sd_only(sigma,expected):
    r=m.plan_confirmation(sigma)
    assert r['independent_clusters']==expected
    assert r['pilot_effect_point_estimate_used'] is False
    if expected:
        assert r['confirm_trajectories']==expected*12
        assert r['clusters_per_founder']==expected//2
        assert r['decision']=='RUN_ONLY_AFTER_PROTOCOL_REVIEW'
    else:
        assert r['decision']=='NO_GO_PRECISION_EXCEEDS_CAP'


def test_power_higher_when_n_or_effect_larger_and_lower_when_sigma_larger():
    assert m.probability_success(.02,.15,1024)>m.probability_success(.02,.15,512)
    assert m.probability_success(.03,.15,512)>m.probability_success(.02,.15,512)
    assert m.probability_success(.02,.2,512)<m.probability_success(.02,.15,512)
    assert m.probability_success(.02,.15,512)>.8
    assert m.probability_success(.02,.2,512)<.8


def test_power_envelope_size_and_no_pseudoreplication():
    r=m.audit()
    assert r['status']=='DESIGN_ONLY_HYPOTHETICAL_NORMAL_POWER_NOT_EMPIRICAL'
    assert len(r['design_grid'])==3*5*6
    assert r['pilot']['clusters']==128 and r['pilot']['trajectories']==1536
    assert r['confirmation_selection_rule']['effect_used']==.02
    assert r['confirmation_selection_rule']['sigma_floor']==.15


def test_bad_inputs_rejected():
    for s in (0,-1,float('nan')):
        with pytest.raises(ValueError):m.plan_confirmation(s)
    for a,b,n in [(0,.1,256),(.1,0,256),(.1,.1,0)]:
        with pytest.raises(ValueError):m.probability_success(a,b,n)
