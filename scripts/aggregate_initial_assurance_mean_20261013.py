"""Recompute all-start intervention contrasts from captured complete archives."""
import argparse
import json
from pathlib import Path
import subprocess
import numpy as np
from scripts import initial_assurance_mean_20261013 as design
from scripts import persistence_expression_mechanism_20261012 as old
from scripts.run_initial_assurance_mean_20261013 import inputs,references,original_state,arrays,json_write,admit_technical_reuse
from scripts.aggregate_persistence_mechanism_20261012 import validate_trace
from scripts.model3_island.types import Config


def aggregate(input_path,reference_root,technical_root,shard_root,out,prior_readout):
    m,s,baseline,lookup=inputs(input_path);references(reference_root)
    runner=Path(__file__).with_name('run_initial_assurance_mean_20261013.py')
    source_sha=old.digest(runner.read_text(encoding='utf-8').encode());design_sha=old.digest(Path(design.__file__).read_text(encoding='utf-8').encode())
    configs={t:Config.from_dict(m['configs'][str(t)]) for t in old.TARGETS}
    admit_technical_reuse(technical_root,reference_root,m,s,lookup,configs,source_sha,design_sha)
    with np.load(Path(reference_root)/'references.npz',allow_pickle=False) as z:
        reference_x=z['occupied'].copy();reference_curves=z['curves'].copy()
    x=np.zeros((2,512,2,3,2),np.int8);curves=np.zeros((2,512,2,3,2,201),np.int8)
    x[:,:,:,0,:]=reference_x[:,:,:,0,:];x[:,:,:,2,:]=reference_x[:,:,:,1,:]
    curves[:,:,:,0,:,:]=reference_curves[:,:,:,0,:,:];curves[:,:,:,2,:,:]=reference_curves[:,:,:,1,:,:]
    expected={old.case_key(t):t for t in design.tasks()};seen=set();commits=set();records=[];secondary={}
    for shard in range(16):
        root=Path(shard_root)/f'initial-mean-shard-{shard}';sr=json.loads((root/'SHARD.json').read_bytes())
        if (sr['status']!='COMPLETE_NATIVE_MEAN_SHARD' or sr['shard']!=shard or sr['cases']!=256 or len(sr['records'])!=256
            or sr['input_sha256']!=design.INPUT_SHA or sr['prior_sha256']!=design.PRIOR_SHA
            or sr['runner_sha256']!=source_sha or sr['design_sha256']!=design_sha):raise ValueError('full shard admission differs')
        commits.add(sr['execution_commit'])
        for rec in sr['records']:
            t=rec['task'];key=old.case_key(t)
            if key not in expected or t!=expected[key] or key in seen or old.shard_for(t)!=shard or rec['archive']!=key+'.npz':
                raise ValueError('full4096 task inventory differs')
            seen.add(key);raw=(root/rec['archive']).read_bytes()
            if old.digest(raw)!=rec['sha256'] or json.loads((root/(key+'.json')).read_bytes())!=rec:raise ValueError('case hash/receipt differs')
            z=arrays(raw);meta=json.loads(str(z['metadata'].item()))
            ix=lookup[t['block'],t['replicate'],t['origin']];assigned,mapping=design.equalize_mean(original_state(s,ix));cfg=configs[t['target']]
            if (meta['task']!=t or meta['input_sha256']!=design.INPUT_SHA
                or meta['config']!=m['configs'][str(t['target'])] or meta['runner_sha256']!=source_sha or meta['design_sha256']!=design_sha):
                raise ValueError('full case metadata differs')
            design.verify_mapping(meta['mapping'],mapping);design.verify_mapping(rec['mapping'],mapping)
            first,second=validate_trace(z,assigned,cfg)
            occupied=bool(z['population'][-1]);duration=int((z['population'][:-1]>0).sum())
            if occupied!=rec['terminal_occupied'] or duration!=rec['restricted_duration']:raise ValueError('case summary differs')
            index=(old.BLOCKS.index(t['block']),t['replicate'],old.TARGETS.index(t['target']),1,old.ORIGINS.index(t['origin']))
            x[index]=occupied;curves[index]=(z['population']>0).astype(np.int8)
            group=(t['target'],t['origin'])
            if group not in secondary:secondary[group]=dict(cases=0,population=np.zeros(201),first=np.zeros((201,3)),second=np.zeros((201,3,3)),diagnostics=np.zeros((200,11)))
            sec=secondary[group];sec['cases']+=1;sec['population']+=z['population'];sec['first']+=first;sec['second']+=second;sec['diagnostics']+=z['diagnostics']
            records.append(dict(task=t,sha256=rec['sha256']))
    if seen!=set(expected) or len(commits)!=1:raise ValueError('full inventory/source incomplete')
    prior=json.loads(Path(prior_readout).read_bytes());prior_d=np.asarray(prior['policy_differences'])
    actual_d=(reference_x[...,0]-reference_x[...,1]).mean(axis=(0,1))
    if not np.array_equal(actual_d,prior_d[:,[0,1]]):raise ValueError('existing native/A_fixed numerical values differ')
    result=design.analyze(x)
    result.update(status='COMPLETE_INITIAL_MEAN_4096_AND_CLAMP8_VERIFIED',new_native_futures=4096,new_clamp_identity_futures=8,
                  reused_original_futures=8192,source_execution_commit=commits.pop(),input_sha256=design.INPUT_SHA,prior_sha256=design.PRIOR_SHA,
                  runner_sha256=source_sha,design_sha256=design_sha,scope='Controlled initial assurance mean contribution and residual lifelong expression; not pure later selection or natural-order benefit.')
    result['secondary_survival']=dict(occupancy_by_update=curves.mean(axis=(0,1)).tolist(),
        restricted_duration_by_target_policy_origin=curves[...,:-1].sum(-1).mean(axis=(0,1)).tolist(),
        scope='Descriptive finite200-update quantities; reused clamp outcomes exclude hidden assurance genomes.')
    summary=[]
    for (target,origin),sec in sorted(secondary.items()):
        if sec['cases']!=1024:raise ValueError('secondary inventory incomplete')
        count=sec['population'];mean=np.divide(sec['first'],count[:,None],out=np.zeros_like(sec['first']),where=count[:,None]>0)
        moment=np.divide(sec['second'],count[:,None,None],out=np.zeros_like(sec['second']),where=count[:,None,None]>0)
        cov=moment-mean[:,:,None]*mean[:,None,:]
        summary.append(dict(target=target,origin=origin,cases=1024,mean_census=(count/1024).tolist(),
                            genotype_means=[row.tolist() if n else None for row,n in zip(mean,count)],
                            genotype_covariances=[row.tolist() if n else None for row,n in zip(cov,count)],
                            mean_reproductive_diagnostics=(sec['diagnostics']/1024).tolist(),scope='Current quantitative genotypes, not neutral diversity.'))
    result['secondary_new_genomes']=summary
    out=Path(out)
    if out.exists():raise ValueError('refuse readout overwrite')
    out.mkdir(parents=True);np.savez_compressed(out/'all_start_outcomes.npz',occupied=x,curves=curves)
    json_write(out/'READOUT.json',result)
    json_write(out/'_COMPLETION.json',dict(status=result['status'],cases=4096,clamp_identity_cases=8,records=records,
        readout_sha256=old.digest((out/'READOUT.json').read_bytes()),outcomes_sha256=old.digest((out/'all_start_outcomes.npz').read_bytes()),
        verifier_execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()))
    print(json.dumps({k:result[k] for k in ('status','new_native_futures','new_clamp_identity_futures','primary','policy_route_differences')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--references',required=True)
    p.add_argument('--technical',required=True);p.add_argument('--shards',required=True);p.add_argument('--out',required=True)
    p.add_argument('--prior-readout',default='data/results/persistence_mechanism_20261012/readout.json')
    a=p.parse_args();aggregate(a.input,a.references,a.technical,a.shards,a.out,a.prior_readout)
