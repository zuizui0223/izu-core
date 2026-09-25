import numpy as np
import pandas as pd

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
