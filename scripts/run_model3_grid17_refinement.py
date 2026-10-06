"""All-condition 17-node continuation; never changes frozen 13-node sources."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import zipfile
import numpy as np
from scripts import run_model3_grid_refinement as prior
from scripts import run_model3_full_mutation as campaign


def refinement_tasks(out):
    result=[]
    for task in prior.refinement_tasks(out):
        values=list(task)
        values[1]=values[1].replace('_n13_','_n17_')
        values[8]=17
        result.append(tuple(values))
    return result


def read_receipt(out,task):
    p=Path(out);key=task[1]
    receipt=p/(key+'.json');data=p/(key+'.npz')
    if not receipt.exists() or not data.exists():
        raise ValueError('incomplete case: '+key)
    r=json.loads(receipt.read_text())
    if r['task']!=list(task[2:]) or hashlib.sha256(data.read_bytes()).hexdigest()!=r['sha256']:
        raise ValueError('invalid case receipt: '+key)
    return r


def verify_predecessor(out):
    p=Path(out);tasks=prior.refinement_tasks(p)
    complete=p/'complete.json'
    if not complete.exists():raise ValueError('incomplete 13-node predecessor')
    marker=json.loads(complete.read_text())
    if marker!=dict(status='completed',n_cases=32,keys=[t[1] for t in tasks]):
        raise ValueError('incomplete or inconsistent 13-node marker')
    if not (p/'sources.json').exists() or not (p/'sources.zip').exists():
        raise ValueError('missing predecessor provenance; cannot recreate it')
    prior.snapshot(p)
    return dict(case_hashes={t[1]:read_receipt(p,t)['sha256'] for t in tasks},
        source_manifest_sha256=hashlib.sha256((p/'sources.json').read_bytes()).hexdigest(),
        source_archive_sha256=hashlib.sha256((p/'sources.zip').read_bytes()).hexdigest())


def snapshot(out,predecessor):
    p=Path(out);p.mkdir(parents=True,exist_ok=True)
    source_paths=sorted(set(list((campaign.ROOT/'scripts/model3_island').glob('*.py'))+
        [Path(__file__),Path(campaign.__file__),Path(prior.__file__),
         campaign.ROOT/'data/design/model3_ch2_bridge_20260927.json',
         campaign.ROOT/'docs/superpowers/plans/2026-10-04-model3-grid-refinement.md',
         campaign.ROOT/'docs/superpowers/plans/2026-10-04-model3-grid17-refinement.md']))
    hashes={f.relative_to(campaign.ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in source_paths}
    manifest=p/'sources.json';archive=p/'sources.zip';parent=p/'predecessor.json'
    if manifest.exists():
        if not parent.exists() or json.loads(parent.read_text())!=predecessor:
            raise ValueError('changed or missing predecessor identity')
        if json.loads(manifest.read_text())!=hashes:raise ValueError('changed 17-node sources')
        try:
            with zipfile.ZipFile(archive) as z:
                if set(z.namelist())!=set(hashes) or len(z.namelist())!=len(hashes):
                    raise ValueError('source archive members mismatch')
                if any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in hashes.items()):
                    raise ValueError('source archive hash mismatch')
        except (FileNotFoundError,zipfile.BadZipFile) as exc:
            raise ValueError('invalid source archive') from exc
    else:
        if any(p.glob('*.npz')) or (p/'complete.json').exists():
            raise ValueError('missing provenance for existing results; cannot recreate it')
        temporary=p/'sources.zip.tmp'
        with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED) as z:
            for f in source_paths:z.write(f,f.relative_to(campaign.ROOT).as_posix())
        os.replace(temporary,archive)
        campaign.atomic_json(parent,predecessor)
        campaign.atomic_json(manifest,hashes)


def run_case(task):
    campaign.AXES[17]=list(np.linspace(0,1,17))
    return campaign.run_case(task)


def compare_traces(coarse,refined):
    if coarse.shape!=(1001,10) or refined.shape!=coarse.shape:
        raise ValueError('unexpected trajectory shape')
    if not np.allclose(coarse[0,:7],refined[0,:7],atol=1e-12,rtol=0):
        raise ValueError('initial distribution mismatch')
    for trace in [coarse,refined]:
        if not np.isfinite(trace[:,0]).all() or (trace[:,0]<0).any():
            raise ValueError('invalid population mass')
        if not np.isfinite(trace[trace[:,0]>0,1:7]).all():
            raise ValueError('nonfinite occupied population moments')
    both=(coarse[:,0]>0)&(refined[:,0]>0)
    delta=refined[both,1:4]-coarse[both,1:4]
    terminal=refined[-1,1:4]-coarse[-1,1:4] if both[-1] else None
    gap=float(np.max(abs(terminal))) if terminal is not None else None
    mismatch=int(np.sum((coarse[:,0]>0)!=(refined[:,0]>0)))
    return dict(terminal_signed_difference=None if terminal is None else terminal.tolist(),
        terminal_max_gap=gap,terminal_pass=bool(gap is not None and gap<.01 and mismatch==0),
        trajectory_max_gap=float(np.max(abs(delta))) if len(delta) else None,
        occupancy_mismatch_count=mismatch,
        population_mass_max_gap=float(np.max(abs(refined[:,0]-coarse[:,0]))),
        refined_terminal_mass=float(refined[-1,0]))


def summarize(out,previous):
    p=Path(out);old=Path(previous);tasks=refinement_tasks(p)
    # Check all receipts first: never publish a selectively completed summary.
    for t in tasks:read_receipt(p,t)
    parent=verify_predecessor(old)
    if not (p/'sources.json').exists():
        raise ValueError('missing stage provenance; cannot recreate it')
    snapshot(p,parent)
    rows=[]
    for t,base in zip(tasks,prior.refinement_tasks(old)):
        with np.load(p/(t[1]+'.npz')) as a:refined=a['trace'].copy()
        with np.load(old/(base[1]+'.npz')) as a:coarse=a['trace'].copy()
        rows.append(dict(key=t[1],setting=t[3],history_seed=t[5],arm=t[7],scheme=t[9],
            **compare_traces(coarse,refined)))
    return dict(n_cases=32,passing=sum(r['terminal_pass'] for r in rows),rows=rows,
        claim_boundary='same-founder 13-to-17 precision diagnostic; not a continuum theorem or ecological retuning')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--previous',required=True)
    parser.add_argument('--summarize',action='store_true')
    parser.add_argument('--resource-record',help='Reviewed timing/memory probe JSON, required for execution')
    args=parser.parse_args();out=Path(args.out)
    if args.summarize:
        result=summarize(out,args.previous)
        campaign.atomic_json(out/'summary.json',result)
        print({k:v for k,v in result.items() if k!='rows'},flush=True)
        return
    parent=verify_predecessor(args.previous)
    if not args.resource_record:raise ValueError('resource probe record required before 17-node execution')
    probe=json.loads(Path(args.resource_record).read_text())
    if probe.get('nodes')!=17 or probe.get('status')!='passed' or probe.get('workers')!=1:
        raise ValueError('17-node single-worker resource probe not passed')
    snapshot(out,parent)
    # Record exact reviewed probe; it is not an ecological gate.
    existing=out/'resource_probe.json'
    if existing.exists() and json.loads(existing.read_text())!=probe:
        raise ValueError('resource probe changed on resume')
    campaign.atomic_json(existing,probe)
    declared=refinement_tasks(out)
    for i,task in enumerate(declared,1):
        # New process per case bounds cache retention; never concurrent with itself.
        with ProcessPoolExecutor(max_workers=1) as pool:
            key=pool.submit(run_case,task).result()
        print(i,'/',len(declared),key,flush=True)
    campaign.atomic_json(out/'complete.json',dict(status='completed',n_cases=32,keys=[t[1] for t in declared]))


if __name__=='__main__':main()
