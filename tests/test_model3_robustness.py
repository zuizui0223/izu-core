import numpy as np
import pytest

from scripts.model3_evolution import simulate
from scripts.model3_robustness import simulate_scenario


@pytest.mark.parametrize('control',['selected','neutral','fixed'])
@pytest.mark.parametrize('survival',[0.,.75])
@pytest.mark.parametrize('island_community',[False,True])
def test_default_scenario_exactly_replays_frozen_model(control,survival,island_community):
    kwargs=dict(seed=47,years=6,selfing=.5,control=control,survival=survival,island_community=island_community)
    reference=simulate(**kwargs)
    scenario=simulate_scenario(**kwargs)
    for key,value in reference.items():
        np.testing.assert_array_equal(scenario[key],value,err_msg=key)


def test_depression_changes_actual_recruitment_and_extinction():
    common=dict(seed=47,years=3,activity=0,selfing=1,survival=0)
    rescued=simulate_scenario(**common,depression=0)
    failed=simulate_scenario(**common,depression=1)
    assert rescued['population'][-1]>0
    assert failed['extinction_year']==1
    assert failed['expected_selfed'][0]==0
    assert failed['selfed_raw'][0]>0
    assert failed['viable_seed_limitation'][0]==1


def test_no_selfing_removes_all_depression_effects():
    a=simulate_scenario(seed=47,years=4,selfing=0,depression=0)
    b=simulate_scenario(seed=47,years=4,selfing=0,depression=1)
    for key in a:
        np.testing.assert_array_equal(a[key],b[key],err_msg=key)


def test_resource_matched_pollen_counterfactual_is_recorded_before_recruitment():
    result=simulate_scenario(seed=47,years=3,activity=0,selfing=.5,depression=.9)
    alive=result['population'][:-1]>0
    np.testing.assert_allclose(result['pollen_limitation_before_selfing'][alive],1)
    np.testing.assert_allclose(result['viable_seed_limitation'][alive],.95)
