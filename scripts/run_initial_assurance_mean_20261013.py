"""Admit immutable references, then execute only the frozen mean intervention."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile
import numpy as np
from scripts import initial_assurance_mean_20261013 as design
from scripts import persistence_expression_mechanism_20261012 as old
from scripts.aggregate_persistence_mechanism_20261012 import validate_trace
from scripts.model3_island.types import Config,PlantState,VisitorState


def json_write(path,value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def arrays(raw):
    with np.load(io.BytesIO(raw),allow_pickle=False) as z:return {k:z[k].copy() for k in z.files}


def inputs(path):
    design.source_gate();m,s,b=old.read_inputs(path,design.INPUT_SHA)
    lookup={(r['block'],r['replicate'],r['origin']):i for i,r in enumerate(m['states'])}
    domain={(b,r,o) for b in old.BLOCKS for r in range(512) for o in old.ORIGINS}
    if len(lookup)!=2048 or set(lookup)!=domain:raise ValueError('initial2048 identity domain differs')
    return m,s,b,lookup


def original_state(s,ix):return PlantState(**{f:s[f][ix].copy() for f in old.FIELDS})


def admit_references(input_path,archive,out):
    m,s,baseline,lookup=inputs(input_path)
    raw=Path(archive).read_bytes()
    if old.digest(raw)!=design.PRIOR_SHA:raise ValueError('prior raw ZIP differs')
    out=Path(out)
    if out.exists():raise ValueError('refuse reference overwrite')
    out.mkdir(parents=True);(out/'technical').mkdir()
    expected={old.case_key(dict(t,policy=p)) for t in design.tasks() for p in ('native','A_fixed')}
    seen=set();records=[];identity_files={};x=np.zeros((2,512,2,2,2),np.int8)
    curves=np.zeros((2,512,2,2,2,201),np.int8)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for shard in range(16):
            prefix=f'mechanism-shard-{shard}/';sr=json.loads(z.read(prefix+'SHARD.json'))
            if sr['status']!='complete_verified' or sr['shard']!=shard or sr['cases']!=1280 or sr['input_sha256']!=design.INPUT_SHA:
                raise ValueError('prior shard identity/status differs')
            if sr['execution_commit']!='4cf462f8aa5275c901f4c612078e1a62c373004c':raise ValueError('prior source identity differs')
            for rec in sr['records']:
                t=rec['task']
                if t['policy'] not in ('native','A_fixed'):continue
                key=old.case_key(t)
                if key not in expected or key in seen or old.shard_for(t)!=shard or rec['archive']!=key+'.npz':
                    raise ValueError('prior8192 inventory differs')
                seen.add(key);body=z.read(prefix+key+'.npz')
                if old.digest(body)!=rec['sha256']:raise ValueError('prior case byte hash differs')
                separate=json.loads(z.read(prefix+key+'.json'))
                if separate!=rec:raise ValueError('prior separate receipt differs')
                trace=arrays(body);meta=json.loads(str(trace['metadata'].item()))
                if meta['task']!=t or meta['input_sha256']!=design.INPUT_SHA or meta['config']!=m['configs'][str(t['target'])]:
                    raise ValueError('prior metadata differs')
                ix=lookup[t['block'],t['replicate'],t['origin']];initial=original_state(s,ix)
                cfg=Config.from_dict(meta['config']);validate_trace(trace,initial,cfg)
                if t['policy']=='native':old.verify_native(trace,baseline,ix*2+old.TARGETS.index(t['target']))
                occupied=bool(trace['population'][-1])
                if occupied!=rec['terminal_occupied']:raise ValueError('prior endpoint differs')
                index=(old.BLOCKS.index(t['block']),t['replicate'],old.TARGETS.index(t['target']),('native','A_fixed').index(t['policy']),old.ORIGINS.index(t['origin']))
                x[index]=occupied;curves[index]=(trace['population']>0).astype(np.int8)
                records.append(dict(task=t,raw_sha256=rec['sha256'],terminal_occupied=occupied))
                if t['policy']=='A_fixed' and t['replicate']==0:
                    relative='technical/'+key+'.npz';(out/relative).write_bytes(body);identity_files[relative]=rec['sha256']
        if seen!=expected or len(seen)!=8192 or len(identity_files)!=8:raise ValueError('incomplete prior references')
    np.savez_compressed(out/'references.npz',occupied=x,curves=curves)
    identity_files['references.npz']=old.digest((out/'references.npz').read_bytes())
    json_write(out/'REFERENCE.json',dict(status='ALL8192_PRIOR_REFERENCES_ADMITTED',raw_zip_sha256=design.PRIOR_SHA,
        input_sha256=design.INPUT_SHA,records=records,cases=8192,files=identity_files))
    print('ALL8192_PRIOR_REFERENCES_ADMITTED',flush=True)


def references(root):
    root=Path(root);r=json.loads((root/'REFERENCE.json').read_bytes())
    if r['status']!='ALL8192_PRIOR_REFERENCES_ADMITTED' or r['raw_zip_sha256']!=design.PRIOR_SHA or r['input_sha256']!=design.INPUT_SHA or r['cases']!=8192:
        raise ValueError('reference admission differs')
    expected={old.case_key(dict(t,policy=p)):dict(t,policy=p) for t in design.tasks() for p in ('native','A_fixed')}
    technical={'technical/'+key+'.npz' for key,t in expected.items() if t['replicate']==0 and t['policy']=='A_fixed'}
    if set(r['files'])!=technical|{'references.npz'} or len(r['records'])!=8192:
        raise ValueError('reference inventory incomplete')
    for name,h in r['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts or old.digest((root/name).read_bytes())!=h:
            raise ValueError('reference payload differs')
    with np.load(root/'references.npz',allow_pickle=False) as z:
        occupied=z['occupied'].copy();curves=z['curves'].copy()
    if occupied.shape!=(2,512,2,2,2) or curves.shape!=(2,512,2,2,2,201) or not np.isin(curves,[0,1]).all() or not np.array_equal(curves[...,-1],occupied):
        raise ValueError('reference numeric inventory differs')
    seen=set()
    for rec in r['records']:
        t=rec['task'];key=old.case_key(t)
        if key not in expected or key in seen or t!=expected[key]:raise ValueError('reference record inventory differs')
        seen.add(key)
        ix=(old.BLOCKS.index(t['block']),t['replicate'],old.TARGETS.index(t['target']),('native','A_fixed').index(t['policy']),old.ORIGINS.index(t['origin']))
        if type(rec['terminal_occupied']) is not bool or rec['terminal_occupied']!=bool(occupied[ix]):raise ValueError('reference endpoint differs')
        if len(rec['raw_sha256'])!=64 or any(c not in '0123456789abcdef' for c in rec['raw_sha256']):raise ValueError('reference raw digest malformed')
        if t['replicate']==0 and t['policy']=='A_fixed' and r['files']['technical/'+key+'.npz']!=rec['raw_sha256']:
            raise ValueError('reference technical digest differs')
    if set(expected)!=seen:raise ValueError('reference inventory incomplete')
    return r


def admit_technical_reuse(root,reference_root,m,s,lookup,configs,source_sha,design_sha):
    root=Path(root);rr=json.loads((root/'SHARD.json').read_bytes())
    if (rr['status']!='TECHNICAL_NATIVE8_CLAMP8_ADMITTED' or rr['runner_sha256']!=source_sha
        or rr['design_sha256']!=design_sha or rr['cases']!=8 or rr['shard']!=0
        or rr['input_sha256']!=design.INPUT_SHA or rr['prior_sha256']!=design.PRIOR_SHA):
        raise ValueError('technical reuse source/status differs')
    expected={old.case_key(t):t for t in design.tasks() if t['replicate']==0}
    records={old.case_key(r['task']):r for r in rr['records']}
    clamps={old.case_key(r['task']):r for r in rr['clamp_checks']}
    if len(rr['records'])!=8 or len(rr['clamp_checks'])!=8 or set(records)!=set(expected) or set(clamps)!=set(expected):
        raise ValueError('technical native/clamp inventory differs')
    for key,t in expected.items():
        assigned,mapping=design.equalize_mean(original_state(s,lookup[t['block'],t['replicate'],t['origin']]))
        cfg=configs[t['target']]
        for rec,identity in ((records[key],False),(clamps[key],True)):
            name=(old.case_key(dict(t,policy='A_mean_equal_fixed_identity')) if identity else key)+'.npz'
            if rec['task']!=t or rec['archive']!=name or (identity and rec['identity']!='PASS'):
                raise ValueError('technical task/identity differs')
            body=(root/name).read_bytes()
            if old.digest(body)!=rec['sha256']:raise ValueError('technical case byte hash differs')
            trace=arrays(body);meta=json.loads(str(trace['metadata'].item()))
            if (meta['task']!=t or meta['input_sha256']!=design.INPUT_SHA or meta['config']!=m['configs'][str(t['target'])]
                or meta['runner_sha256']!=source_sha or meta['design_sha256']!=design_sha):
                raise ValueError('technical metadata differs')
            design.verify_mapping(meta['mapping'],mapping)
            validate_trace(trace,assigned,cfg)
            if identity:
                if meta.get('identity_policy')!='A_fixed':raise ValueError('technical clamp policy differs')
                ref=arrays((Path(reference_root)/'technical'/(old.case_key(dict(t,policy='A_fixed'))+'.npz')).read_bytes())
                design.verify_clamp_identity(trace,ref)
            else:
                design.verify_mapping(rec['mapping'],mapping)
                if rec['terminal_occupied']!=bool(trace['population'][-1]):raise ValueError('technical native summary differs')
    return records


def run_shard(input_path,reference_root,shard,out,*,technical=False,reuse=None):
    if type(shard) is not int or shard not in range(16):raise ValueError('invalid shard')
    if not technical and not reuse:raise ValueError('production requires complete technical admission and reuse')
    m,s,baseline,lookup=inputs(input_path);references(reference_root)
    out=Path(out)
    if out.exists():raise ValueError('refuse output overwrite')
    out.mkdir(parents=True)
    source_sha=old.digest(Path(__file__).read_text(encoding='utf-8').encode())
    design_sha=old.digest(Path(design.__file__).read_text(encoding='utf-8').encode())
    selected=[t for t in design.tasks() if old.shard_for(t)==shard and (not technical or t['replicate']==0)]
    if technical and shard!=0:raise ValueError('technical cases occupy shard0 only')
    configs={t:Config.from_dict(m['configs'][str(t)]) for t in old.TARGETS}
    visitors=VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
    reused={}
    if reuse:
        reused=admit_technical_reuse(reuse,reference_root,m,s,lookup,configs,source_sha,design_sha)
    records=[];clamps=[]
    for t in selected:
        ix=lookup[t['block'],t['replicate'],t['origin']];initial=original_state(s,ix)
        assigned,mapping=design.equalize_mean(initial);cfg=configs[t['target']];key=old.case_key(t)
        dest=out/(key+'.npz')
        if key in reused:
            rec=reused[key];raw=(Path(reuse)/rec['archive']).read_bytes()
            if rec['task']!=t or old.digest(raw)!=rec['sha256']:raise ValueError('technical reuse case drift')
            trace=arrays(raw);validate_trace(trace,assigned,cfg);dest.write_bytes(raw)
        else:
            trace=old.trajectory(assigned,visitors,cfg,old.future_seed(t),'native')
            validate_trace(trace,assigned,cfg)
            meta=dict(task=t,input_sha256=design.INPUT_SHA,config=m['configs'][str(t['target'])],mapping=mapping,
                      runner_sha256=source_sha,design_sha256=design_sha)
            with dest.open('xb') as f:np.savez_compressed(f,metadata=np.array(json.dumps(meta,sort_keys=True)),**trace)
            rec=dict(task=t,archive=dest.name,sha256=old.digest(dest.read_bytes()),mapping=mapping,
                     terminal_occupied=bool(trace['population'][-1]),restricted_duration=float((trace['population'][:-1]>0).sum()))
        json_write(out/(key+'.json'),rec);records.append(rec)
        if technical:
            ct=dict(t,policy='A_fixed');reference=arrays((Path(reference_root)/'technical'/(old.case_key(ct)+'.npz')).read_bytes())
            controlled=old.trajectory(assigned,visitors,cfg,old.future_seed(t),'A_fixed')
            design.verify_clamp_identity(controlled,reference);validate_trace(controlled,assigned,cfg)
            ck=old.case_key(dict(t,policy='A_mean_equal_fixed_identity'))
            cdest=out/(ck+'.npz')
            with cdest.open('xb') as f:np.savez_compressed(f,metadata=np.array(json.dumps(dict(task=t,identity_policy='A_fixed',mapping=mapping,
                input_sha256=design.INPUT_SHA,config=m['configs'][str(t['target'])],runner_sha256=source_sha,design_sha256=design_sha))),**controlled)
            clamps.append(dict(task=t,archive=cdest.name,sha256=old.digest(cdest.read_bytes()),identity='PASS'))
        if len(records)%32==0:print('mean-shift verified',shard,len(records),'/',len(selected),flush=True)
    if len(records)!=(8 if technical else 256) or len(clamps)!=(8 if technical else 0):raise ValueError('shard inventory incomplete')
    if old.digest(Path(__file__).read_text(encoding='utf-8').encode())!=source_sha:raise ValueError('runner changed during run')
    if old.digest(Path(design.__file__).read_text(encoding='utf-8').encode())!=design_sha:raise ValueError('design code changed during run')
    design.source_gate()
    root=Path(__file__).resolve().parents[1]
    for name,h in m['normalized_biology_sha256'].items():
        if old.digest((root/name).read_text(encoding='utf-8').encode())!=h:raise ValueError('biology changed during run')
    receipt=dict(status='TECHNICAL_NATIVE8_CLAMP8_ADMITTED' if technical else 'COMPLETE_NATIVE_MEAN_SHARD',
        shard=shard,cases=len(records),records=records,clamp_checks=clamps,input_sha256=design.INPUT_SHA,
        prior_sha256=design.PRIOR_SHA,runner_sha256=source_sha,design_sha256=design_sha,
        execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),numpy=np.__version__)
    json_write(out/'SHARD.json',receipt);print(receipt['status'],shard,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('references');r.add_argument('--input',required=True);r.add_argument('--prior',required=True);r.add_argument('--out',required=True)
    r=sub.add_parser('run');r.add_argument('--input',required=True);r.add_argument('--references',required=True)
    r.add_argument('--shard',type=int,required=True);r.add_argument('--out',required=True);r.add_argument('--technical',action='store_true');r.add_argument('--reuse-technical')
    a=p.parse_args()
    if a.command=='references':admit_references(a.input,a.prior,a.out)
    else:run_shard(a.input,a.references,a.shard,a.out,technical=a.technical,reuse=a.reuse_technical)
