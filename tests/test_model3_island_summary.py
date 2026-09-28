import numpy as np
import pytest

from scripts.model3_island.summarize import (summarize,decompose_crossed,
    paired_contrast,effective_exposure,transport_score)


def record(case,trait,density,occupied=True,ancestry=1.,history=1,cell='a'):
    return dict(case_id=case,cell_id=cell,cohort='production',history_seed=history,
        demographic_seed=1,family='chronology',pair_group='test',start_id='s',weight=1.,
        result=dict(population=np.array([2,2 if occupied else 0]),
        trait_mean=np.array([[.5,.5,.5],[.5,trait,.5] if occupied else [np.nan]*3]),
        density_traits=np.array([[.5,.5,.5],[.5,density,.5]]),
        density_mass=np.array([2.,2.]),founder_ancestry=np.array([1.,ancestry if occupied else np.nan]),
        trait_variance=np.zeros((2,3)),heterozygosity=np.ones((2,3))*.5,
        extinction_year=-1 if occupied else 1,recolonizations=0,
        demographic=np.array([[0,1,0,0,1,0,2,2]]),
        demographic_keys=np.array(['survivors','resident_potential','immigrant_candidates','immigrant_settled',
            'resident_recruits','immigrant_recruits','parent_age_sum','parent_contributions'])))


def test_extinction_denominators_and_immigrant_replacement():
    out=summarize([record('1',0.,.5,False),record('2',0.,.5,False,history=2)],{})
    cell=out['cells'][0]
    assert cell['n_total']==2 and cell['n_survivors']==0
    assert cell['mean_investment_change'] is None and cell['occupancy']==0
    assert cell['occupancy_ci'][1]>0
    out=summarize([record('1',.7,.6,ancestry=0.)],{})['cells'][0]
    assert out['mean_founder_ancestry']==0 and out['founder_lineage_persistence']==0


def test_signed_bias_is_not_mae():
    rows=[record('1',1.,0.,history=1),record('2',0.,1.,history=2)]
    out=summarize(rows,{})['cells'][0]
    assert out['individual_density_bias']==pytest.approx(0.)
    assert out['individual_density_mae']==pytest.approx(1.)


def test_asymmetric_pair_survival_keeps_marginals_and_eligible_ids():
    a=[record('a1',.2,.4,history=1),record('a2',.4,.4,False,history=2)]
    b=[record('b1',.3,.4,history=1,cell='b'),record('b2',.5,.4,history=2,cell='b')]
    x=paired_contrast(a,b)
    assert x['n_pairs']==2 and x['n_joint_survivors']==1
    assert x['occupancy_a']==.5 and x['occupancy_b']==1.
    assert x['conditional_mean_b_minus_a']==pytest.approx(.1)
    assert x['eligible_pairs']==[['a1','b1']]
    assert x['conditional_ci'] is None


def test_sci_additive_interaction_and_noise_are_distinct():
    w={'S':[.5,.5],'C':[.5,.5]}
    additive=np.array([[0.,1.],[2.,3.]])
    x=np.stack([additive-.2,additive+.2],axis=2)
    d=decompose_crossed(x,w)
    assert d['I']==pytest.approx(0.,abs=1e-14)
    assert d['within_cell_variance']>0
    assert d['S']+d['C']+d['I']==pytest.approx(1.)
    x=np.repeat(np.array([[1.,-1.],[-1.,1.]])[:,:,None],2,axis=2)
    assert decompose_crossed(x,w)['I']==pytest.approx(1.)
    x[0,0,0]=np.nan
    assert decompose_crossed(x,w)['status']=='not_evaluable'


def test_effective_exposure_valid_limits_and_invalid_context():
    series=np.array([0.,1.,0.,1.]); w=np.ones(4)
    assert effective_exposure(series,w,np.eye(4))['k_eff']==pytest.approx(4.)
    assert effective_exposure(series,w,np.ones((4,4)))['k_eff']==pytest.approx(1.)
    corr=np.eye(4)*1.2-np.ones((4,4))*.2
    assert effective_exposure(series,w,corr)['k_eff']>4
    for s,weights,r in [(np.ones(4),w,np.eye(4)),(series,-w,np.eye(4)),
            (series,w,np.eye(4)*2),(series,w,np.eye(4)*2-np.ones((4,4)))]:
        assert effective_exposure(s,weights,r)['status']=='not_evaluable'
    assert effective_exposure(series,w,np.eye(4),stationary=False)['status']=='not_evaluable'


def test_transport_refuses_changed_factor_support():
    x=np.arange(8.).reshape(2,2,2); w={'S':[.5,.5],'C':[.5,.5]}
    assert transport_score(x,x,w,w)['mae']==0.
    with pytest.raises(ValueError): transport_score(x,x,w,{'S':[.7,.3],'C':[.5,.5]})

def test_crossed_campaign_outputs_partition_and_heldout_transport():
    rows=[]
    for cohort,base in [('production',10),('heldout',20)]:
        for s in range(2):
            for h in range(2):
                for d in range(2):
                    r=record(f'{cohort}-{s}-{h}-{d}',.2+s*.1+h*.02+d*.001,.4,
                             history=base+h,cell=f's{s}')
                    r.update(cohort=cohort,start_id=f's{s}',family='transport',demographic_seed=d)
                    rows.append(r)
    out=summarize(rows,{})
    assert len(out['crossed'])==2 and len(out['transport'])==1
    assert out['crossed'][0]['investment']['status']=='descriptive_cell_means'
    assert out['transport'][0]['investment']['mae']==pytest.approx(0.)

def test_reference_service_is_fixed_panel_not_evolved_population():
    from dataclasses import replace
    from test_model3_island_state import config_fixture
    from test_model3_island_assays import visitors
    from scripts.model3_island.assays import reference_service
    c=config_fixture()
    values=reference_service((visitors(0),visitors(4)),c)
    assert values.shape==(2,)
    assert values[0]==0 and 0<values[1]<1
    other=reference_service((visitors(0),visitors(4)),replace(c,capacity=192,fixed_assurance=.9))
    np.testing.assert_array_equal(values,other)

def test_undefined_resident_control_cannot_become_extinction_effect():
    r=record('1',.0,.2,False)
    r['result']['resident_control_undefined']=np.array([True])
    out=summarize([r],{})['cells'][0]
    assert out['status']=='not_evaluable' and out['n_undefined']==1
    assert 'occupancy' not in out
    assert paired_contrast([r],[record('2',.2,.3)])['status']=='not_evaluable'
