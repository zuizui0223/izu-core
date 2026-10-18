"""Technical validation only: no production seed consumption or science verdict."""
import copy
import json
import shutil
from pathlib import Path
import numpy as np
import pytest
from scripts import q3_native_runner_20261019 as r


def test_production_is_blocked_before_creating_outputs(tmp_path):
    p=r.technical_plan(); p['mode']='confirmation'
    with pytest.raises(ValueError,match='technical'):
        r.initialize(tmp_path/'bad',p)
    assert not (tmp_path/'bad').exists()
    p=r.technical_plan(); p['founders'][0]=401001
    with pytest.raises(ValueError,match='technical'):
        r.initialize(tmp_path/'bad',p)
    assert not (tmp_path/'bad').exists()


def test_matched_founders_and_disjoint_technical_streams():
    p=r.technical_plan(); s=r.founder(p['founders'][0])
    assert s.alleles.shape==(48,3,2)
    assert np.all(s.alleles[:,2,:].mean(axis=1)==.5)
    assert np.var(s.alleles[:,2,:])>0
    assert np.array_equal(s.alleles,r.founder(p['founders'][0]).alleles)
    seeds=[r.master(p,f,v,stage) for f in p['founders'] for v in p['visitors']
           for stage in ('prefix','fork')]
    assert len(set(seeds))==18 and all(0<=s<2**128 for s in seeds)
    assert r.budget(160,160)['unique_updates']==6400000
    assert r.budget(3,3)['unique_updates']==2250


@pytest.fixture(scope='module')
def completed(tmp_path_factory):
    root=tmp_path_factory.mktemp('continuous')/'run'
    r.initialize(root,r.technical_plan()); summary=r.run(root,save_every=35)
    assert summary['new_updates']==2250 and summary['complete']
    return root


def test_resume_equals_continuous_states_rng_and_inference(tmp_path,completed):
    root=tmp_path/'resumed'; r.initialize(root,r.technical_plan())
    assert r.run(root,max_updates=12,save_every=7)['new_updates']==12
    with pytest.raises(ValueError,match='incomplete'):
        r.collect(root)
    # Stop exactly at fork35, inside a branch, and after a branch boundary.
    for n in (23,13,32,1,57):
        assert r.run(root,max_updates=n,save_every=7)['new_updates']==n
    final=r.run(root,save_every=19)
    assert final['new_updates']==2250-(12+23+13+32+1+57)
    a=r.collect(root); b=r.collect(completed)
    assert a==b
    files=sorted((completed/'states').glob('*.npz'))
    assert len(files)==54
    for f in files:
        ma,aa=r.read_snapshot(f)
        mb,ab=r.read_snapshot(root/'states'/f.name)
        assert ma==mb
        for key in aa: np.testing.assert_array_equal(aa[key],ab[key])
    before={f.name:f.read_bytes() for f in (root/'states').glob('*.npz')}
    assert r.run(root)['new_updates']==0
    assert before=={f.name:f.read_bytes() for f in (root/'states').glob('*.npz')}


def test_full_source_trace_and_endpoint_mass(completed):
    result=r.collect(completed)
    assert result['status']=='TECHNICAL_PIPELINE_ONLY_NOT_SCIENTIFIC_EVIDENCE'
    assert result['saved_genotype_censuses']==2304
    assert result['confirmation_seeds_consumed']==0
    assert result['endpoint_analysis']['execution_authorized'] is False
    for arm in result['arms']:
        assert arm['alive_accessible']+arm['alive_closed']+arm['extinct']==9
        assert arm['genetic_first']+arm['extinction_first']+arm['alive_accessible']==9


def test_order_of_cells_does_not_change_rng_or_results(tmp_path,completed):
    root=tmp_path/'reverse'; p=r.technical_plan(); r.initialize(root,p)
    cells=list(reversed([(f,v) for f in p['founders'] for v in p['visitors']]))
    assert r.run(root,cells=cells,save_every=80)['new_updates']==2250
    assert r.collect(root)==r.collect(completed)


def test_resume_matches_direct_native_operator_without_checkpoint(tmp_path):
    p=r.technical_plan();root=tmp_path/'one'; r.initialize(root,p)
    f,v=p['founders'][0],p['visitors'][0]
    r.run(root,max_updates=48)
    spec=r.tasks(p,[(f,v)])[1]
    meta,arrays=r.read_snapshot(r.task_path(root,spec))
    s=r.founder(f); rng=r.rngs(r.master(p,f,v,'prefix'))
    full,sparse,empty=r.visitors(v); cfg=r.configuration('fixed',8.)
    for t in range(35):
        s,_=r.advance(s,r.reproduce(s,full if t<5 else sparse,cfg),
                      r.empty(s),cfg,rng,year=t,mutation_traits=(False,False,False))
    rng=r.rngs(r.master(p,f,v,'fork'))
    for t in range(35,48):
        s,_=r.advance(s,r.reproduce(s,empty,cfg),r.empty(s),cfg,rng,
                      year=t,mutation_traits=(False,False,False))
    saved=r.state_at(arrays,-1)
    for k in r.FIELDS: np.testing.assert_array_equal(getattr(saved,k),getattr(s,k))
    assert meta['rng']=={k:g.bit_generator.state for k,g in rng.items()}


