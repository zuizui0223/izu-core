import pytest
import numpy as np
import csv
from pathlib import Path
from scripts.audit_persistence_duration_accounting_20261013 import contrast_curves, first_entry_by_census, compare_compact_lifetime


def rows(values):
    return [dict(update=t, occupied=x, low_fixed_alive=x, high_fixed_alive=0., segregating_alive=0.) for t,x in enumerate(values)]


def test_positive_endpoint_does_not_cancel_earlier_duration_loss():
    r=contrast_curves(rows([1.,.6,.5]),rows([1.,.8,.4]))
    assert r['endpoint_difference']==pytest.approx(.1)
    assert r['restricted_duration_difference']==pytest.approx(-.2)
    assert r['negative_curve_area']==pytest.approx(-.2)
    assert r['positive_curve_area']==0.
    assert r['sign_change_updates']==[2]
    assert r['class_duration_contributions']['low_fixed_alive']==pytest.approx(-.2)


def test_all_curve_intervals_are_retained():
    r=contrast_curves(rows([1.,.8,.7,.6]),rows([1.,.6,.65,.5]))
    assert r['restricted_duration_difference']==pytest.approx(.25)
    assert r['positive_curve_area']==pytest.approx(.25)
    assert r['negative_curve_area']==0.
    assert r['sign_change_updates']==[]


def test_reject_nonpartitioned_or_misaligned_curves():
    native=rows([1.,.6,.5]);native[1]['low_fixed_alive']=.1
    with pytest.raises(ValueError,match='partition'):
        contrast_curves(native,rows([1.,.8,.4]))
    with pytest.raises(ValueError,match='updates'):
        contrast_curves(rows([1.,.6]),rows([1.,.8,.4]))


def test_first_entry_census_counts_once_even_when_fixed_survives():
    states=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])
    T=np.array([[1,0,0,0],[.5,.5,0,0],[.4,.3,.2,.1],[.2,0,0,.8]])
    entry=first_entry_by_census(T,states,np.array([0.,0.,1.,0.]),2)
    assert entry.shape==(3,2,1)
    np.testing.assert_allclose(entry[:,:,0],[[0.,0.],[.3,.1],[.06,.02]])


def test_original48_gate_rejects_duration_changes_and_altered_bytes(tmp_path):
    # Canonical frozen fixture bytes; production never normalizes an input.
    fixture=Path(__file__).resolve().parents[1]/'data/results/pr471_fixation_lifetime_readout_20261012.csv'
    p=tmp_path/'frozen.csv';p.write_bytes(fixture.read_bytes().replace(b'\r\n',b'\n'))
    with p.open(newline='',encoding='utf-8') as f:original=list(csv.DictReader(f))
    pairs=[dict(mismatch_fraction=float(r['mismatch_fraction']),setting=r['setting'],budget=float(r['budget']),
                visitor_arm=r['visitor_arm'],endpoint_difference=float(r['delta_P_H_occupied']),
                restricted_duration_difference=float(r['delta_restricted_mean_time_to_extinction']),
                low_first_entry_difference=float(r['delta_P_low_fixed_ever_by_H'])) for r in original]
    assert compare_compact_lifetime(pairs,p)['comparisons']==144
    pairs[0]['restricted_duration_difference']+=.01
    with pytest.raises(ValueError,match='contrast mismatch'):
        compare_compact_lifetime(pairs,p)
    p.write_bytes(p.read_bytes()+b'\n')
    with pytest.raises(ValueError,match='byte identity'):
        compare_compact_lifetime(pairs,p)
