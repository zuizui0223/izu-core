import pytest
from scripts.audit_existing_response_timing_20261013 import window, classify, case

def fixture():
    return {'task': {'key': 'fixture'}, 'status':'original_birth_and_ledger_replayed',
            'updates':200, 'rows':[dict(year=t, eligible=True,
                selection=[0.,-.001,.001], parent_sampling=[0.,0.,0.],
                transmission=[0.,0.,0.],birth_mutation=[0.,0.,0.],
                observed_change=[0.,-.001,.001],
                sexual_selection_components=[[0.,-.001,.001],[0.,0.,0.],[0.,0.,0.]]) for t in range(200)]}

def test_window_requires_full_sustained_period_and_retains_censoring():
    assert window([True]*19+[False]*181) is None
    assert window([False]*2+[True]*20) == 3
    assert window([False]*200) is None

def test_classification_does_not_rank_missing_events():
    assert classify(None,10)=='investment_only'
    assert classify(10,None)=='assurance_only'
    assert classify(None,None)=='neither'
    assert classify(10,15)=='near_simultaneous'
    assert classify(10,16)=='assurance_first'

def test_accounted_path_clock_is_not_counterfactual():
    r=case(fixture())
    assert r['A']['first_favorable_window']==1
    assert r['A']['actual_crossing']==50
    assert r['I']['selection_crossing']==50
    assert r['actual_order']=='near_simultaneous'

def test_missing_nonfinite_and_broken_accounting_fail():
    r=fixture();r['rows'].pop()
    with pytest.raises(ValueError):case(r)
    r=fixture();r['rows'][0]['selection'][2]=float('nan')
    with pytest.raises(ValueError):case(r)
    r=fixture();r['rows'][0]['observed_change'][2]=.1
    with pytest.raises(ValueError):case(r)
