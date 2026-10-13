"""Authenticate the recovered original ZIP and compare recorded replay fields only.

No archived code execution, biological advance, historical runtime or annual-genome
admission. Earlier failed/unavailable receipts remain unchanged.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import tempfile
import zipfile
from scripts.audit_independent32_replay_admission_20261013 import audit

ORIGINAL_SHA='cd9f998e38ec51e747c4495dbe94b1fe1168d48d31ef54a438250bfa0ace5a21'
REPLAY_SHA='e73fce6c37fc928e22f73b3f370e510cf2e310c25f7aaa94745f5164df9192f1'
DIAGNOSTIC='initial_viable_maternal_per_capita'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def checked_members(z):
    names=z.namelist()
    if len(names)!=len(set(names)):raise ValueError('duplicate archive member')
    for name in names:
        p=PurePosixPath(name)
        if '\\' in name or p.is_absolute() or '..' in p.parts or str(p)!=name:
            raise ValueError('unsafe archive member')
    if z.testzip() is not None:raise ValueError('archive CRC mismatch')
    return names


def logged_projection(rows):
    result=copy.deepcopy(rows)
    for row in result:
        for case in row['post_cases']:
            case.pop(DIAGNOSTIC)
    return sha(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False).encode())


def compare_records(a,b,path=()):
    if isinstance(a,dict):
        if not isinstance(b,dict) or set(a)!=set(b):raise ValueError('record keys differ')
        return [d for key in a for d in compare_records(a[key],b[key],path+(key,))]
    if isinstance(a,list):
        if not isinstance(b,list) or len(a)!=len(b):raise ValueError('record list differs')
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in compare_records(x,y,path+(i,))]
    if type(a) is not type(b):raise ValueError('record scalar type differs')
    if a==b:return []
    permitted=(len(path)==4 and isinstance(path[0],int) and path[1]=='post_cases'
               and isinstance(path[2],int) and path[3]==DIAGNOSTIC)
    if not permitted:raise ValueError('non-diagnostic recorded difference: '+repr(path))
    if not isinstance(a,(int,float)) or not math.isfinite(a) or not math.isfinite(b):
        raise ValueError('invalid diagnostic')
    delta=abs(a-b)
    if delta>1e-12:raise ValueError('diagnostic exceeds frozen tolerance')
    return [dict(path=list(path),original=a,replay=b,absolute_difference=delta)]


def inspect(archive,replay,design,frozen):
    original_raw=Path(archive).read_bytes();replay_raw=Path(replay).read_bytes()
    if len(original_raw)!=335015 or sha(original_raw)!=ORIGINAL_SHA:
        raise ValueError('original outer archive identity differs')
    if sha(replay_raw)!=REPLAY_SHA:raise ValueError('actual replay artifact identity differs')
    members=[];comparisons=[]
    with zipfile.ZipFile(io.BytesIO(original_raw)) as z, zipfile.ZipFile(io.BytesIO(replay_raw)) as r:
        names=checked_members(z);replay_names=checked_members(r)
        manifest=json.loads(z.read('demographic_stress_archive_manifest.json'))
        declared=manifest['source_files']
        if set(names)!=set(declared)|{'demographic_stress_archive_manifest.json'} or len(declared)!=26:
            raise ValueError('original manifest inventory differs')
        for name in sorted(declared):
            raw=z.read(name)
            if sha(raw)!=declared[name]:raise ValueError('original member identity differs: '+name)
            members.append(dict(name=name,bytes=len(raw),sha256=sha(raw)))
        with zipfile.ZipFile(io.BytesIO(z.read('sources.zip'))) as source:
            source_names=checked_members(source)
            if len(source_names)!=25:raise ValueError('archived source inventory differs')
            sources=[dict(name=name,bytes=len(source.read(name)),sha256=sha(source.read(name)))
                     for name in sorted(source_names)]
        with tempfile.TemporaryDirectory(prefix='pr490original-') as tmp:
            folder=Path(tmp)
            for i in range(8):
                name=f'demographic_independent32_shard_{i:02d}.json'
                matching=[x for x in replay_names if PurePosixPath(x).name==name]
                if len(matching)!=1:raise ValueError('actual replay shard inventory differs')
                original=z.read(name);actual=r.read(matching[0]);a=json.loads(original);b=json.loads(actual)
                changes=compare_records(a,b)
                if logged_projection(a)!=logged_projection(b):raise ValueError('logged projection differs')
                (folder/name).write_bytes(original)
                comparisons.append(dict(shard=i,groups=len(a),post_cases=sum(len(x['post_cases']) for x in a),
                    original_sha256=sha(original),actual_replay_sha256=sha(actual),byte_identical=original==actual,
                    logged_state_projection_sha256=logged_projection(a),projection_exact=True,
                    diagnostic_differences=changes,maximum_diagnostic_difference=max([x['absolute_difference'] for x in changes]+[0.])))
            numeric=audit(folder,design,frozen)
            if not numeric['numerical_agreement'] or not numeric['declared_byte_agreement']:
                raise ValueError('original numerical or frozen shard admission differs')
    return dict(status='ORIGINAL_OFFLINE_ZIP_DIRECTLY_AUTHENTICATED_AND_ACTUAL_REPLAY_LOGGED_FIELDS_MATCH',
        original_archive=dict(bytes=len(original_raw),sha256=sha(original_raw),members=len(names)),
        manifest_members_verified=members,nested_sources_verified=sources,
        actual_replay=dict(run_id=38272136110,sha256=sha(replay_raw)),shards=comparisons,numerical_admission=numeric,
        new_biological_histories=0,original_annual_genomes_authenticated=False,historical_executed_runtime_authenticated=False,
        limits=['Direct original ZIP and all recorded-field comparison, not full annual-genome or runtime replay.',
                'All archived source bytes verified as contents, not proof of historical execution.',
                'Only the predeclared handoff diagnostic may differ within the existing1e-12 tolerance.',
                'Earlier byte-divergence receipts preserved; pilot-informed grid and32-history study unit unchanged.'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('archive','replay','design','frozen','out'):p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():raise ValueError('refuse existing receipt')
    result=inspect(args.archive,args.replay,json.loads(args.design.read_bytes()),json.loads(args.frozen.read_bytes()))
    result.update(auditor_sha256=sha(Path(__file__).read_bytes()),
                  numerical_auditor_sha256=sha(Path(__file__).with_name('audit_independent32_replay_admission_20261013.py').read_bytes()),
                  design_sha256=sha(args.design.read_bytes()),frozen_sha256=sha(args.frozen.read_bytes()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k] for k in ('status','original_archive','new_biological_histories')}))


if __name__=='__main__':main()
