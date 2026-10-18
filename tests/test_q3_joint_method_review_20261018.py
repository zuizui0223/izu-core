"""No evolutionary simulations: tests for source-bound Q3 method-review plan."""
import copy
import hashlib
import json
from pathlib import Path
import pytest
from scripts.review_chapter2_joint_method_plan_20261018 import (
    load_inputs, derive_inputs, candidate_plan, review_candidate, budget,
    decision, allocation_frontier, conditional_gaussian_screen,
)


def test_variance_inputs_cover_original_and_both_control_future_families():
    rec, events = load_inputs()
    p = derive_inputs(rec, events)
    g = p['component_envelopes']['genetic_loss']
    assert g['founder'] == pytest.approx(.02833333333333334)
    assert g['visitor'] == pytest.approx(.03333333333333333)
    assert g['interaction'] == pytest.approx(.06555555555555553)
    assert g['within_cell'] == pytest.approx(.5138888888888888)
    assert set(p['genetic_loss_component_sources']) == {'original', '90', '104'}
    assert g['within_cell'] > .4  # previous stress assumption insufficient for the fork endpoint
    s = p['component_envelopes']['survival_interaction']
    assert s['within_cell'] == pytest.approx(1/12)
    assert p['independent_source_counts'] == {'founders':6, 'visitors':6, 'historical_repeats':2}


def test_terminal_support_is_not_cumulative_incidence_if_control_has_deaths():
    rec, events = load_inputs()
    bad=copy.deepcopy(rec)
    codes=bad['streams']['90']['terminal_status_codes']
    codes['fixed_B8']='0'+codes['fixed_B8'][1:]
    with pytest.raises(ValueError, match='B8 deaths'):
        derive_inputs(bad, events)


def test_gate_pass_is_only_method_review_and_132_fails_stress_margin():
    p = derive_inputs(*load_inputs())
    plan = candidate_plan(p)
    reviewed = review_candidate(plan, p)
    assert plan['founder_count'] == plan['visitor_history_count'] == 136
    assert reviewed['legacy_gate']['status']=='GO_FOR_METHOD_REVIEW_NOT_EXECUTION'
    assert reviewed['execution_authorized'] is False
    assert reviewed['registered'] is False
    assert reviewed['method_reviewer_approved'] is False
    assert reviewed['legacy_gate']['checks']['adverse']['genetic_loss']['MDE_proxy'] == pytest.approx(.09846956601383887)
    small=candidate_plan(p, n=132)
    assert review_candidate(small,p)['legacy_gate']['status']=='HOLD_PRECISION_INADEQUATE'


def test_real_shared_prefix_budget_is_not_misreported_as_full_80_per_branch():
    b=budget(136,136,1)
    assert b['historical_prefix_paths']==36992
    assert b['terminal_branch_paths']==73984
    assert b['shared_prefix_updates']==1294720
    assert b['future_branch_updates']==3329280
    assert b['unique_update_ceiling']==4624000
    assert b['legacy_rectangular_update_ceiling']==5918720
    assert b['unique_update_ceiling'] < b['legacy_rectangular_update_ceiling']
    assert b['new_pollinator_return_futures']==0
    assert budget(136,136,2)['unique_update_ceiling']==9248000


def test_fresh_cohort_and_seed_namespaces_are_reserved_not_run():
    p=derive_inputs(*load_inputs());plan=candidate_plan(p)
    sr=plan['prospective_seed_registry']
    assert len(sr['founders'])==len(set(sr['founders']))==136
    assert len(sr['visitors'])==len(set(sr['visitors']))==136
    assert not set(sr['founders']) & set(range(301001,301007))
    assert not set(sr['visitors']) & set(range(302001,302007))
    assert sr['biological_streams_consumed']==0
    assert sr['master_bit_width']==128
    bad=copy.deepcopy(plan);bad['prospective_seed_registry']['founders'][0]=301001
    with pytest.raises(ValueError,match='overlap'):
        review_candidate(bad,p)


def test_changed_source_bytes_and_false_adverse_scenario_are_rejected():
    p=derive_inputs(*load_inputs()); plan=candidate_plan(p)
    different=copy.deepcopy(p);different['source_note']='changed'
    with pytest.raises(ValueError,match='provenance'):
        review_candidate(plan,different)
    wrong=copy.deepcopy(plan)
    wrong['variance_uncertainty_scenarios'][1]['by_endpoint']['genetic_loss']['interaction']=.01
    with pytest.raises(ValueError,match='adverse'):
        review_candidate(wrong,p)


def test_significance_is_not_minimum_effect_and_null_is_not_equivalence():
    d=decision([.03,.17],[.40,.8],.1)
    assert d['joint_positive_direction'] is True
    assert d['both_effects_demonstrated_above_margin'] is False
    d=decision([.11,.24],[.40,.8],.1)
    assert d['both_effects_demonstrated_above_margin'] is True
    d=decision([-.08,.07],[-.04,.06],.1)
    assert d['joint_positive_direction'] is False
    assert d['both_inside_equivalence_band'] is True
    assert decision([-.5,.4],[-.5,.5],.1)['both_inside_equivalence_band'] is False
    with pytest.raises(ValueError):decision([.2,-.1],[.4,.8],.1)


def test_allocation_frontier_separates_pilot_repeats_from_future_independent_axes():
    f=allocation_frontier(.1)
    assert [x['nested_repeats'] for x in f]==[1,2,4]
    assert [x['minimum_square_n'] for x in f]==[133,130,128]
    assert f[0]['rounded_n']==136
    assert f[0]['unique_updates'] < f[1]['unique_updates'] < f[2]['unique_updates']


def test_gaussian_screen_is_conditional_not_ecological_power_validation():
    p=derive_inputs(*load_inputs());plan=candidate_plan(p)
    a=conditional_gaussian_screen(plan)
    assert a['normal_model_only'] is True
    assert a['known_variance_assumed'] is True
    assert a['biological_histories_generated']==0
    assert a['union_bound_joint_correct_direction_at_design_effect'] >= .8
    assert a['guarantees_power_for_Model3'] is False
    assert a['FWER_at_global_null_union_bound'] <= .05+1e-12
