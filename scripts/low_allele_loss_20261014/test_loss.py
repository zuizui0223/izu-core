import math
import numpy as np
import pytest
from audit_loss import response,loss_probability
from audit_loss import aggregate,frozen_sources,CLASSES
from verify_loss import source_gate


def test_selfing_gametes_are_independent_and_expected_response_telescopes():
    r=response(np.zeros((2,2)),np.array([3.,1.]),np.array([.5,0.]))
    assert r['current_frequency']==.25 and r['expected_frequency']==.375
    assert r['self_response']==.125 and r['female_response']==r['paternal_response']==0
    assert r['q0']==.4375
    assert r['observed_change']==r['parent_weighting_response']+r['sampling_transmission_residual']
    p,logp=loss_probability(r['q0'],4)
    assert p==r['q0']**4 and logp==4*math.log(r['q0'])


def test_father_rows_and_mother_columns_are_not_swapped():
    r=response(np.array([[0.,3.],[1.,0.]]),np.zeros(2),np.array([1.,0.]))
    assert r['female_response']==-.125 and r['paternal_response']==.125
    assert r['expected_frequency']==.5 and r['q0']==0


def test_heterozygote_selfing_does_not_copy_one_gamete_twice():
    r=response(np.zeros((1,1)),np.ones(1),np.array([.5]))
    assert r['q0']==.25 and r['parent_weighting_response']==0


@pytest.mark.parametrize('out,selfed,x',[
    (np.zeros((1,1)),np.zeros(1),np.array([.5])),
    (np.array([[1.]]),np.ones(1),np.array([.5])),
    (np.zeros((1,1)),np.array([-1.]),np.array([.5])),
    (np.zeros((1,1)),np.ones(1),np.array([np.nan])),
    (np.zeros((1,1)),np.ones(1),np.array([1.1])),
])
def test_invalid_parental_returns_fail_closed(out,selfed,x):
    with pytest.raises(ValueError):response(out,selfed,x)


@pytest.mark.parametrize('q,n',[(0.,1),(.5,0),(.5,True),(1.1,2)])
def test_impossible_loss_or_unoccupied_state_is_not_admitted(q,n):
    with pytest.raises(ValueError):loss_probability(q,n)


def test_certain_loss_has_log_zero():
    assert loss_probability(1.,48)==(1.,0.)


def test_zero_original_categories_are_retained():
    value=aggregate([dict(transition_status='no_exclusion',original_category='assurance_only')])
    assert set(value['original_categories'])==set(CLASSES)
    assert value['original_categories']['assurance_only']==1
    assert sum(value['original_categories'].values())==1


@pytest.mark.parametrize('gate',[frozen_sources,source_gate])
def test_replaced_source_and_updated_manifest_cannot_replace_start_freeze(tmp_path,gate):
    import hashlib,json
    names=['PROTOCOL.md','audit_loss.py','verify_loss.py','test_loss.py','RECIPE_SOURCE.py',
           'native/__init__.py','native/types.py','native/reproduction.py','native/population.py']
    pins={}
    for name in names:
        p=tmp_path/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'initial')
        pins[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=tmp_path/'FROZEN_SOURCES.json';manifest.write_text(json.dumps(pins),encoding='utf-8')
    captured=gate(tmp_path)
    (tmp_path/'audit_loss.py').write_bytes(b'replaced')
    pins['audit_loss.py']=hashlib.sha256(b'replaced').hexdigest()
    manifest.write_text(json.dumps(pins),encoding='utf-8')
    with pytest.raises(ValueError,match='manifest changed'):gate(tmp_path,captured)
