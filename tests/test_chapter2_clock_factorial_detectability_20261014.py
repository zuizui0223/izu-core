"""Fixed independent-unit assumption audits; no model simulation or pilot outcomes."""
import math
import pytest
from scripts.audit_chapter2_clock_factorial_detectability_20261014 import (
    audit, normal_cdf, one_direction_ci_positive_probability, hypothetical_effect_for_80pct,
    hypothetical_later_confirmation, N_PILOT, N_TRAJECTORIES,
)


def test_source_recorded_pilot_grain_and_all_five_descriptive_contrasts():
    r=audit()
    g=r['pilot_grain']
    assert g['independent_founder_stream_clusters']==128
    assert g['trajectories_per_cluster']==12
    assert g['registered_trajectories']==1536
    assert g['actual_new_model3_histories_generated_in_this_audit']==0
    assert len(r['source_frozen_analysis']['five_predeclared_descriptive_contrasts'])==5
    assert r['source_frozen_design']['git_blob']=='75d49de2781a240c14bdc3f9106212b0dbbda6aa'
    assert r['source_frozen_analysis']['git_blob']=='06c343b6e20a08c0575ddbe6ace5ef5fbdeb85ed'


def test_earlier_exposed_logloss_power_reproduced_exactly():
    assert math.isclose(one_direction_ci_positive_probability(.02,.15,128),.325825594750103,abs_tol=1e-13)
    assert math.isclose(one_direction_ci_positive_probability(.02,.15,512),.8547498992894756,abs_tol=1e-13)
    assert math.isclose(one_direction_ci_positive_probability(.02,.2,896),.8492827211233429,abs_tol=1e-13)
    assert math.isclose(one_direction_ci_positive_probability(.02,.25,1024),.7257588833575942,abs_tol=1e-13)


def test_128_vs_64_units_are_not_1536_independent_paths():
    assert N_PILOT==128 and N_TRAJECTORIES==1536
    assert math.isclose(hypothetical_effect_for_80pct(.2,128),.04952549764499182,abs_tol=1e-13)
    assert math.isclose(hypothetical_effect_for_80pct(.2,64)/hypothetical_effect_for_80pct(.2,128),math.sqrt(2))


def test_future_confirm_rule_uses_sigma_only_and_frozen_cap():
    expected={.1:512,.15:512,.2:896,.225:1024,.25:1280}
    for sd,n in expected.items():
        result=hypothetical_later_confirmation(sd)
        assert result['rounded_required_clusters']==n
        assert result['scientific_confirmation_authorized'] is False
        assert result['model_based_sigma_measured_from_current_pilot'] is False
        if sd==.25:
            assert result['decision_if_models_were_frozen_and_sd_were_valid'].startswith('NO_GO')
            assert result['would_require_trajectories'] is None
        else:
            assert result['would_require_trajectories']==n*12


def test_support_bounds_and_all_six_outcomes_not_partial_survivor_subset():
    r=audit()
    b=r['bounded_factorial_contrast_support']
    assert b['A_incidence_and_I_incidence_main_factor_contrasts']==[-1,1]
    assert b['D_main_factor_contrasts']==[-2,2]
    assert b['D_Awidth_x_Ihidden_interaction']==[-4,4]
    assert 'all included in six-class denominator' in b['D_definition']


def test_models_not_frozen_prevents_conflating_factorial_sd_and_future_logloss_sd():
    x=audit()['existing_future_prediction_score_rule_if_fully_reviewed']
    assert x['predictive_clock_and_equal_or_more_flexible_null_currently_frozen'] is False
    assert x['post_pilot_prediction_model_specific_sigma_currently_identified'] is False
    assert x['pilot_factorial_contrast_sd_cannot_substitute_for_prediction_logloss_difference_sd'] is True


@pytest.mark.parametrize('effect,sd,n',[(float('nan'),.2,128),(-.02,.2,128),(.02,0.,128),(.02,.2,1),(.02,.2,128.0)])
def test_invalid_power_inputs_rejected(effect,sd,n):
    with pytest.raises(ValueError):
        one_direction_ci_positive_probability(effect,sd,n)


def test_positive_effect_has_higher_success_probability():
    assert normal_cdf(0)==.5
    assert one_direction_ci_positive_probability(.05,.2,128)>one_direction_ci_positive_probability(.02,.2,128)
