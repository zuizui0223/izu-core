"""Small closed-form matrix tests; not biological replication."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest

MODULE = Path(__file__).resolve().parents[1] / 'scripts/audit_pr471_fixation_lifetime_20261012.py'


def tool():
    assert MODULE.exists(), 'first-passage lifetime accounting is not implemented'
    spec = importlib.util.spec_from_file_location('fixation_lifetime', MODULE)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def fixture():
    states = np.array([[0,0,0],[1,0,0],[0,0,1],[0,1,0]], dtype=int)
    T = np.array([[1,0,0,0],[.2,.8,0,0],[.4,0,.6,0],[.1,.3,.2,.4]])
    p0 = np.array([0.,0.,0.,1.])
    return T, states, p0


def test_two_updates_by_hand():
    m=tool(); T,s,p=fixture(); a=m.analyze_kernel(T,s,p,2)
    r=a['summary']
    assert r['restricted_mean_time_to_extinction'] == pytest.approx(1.9)
    assert r['expected_occupied_censuses_1_to_H'] == pytest.approx(1.62)
    assert r['P_H_occupied'] == pytest.approx(.72)
    assert r['P_low_fixed_ever_by_H'] == pytest.approx(.42)
    assert r['P_high_fixed_ever_by_H'] == pytest.approx(.28)
    assert r['P_H_low_fixed_alive'] == pytest.approx(.36)
    assert r['P_H_high_fixed_alive'] == pytest.approx(.2)
    assert r['P_extinct_after_low_fixation_by_H'] == pytest.approx(.06)
    assert r['P_extinct_after_high_fixation_by_H'] == pytest.approx(.08)
    assert r['P_extinct_before_fixation_by_H'] == pytest.approx(.14)
    assert r['P_H_segregating_alive'] == pytest.approx(.16)
    assert r['P_H_occupied_given_low_fixation_by_H'] == pytest.approx(6/7)
    assert r['mean_low_fixation_update_given_fixed_by_H'] == pytest.approx(9/7)
    assert a['verification']['max_error'] < 1e-12


def test_first_entry_not_every_fixed_visit():
    m=tool(); T,s,p=fixture(); T[1]=[0,1,0,0]; T[2]=[0,0,1,0]
    a=m.analyze_kernel(T,s,p,8)
    assert a['summary']['P_low_fixed_ever_by_H'] == pytest.approx(.3*(1-.4**8)/.6)
    assert a['summary']['P_extinct_after_low_fixation_by_H'] == 0
    assert sum(x['low_first_entry'] for x in a['timeseries']) == pytest.approx(a['summary']['P_low_fixed_ever_by_H'])


def test_initial_fixation_counts_once_at_zero():
    m=tool(); T,s,p=fixture(); p=np.array([0.,1.,0.,0.]); a=m.analyze_kernel(T,s,p,3)
    assert a['summary']['P_low_fixed_ever_by_H'] == 1
    assert a['timeseries'][0]['low_first_entry'] == 1
    assert a['summary']['P_H_low_fixed_alive'] == pytest.approx(.8**3)
    assert a['summary']['P_extinct_after_low_fixation_by_H'] == pytest.approx(1-.8**3)
    assert a['summary']['P_H_occupied_given_high_fixation_by_H'] is None


def test_immediate_extinction_missing_conditionals_not_zero():
    m=tool(); T,s,p=fixture(); T[3]=[1,0,0,0]; a=m.analyze_kernel(T,s,p,5)
    assert a['summary']['restricted_mean_time_to_extinction']==1
    assert a['summary']['P_H_occupied']==0
    assert a['summary']['P_extinct_before_fixation_by_H']==1
    assert a['summary']['P_H_occupied_given_low_fixation_by_H'] is None
    assert a['summary']['mean_low_fixation_update_given_fixed_by_H'] is None


@pytest.mark.parametrize('mode',['nonfinite','negative','mass','unabsorbed','fixed_to_seg','bad_states','bad_initial','bad_horizon'])
def test_bad_inputs_rejected(mode):
    m=tool(); T,s,p=fixture(); h=2
    if mode=='nonfinite': T[3,0]=np.nan
    elif mode=='negative': T[3,0]=-.1;T[3,3]=.6
    elif mode=='mass': T[3,3]=.8
    elif mode=='unabsorbed': T[0]=[.9,0,0,.1]
    elif mode=='fixed_to_seg': T[1]=[.2,.7,0,.1]
    elif mode=='bad_states': s[3]=s[2]
    elif mode=='bad_initial': p=np.array([1.,0.,0.,0.])
    elif mode=='bad_horizon': h=True
    with pytest.raises(ValueError): m.analyze_kernel(T,s,p,h)


def test_no_change_between_identical_policies():
    m=tool(); T,s,p=fixture(); a=m.analyze_kernel(T,s,p,5)
    b=m.analyze_kernel(T.copy(),s,p,5)
    assert a['summary']==b['summary']
