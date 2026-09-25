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
