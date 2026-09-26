from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import json
import numpy as np
import pytest

from test_model3_island_state import config_fixture
from scripts.model3_island.design import compile_design, validate_design, source_hashes
from scripts.model3_island.run import run_campaign


def document():
    c=asdict(config_fixture()); c['years']=2; c['capacity']=4
    return dict(schema_version=1,frozen=False,model='discrete_genotype_density',
        base_config=c,units={'time':'reproductive_year','distance':'dispersal_scale','traits':'unit_interval'},
        parameter_ranges={'trait':[0.,1.],'distance':[0.,10.]},
        mechanism_flags={'self_exclusion':True,'fixed_inbreeding_depression':True,'evolving_load':False},
        cohorts={'pilot':[101,102],'production':[201,202],'heldout':[301,302]},
        demographic_seeds=[1,2],founder_seed=7,
        numerical_tolerances={'trait':.02,'occupancy':.1},effect_thresholds={'investment':.05},
        horizons=[2],precision={'proportion_half_width':.7,'confidence':.95,'max_histories':2,
            'conditional_rule':'fixed_R_report_interval_and_eligible_n','rare_event_rule':'report_upper_bound'},
        resource_limits={'runtime_seconds':60.,'memory_mb':1024.},source_hashes=source_hashes(),
        claim_exclusions=['PDE','Q1_fit','drift_only','continuous_trait_convergence'],
        families=[{'name':'chronology','question':'same exposure, different order',
          'cells':[{'id':'control','kind':'trajectory','config_patch':{},
            'grid_axes':[[0.,.5,1.]]*3,'founders':{'count':4,'means':[.5,.5,.5],'sd':.1,'birth_year':0},
            'history':{'kind':'segments','segments':[{'years':2,'pool':0,'count':2,'optimum':.5,'sd':.1}]},
            'cohorts':['pilot','production','heldout'],'weight':1.,'start_id':'s1','pair_group':'order'}]}])


def test_exact_cases_and_validation():
    d=document(); validate_design(d)
    cases=compile_design(d)
    assert len(cases)==12 and len({c['case_id'] for c in cases})==12
    assert len([c for c in cases if c['cohort']=='pilot'])==4


@pytest.mark.parametrize('field',['units','parameter_ranges','mechanism_flags','cohorts',
    'numerical_tolerances','effect_thresholds','precision','resource_limits','source_hashes','claim_exclusions'])
def test_missing_scientific_fields_rejected(field):
    d=document(); del d[field]
    with pytest.raises(ValueError): validate_design(d)


def test_bad_cohorts_labels_case_ids_and_precision_rejected():
    for field,value in [('model','PDE'),('units',{'time':'year','distance':'km','traits':'unit_interval'})]:
        d=document(); d[field]=value
        with pytest.raises(ValueError): validate_design(d)
    d=document(); d['cohorts']['heldout']=[101,303]
    with pytest.raises(ValueError): validate_design(d)
    d=document(); d['families'][0]['cells']*=2
    with pytest.raises(ValueError): validate_design(d)
    d=document(); d['precision']['proportion_half_width']=.05
    with pytest.raises(ValueError): validate_design(d)
    d=document(); d['families'][0]['cells'][0]['config_patch']={'made_up':2}
    with pytest.raises(ValueError): validate_design(d)


def test_frozen_production_requires_all_families_and_verified_sources(tmp_path):
    d=document()
    with pytest.raises(ValueError): run_campaign(d,tmp_path/'out',mode='production')
    d['frozen']=True
    with pytest.raises(ValueError): validate_design(d)
    d=document(); d['source_hashes']['scripts/model3_island/types.py']='0'*64
    with pytest.raises(ValueError): run_campaign(d,tmp_path/'out',mode='pilot')


def test_resume_replay_and_collision_detection(tmp_path):
    d=document()
    a=run_campaign(d,tmp_path/'interrupted',mode='pilot',case_limit=1)
    assert a['completed']==1 and not a['complete']
    a=run_campaign(d,tmp_path/'interrupted',mode='pilot')
    b=run_campaign(d,tmp_path/'full',mode='pilot')
    assert a['complete'] and a['completed']==b['completed']==4
    for f in (tmp_path/'full').glob('*/arrays.npz'):
        with np.load(f) as x,np.load(tmp_path/'interrupted'/f.parent.name/'arrays.npz') as y:
            assert x.files==y.files
            for key in x.files: np.testing.assert_array_equal(x[key],y[key])
    receipt=next((tmp_path/'interrupted').glob('*/receipt.json'))
    bad=json.loads(receipt.read_text()); bad['case_hash']='wrong'; receipt.write_text(json.dumps(bad))
    with pytest.raises(ValueError): run_campaign(d,tmp_path/'interrupted',mode='pilot')
    changed=deepcopy(d); changed['families'][0]['cells'][0]['weight']=2.
    with pytest.raises(ValueError): run_campaign(changed,tmp_path/'full',mode='pilot')


def test_orphan_array_is_not_completion(tmp_path):
    d=document(); run_campaign(d,tmp_path,mode='pilot',case_limit=1)
    receipt=next(tmp_path.glob('*/receipt.json')); receipt.unlink()
    result=run_campaign(d,tmp_path,mode='pilot')
    assert result['complete'] and result['completed']==4

def test_compile_rejects_unexecutable_mutation_grid_and_pool_collision():
    d=document(); cell=d['families'][0]['cells'][0]
    cell['config_patch']={'mutation_rate':.1,'mutation_sd':.1}
    cell['grid_axes']=[[.2,.5,.8]]*3
    with pytest.raises(ValueError): validate_design(d)
    d=document(); cell=d['families'][0]['cells'][0]
    cell['history']['segments']=[{'years':1,'pool':0,'count':1,'optimum':.5,'sd':.1},
                                {'years':1,'pool':0,'count':2,'optimum':.5,'sd':.1}]
    with pytest.raises(ValueError): validate_design(d)


def test_budget_exhaustion_never_marks_partial_case_complete(tmp_path,monkeypatch):
    from scripts.model3_island import run
    d=document()
    class FakeMemory:
        rss=2**40
    class FakeProcess:
        def memory_info(self): return FakeMemory()
    monkeypatch.setattr(run.psutil,'Process',lambda:FakeProcess())
    status=run_campaign(d,tmp_path,mode='pilot')
    assert not status['complete'] and status['completed']==0
    assert status['stop_reason']=='memory_budget'
