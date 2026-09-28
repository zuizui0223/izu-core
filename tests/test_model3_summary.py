import numpy as np
import pandas as pd
import pytest

from scripts.summarize_model3_evolution import paired_summary, wilson


def test_wilson_interval_includes_boundaries_without_zero_uncertainty():
    low,high = wilson(0,256)
    assert low == 0 and 0 < high < .02
    low,high = wilson(256,256)
    assert .98 < low < 1 and high == 1


def test_pairing_does_not_subtract_different_survivor_groups():
    common = dict(campaign='primary',environment='mainland',survival=0.,selfing=0.,start=.3,year=100)
    rows=[]
    for seed,a,b in [(1,.4,.3),(2,.8,np.nan),(3,np.nan,.1)]:
        for control,value in [('selected',a),('neutral',b)]:
            rows.append(dict(**common,seed=seed,control=control,population=0 if np.isnan(value) else 48,
                             access=value,investment=value))
    out = paired_summary(pd.DataFrame(rows))
    assert len(out)==1
    assert out.iloc[0]['paired_survivors']==1
    assert out.iloc[0]['all_pairs']==3
    assert np.isclose(out.iloc[0]['access_selected_minus_neutral'],.1)
    assert np.isnan(out.iloc[0]['access_mcse'])


def test_variants_remain_separate_in_paired_summaries():
    common=dict(campaign='assurance',environment='both',survival=0.,selfing=.5,start=.3,year=100,seed=47,population=48)
    rows=[]
    for variant,depression in [('low',0.),('high',.9)]:
        for control,value in [('selected',.4),('neutral',.3)]:
            rows.append(dict(**common,variant=variant,depression=depression,
                             ovule_effort='lifetime',pollen_effort='lifetime',
                             control=control,access=value,investment=value))
    result=paired_summary(pd.DataFrame(rows))
    assert len(result)==2
    assert set(result.variant)=={'low','high'}


def test_pooled_limitation_uses_ovule_weighting_not_mean_annual_ratio():
    from scripts.summarize_model3_evolution import reproductive_totals
    result=reproductive_totals(np.array([1.,9.]),np.array([0.,9.]),np.array([.5,0.]),np.array([1.,0.]))
    assert np.isclose(result['cumulative_pollen_limitation'],.1)
    assert np.isclose(result['cumulative_viable_seed_limitation'],.05)
    assert result['cumulative_inbreeding_loss']==.5


def test_direction_frequencies_include_extinction_in_denominator():
    from scripts.summarize_model3_evolution import direction_summary
    result=direction_summary(np.array([.1,-.1,.01,np.nan]),np.array([48,48,48,0]))
    assert result['increasing_fraction']==.25
    assert result['decreasing_fraction']==.25
    assert result['small_change_fraction']==.25
    assert result['extinction_fraction']==.25


def test_assurance_contrasts_pair_seeds_and_effort_to_separate_campaign_reference():
    from scripts.summarize_model3_evolution import intervention_summary
    rows=[]
    common=dict(environment='both',survival=.75,selfing=.5,start=.3,control='selected',year=100)
    for seed in (1,2):
        for campaign,variant,depression,effort,value in [
                ('assurance','a0.5_d0.0',0.,'lifetime',.3),
                ('assurance','a0.5_d0.5',.5,'lifetime',.4),
                ('effort_separation','annual',.5,'annual',.5 if seed==1 else np.nan)]:
            rows.append(dict(**common,campaign=campaign,variant=variant,depression=depression,
                ovule_effort=effort,pollen_effort='lifetime',seed=seed,
                population=0 if np.isnan(value) else 48,access=value,investment=value))
    result=intervention_summary(pd.DataFrame(rows))
    assert len(result)==2
    effort=result[result.comparison=='effort_vs_lifetime'].iloc[0]
    assert effort.all_pairs==2 and effort.paired_survivors==1
    assert np.isclose(effort.access_difference,.1)
    assert effort.extinction_difference==.5
    depression=result[result.comparison=='depression_vs_zero'].iloc[0]
    assert depression.paired_survivors==2
    assert np.isclose(depression.access_difference,.1)


def test_missing_assurance_reference_is_not_silently_dropped():
    from scripts.summarize_model3_evolution import intervention_summary
    row=dict(campaign='assurance',variant='a0.5_d0.9',depression=.9,
        ovule_effort='lifetime',pollen_effort='lifetime',environment='both',
        survival=0.,selfing=.5,start=.3,control='selected',year=100,seed=1,
        population=0,access=np.nan,investment=np.nan)
    with pytest.raises(ValueError,match='missing intervention reference'):
        intervention_summary(pd.DataFrame([row]))


def test_zero_ovules_do_not_report_zero_pollen_limitation():
    from scripts.summarize_model3_evolution import reproductive_totals
    result=reproductive_totals([0.],[0.],[0.],[0.])
    assert np.isnan(result['cumulative_pollen_limitation'])
    assert np.isnan(result['cumulative_viable_seed_limitation'])


def test_summary_rejects_structural_verification_without_replay(tmp_path):
    import hashlib
    import json
    from scripts.summarize_model3_evolution import summarize
    manifest=json.dumps({'artifacts':[{'path':'cell_000.npz'}]}).encode()
    (tmp_path/'manifest.json').write_bytes(manifest)
    (tmp_path/'verification.json').write_text(json.dumps(dict(status='verified',
        manifest_sha256=hashlib.sha256(manifest).hexdigest(),artifacts=1,replayed_cases=0)))
    with pytest.raises(ValueError,match='replay coverage'):
        summarize(tmp_path,tmp_path/'summary')


def test_demographic_totals_keep_potential_and_realized_recruits_separate():
    from scripts.summarize_model3_evolution import demographic_totals
    result=demographic_totals([1,2],[10,20],[4,3])
    assert result==dict(cumulative_established=3,cumulative_potential_recruits=30,
                       cumulative_adult_survivals=7)
