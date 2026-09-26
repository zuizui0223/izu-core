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
        storage={'density_counts':'checkpoints_and_replay_digest','checkpoint_every':100},
        base_config=c,units={'time':'reproductive_year','distance':'dispersal_scale','traits':'unit_interval'},
        parameter_ranges={'trait':[0.,1.],'distance':[0.,10.]},
        mechanism_flags={'self_exclusion':True,'fixed_inbreeding_depression':True,'evolving_load':False},
        cohorts={'pilot':[101,102],'production':[201,202],'heldout':[301,302]},
        demographic_seeds=[1,2],founder_seed=7,
        numerical_tolerances={'trait':.02,'occupancy':.1},effect_thresholds={'investment':.05},
        horizons=[2],precision={'proportion_half_width':.7,'confidence':.95,'max_histories':2,
            'conditional_rule':'fixed_R_report_interval_and_eligible_n','rare_event_rule':'report_upper_bound'},
        resource_limits={'runtime_seconds':60.,'memory_mb':1024.,'output_mb':16.,'min_free_mb':100.},source_hashes=source_hashes(),
        claim_exclusions=['PDE','Q1_fit','drift_only','continuous_trait_convergence'],
        families=[{'name':'chronology','question':'same exposure, different order',
          'cells':[{'id':'control','kind':'trajectory','config_patch':{},
            'grid_axes':[[0.,.5,1.]]*3,'founders':{'count':4,'means':[.5,.5,.5],'sd':.1,'birth_year':0},
            'history':{'kind':'segments','segments':[{'years':2,'pool':0,'count':2,'optimum':.5,'sd':.1}]},
            'cohorts':['pilot','production','heldout'],'weight':1.,'start_id':'s1','pair_group':'order',
            'projection_mode':'grid','immigration_mode':'source','counterfactual':None}]}])


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

def test_seed_arrivals_can_be_restricted_to_recovery_window():
    from dataclasses import replace
    from scripts.model3_island.run import history_from_spec
    c=replace(config_fixture(),years=4,seed_arrival=replace(config_fixture().seed_arrival,supply=100.,distance=0.))
    h=history_from_spec(c,{'kind':'assembly','seed_window':[2,4]},101)
    assert [len(p.ids) for p in h.seed_candidates[:2]]==[0,0]
    assert all(len(p.ids)>0 for p in h.seed_candidates[2:])
    assert all(np.all(p.birth_years==year+1) for year,p in enumerate(h.seed_candidates))

def test_ecological_campaign_has_declared_controls_and_disjoint_pilot():
    from scripts.model3_island.campaign import build_design
    from scripts.model3_island.design import FAMILIES
    d=build_design(pilot=False)
    validate_design(d)
    assert d['frozen'] is True
    assert {f['name'] for f in d['families']}==FAMILIES
    cells=[c for f in d['families'] for c in f['cells']]
    assert any(c['immigration_mode']=='resident_matched' for c in cells)
    assert {c['projection_mode'] for c in cells}=={'continuous','grid'}
    assert any(c['config_patch'].get('survival',0)>.8 for c in cells)
    assert any(c['founders']['count']==0 for c in cells)
    assert any(c['config_patch'].get('years',0)>=2000 for c in cells)
    assert all(c['cohorts']==['production','heldout'] for c in cells if c['pair_group'].startswith('transport_'))
    p=build_design(pilot=True)
    validate_design(p)
    assert not p['frozen'] and p['cohorts']==d['cohorts']
    assert all(c['cohorts']==['pilot'] for f in p['families'] for c in f['cells'])

def test_density_checkpoint_storage_is_replay_verifiable():
    from scripts.model3_island.storage import pack_result,verify_replay
    raw={'density_counts':np.arange(42.).reshape(7,6),'population':np.array([2]*7)}
    options={'density_counts':'checkpoints_and_replay_digest','checkpoint_every':3}
    packed=pack_result(raw,options)
    assert 'density_counts' not in packed
    assert packed['density_checkpoint_years'].tolist()==[0,3,6]
    np.testing.assert_array_equal(packed['density_checkpoints'],raw['density_counts'][[0,3,6]])
    assert verify_replay(packed,raw,options)
    changed=deepcopy(raw); changed['density_counts'][2,2]+=.01
    with pytest.raises(ValueError): verify_replay(packed,changed,options)

def test_capacity_series_preserves_initial_genotype_frequencies():
    from scripts.model3_island.run import founders_from_spec
    spec={'count':4,'draw_count':4,'means':[.5]*3,'sd':.15,'birth_year':0}
    small=founders_from_spec(spec,71)
    large=founders_from_spec({**spec,'count':16},71)
    np.testing.assert_array_equal(large.alleles,np.tile(small.alleles,(4,1,1)))
    assert len(np.unique(large.allele_origin))==16*6

def test_resume_requires_source_snapshot_and_matching_runtime(tmp_path):
    d=document(); run_campaign(d,tmp_path,mode='pilot',case_limit=1)
    snapshot=tmp_path/'source_snapshot.zip'
    original=snapshot.read_bytes();snapshot.write_bytes(b'broken')
    with pytest.raises(ValueError): run_campaign(d,tmp_path,mode='pilot')
    snapshot.write_bytes(original)
    runtime=json.loads((tmp_path/'runtime.json').read_text());runtime['numpy']='different'
    (tmp_path/'runtime.json').write_text(json.dumps(runtime))
    with pytest.raises(ValueError): run_campaign(d,tmp_path,mode='pilot')

def test_saved_campaign_can_be_stream_audited_and_summary_omits_raw_states(tmp_path):
    from scripts.model3_island.audit import audit_campaign
    from scripts.model3_island.summarize import load_records
    d=document();run_campaign(d,tmp_path,mode='pilot')
    result=audit_campaign(d,tmp_path,mode='pilot',replay_per_cell=True)
    assert result['status']=='passed' and result['cases_checked']==4 and result['replayed']==1
    rows=load_records(d,tmp_path,mode='pilot')
    assert 'state_alleles' not in rows[0]['result']
    assert 'trait_mean' in rows[0]['result']