def test_corrupt_state_or_rng_is_rejected(tmp_path,completed):
    root=tmp_path/'corrupt';shutil.copytree(completed,root)
    f=next((root/'states').glob('*.npz'))
    meta,arrays=r.read_snapshot(f)
    meta['rng']['parents']['state']['state']+=1
    # Deliberately retain old checksum, as a torn/tampered metadata record.
    arrays['_meta']=np.frombuffer(r.canonical(meta),dtype=np.uint8)
    with f.open('wb') as out:np.savez_compressed(out,**arrays)
    with pytest.raises(ValueError,match='checksum'):
        r.collect(root)


def test_missing_budget_and_wrong_contract_fail_closed(tmp_path,completed):
    root=tmp_path/'missing';shutil.copytree(completed,root)
    f=next((root/'states').glob('*_B4p5.npz')); f.unlink()
    with pytest.raises(ValueError,match='incomplete'): r.collect(root)
    other=tmp_path/'changed';shutil.copytree(completed,other)
    path=other/'RUN.json'; j=json.loads(path.read_text());j['plan']['fork']=36
    path.write_text(json.dumps(j))
    with pytest.raises(ValueError,match='contract'):r.run(other)


def test_source_drift_runtime_drift_and_duplicate_cells_rejected(tmp_path,monkeypatch):
    root=tmp_path/'drift';p=r.technical_plan();r.initialize(root,p)
    with pytest.raises(ValueError,match='duplicate'):
        r.run(root,cells=[(p['founders'][0],p['visitors'][0])]*2)
    original=r.provenance
    def changed():
        d=original();d['numpy']='not-the-original-runtime';return d
    monkeypatch.setattr(r,'provenance',changed)
    with pytest.raises(ValueError,match='source or runtime'):r.run(root)


def test_atomic_save_failure_retains_previous_checkpoint(tmp_path,monkeypatch):
    root=tmp_path/'atomic';r.initialize(root,r.technical_plan());r.run(root,max_updates=12)
    f=next((root/'states').glob('*.npz'));old=f.read_bytes()
    def fail(*args,**kwargs):raise OSError('injected interrupted rename')
    monkeypatch.setattr(r.os,'replace',fail)
    with pytest.raises(OSError,match='injected'):r.run(root,max_updates=1)
    assert f.read_bytes()==old
    assert not list((root/'states').glob('*.partial*'))
    assert not (root/'RUN.lock').exists()


def test_closed_then_extinct_is_genetic_first_not_zero_trait():
    assert r.events([.6,.4,None],.5)=={'first_G':1,'first_E':2,'G_first':True,'E_first':False}
    assert r.events([.6,None,None],.5)=={'first_G':None,'first_E':1,'G_first':False,'E_first':True}
    with pytest.raises(ValueError,match='resurrection'):r.events([.6,None,.4],.5)
    with pytest.raises(ValueError,match='increase'):r.events([.6,.4,.5],.5)


def test_independent_raw_reviewer_recovers_both_endpoints(completed):
    from scripts.audit_q3_native_pipeline_20261019 import audit
    report=audit(completed,r.collect(completed))
    assert report['status']=='TECHNICAL_RAW_PIPELINE_AUDIT_PASS'
    assert report['files']==54 and report['saved_states']==2304
    assert report['fork_start_matches']==36
    assert report['candidate_inference_matched'] is True


def test_checkpoint_writer_does_not_accept_foreign_genetic_material(tmp_path,completed):
    root=tmp_path/'foreign';shutil.copytree(completed,root)
    f=next((root/'states').glob('*_B8.npz'));m,a=r.read_snapshot(f)
    states=[r.state_at(a,t) for t in range(len(a['counts']))]
    from dataclasses import replace
    final=states[-1]
    if not len(final.ids):pytest.skip('technical cell extinct')
    edited=final.alleles.copy();edited[0,1,0]=.99
    states[-1]=replace(final,alleles=edited)
    r.save_snapshot(f,m,states) # valid checksum, biologically invalid archive
    with pytest.raises(ValueError,match='genotype/origin'):
        r.collect(root)
    from scripts.audit_q3_native_pipeline_20261019 import audit
    with pytest.raises(ValueError):audit(root,None)
