"""Technical scheduling checks, not new Q3 scientific histories."""
import copy
import json
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pytest
from scripts import q3_native_runner_20261019 as native
from scripts import q3_partitioned_runner_20261019 as split


def execute_worker(root, shard, cap=None):
    return split.worker(Path(root), shard, max_updates=cap)


def test_dry_layout_covers_candidate_without_creating_biological_sources(tmp_path):
    d=split.dry_layout(160,160,32)
    assert d['crossings']==25600 and d['prefix_tasks']==51200
    assert d['branch_tasks']==102400 and d['unique_updates']==6400000
    assert d['raw_array_bytes']==37172019200
    assert all(s['crossings']==800 and s['unique_updates']==200000 for s in d['shards'])
    assert d['execution_authorized'] is False
    assert not list(tmp_path.iterdir())
    for n in (0,True,2.5,25601):
        with pytest.raises(ValueError):split.dry_layout(160,160,n)


def test_prepare_pins_same_contract_and_disjoint_complete_crossings(tmp_path):
    root=tmp_path/'run';m=split.prepare(root,3)
    allcells=[tuple(c) for x in m['shards'] for c in x['cells']]
    expected=[(f,v) for f in native.technical_plan()['founders'] for v in native.technical_plan()['visitors']]
    assert len(allcells)==len(set(allcells))==9 and set(allcells)==set(expected)
    for x in m['shards']:
        c=native.contract(split.shard_root(root,x['id']))
        assert c['contract_sha256']==m['native_contract_sha256']
    with pytest.raises(ValueError):split.prepare(root,3)
    with pytest.raises(ValueError):split.prepare(tmp_path/'bad',10)


def test_manifest_rewrite_rehash_still_cannot_change_scope(tmp_path):
    root=tmp_path/'run';split.prepare(root,3)
    p=root/'PARTITION.json';m=json.loads(p.read_text())
    m['shards'][0]['cells'][0][0]=401001
    m['manifest_sha256']=split.seal_hash(m,'manifest_sha256')
    p.write_text(json.dumps(m))
    with pytest.raises(ValueError,match='layout|technical|partition'):
        split.worker(root,0)
    assert not list((root/'shards').rglob('*.npz'))


@pytest.fixture(scope='module')
def executed(tmp_path_factory):
    base=tmp_path_factory.mktemp('sharding')
    root=base/'parallel';split.prepare(root,3)
    paused=split.worker(root,0,max_updates=48)
    assert paused['new_updates']==48 and not paused['complete']
    assert not (split.shard_root(root,0)/'SEALED.json').exists()
    with pytest.raises(ValueError,match='incomplete|unsealed'):
        split.merge(root,base/'too_early')
    with ProcessPoolExecutor(max_workers=3, mp_context=multiprocessing.get_context('spawn')) as pool:
        # Deliberately reverse completion submission order.
        results=list(pool.map(execute_worker,[str(root)]*3,[2,1,0]))
    assert sum(x['new_updates'] for x in results)+48==2250
    assert all(x['complete'] for x in results)
    merged=base/'merged';summary=split.merge(root,merged)
    single=base/'single';native.initialize(single,native.technical_plan())
    assert native.run(single)['new_updates']==2250
    assert summary==native.collect(single)
    return base,root,merged,single


def test_concurrent_resume_matches_every_serial_state_and_rng(executed):
    _,root,merged,single=executed
    for spec in native.tasks(native.technical_plan()):
        a,aa=native.read_snapshot(native.task_path(merged,spec))
        b,bb=native.read_snapshot(native.task_path(single,spec))
        assert a==b   # Includes every named RNG state and parent payload hash.
        for k in aa:np.testing.assert_array_equal(aa[k],bb[k])
    receipt=json.loads((merged/'MERGE_RECEIPT.json').read_text())
    assert receipt['task_count']==54 and receipt['saved_genotype_censuses']==2304
    before={p.name:p.read_bytes() for p in (merged/'states').glob('*.npz')}
    assert split.merge(root,merged)==native.collect(single)
    assert before=={p.name:p.read_bytes() for p in (merged/'states').glob('*.npz')}
    assert all(split.worker(root,i)['new_updates']==0 for i in range(3))


