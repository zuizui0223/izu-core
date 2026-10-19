import hashlib
import json
import numpy as np
import pytest
from scripts.readaptation_campaign_20261019 import checkpoint, admit_execution, future_config
from scripts.readaptation_contract_20261019 import load_contract, canonical


def approval():
    c=load_contract()
    return dict(schema='readaptation_actions_authorization_v1',execution_authorized=True,
                contract_sha256=hashlib.sha256(canonical(c)).hexdigest(),
                future_paths=10240,updates=819200,output_bytes=8*2**30,
                minimum_memory_bytes=2**30,minimum_disk_bytes=10*2**30,
                platform='github_actions',decision='user_explicit_20261019')


def test_admit_only_approved_unchanged_design():
    a=approval(); assert admit_execution(a,load_contract())==a
    for key,value in [('execution_authorized',False),('future_paths',10241),('output_bytes',9*2**30),('contract_sha256','0'*64)]:
        bad=dict(a);bad[key]=value
        with pytest.raises(ValueError): admit_execution(bad,load_contract())


def test_checkpoint_resume_and_missing_receipted_file(tmp_path):
    path=tmp_path/'one.npz'; calls=[]; validations=[]
    def produce(): calls.append(1);return dict(values=np.arange(3),label='synthetic')
    def validate(raw): validations.append(1);np.testing.assert_array_equal(raw['values'],np.arange(3))
    raw,one=checkpoint(path,[0],produce,validate)
    raw,two=checkpoint(path,[0],produce,validate)
    assert one==two and len(calls)==1 and len(validations)>=2
    path.unlink()
    with pytest.raises(ValueError,match='missing'): checkpoint(path,[0],produce,validate)
    assert len(calls)==1


def test_checkpoint_corruption_is_not_regenerated(tmp_path):
    path=tmp_path/'one.npz'
    checkpoint(path,[0],lambda:dict(x=np.arange(2)),lambda raw:None)
    path.write_bytes(b'bad')
    with pytest.raises(ValueError): checkpoint(path,[0],lambda:pytest.fail('rerun'),lambda raw:None)


def test_all_five_configs_have_same_biology():
    c=load_contract()
    configs=[future_config(c,d) for d in range(5)]
    assert [x.activity for x in configs]==[0,.25,.25,1,1]
    assert all(x.assurance_mode=='evolving' and x.years==80 and x.capacity==48 for x in configs)

def test_synthetic_cohort_future_archive_and_resume(tmp_path,monkeypatch):
    from scripts.readaptation_campaign_20261019 import process_cohort
    from test_readaptation_transfer_20261019 import synthetic_donor
    monkeypatch.setattr('scripts.readaptation_runtime_20261019.measure_resources',
                        lambda p:dict(available_memory=2*2**30,free_disk=20*2**30))
    c=load_contract();keys=[(0,0,'fixed',0,d,.5,0) for d in (0,4)]
    first=process_cohort(tmp_path,synthetic_donor(),(0,0,'fixed'),0,c,keys,0)
    before={str(p.relative_to(tmp_path)):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    second=process_cohort(tmp_path,synthetic_donor(),(0,0,'fixed'),0,c,keys,first[-1])
    assert first==second
    assert before=={str(p.relative_to(tmp_path)):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    assert len(first[2])==2

def test_workflow_never_runs_production_on_pr():
    import yaml
    from scripts.readaptation_contract_20261019 import ROOT
    w=yaml.safe_load((ROOT/'.github/workflows/readaptation-20261019.yml').read_text())
    assert w['jobs']['production']['if']=="github.event_name == 'workflow_dispatch'"
    assert w['jobs']['production']['needs']=='technical'
    assert w['concurrency']['cancel-in-progress'] is False
    assert w['permissions']==dict(contents='read',actions='read')

def test_actions_has_historical_source_commit_for_original_admission():
    import yaml
    from scripts.readaptation_contract_20261019 import ROOT
    w=yaml.safe_load((ROOT/'.github/workflows/readaptation-20261019.yml').read_text())
    checkout=next(s for s in w['jobs']['production']['steps'] if s.get('uses')=='actions/checkout@v4')
    assert checkout['with'].get('fetch-depth')==0

def test_actions_rerun_cannot_skip_checkpoint_restore():
    import yaml
    from scripts.readaptation_contract_20261019 import ROOT
    w=yaml.safe_load((ROOT/'.github/workflows/readaptation-20261019.yml').read_text())
    restore=next(s for s in w['jobs']['production']['steps'] if s.get('name')=='Restore explicitly selected prior checkpoint')
    assert 'github.run_attempt' in restore['if']
    assert 'GITHUB_RUN_ID' in restore['run']
