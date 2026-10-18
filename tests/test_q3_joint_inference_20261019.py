import itertools
import numpy as np
import pytest
from scripts.q3_joint_inference_20261019 import contrasts, summarize, ph_statistics
from scripts.validate_q3_joint_oc_20261019 import marginal, decode_survival, sample_pair, decide_counts


def test_actual_four_arm_contrast_retains_both_extremes():
    s=np.arange(-2,3,dtype=np.int8)
    y=decode_survival(s)
    assert y.shape==(5,2,2)
    assert set(np.unique(y)) <= {0,1}
    assert np.array_equal((y[:,1,1]-y[:,1,0])-(y[:,0,1]-y[:,0,0]),s)
    g=np.zeros((5,3,2),int)
    occ=np.broadcast_to(y[:,None,:,:],(5,3,2,2)).copy()
    d=contrasts(g,occ)
    assert np.array_equal(d[...,1],np.broadcast_to(s[:,None],(5,3)))
    occ[0,0,0,0]=2
    with pytest.raises(ValueError): contrasts(g,occ)


def test_pigeonhole_variance_matches_all_small_resamples():
    x=np.array([[2.,-1.,0.],[-2.,1.,2.]])
    means=[]
    for rows in itertools.product(range(2),repeat=2):
        for cols in itertools.product(range(3),repeat=3):
            means.append(x[np.ix_(rows,cols)].mean())
    m,v=ph_statistics(x[None,:,:,None])
    assert m[0,0]==pytest.approx(x.mean())
    assert v[0,0]==pytest.approx(np.var(means),abs=1e-14)


def test_inference_does_not_call_zero_variance_significant_or_change_margin():
    d=np.zeros((4,5,2));d[...,1]=1
    r=summarize(d,margin=.1)
    assert r['execution_authorized'] is False
    assert not r['joint_positive']
    assert all(x['classification']=='degenerate_unresolved' for x in r['endpoints'])
    with pytest.raises(ValueError): summarize(d,margin=-.1)
    with pytest.raises(ValueError): summarize(d[:1],margin=.1)


def test_distributions_have_exact_declared_moments_and_full_S_support():
    for mu in (0.,.1):
        for support, tails in (([-1,0,1],None),([-2,-1,0,1,2],[.04,.08])):
            p=marginal(mu,.95,support,tails)
            x=np.array(support)
            assert p.sum()==pytest.approx(1)
            assert np.dot(p,x)==pytest.approx(mu)
            assert np.dot(p,(x-mu)**2)==pytest.approx(.95)
            assert (p>=0).all()
    p=marginal(.95,.0475,[-2,-1,0,1,2],[0.,0.])
    np.testing.assert_allclose(p,[0.,0.,.05,.95,0.],atol=1e-14)
    with pytest.raises(ValueError): marginal(.95,.001,[-1,0,1],None)


def test_joint_DGP_has_correct_support_and_replays_exactly():
    s={'n':4,'mu':[.1,.1],'components':[[.05,.05,.85],[.05,.05,.85]],
       'S_tail_mass':[.04,.08],'coupling':'opposed'}
    a=sample_pair(np.random.default_rng(18004),s,12)
    b=sample_pair(np.random.default_rng(18004),s,12)
    assert a.shape==(12,4,4,2)
    np.testing.assert_array_equal(a,b)
    assert set(np.unique(a[...,0])) <= {-1,0,1}
    assert set(np.unique(a[...,1])) <= {-2,-1,0,1,2}


def test_joint_decision_respects_partial_null_and_mixed_signs():
    m=np.array([[.1,.9],[0.,.9],[-.1,.9]])
    v=np.full_like(m,1e-6)
    r=decide_counts(m,v,[0.,.9],critical=2.3)
    assert r['false_reject_any_true_null']==2
    assert r['joint_positive']==1
    assert r['joint_negative']==0
    assert r['positive_each']==[1,3]
