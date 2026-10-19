"""Partitioned LOCAL execution of the pinned 3x3 technical Model3 cohort.

Complete founder/visitor crossings (both A policies and both budgets) stay
in one shard. Each shard owns a separate directory and single-writer lock.
Production layouts are arithmetic-only; this module cannot run 160x160.
Neither native biology, native checkpointing, nor inference is modified.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager, ExitStack
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

from scripts import q3_native_runner_20261019 as native

NATIVE_DRIVER_BLOB='9c8ba3297df8c5a7655e0c5d1590af84de6858bd'
SCHEMA='q3_partitioned_technical_execution_v1'


def seal_hash(obj,field):
    return native.digest(native.canonical({k:v for k,v in obj.items() if k!=field}))


def _integer(x,lo,hi):
    if type(x) is not int or not lo<=x<=hi:raise ValueError('invalid bounded integer layout')


def _regular(path):
    path=Path(path)
    # Check ancestor directories as well as the leaf; shard receipts never
    # authorize following a symlink to an external run or snapshot.
    if any(x.is_symlink() for x in (path,*path.parents)):
        raise ValueError('symlink in technical artifact path')
    if not path.is_file():raise ValueError('missing file: '+path.name)
    return path


def _read(path):
    try:return json.loads(_regular(path).read_text(encoding='utf8'))
    except (OSError,json.JSONDecodeError) as e:raise ValueError('invalid JSON artifact') from e


def _write_new(path,value):
    with Path(path).open('x',encoding='utf8') as f:
        json.dump(value,f,sort_keys=True,indent=2,allow_nan=False)
        f.write('\n');f.flush();os.fsync(f.fileno())


def _file_sha(path):return hashlib.sha256(_regular(path).read_bytes()).hexdigest()


def _identity():
    raw=Path(native.__file__).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!=NATIVE_DRIVER_BLOB:raise ValueError('native driver changed')
    return dict(native=native.provenance(),
                partition_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


def dry_layout(nf=160,nv=160,shards=32):
    """Candidate arithmetic only: no founder RNG or native evolution calls."""
    _integer(nf,1,100000);_integer(nv,1,100000);_integer(shards,1,min(nf*nv,4096))
    n=nf*nv;counts=[n//shards+(i<n%shards) for i in range(shards)]
    return dict(crossings=n,prefix_tasks=2*n,branch_tasks=4*n,
                unique_updates=250*n,raw_array_bytes=n*256*(48*118+8),
                shards=[dict(id=i,crossings=k,prefix_tasks=2*k,branch_tasks=4*k,
                             unique_updates=250*k,raw_array_bytes=k*256*(48*118+8))
                        for i,k in enumerate(counts)],
                execution_authorized=False,scope='LAYOUT_ONLY_NO_BIOLOGICAL_SOURCES')


def _layout(plan,n):
    _integer(n,1,9)
    cells=[(f,v) for f in plan['founders'] for v in plan['visitors']]
    return [dict(id=i,cells=[list(x) for j,x in enumerate(cells) if j%n==i])
            for i in range(n)]


def shard_root(root,shard):
    _integer(shard,0,8)
    return Path(root)/'shards'/f'shard-{shard:03d}'


def prepare(root,shards=3):
    root=Path(root);plan=native.technical_plan();layout=_layout(plan,shards)
    if root.exists():raise ValueError('new empty partition root required')
    if any(p.is_symlink() for p in (root,*root.parents)):
        raise ValueError('symlink output parent')
    identity=_identity()
    parent=root.parent
    while not parent.exists():parent=parent.parent
    # Conservative technical array-only admission, not a prediction of
    # compressed production output size or a cloud-quota guarantee.
    space_required=2*native.budget(3,3)['uncompressed_padded_array_bytes']
    if shutil.disk_usage(parent).free<space_required:
        raise ValueError('insufficient free space for technical run and staging')
    root.mkdir(parents=True,exist_ok=False);(root/'shards').mkdir()
    hashes=[]
    for item in layout:
        c=native.initialize(shard_root(root,item['id']),plan)
        hashes.append(c['contract_sha256'])
    if len(set(hashes))!=1:raise ValueError('technical native contracts differ')
    m=dict(schema=SCHEMA,technical_plan=plan,shards=layout,
           native_contract_sha256=hashes[0],source_identity=identity,
           admission_raw_array_space_bytes=space_required,
           confirmation_authorized=False)
    m['manifest_sha256']=seal_hash(m,'manifest_sha256')
    # Manifest is last: interrupted initialization is not an admitted run.
    _write_new(root/'PARTITION.json',m)
    return m


def manifest(root):
    root=Path(root);m=_read(root/'PARTITION.json')
    if (m.get('schema')!=SCHEMA or m.get('technical_plan')!=native.technical_plan()
        or m.get('confirmation_authorized') is not False
        or m.get('manifest_sha256')!=seal_hash(m,'manifest_sha256')):
        raise ValueError('invalid technical partition contract')
    items=m.get('shards')
    if not isinstance(items,list) or items!=_layout(native.technical_plan(),len(items)):
        raise ValueError('partition layout differs from exact technical cohort')
    if m['source_identity']!=_identity():raise ValueError('partition source/runtime changed')
    if {p.name for p in (root/'shards').iterdir()}!={f'shard-{x["id"]:03d}' for x in items}:
        raise ValueError('unexpected shard inventory')
    for x in items:
        sr=shard_root(root,x['id']);_regular(sr/'RUN.json')
        c=native.contract(sr)
        if c['contract_sha256']!=m['native_contract_sha256']:
            raise ValueError('native shard identity differs')
    return m


@contextmanager
def _lock(path):
    # Local exclusive-file locking; no multi-host or object-store guarantee.
    path=Path(path);fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    try:
        os.write(fd,str(os.getpid()).encode());os.close(fd);fd=None
        yield
    finally:
        if fd is not None:os.close(fd)
        path.unlink()   # Only the lock successfully created by this invocation.


def _scan(root,m,idx,*,complete=False):
    _integer(idx,0,len(m['shards'])-1)
    sr=shard_root(root,idx);cells=[tuple(x) for x in m['shards'][idx]['cells']]
    specs=native.tasks(m['technical_plan'],cells)
    expected={native.task_path(sr,s).name:s for s in specs}
    found={p.name for p in (sr/'states').glob('*.npz')}
    if found-set(expected) or (complete and found!=set(expected)):
        raise ValueError('shard snapshot inventory missing or unexpected')
    records=[]
    for name in sorted(found):
        p=sr/'states'/name;_regular(p);spec=expected[name]
        meta,arrays=native.read_snapshot(p,m['native_contract_sha256'])
        seed=native.master(m['technical_plan'],spec['founder'],spec['visitor'],
                           'prefix' if spec['stage']=='prefix' else 'fork')
        if (meta['task']!=spec or meta['master']!=seed or
            not spec['start']<=meta['current']<=spec['end']):
            raise ValueError('shard snapshot task identity differs')
        if complete and meta['current']!=spec['end']:
            raise ValueError('incomplete native task')
        records.append(dict(name=name,file_sha256=_file_sha(p),
                            payload_sha256=meta['payload_sha256'],
                            current=meta['current'],end=spec['end'],
                            bytes=p.stat().st_size))
    return records,len(found)==len(expected) and all(x['current']==x['end'] for x in records)


def _validate_seal(root,m,idx):
    sr=shard_root(root,idx);p=sr/'SEALED.json'
    if not p.exists():raise ValueError('incomplete or unsealed shard')
    receipt=_read(p)
    if (receipt.get('receipt_sha256')!=seal_hash(receipt,'receipt_sha256')
        or receipt.get('id')!=idx or receipt.get('manifest_sha256')!=m['manifest_sha256']):
        raise ValueError('shard receipt identity mismatch')
    # Check whole-file digest before decoding a potentially damaged NPZ.
    expected=receipt.get('files')
    if not isinstance(expected,list):raise ValueError('invalid receipt files')
    for r in expected:
        name=r.get('name','')
        if Path(name).name!=name or not name.endswith('.npz'):
            raise ValueError('invalid receipt filename')
        if _file_sha(sr/'states'/name)!=r['file_sha256']:
            raise ValueError('snapshot hash differs from sealed receipt')
    records,done=_scan(root,m,idx,complete=True)
    if not done or records!=expected:raise ValueError('sealed receipt inventory mismatch')
    return receipt


def worker(root,shard,*,max_updates=None):
    root=Path(root);m=manifest(root);_integer(shard,0,len(m['shards'])-1)
    sr=shard_root(root,shard)
    with _lock(sr/'WORKER.lock'):
        if (sr/'RUN.lock').exists():raise FileExistsError('native lock needs review')
        if (sr/'SEALED.json').exists():
            _validate_seal(root,m,shard)
            return dict(shard=shard,new_updates=0,complete=True,confirmation_seeds_consumed=0)
        _scan(root,m,shard)
        result=native.run(sr,max_updates=max_updates,
                          cells=[tuple(x) for x in m['shards'][shard]['cells']])
        records,done=_scan(root,m,shard)
        if done:
            receipt=dict(id=shard,manifest_sha256=m['manifest_sha256'],files=records,
                         confirmation_seeds_consumed=0)
            receipt['receipt_sha256']=seal_hash(receipt,'receipt_sha256')
            _write_new(sr/'SEALED.json',receipt)
        return dict(shard=shard,new_updates=result['new_updates'],complete=done,
                    confirmation_seeds_consumed=0)


def _reuse_merged(dest,m,seals):
    rec=_read(dest/'MERGE_RECEIPT.json')
    if (rec.get('receipt_sha256')!=seal_hash(rec,'receipt_sha256')
        or rec.get('manifest_sha256')!=m['manifest_sha256']
        or rec.get('shard_receipts')!=[s['receipt_sha256'] for s in seals]):
        raise ValueError('merged receipt identity mismatch')
    if _file_sha(dest/'SUMMARY.json')!=rec['summary_sha256']:
        raise ValueError('merged summary hash mismatch')
    for s in seals:
        for r in s['files']:
            if _file_sha(dest/'states'/r['name'])!=r['file_sha256']:
                raise ValueError('merged snapshot hash mismatch')
    summary=native.collect(dest)
    if summary!=_read(dest/'SUMMARY.json'):raise ValueError('merged summary mismatch')
    return summary


def merge(root,destination):
    root=Path(root);dest=Path(destination);m=manifest(root)
    if any(x.is_symlink() for x in (dest,*dest.parents)):
        raise ValueError('symlink merge destination')
    if dest.resolve()==root.resolve() or root.resolve() in dest.resolve().parents:
        raise ValueError('destination must be outside worker tree')
    # Hold all per-shard locks in ID order while validating and copying.
    # Workers in different directories do not share a write lock.
    with _lock(root/'MERGE.lock'),ExitStack() as locks:
        for item in m['shards']:
            sr=shard_root(root,item['id']);locks.enter_context(_lock(sr/'WORKER.lock'))
            locks.enter_context(_lock(sr/'RUN.lock'))
        seals=[_validate_seal(root,m,x['id']) for x in m['shards']]
        if dest.exists():return _reuse_merged(dest,m,seals)
        dest.parent.mkdir(parents=True,exist_ok=True)
        required=native.budget(3,3)['uncompressed_padded_array_bytes']
        if shutil.disk_usage(dest.parent).free<required:
            raise ValueError('insufficient merge staging space')
        staging_parent=Path(tempfile.mkdtemp(prefix=dest.name+'.staging-',dir=dest.parent))
        staging=staging_parent/'complete'
        try:
            c=native.initialize(staging,m['technical_plan'])
            if c['contract_sha256']!=m['native_contract_sha256']:
                raise ValueError('collector contract differs')
            seen=set()
            for idx,seal in enumerate(seals):
                for r in seal['files']:
                    if r['name'] in seen:raise ValueError('duplicate task in aggregate')
                    seen.add(r['name']);p=staging/'states'/r['name']
                    shutil.copyfile(shard_root(root,idx)/'states'/r['name'],p)
                    if _file_sha(p)!=r['file_sha256']:raise ValueError('copy checksum differs')
                    with p.open('rb') as f:os.fsync(f.fileno())
            # Full native ancestry + array review before publication; zero evolution.
            result=native.collect(staging);_write_new(staging/'SUMMARY.json',result)
            receipt=dict(manifest_sha256=m['manifest_sha256'],
                         shard_receipts=[s['receipt_sha256'] for s in seals],
                         task_count=len(seen),saved_genotype_censuses=result['saved_genotype_censuses'],
                         summary_sha256=_file_sha(staging/'SUMMARY.json'),
                         confirmation_seeds_consumed=0)
            receipt['receipt_sha256']=seal_hash(receipt,'receipt_sha256')
            _write_new(staging/'MERGE_RECEIPT.json',receipt)
            if dest.exists():raise ValueError('merge destination appeared concurrently')
            os.rename(staging,dest)  # Atomic directory publication on this filesystem.
            return result
        finally:
            shutil.rmtree(staging_parent)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('init','worker','collect','layout'))
    p.add_argument('--root',type=Path);p.add_argument('--destination',type=Path)
    p.add_argument('--shards',type=int,default=3);p.add_argument('--shard',type=int)
    p.add_argument('--max-updates',type=int);p.add_argument('--axis-count',type=int,default=160)
    a=p.parse_args()
    if a.action=='layout':out=dry_layout(a.axis_count,a.axis_count,a.shards)
    else:
        if a.root is None:p.error('--root required')
        if a.action=='init':out=prepare(a.root,a.shards)
        elif a.action=='worker':out=worker(a.root,a.shard,max_updates=a.max_updates)
        else:
            if a.destination is None:p.error('--destination required')
            out=merge(a.root,a.destination)
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False))
