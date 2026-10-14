import numpy as np
import pytest
from scripts.run_ecological_order_boundary_20261013 import tasks, seed, events, interval
from scripts.read_ecological_order_boundary_20261013 import summarize

def test_complete_context_inventory_and_paired_seeds():
    ts=list(tasks())
    assert len(ts)==2304 and len({(t['block'],t['context'],t['replicate']) for t in ts})==2304
    assert len({seed(t) for t in ts})==256
    assert all(seed(t)!=seed(t,technical=True) for t in ts)
    assert len({t['context'] for t in ts})==9

def test_events_retain_missing_censoring_and_full_window():
    a=np.zeros((201,3));a[:,1:]=.5
    a[4:,2]=.55;a[12:,1]=.44
    assert events(a,np.full(201,48))=={'A':4,'I':12,'category':'assurance_first'}
    a[-19:,2]=.6;a[:182,2]=.5
    assert events(a,np.full(201,48))['A'] is None
    n=np.zeros(201,int);n[:8]=48
    a[8:]=np.nan
    assert events(a,n)['category']=='neither'

def test_event_invalid_state_and_interval_count_rejected():
    with pytest.raises(ValueError):events(np.full((201,3),np.nan),np.full(201,48))
    with pytest.raises(ValueError):interval(129,0,128)

def test_exact_intervals_do_not_call_zero_equivalence():
    lo,hi=interval(0,0,128)
    assert lo<0<hi
    lo,hi=interval(128,0,128)
    assert lo>0 and hi==1

def test_reader_requires_every_start_and_both_founder_reversal():
    records=[{'task':t,'events':{'category':'assurance_first' if t['context']<=2 else 'investment_first'}} for t in tasks()]
    s=summarize(records)
    assert len(s['cells'])==18
    assert s['supported_supply_pairs']
    with pytest.raises(ValueError):summarize(records[:-1])
    records[-1]=records[0]
    with pytest.raises(ValueError):summarize(records)
