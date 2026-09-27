import numpy as np
import pytest
from scripts.audit_model3_ch2_bridge import classify_histories

def test_mixed_requires_opposite_starts():
    x=np.array([[[.2,.2],[.2,.2]], [[-.2,-.2],[.3,.3]]])
    r=classify_histories(x,.05)
    assert r['counts']=={'mixed':1,'positive':1,'negative':0,'neutral':0,'undefined':0}
    assert r['repeat_disagreements']==0

def test_deadband_and_undefined_are_not_negative_or_zero():
    x=np.array([[[.01,.01],[np.nan,.2]], [[-.01,-.01],[-.2,-.2]]])
    r=classify_histories(x,.01)
    assert r['counts']['neutral']==1 and r['counts']['undefined']==1
    assert r['n_eligible']==1

def test_demographic_repeat_disagreement_is_visible():
    x=np.array([[[.2,-.1]], [[-.2,-.1]]])
    r=classify_histories(x,0)
    assert r['counts']['mixed']==1
    assert r['repeat_disagreements']==1

@pytest.mark.parametrize('x,e',[(np.zeros((2,3)),0),(np.zeros((1,3,2)),0),(np.zeros((2,0,2)),0),(np.zeros((2,3,2)),-.1)])
def test_invalid_contract_rejected(x,e):
    with pytest.raises(ValueError): classify_histories(x,e)
