"""Frozen renewal contrast: pure/synthetic tests, no scientific native updates."""
import numpy as np
import pytest
from scripts import ecological_I_renewal_20261015 as c

def test_exact_inventory_reuses_original_contexts_and_seeds():
    ts=list(c.tasks())
    assert len(ts)==len({c.key(t) for t in ts})==2304
    assert len(c.references(ts))==8
    assert c.NEW_MASK==(False,True,True) and c.OLD_MASK==(False,False,True)
    assert c.SCHEDULED_UPDATES==923216 and c.UPDATE_CAP==923232
    c.check_inventory(ts)

@pytest.mark.parametrize('how',['missing','duplicate','context','replicate'])
def test_invalid_inventory_rejected(how):
    ts=list(c.tasks())
    if how=='missing':ts.pop()
    elif how=='duplicate':ts[-1]=dict(ts[0])
    elif how=='context':ts[0]=dict(ts[0],supply=1.)
    else:ts[0]=dict(ts[0],replicate=128)
    with pytest.raises(ValueError):c.check_inventory(ts)

def test_caps_and_meaning_keep_old_nulls():
    assert c.reserve(0,c.SCHEDULED_UPDATES)==c.SCHEDULED_UPDATES
    with pytest.raises(ValueError):c.reserve(c.UPDATE_CAP,1)
    with pytest.raises(ValueError):c.reserve(0,-1)
    counts=dict(assurance_first=64,investment_first=64,near_simultaneous=0,assurance_only=0,investment_only=0,neither=0)
    r=c.cell_readout(counts)
    assert r['D']==0 and r['interval'][0]<0<r['interval'][1]
    counts['neither']=1
    with pytest.raises(ValueError):c.cell_readout(counts)

