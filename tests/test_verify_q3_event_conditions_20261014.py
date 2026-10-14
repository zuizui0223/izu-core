"""Synthetic adversarial checks for the separate verifier."""
import csv
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('independent_q3',Path(__file__).parents[1]/'scripts'/'verify_q3_event_conditions_20261014.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def test_windows_and_longest():
    assert v.events([0.0]*19,0.1)==dict(start=None,completion=None,longest=19)
    assert v.events([None]+[0.0]*20+[0.1]+[0.0]*23,0.1)==dict(start=1,completion=20,longest=23)
    assert v.events([0.05]*20,0.1)['completion']==19
    assert v.events([0.05000000000000001]*20,0.1)['start'] is None


@pytest.mark.parametrize('base,cls',[(0.01,'support_excluded'),(0.12,'gain_possible'),(0.18,'loss_possible'),(0.3,'all_support_eligible')])
def test_geometry(base,cls):
    assert v.geometry(base,0.125)==cls


def test_shared_history():
    means=[0.25]+[0.125]*200
    h=v.describe_history(means,20)
    assert h['preexisting'] and h['prefix_start']==1
    h=v.describe_history(means,19)
    assert not h['preexisting'] and h['trailing']==19 and h['native_event_predicted']
    means=[0.25]*190+[0.125]*11
    assert v.describe_history(means,195)['window_excluded']


def test_refixation_timing_and_absence():
    assert v.first_fixation([None,None,0.0625,0.0625],197,0.125,199)['refix_event_complete_at_refixation']
    assert not v.first_fixation([None,0.1875,0.1875],198,0.125,200)['refix_event_complete_at_refixation']
    assert v.first_fixation([None,None],199,0.125,None)['refix_endpoint']=='unfixed'
    with pytest.raises(ValueError,match='absorbing'):
        v.first_fixation([None,0.0625,None],198,0.125,None)


@pytest.mark.parametrize('cls,native,restored',[('gain_possible',True,False),('loss_possible',False,True),('support_excluded',False,True),('all_support_eligible',True,False)])
def test_forbidden_joint(cls,native,restored):
    with pytest.raises(ValueError,match='forbidden'):
        v.logical_check(dict(support_class=cls,preexisting=False,window_excluded=False,native_event_predicted=native),native,restored)


def test_csv_checks_every_field_and_duplicates(tmp_path):
    p=tmp_path/'table.csv'
    p.write_text('a,b\nTrue,\n',encoding='utf-8')
    v.compare_csv(p,[{'a':True,'b':None}],['a','b'])
    with pytest.raises(ValueError,match='field b'):
        v.compare_csv(p,[{'a':True,'b':0}],['a','b'])
    p.write_text('a,b\nTrue,\nTrue,\n',encoding='utf-8')
    with pytest.raises(ValueError,match='row count'):
        v.compare_csv(p,[{'a':True,'b':None}],['a','b'])

@pytest.mark.parametrize('offsets,copies,message',[
    ([0,0,2],[[0.125,0.125],[0.125,0.125]],'occupied'),
    ([0,1,2],[[0.125,0.125],[0.2,0.125]],'foreign'),
])
def test_raw_rejects_empty_and_foreign_support(offsets,copies,message):
    import io
    import json
    import zipfile
    import numpy as np
    raw=io.BytesIO()
    alleles=np.zeros((2,3,2))
    alleles[:,1,:]=copies
    np.savez(raw,alleles=alleles,offsets=np.asarray(offsets),metadata=json.dumps({}))
    zipped=io.BytesIO()
    with zipfile.ZipFile(zipped,'w') as z:
        z.writestr('test.npz',raw.getvalue())
    with zipfile.ZipFile(zipped) as z:
        with pytest.raises(ValueError,match=message):
            v.read_path(z,'test.npz',2,[0.125])
