"""Transfer the unchanged 3x3 technical cohort across isolated Actions jobs.

Artifacts carry exact source/run identity and checksums; they do not authorize
160x160 production, supply global filesystem locks, or sign scientific data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

from scripts import q3_partitioned_runner_20261019 as part

SCHEMA='q3_actions_technical_transfer_v1'
HEADER='TRANSFER.json'
MAX_BYTES=64*1024*1024


def _identity(source,batch):
    if not re.fullmatch(r'[a-f0-9]{40}',source) or not re.fullmatch(r'[0-9]+-[0-9]+',batch):
        raise ValueError('invalid Actions source/run identity')


def _hash(raw):return hashlib.sha256(raw).hexdigest()


def _plan_names():
    return {'PARTITION.json'}|{f'shards/shard-{i:03d}/RUN.json' for i in range(3)}


def pack(root,output,*,source,batch,shard=None):
    _identity(source,batch);root=Path(root);output=Path(output)
    if output.exists():raise ValueError('artifact already exists')
    m=part.manifest(root)
    if len(m['shards'])!=3:raise ValueError('exactly three technical shards required')
    if shard is None:
        if list(root.rglob('*.npz')) or list(root.rglob('SEALED.json')):
            raise ValueError('initial plan must not include evolved states')
        names=_plan_names()
    else:
        if type(shard) is not int or shard not in (0,1,2):
            raise ValueError('technical shard outside 0..2')
        seal=part._validate_seal(root,m,shard)
        base=f'shards/shard-{shard:03d}/'
        names={base+'RUN.json',base+'SEALED.json'}|{
            base+'states/'+r['name'] for r in seal['files']}
    data={name:part._regular(root/name).read_bytes() for name in sorted(names)}
    if sum(map(len,data.values()))>MAX_BYTES:raise ValueError('technical artifact too large')
    metadata=dict(schema=SCHEMA,source_commit=source,batch=batch,shard=shard,
        manifest_sha256=m['manifest_sha256'],confirmation_authorized=False,
        files={n:dict(sha256=_hash(b),bytes=len(b)) for n,b in data.items()})
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(HEADER,json.dumps(metadata,sort_keys=True,allow_nan=False))
        for name,raw in data.items():z.writestr(name,raw)
    return metadata


def _read_packet(path,source,batch):
    _identity(source,batch)
    with zipfile.ZipFile(path) as z:
        info=z.infolist();names=[i.filename for i in info]
        if len(names)!=len(set(names)) or HEADER not in names or len(names)>24:
            raise ValueError('artifact inventory is duplicated or missing')
        if sum(i.file_size for i in info)>MAX_BYTES:
            raise ValueError('technical artifact too large')
        if any(stat.S_ISLNK(i.external_attr>>16) for i in info):
            raise ValueError('symlink in artifact')
        meta=json.loads(z.read(HEADER))
        if (meta.get('schema')!=SCHEMA or meta.get('source_commit')!=source
            or meta.get('batch')!=batch or meta.get('confirmation_authorized') is not False):
            raise ValueError('artifact source/run identity mismatch')
        fs=meta.get('files')
        if not isinstance(fs,dict) or set(names)!={HEADER}|set(fs):
            raise ValueError('artifact inventory differs from receipt')
        data={n:z.read(n) for n in fs}
        for name,raw in data.items():
            if fs[name]!=dict(sha256=_hash(raw),bytes=len(raw)):
                raise ValueError('artifact payload digest mismatch')
    return meta,data


def restore(packet,root,*,source,batch):
    """Only whitelist expected files; never use ZIP extractall or overwrite data."""
    root=Path(root);meta,data=_read_packet(packet,source,batch)
    if any(p.is_symlink() for p in (root,*root.parents)):
        raise ValueError('symlink output path')
    shard=meta['shard']
    if shard is None:
        if set(data)!=_plan_names():raise ValueError('unexpected initial plan inventory')
        if root.exists():raise ValueError('restore destination exists')
        m=json.loads(data['PARTITION.json'])
        if (m.get('manifest_sha256')!=meta['manifest_sha256']
            or m.get('manifest_sha256')!=part.seal_hash(m,'manifest_sha256')
            or m.get('technical_plan')!=part.native.technical_plan()
            or m.get('source_identity')!=part._identity()
            or m.get('shards')!=part._layout(part.native.technical_plan(),3)):
            raise ValueError('technical plan/source identity mismatch')
    else:
        if type(shard) is not int or shard not in (0,1,2):
            raise ValueError('technical shard outside 0..2')
        m=part.manifest(root)
        if meta['manifest_sha256']!=m['manifest_sha256']:
            raise ValueError('shard parent plan identity differs')
        base=f'shards/shard-{shard:03d}/'
        tasks=part.native.tasks(m['technical_plan'],[tuple(x) for x in m['shards'][shard]['cells']])
        expected={base+'RUN.json',base+'SEALED.json'}|{
            base+'states/'+part.native.task_path(root,t).name for t in tasks}
        if set(data)!=expected:raise ValueError('unexpected shard payload inventory')
        sr=part.shard_root(root,shard)
        if list((sr/'states').iterdir()) or (sr/'SEALED.json').exists():
            raise ValueError('shard destination exists or is not empty')
        if data[base+'RUN.json']!=(sr/'RUN.json').read_bytes():
            raise ValueError('shard initial contract differs')
    # Whitelist verification finishes before any file is written. If the disk
    # fails mid-copy, no completion is claimed; the final native collector refuses it.
    for name,raw in data.items():
        p=root/name
        if shard is not None and name.endswith('/RUN.json'):continue
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(raw)
    if shard is None:
        for i in range(3):(part.shard_root(root,i)/'states').mkdir(exist_ok=True)
        part.manifest(root)
    else:
        part._validate_seal(root,m,shard)
    return dict(status='ACTIONS_TRANSFER_VERIFIED',shard=shard,
                source_commit=source,batch=batch,confirmation_authorized=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('pack','restore'))
    p.add_argument('--root',required=True,type=Path)
    p.add_argument('--packet',required=True,type=Path)
    p.add_argument('--source',required=True);p.add_argument('--batch',required=True)
    p.add_argument('--shard',type=int)
    a=p.parse_args()
    if a.action=='pack':out=pack(a.root,a.packet,source=a.source,batch=a.batch,shard=a.shard)
    else:out=restore(a.packet,a.root,source=a.source,batch=a.batch)
    print(json.dumps(out,sort_keys=True,allow_nan=False))

if __name__=='__main__':main()
