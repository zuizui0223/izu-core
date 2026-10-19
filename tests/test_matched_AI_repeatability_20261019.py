import pytest
from scripts.audit_matched_AI_repeatability_20261019 import summarize_records


def fixture():
    per=[dict(demographic_seed=i,paired_occupied=True,near_assurance=.5,
              far_assurance=.5,near_investment=.5,far_investment=v)
         for i,v in enumerate([.25,.5,.75,1.])]
    return [dict(initial_state={'id':'synthetic'},histories=[
        dict(history_seed=7,eligible=True,per_repeat=per,
             far_minus_near_assurance=0.,far_minus_near_investment=.125)])]


def test_matched_variance_does_not_treat_fixed_endpoint_as_directional_change():
    r=summarize_records(fixture())['synthetic']
    assert r['allocated_arm_trajectories']==8
    assert r['paired_eligible_contexts']==1
    assert r['A']['far_mean_within_context_sample_variance']==0
    assert r['I']['far_mean_within_context_sample_variance']==pytest.approx(5/48)
    assert r['A']['contrast_labels']['0.0']['all_neutral_contexts']==1
    assert r['I']['contrast_labels']['0.0']['unanimous_contexts']==0


def test_partial_extinction_is_counted_but_excluded_from_matched_trait_comparison():
    records=fixture(); h=records[0]['histories'][0]; p=h['per_repeat'][0]
    p.update(far_assurance=None,far_investment=None,paired_occupied=False)
    h.update(eligible=False,far_minus_near_assurance=None,far_minus_near_investment=None)
    r=summarize_records(records)['synthetic']
    assert r['allocated_arm_trajectories']==8
    assert r['occupied_arm_trajectories']==7
    assert r['paired_eligible_contexts']==0
    assert r['A']['far_mean_within_context_sample_variance'] is None


@pytest.mark.parametrize('tamper', ['duplicate','missing_trait','bad_mean'])
def test_invalid_source_rows_fail(tamper):
    records=fixture(); h=records[0]['histories'][0]
    if tamper=='duplicate': h['per_repeat'][1]['demographic_seed']=0
    elif tamper=='missing_trait': h['per_repeat'][0]['near_assurance']=None
    else: h['far_minus_near_assurance']=.1
    with pytest.raises(ValueError): summarize_records(records)