def clone_run(executed,tmp_path):
    import shutil
    _,root,_,_=executed
    dst=tmp_path/'corrupted';shutil.copytree(root,dst);return dst


def test_missing_and_foreign_files_block_merge(executed,tmp_path):
    root=clone_run(executed,tmp_path);sr=split.shard_root(root,0)
    p=next((sr/'states').glob('*.npz'));backup=p.read_bytes();p.unlink()
    with pytest.raises(ValueError,match='inventory|missing'):
        split.merge(root,tmp_path/'out')
    p.write_bytes(backup)
    (sr/'states'/'unexpected.npz').write_bytes(backup)
    with pytest.raises(ValueError,match='inventory|unexpected'):
        split.merge(root,tmp_path/'out')
    assert not (tmp_path/'out').exists()


def test_changed_snapshot_or_receipt_blocks_merge(executed,tmp_path):
    root=clone_run(executed,tmp_path);sr=split.shard_root(root,0)
    p=next((sr/'states').glob('*.npz'));b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]))
    with pytest.raises(ValueError,match='hash|checksum|snapshot'):
        split.merge(root,tmp_path/'out')
    p.write_bytes(b)
    receipt=sr/'SEALED.json';d=json.loads(receipt.read_text());d['id']=1
    d['receipt_sha256']=split.seal_hash(d,'receipt_sha256');receipt.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='receipt|identity'):
        split.merge(root,tmp_path/'out')


def test_locks_and_symbolic_files_fail_closed(executed,tmp_path):
    root=clone_run(executed,tmp_path);sr=split.shard_root(root,0)
    lock=sr/'WORKER.lock';lock.write_text('simulated other process')
    with pytest.raises(FileExistsError):split.worker(root,0)
    assert lock.exists();lock.unlink()
    p=next((sr/'states').glob('*.npz'));back=tmp_path/'external.npz';back.write_bytes(p.read_bytes())
    p.unlink();p.symlink_to(back)
    with pytest.raises(ValueError,match='symlink'):
        split.merge(root,tmp_path/'out')


def test_partial_native_lock_not_silently_removed(tmp_path):
    root=tmp_path/'run';split.prepare(root,3);sr=split.shard_root(root,0)
    lock=sr/'RUN.lock';lock.write_text('stale-lock-review-required')
    with pytest.raises(FileExistsError):split.worker(root,0)
    assert lock.exists() and not (sr/'WORKER.lock').exists()


def test_failed_merge_publishes_no_partial_result_and_retries(executed,tmp_path,monkeypatch):
    import shutil
    root=clone_run(executed,tmp_path);dest=tmp_path/'out';real=shutil.copyfile;count=[0]
    def broken(src,dst,*a,**kw):
        count[0]+=1
        if count[0]==3:raise OSError('injected copy failure')
        return real(src,dst,*a,**kw)
    with monkeypatch.context() as m:
        m.setattr(split.shutil,'copyfile',broken)
        with pytest.raises(OSError,match='injected'):split.merge(root,dest)
    assert not dest.exists() and not (root/'MERGE.lock').exists()
    assert split.merge(root,dest)['saved_genotype_censuses']==2304


def test_bad_completed_summary_cannot_be_reused(executed,tmp_path):
    root=clone_run(executed,tmp_path);dest=tmp_path/'out';split.merge(root,dest)
    p=dest/'SUMMARY.json';d=json.loads(p.read_text());d['confirmation_seeds_consumed']=1
    p.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='summary|receipt'):
        split.merge(root,dest)


def test_storage_preflight_blocks_writes(tmp_path,monkeypatch):
    from collections import namedtuple
    usage=namedtuple('usage','total used free')
    monkeypatch.setattr(split.shutil,'disk_usage',lambda _:usage(10,9,1))
    with pytest.raises(ValueError,match='space'):
        split.prepare(tmp_path/'run',3)
    assert not (tmp_path/'run').exists()
