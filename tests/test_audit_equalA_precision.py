import copy
import itertools
import json
from pathlib import Path
import numpy as np
import pytest
from scripts.audit_chapter2_equalA_precision_20261018 import (
    review, exact_pigeonhole, variance_components, mde_proxy, SOURCE)


def test_exact_enumeration_matches_all_ordered_two_by_two_draws():
    x=np.array([[[0,1],[1,-1]],[[-1,0],[1,1]]],dtype=int)
    result=exact_pigeonhole(x)
    draws=[]
    for f in itertools.product(range(2),repeat=2):
        for v in itertools.product(range(2),repeat=2):
            draws.append(x[np.ix_(f,v,range(2))].mean())
    values,counts=np.unique(draws,return_counts=True)
    assert result['ordered_resample_weight']==16
    assert result['mean']==pytest.approx(x.mean())
    for p,key in ((.025,'lower95'),(.975,'upper95'),(.0125,'lower975'),(.9875,'upper975')):
        i=np.searchsorted(np.cumsum(counts)/16,p)
        assert result[key]==values[i]


def test_original_event_record_rederivation_and_paired_uncertainty():
    data=json.loads(SOURCE.read_text())
    got=review(data)
    assert got['counts']['fixed_high_I_loss']==42
    assert got['counts']['evolving_high_I_loss']==58
    assert got['risk_difference']==pytest.approx(2/9)
    assert got['restricted_access_census_difference']==pytest.approx(-10.36111111111111)
    assert got['bootstrap_risk']['ordered_resample_weight']==6**12
    assert got['bootstrap_risk']['count_vector_pairs']==462**2
    assert got['bootstrap_risk']['lower95']==0
    assert got['bootstrap_risk']['upper95']==pytest.approx(33/72)
    assert got['bootstrap_risk']['lower975']==pytest.approx(-3/72)
    assert got['bootstrap_risk']['upper975']==.5
    assert got['bootstrap_access_time']['lower975']<0<got['bootstrap_access_time']['upper975']
    assert got['paired_joint_I_loss_counts']=={'neither':8,'evolving_only':22,'fixed_only':6,'both':36}
    assert got['CIF_G_strictly_before_TE']=={'fixed':7,'evolving':18}
    assert got['formal_confirmation_authorized'] is False
    assert got['survival_endpoint_is_saturated'] is True


def test_wrong_source_missing_records_and_zero_imputation_fail_closed():
    data=json.loads(SOURCE.read_text())
    for mutate in (
      lambda x:x['first_I_loss_fixed'][0].pop(),
      lambda x:x['first_I_loss_fixed'][0].__setitem__(2,0),
      lambda x:x['source'].__setitem__('ci_run_id',123),
      lambda x:x.__setitem__('all_144_paths_alive_at_80',False)):
        d=copy.deepcopy(data);mutate(d)
        with pytest.raises(ValueError): review(d)


def test_independent_variance_fixture_and_screening_is_not_authorization():
    a=np.array([1,-1,2,-2,3,-3])[:,None,None]
    b=np.array([-.1,.1,0,.5,-.5,.3])[None,:,None]
    noise=np.array([-.25,.25])[None,None,:]
    c=variance_components(a+b+noise)
    assert c['within_cell']==pytest.approx(.125)
    assert c['founder']>=0 and c['visitor']>=0
    z={'founder':.023333333333333345,'visitor':0.,'interaction':.06555555555555553,'within_cell':.2777777777777778}
    assert mde_proxy(z,6,6,2)==pytest.approx(.3446000613971081)
    assert mde_proxy(z,32,32,2)<mde_proxy(z,6,6,2)
    with pytest.raises(ValueError):exact_pigeonhole(np.zeros((7,6,2),dtype=int))
