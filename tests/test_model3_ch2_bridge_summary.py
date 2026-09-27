import numpy as np
import pytest
from scripts.summarize_model3_ch2_bridge import effect_report,paired_mean,compare_effects

def test_pair_effect_and_history_denominator():
    near=np.zeros((3,4,8));far=np.full_like(near,-.2)
    r=effect_report(near,far)
    assert r['mean']==pytest.approx(-.2)
    assert r['mean_ci']==pytest.approx([-.2,-.2])
    assert r['n_pairs']==96 and r['n_eligible_pairs']==96
    assert r['classification'][0]['counts']['negative']==4
    assert r['decomposition']['status']=='not_evaluable'

def test_extinction_not_zero_and_incomplete_histories_visible():
    near=np.zeros((3,4,8));far=np.ones_like(near)*.2;far[0,0,0]=np.nan
    r=effect_report(near,far)
    assert r['mean']==pytest.approx(.2) and r['n_eligible_pairs']==95
    assert r['classification'][0]['counts']['undefined']==1
    assert r['decomposition']['reason']=='incomplete_survivor_support'

def test_joint_support_contrast_not_difference_of_separate_means():
    a=np.array([[[.2,np.nan],[.4,.4]],[[.2,.2],[.4,.4]]])
    b=np.array([[[.3,100],[.5,.5]],[[.3,.3],[.5,.5]]])
    r=paired_mean(b-a)
    assert r['mean']==pytest.approx(.1)
    assert r['n_eligible_pairs']==7

def test_mean_zero_can_coexist_with_mixed_signs():
    a=np.zeros((3,4,8));b=a.copy();b[0]=.2;b[1]=-.2
    r=effect_report(a,b)
    assert r['mean']==pytest.approx(0)
    assert r['classification'][2]['counts']['mixed']==4
    assert r['repeat_label_disagreement']==0

def test_intervention_differences_keep_deadbands_and_pairing():
    a=np.ones((3,4,8))*.2;b=a+.1
    r=compare_effects(a,b)
    assert r['mean_difference']['mean']==pytest.approx(.1)
    assert len(r['mixed_fraction_differences'])==3
    assert r['mixed_fraction_differences'][0]['mean_difference']==0

def test_all_case_audit_requires_terminal_and_detects_corruption(tmp_path):
    import json
    from pathlib import Path
    from scripts.run_model3_ch2_bridge import run_campaign,sources
    from scripts.report_model3_ch2_bridge import audit_campaign
    d=json.loads(Path('data/design/model3_ch2_bridge_candidate_20260927.json').read_text())
    d.update(status='frozen',history_seeds=[74909],demographic_seeds=[101],starts=[.5],arms=['near','far'],cases=2,source_hashes=sources())
    d['years']=d['base_config']['years']=2
    out=tmp_path/'run';run_campaign(d,out)
    data,visits,receipts,audit=audit_campaign(d,out)
    assert audit['cases_checked']==audit['replayed']==2
    assert data['near']['individual'].shape==(1,1,1)
    f=next(out.glob('*/arrays.npz'));f.write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='array hash differs'):audit_campaign(d,out)

def test_unconditional_all_survivors_do_not_get_zero_width_interval():
    from scripts.summarize_model3_ch2_bridge import bounded_history_mean
    r=bounded_history_mean(np.ones((3,128,8)),0,1)
    assert r['mean']==1 and r['mean_ci'][0]<.9
    assert r['n_histories']==128
    with pytest.raises(ValueError):bounded_history_mean(np.array([[[np.nan]]]),0,1)

def test_numerical_refinement_compares_isolation_effect_not_raw_endpoint():
    from scripts.report_model3_ch2_bridge import numerical_comparison
    d={'starts':[.3,.5,.7],'history_seeds':[1,2,3,4],'demographic_seeds':[1,2],
       'analysis_contract':{'numerical_tolerances':{'trait':.01}}}
    from scripts.report_model3_ch2_bridge import PAIRS
    base={};new={}
    for _,near,far in PAIRS:
        for arm,value in ((near,0),(far,-.2)):
            base[arm]={k:np.full((3,4,2),value) for k in ('individual','density')}
            new[arm]={k:np.full((3,4,2),value+.1) for k in ('individual','density')}
    report=numerical_comparison(d,d,base,new)
    assert report['natural']['individual']['mean']==pytest.approx(0)
    assert report['natural']['individual']['assessment']=='interval_within_tolerance'
