"""Freeze, then execute the approved bounded natural-state mean-policy study once."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import io
import json
import multiprocessing as mp
from pathlib import Path
import sys
import time
import zipfile

import numpy as np

from scripts import natural_order_mean_control_20261015 as contract
from scripts import natural_order_mean_replay_20261015 as consumer
from scripts import persistence_expression_mechanism_20261012 as native

ROOT = Path(__file__).resolve().parents[1]
MAX_PATH_BYTES = 1024**2
MAX_SECONDS = 4*3600
MAX_BYTES = 16*1024**3
FIELDS = native.FIELDS
CTX = None
INIT_ERROR = None
FROZEN_CLOSURE = None


def write_json(path, obj):
    with Path(path).open('x', encoding='utf8') as f:
        json.dump(obj, f, sort_keys=True, indent=2, allow_nan=False)
        f.write('\n')


def verify_closure(frozen, root=ROOT):
    if frozen['python'] != sys.version or frozen['numpy'] != np.__version__:
        raise ValueError('frozen runtime changed')
    for rel, sha in frozen['files'].items():
        path = root/rel
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('source closure path escape')
        if contract.digest(path.read_text(encoding='utf8').encode()) != sha:
            raise ValueError('frozen executable source drift: '+rel)


def closure():
    files = {}
    for module in list(sys.modules.values()):
        f = getattr(module, '__file__', None)
        if f and str(f).endswith('.py'):
            p = Path(f).resolve()
            if p.is_relative_to(ROOT) and p.relative_to(ROOT).parts[0] == 'scripts':
                files[p.relative_to(ROOT).as_posix()] = contract.digest(p.read_text(encoding='utf8').encode())
    for rel in ['tests/test_natural_order_mean_control_20261015.py',
                'data/design/natural_order_mean_execution_approval_20261015.json',
                'docs/NATURAL_ORDER_MEAN_CONTROL_EXECUTION_20261015.md']:
        files[rel] = contract.digest((ROOT/rel).read_text(encoding='utf8').encode())
    return dict(python=sys.version, numpy=np.__version__, files=files)


def key(task):
    return contract.digest(json.dumps(task, sort_keys=True).encode())[:24]


def original_path(original, row, target):
    return Path(original)/'archives/challenge'/(key(dict(row['task'],target=target))+'.npz')


def load_original(original, row, target):
    p = original_path(original,row,target)
    raw = p.read_bytes()
    if contract.digest(raw) != row['original_futures'][str(target)]:
        raise ValueError('original future archive drift')
    with np.load(io.BytesIO(raw),allow_pickle=False) as z:
        meta=json.loads(str(z['metadata'].item()))
        arrays={f:z[f].copy() for f in z.files if f!='metadata'}
    if meta['task'] != dict(row['task'],target=target) or meta['start'] != 200:
        raise ValueError('original future task identity')
    return arrays,meta


def validate_trace(d, *, horizon=200):
    required=set(FIELDS)|{'population','offsets','means','diagnostics','parentage'}
    if not required.issubset(d):
        raise ValueError('complete archived trace fields required')
    n=np.asarray(d['population']);off=np.asarray(d['offsets'])
    if n.shape!=(horizon+1,) or off.shape!=(horizon+2,) or not np.array_equal(np.diff(off),n):
        raise ValueError('complete census/offset layout required')
    if off[0]!=0 or (n<0).any() or (n>8).any() or off[-1]!=len(d['alleles']):
        raise ValueError('native capacity and offsets')
    if d['means'].shape!=(horizon+1,3) or d['diagnostics'].shape!=(horizon,11):
        raise ValueError('trace numerical layout')
    if d['parentage'].ndim!=2 or len(d['parentage'])!=sum(n[1:]) or d['parentage'].shape[1]!=3:
        raise ValueError('all inherited parentage required')
    if not np.isfinite(d['alleles']).all() or (d['alleles']<0).any() or (d['alleles']>1).any():
        raise ValueError('allele support')
    ptr=0
    for t, count in enumerate(n):
        lo,hi=map(int,off[t:t+2]);s={f:d[f][lo:hi] for f in FIELDS}
        if len(np.unique(s['ids']))!=count:
            raise ValueError('duplicate individual identity')
        if count:
            np.testing.assert_array_equal(d['means'][t],s['alleles'].mean(axis=(0,2)))
        elif not np.isnan(d['means'][t]).all() or n[t:].any():
            raise ValueError('absorbing extinction')
        if t:
            if not (s['birth_years']==200+t).all():
                raise ValueError('annual birth clock')
            parents=d['parentage'][ptr:ptr+count];ptr+=count
            np.testing.assert_array_equal(parents[:,0],s['ids'])
            previous=d['ids'][off[t-1]:off[t]]
            if not np.isin(parents[:,1:3],previous).all():
                raise ValueError('parent outside previous census')
    np.testing.assert_allclose(d['diagnostics'][:,0],d['diagnostics'][:,1]+d['diagnostics'][:,3],atol=1e-10,rtol=0)


def freeze(bank, original, out):
    from scripts.initial_assurance_mean_20261013 import source_gate
    source_gate()
    manifest,states=contract.read_bank(bank)
    baselines=[]
    original_native_source_checks={}
    for ix,row in enumerate(manifest['cases']):
        for target in contract.TARGETS:
            d,meta=load_original(original,row,target)
            validate_trace(d)
            if meta['config']!=manifest['configs'][str(target)]:
                raise ValueError('original config mismatch')
            if not original_native_source_checks:
                for old_path,old_sha in meta['identity']['files'].items():
                    normalized=old_path.replace('\\','/')
                    if '/scripts/' not in normalized or not normalized.endswith('.py'):continue
                    rel='scripts/'+normalized.split('/scripts/',1)[1]
                    before=Path(old_path).read_bytes()
                    if contract.digest(before)!=old_sha:raise ValueError('original frozen source drift')
                    if before.decode().replace('\r\n','\n')!=(ROOT/rel).read_text(encoding='utf8'):
                        raise ValueError('native biology changed: '+rel)
                    original_native_source_checks[rel]=dict(original_raw_sha256=old_sha,
                        normalized_sha256=contract.digest((ROOT/rel).read_text(encoding='utf8').encode()))
            for f in FIELDS:np.testing.assert_array_equal(d[f][:8],states[f][ix])
            baselines.append(dict(block=row['task']['block'],replicate=row['task']['replicate'],target=target,
                category=row['category'],native=int(d['population'][-1]>0),
                native_duration=int(np.count_nonzero(d['population'][1:])),sha256=row['original_futures'][str(target)]))
    approval=json.loads((ROOT/'data/design/natural_order_mean_execution_approval_20261015.json').read_text())
    if approval['approved'] is not True:
        raise ValueError('explicit execution approval missing')
    result=dict(schema='natural_mean_execution_freeze_v1',bank_sha256=contract.BANK_SHA,
        closure=closure(),baselines=baselines,workers=2,seconds_cap=MAX_SECONDS,bytes_cap=MAX_BYTES,
        update_cap=contract.UPDATE_CAP,scientific_paths=2048,reference_paths=8,replay_paths=2048,
        fixture_updates=4,scheduled_updates=820804,
        fixture='main replicate0 target1.05 normalized two updates producer+consumer; exactly4 updates',
        approval=approval,no_automatic_retry=True,original_native_source_checks=original_native_source_checks)
    write_json(out,result)
    source_zip=Path(out).with_suffix('.source.zip')
    with zipfile.ZipFile(source_zip,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for rel in result['closure']['files']:z.writestr(rel,(ROOT/rel).read_text(encoding='utf8').encode())
        z.writestr('EXECUTION_FREEZE.json',Path(out).read_bytes())
        z.writestr('NATIVE_STATE_BANK.zip',Path(bank).read_bytes())
    print(json.dumps(dict(status='FROZEN_NO_NEW_BIOLOGY',freeze_sha256=contract.digest(Path(out).read_bytes()),source_zip_sha256=contract.digest(source_zip.read_bytes()),files=len(result['closure']['files']))),flush=True)


def init_worker(bank,original,output,deadline,frozen_closure):
    global CTX, INIT_ERROR, FROZEN_CLOSURE
    CTX=None;INIT_ERROR=None;FROZEN_CLOSURE=frozen_closure
    try:
        verify_closure(frozen_closure)
        m,s=contract.read_bank(bank)
        visitors=native.VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
        CTX=(m,s,Path(original),Path(output),deadline,visitors)
    except Exception as error:
        # Returning the error through the task avoids Pool's initializer-respawn loop.
        INIT_ERROR=repr(error)


def work(job):
    if INIT_ERROR is not None:raise ValueError('worker source admission failed: '+INIT_ERROR)
    verify_closure(FROZEN_CLOSURE)
    stage,ix,target=job
    m,states,original,out,deadline,visitors=CTX
    if time.time()>=deadline:raise TimeoutError('four-hour cap')
    row=m['cases'][ix];task=dict(block=row['task']['block'],replicate=row['task']['replicate'],target=target)
    state=native.PlantState(**{f:states[f][ix].copy() for f in FIELDS})
    config=native.Config.from_dict(m['configs'][str(target)])
    dest=out/('references' if stage=='reference' else 'paths')/(key(task)+'.npz')
    if stage=='replay':
        actual=consumer.replay(state,visitors,config,task)
        with np.load(dest,allow_pickle=False) as z:
            if json.loads(str(z['metadata'].item()))['task']!=task:raise ValueError('replay task mismatch')
            for f,arr in actual.items():np.testing.assert_array_equal(arr,z[f])
        validate_trace(actual)
        verify_closure(FROZEN_CLOSURE)
        return dict(task=task,status='ALL_ARRAYS_REPLAY_EXACT',sha256=contract.digest(dest.read_bytes()))
    if stage=='reference':
        actual=native.trajectory(state,visitors,config,contract.future_seed(task),'native')
        expected,meta=load_original(original,row,target)
        for f,arr in actual.items():np.testing.assert_array_equal(arr,expected[f])
        mapping=None
    else:
        state,mapping=contract.equalize_mean(state)
        actual=native.trajectory(state,visitors,config,contract.future_seed(task),'native')
    validate_trace(actual)
    verify_closure(FROZEN_CLOSURE)
    buffer=io.BytesIO()
    np.savez_compressed(buffer,metadata=np.array(json.dumps(dict(task=task,category=row['category'],
        stage=stage,bank_sha256=contract.BANK_SHA,master_seed=contract.future_seed(task),
        config=asdict(config),mapping=mapping),sort_keys=True)),**actual)
    raw=buffer.getvalue()
    if len(raw)>MAX_PATH_BYTES:raise ValueError('predeclared per-path storage bound')
    with dest.open('xb') as f:f.write(raw)
    if time.time()>=deadline:raise TimeoutError('four-hour cap')
    return dict(task=task,category=row['category'],normalized=int(actual['population'][-1]>0),
        normalized_duration=int(np.count_nonzero(actual['population'][1:])),sha256=contract.digest(raw),mapping=mapping)


def run(freeze_path,freeze_sha,bank,original,output):
    raw=Path(freeze_path).read_bytes()
    if contract.digest(raw)!=freeze_sha:raise ValueError('published freeze drift')
    frozen=json.loads(raw);verify_closure(frozen['closure'])
    if not frozen['approval']['approved']:raise ValueError('execution not approved')
    out=Path(output)
    out.mkdir(exist_ok=False);(out/'references').mkdir();(out/'paths').mkdir()
    (out/'EXECUTION_FREEZE.json').write_bytes(raw)
    start=time.time();deadline=start+MAX_SECONDS;used=0;completed=0
    ledger=[]
    def reserve(stage,count):
        nonlocal used
        used=contract.reserve_updates(used,count)
        row=dict(stage=stage,reserved_updates=count,cumulative_reserved=used)
        ledger.append(row);write_json(out/f'RESERVATION_{len(ledger):02d}.json',row)
    def phase(stage,jobs):
        nonlocal completed
        verify_closure(frozen['closure'])
        reserve(stage,len(jobs)*200)
        records=[]
        pool=mp.get_context('spawn').Pool(2,initializer=init_worker,initargs=(str(bank),str(original),str(out),deadline,frozen['closure']))
        try:
            iterator=pool.imap_unordered(work,jobs,chunksize=1)
            while len(records)<len(jobs):
                remaining=deadline-time.time()
                if remaining<=0:raise TimeoutError('four-hour cap')
                try:r=iterator.next(timeout=min(30,remaining))
                except mp.TimeoutError:continue
                records.append(r);completed+=200
                write_json(out/(stage+'_'+key(r['task'])+'.json'),r)
                if len(records)%64==0:print(stage,len(records),'/',len(jobs),flush=True)
                if sum(p.stat().st_size for p in out.rglob('*') if p.is_file())>MAX_BYTES:
                    raise ValueError('16GiB cap')
            pool.close();pool.join()
        except BaseException:
            pool.terminate();pool.join();raise
        verify_closure(frozen['closure'])
        write_json(out/(stage.upper()+'_COMPLETE.json'),dict(paths=len(records),records=records))
        return records
    try:
        manifest,states=contract.read_bank(bank)
        verify_closure(frozen['closure'])
        reserve('two-step producer+consumer fixture',4)
        ix=next(i for i,r in enumerate(manifest['cases']) if r['task']['block']=='main' and r['task']['replicate']==0)
        s=native.PlantState(**{f:states[f][ix].copy() for f in FIELDS});c=native.Config.from_dict(manifest['configs']['1.05'])
        v=native.VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4));task=dict(block='main',replicate=0,target=1.05)
        treated,_=contract.equalize_mean(s)
        a=native.trajectory(treated,v,c,contract.future_seed(task),'native',horizon=2)
        b=consumer.replay(s,v,c,task,horizon=2)
        for f in a:np.testing.assert_array_equal(a[f],b[f])
        verify_closure(frozen['closure'])
        completed+=4;write_json(out/'FIXTURE.json',dict(status='FOUR_NATIVE_UPDATES_EXACT',updates=4))
        refs=[('reference',i,t) for i,r in enumerate(manifest['cases']) if r['task']['replicate'] in (0,1) for t in contract.TARGETS]
        if len(refs)!=8:raise ValueError('eight reference inventory')
        phase('reference',refs)
        jobs=[('production',i,t) for i in range(1024) for t in contract.TARGETS]
        produced=phase('production',jobs)
        replayed=phase('replay',[('replay',i,t) for i in range(1024) for t in contract.TARGETS])
        bases={(r['block'],r['replicate'],r['target']):r for r in frozen['baselines']}
        rows=[]
        for r in produced:
            t=r['task'];base=bases[(t['block'],t['replicate'],t['target'])]
            if r['category']!=base['category']:raise ValueError('historical label drift')
            rows.append(dict(base,normalized=r['normalized'],normalized_duration=r['normalized_duration']))
        contract.check_inventory(rows)
        readout=contract.describe(rows)
        readout.update(status='ALL2048_PRODUCTION_AND_INDEPENDENT_REPLAY_VERIFIED',source_freeze_sha256=freeze_sha,
            scientific_paths=2048,references=8,independent_replays=len(replayed),completed_updates=completed,
            cumulative_reserved_updates=used,cap=contract.UPDATE_CAP,elapsed_seconds=time.time()-start)
        verify_closure(frozen['closure'])
        write_json(out/'READOUT.json',readout);write_json(out/'ALL_START_OUTCOMES.json',rows)
        print('COMPLETE_VERIFIED',completed,'native updates',flush=True)
    except BaseException as error:
        write_json(out/'TECHNICAL_HOLD.json',dict(error=repr(error),reserved_updates_upper_bound=used,
            completed_updates_lower_bound=completed,elapsed_seconds=time.time()-start,no_automatic_retry=True))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['freeze','run'])
    p.add_argument('--bank',type=Path,required=True);p.add_argument('--original',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--freeze',type=Path);p.add_argument('--freeze-sha')
    a=p.parse_args()
    if a.action=='freeze':freeze(a.bank,a.original,a.out)
    else:
        if not a.freeze or not a.freeze_sha:p.error('run requires published --freeze and --freeze-sha')
        run(a.freeze,a.freeze_sha,a.bank,a.original,a.out)


if __name__=='__main__':main()