def test_only_I_mask_changes_in_producer():
    from types import SimpleNamespace
    state=SimpleNamespace(ids=np.array([0]),alleles=np.full((1,3,2),.5),allele_origin=np.zeros((1,3,2),int),mutation_flags=np.zeros((1,3,2),bool),birth_years=np.array([0]))
    calls=[]
    class Pop:
        @staticmethod
        def subset(s,ix):return s
        @staticmethod
        def advance(s,l,e,config,streams,**kw):
            calls.append(kw['mutation_traits']);return s,{'parentage':np.array([[0,0,0]])}
    ledger=SimpleNamespace(**{n:np.ones((1,1)) if n=='outcross' else np.ones(1) for n in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')})
    rand=SimpleNamespace(STREAM_IDS=['x'],stream=lambda *a:None)
    modules=(None,Pop,SimpleNamespace(reproduce=lambda *a:ledger),rand,None,None)
    task=next(c.tasks())
    c.produce(task,modules,initial=(None,state,None),horizon=2,renew=True)
    assert calls==[c.NEW_MASK]*2
    calls.clear();c.produce(task,modules,initial=(None,state,None),horizon=2,renew=False)
    assert calls==[c.OLD_MASK]*2


def test_independent_seed_exact_for_all_original_tasks():
    from scripts.ecological_I_renewal_replay_20261015 import independent_seed
    for task in c.tasks():assert independent_seed(task)==c.old.seed(task)


def test_replication_requires_same_direction_in_both_founders():
    rows=[]
    for t in c.tasks():
        category='neither'
        if t['context'] in (1,3):
            positive=(t['context']==1)==(t['block']=='main')
            category='assurance_first' if positive else 'investment_first'
        rows.append(dict(task=t,events=dict(category=category,A=None,I=None)))
    assert c.readout(rows,rows)['supported_supply_pairs']==[]


def test_source_drift_and_runtime_rejected_before_updates(tmp_path):
    import sys
    from scripts import run_ecological_I_renewal_20261015 as runner
    p=tmp_path/'source.py';p.write_bytes(b'original\n')
    import scipy
    frozen=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,files={'source.py':c.digest(p.read_bytes())})
    runner.verify_closure(frozen,tmp_path)
    p.write_bytes(b'changed\n')
    with pytest.raises(ValueError,match='source'):runner.verify_closure(frozen,tmp_path)
    frozen['python']='wrong'
    with pytest.raises(ValueError,match='runtime'):runner.verify_closure(frozen,tmp_path)


def test_original_reversal_rule_and_new_readout_agree_for_consistent_signs():
    from scripts.read_ecological_order_boundary_20261013 import summarize
    rows=[]
    for t in c.tasks():
        category='assurance_first' if t['context']==1 else 'investment_first' if t['context']==3 else 'neither'
        rows.append(dict(task=t,events=dict(category=category,A=2 if category!='neither' else None,I=10 if category!='neither' else None)))
    r=c.readout(rows,rows);old=summarize(rows)
    assert r['supported_supply_pairs']==old['supported_supply_pairs']
    assert len(r['supported_supply_pairs'])==1
    assert len(r['cells'])==18
    assert all(x['paired_D_change_descriptive']==0 for x in r['cells'])


def test_storage_cannot_escape_frozen_study_directory(tmp_path):
    from scripts import run_ecological_I_renewal_20261015 as runner
    freeze=tmp_path/'study/EXECUTION_FREEZE.json'
    assert runner.contained_output(freeze,tmp_path/'study/run')==(tmp_path/'study/run').resolve()
    for p in (tmp_path/'other/run',tmp_path/'study',tmp_path/'study/../escaped'):
        with pytest.raises(ValueError,match='storage'):runner.contained_output(freeze,p)

def test_scipy_version_is_part_of_execution_closure(tmp_path):
    import sys,scipy
    from scripts import run_ecological_I_renewal_20261015 as runner
    frozen=dict(python=sys.version,numpy=np.__version__,scipy='different',files={})
    with pytest.raises(ValueError,match='runtime'):runner.verify_closure(frozen,tmp_path)


def test_original_provider_capture_sidecar_is_explicit_and_exhaustive():
    from scripts import run_ecological_I_renewal_20261015 as runner
    providers=[f'shard_{i}.zip' for i in range(9)]
    runner.validate_provider_inventory(providers+['PROVIDER_CAPTURE_9.json'],providers)
    for names in (providers,providers+['unknown.json'],providers+['PROVIDER_CAPTURE_9.json','shard_0.zip']):
        with pytest.raises(ValueError):runner.validate_provider_inventory(names,providers)


def test_config_admission_normalizes_json_tuple_only():
    from scripts import run_ecological_I_renewal_20261015 as runner
    native={'source_allele_means':(.5,.5,.5),'activity':.2}
    saved={'source_allele_means':[.5,.5,.5],'activity':.2}
    assert runner.same_config(native,saved)
    assert not runner.same_config(native,dict(saved,activity=.21))


def reference_fixture():
    names=set(c.old.FIELDS)|{'offsets','means','population','parentage','parent_offsets','returns','sexual_selection'}
    return {name:np.ones(1) for name in names}

def test_reference_keeps_biology_exact_and_uses_original_diagnostic_screen():
    from scripts import run_ecological_I_renewal_20261015 as runner
    before=reference_fixture();after={k:v.copy() for k,v in before.items()}
    after['returns'][0]+=1e-14;after['sexual_selection'][0]+=1e-14
    r=runner.admit_reference(after,before)
    assert r['biological_arrays_exact'] is True
    for name in ('alleles','mutation_flags','means','parentage'):
        bad={k:v.copy() for k,v in before.items()};bad[name][0]=np.nextafter(1.,2.)
        with pytest.raises(AssertionError):runner.admit_reference(bad,before)

@pytest.mark.parametrize('name',['returns','sexual_selection'])
def test_reference_rejects_substantive_diagnostic_drift(name):
    from scripts import run_ecological_I_renewal_20261015 as runner
    before=reference_fixture();after={k:v.copy() for k,v in before.items()};after[name][0]+=.000001
    with pytest.raises(AssertionError):runner.admit_reference(after,before)


def test_technical_restart_requires_its_own_explicit_approval():
    from scripts import run_ecological_I_renewal_20261015 as runner
    a=dict(approved=False,prior_reserved_upper_bound=1616,combined_update_cap=924848,new_scientific_paths=2304)
    with pytest.raises(ValueError,match='restart approval'):runner.require_restart_approval(a)
    runner.require_restart_approval(dict(a,approved=True))
    with pytest.raises(ValueError):runner.require_restart_approval(dict(a,approved=True,new_scientific_paths=2305))


def test_false_restart_prevents_freeze_directory_or_input_reads(tmp_path,monkeypatch):
    import json
    from scripts import run_ecological_I_renewal_20261015 as runner
    flag=tmp_path/'data/design/ecological_I_renewal_technical_restart_20261015.json'
    flag.parent.mkdir(parents=True);flag.write_text(json.dumps(dict(approved=False)))
    monkeypatch.setattr(runner,'ROOT',tmp_path)
    out=tmp_path/'not_created'
    with pytest.raises(ValueError,match='restart approval'):runner.freeze(tmp_path/'missing',tmp_path/'missing',out)
    assert not out.exists()

def test_false_restart_prevents_native_run_output(tmp_path,monkeypatch):
    import json
    from scripts import run_ecological_I_renewal_20261015 as runner
    frozen=dict(closure={},source={},technical_restart_approval=dict(approved=False))
    p=tmp_path/'freeze.json';p.write_bytes(json.dumps(frozen).encode())
    monkeypatch.setattr(runner,'verify_closure',lambda *a:None)
    monkeypatch.setattr(runner,'verify_original',lambda *a:None)
    out=tmp_path/'not_created'
    with pytest.raises(ValueError,match='restart approval'):runner.run(p,c.digest(p.read_bytes()),out)
    assert not out.exists()
