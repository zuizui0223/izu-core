"""Complete raw admission of the frozen all-start future parent-sampler cohort."""
import argparse,json
from pathlib import Path
import numpy as np
from scripts import future_parent_selection_20261013 as design
from scripts import initial_assurance_mean_20261013 as mean
from scripts import persistence_expression_mechanism_20261012 as old
from scripts.run_initial_assurance_mean_20261013 import inputs,original_state,arrays,json_write
from scripts.run_future_parent_selection_20261013 import verify,admit_reference_root,technical_gate
from scripts.model3_island.types import Config,VisitorState


def admit_shard_header(r,shard,runner_sha,design_sha):
    if (r['status']!='COMPLETE_EQUAL_PARENT_SHARD' or r['cases']!=256 or len(r['records'])!=256 or r['shard']!=shard
            or r['input_sha256']!=mean.INPUT_SHA or r['runner_sha256']!=runner_sha or r['design_sha256']!=design_sha
            or r['updates']!=51200):raise ValueError('shard/source/count admission differs')


def trace_summaries(z):
    h=len(z['population']);occupied=(z['population']>0).astype(np.int64)
    variance=np.zeros((h,3));fixed=np.zeros((h,3),np.int64)
    means=np.where(occupied[:,None],z['means'],0.)
    for t in range(h):
        a,b=z['offsets'][t:t+2]
        if b>a:
            genes=z['alleles'][a:b];variance[t]=genes.var(axis=(0,2))
            fixed[t]=np.all(genes==genes[:1,:,:1],axis=(0,2)).astype(np.int64)
    return dict(occupied=occupied,allele_variance=variance,fixed=fixed,means=means,
                native_diagnostics=z['diagnostics'].copy())


def finite_values(values):
    return [[float(x) if np.isfinite(x) else None for x in row] for row in values]


def aggregate(input_path,reference_root,technical_root,shard_root,out):
    m,s,baseline,lookup=inputs(input_path);admit_reference_root(reference_root)
    configs={t:Config.from_dict(m['configs'][str(t)]) for t in old.TARGETS}
    visitors=VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
    technical_gate(technical_root,m,s,lookup,configs,visitors)
    runner=Path(__file__).with_name('run_future_parent_selection_20261013.py')
    runner_sha=old.digest(runner.read_text(encoding='utf-8').encode());design_sha=old.digest(Path(design.__file__).read_text(encoding='utf-8').encode())
    expected={old.case_key(t):t for t in design.tasks()};seen=set();commits=set();records=[];updates=0;secondary={}
    x=np.zeros((2,512,2,2),np.int8);curves=np.zeros((2,512,2,2,201),np.int8)
    for shard in range(16):
        folder=Path(shard_root)/f'parent-selection-shard-{shard}';r=json.loads((folder/'SHARD.json').read_bytes())
        admit_shard_header(r,shard,runner_sha,design_sha)
        commits.add(r['execution_commit'])
        for row in r['records']:
            t=row['task'];key=old.case_key(t)
            if key not in expected or t!=expected[key] or key in seen or old.shard_for(t)!=shard or row['archive']!=key+'.npz':
                raise ValueError('complete4096 unique case domain required')
            seen.add(key);body=(folder/row['archive']).read_bytes()
            if old.digest(body)!=row['sha256']:raise ValueError('raw case digest differs')
            z=arrays(body);meta=json.loads(str(z['metadata'].item()))
            if meta['task']!=t or meta['actual_policy']!=design.POLICY or meta['input_sha256']!=mean.INPUT_SHA or meta['config']!=m['configs'][str(t['target'])]:
                raise ValueError('case metadata differs')
            assigned,mapping=mean.equalize_mean(original_state(s,lookup[t['block'],t['replicate'],t['origin']]))
            mean.verify_mapping(meta['mapping'],mapping)
            if len(z['population'])!=201:raise ValueError('fixed200 horizon required')
            updates+=verify(z,assigned,visitors,configs[t['target']],old.future_seed(t),design.POLICY)
            occupied=bool(z['population'][-1])
            if occupied!=row['terminal_occupied']:raise ValueError('endpoint summary differs')
            ix=(old.BLOCKS.index(t['block']),t['replicate'],old.TARGETS.index(t['target']),old.ORIGINS.index(t['origin']))
            x[ix]=occupied;curves[ix]=(z['population']>0).astype(np.int8)
            group=(t['block'],t['target'],t['origin']);metrics=trace_summaries(z)
            if group not in secondary:
                secondary[group]=dict(cases=0,**{name:np.zeros_like(value) for name,value in metrics.items()})
            secondary[group]['cases']+=1
            for name,value in metrics.items():secondary[group][name]+=value
            records.append(dict(task=t,sha256=row['sha256']))
    if seen!=set(expected) or len(commits)!=1 or updates!=819200:raise ValueError('complete cohort/source gate failed')
    with np.load(Path(reference_root)/'verified/all_start_outcomes.npz',allow_pickle=False) as z:
        original=z['occupied'].copy();prior_curves=z['curves'].copy()
    assembled=design.assemble_outcomes(original,x);result=design.analyze(assembled)
    allcurves=np.empty((2,512,2,3,2,201),np.int8)
    allcurves[:,:,:,0]=prior_curves[:,:,:,1];allcurves[:,:,:,1]=curves;allcurves[:,:,:,2]=prior_curves[:,:,:,2]
    result.update(status='ALL4096_EQUAL_PARENT_FUTURES_ADMITTED',cases=4096,updates=updates,technical_cases=8,
                  execution_commit=commits.pop(),input_sha256=mean.INPUT_SHA,runner_sha256=runner_sha,design_sha256=design_sha,
                  secondary_occupancy=allcurves.mean(axis=(0,1)).tolist(),
                  secondary_duration=allcurves[...,:-1].sum(-1).mean(axis=(0,1)).tolist())
    summary=[]
    for (block,target,origin),v in sorted(secondary.items()):
        if v['cases']!=512:raise ValueError('descriptive cohort inventory differs')
        count=v['occupied'];traitmean=np.divide(v['means'],count[:,None],out=np.full_like(v['means'],np.nan),where=count[:,None]>0)
        allelevar=np.divide(v['allele_variance'],count[:,None],out=np.full_like(v['allele_variance'],np.nan),where=count[:,None]>0)
        summary.append(dict(block=block,target=target,origin=origin,cases=512,
            occupied_by_census=count.tolist(),fixed_allele_counts=v['fixed'].tolist(),
            conditional_trait_means=finite_values(traitmean),conditional_allele_variance=finite_values(allelevar),
            all_start_mean_native_diagnostics=(v['native_diagnostics']/512).tolist()))
    result['secondary_native_genetic_reproductive']=summary
    result['secondary_scope']='Descriptive equal-history means; extinct traits undefined. Quantitative allele variance/fixation, not neutral genetic diversity. Native returns separate from effective parent sampler.'
    out=Path(out)
    if out.exists():raise ValueError('refuse readout overwrite')
    out.mkdir(parents=True);np.savez_compressed(out/'all_start_outcomes.npz',occupied=assembled,curves=allcurves)
    json_write(out/'READOUT.json',result)
    json_write(out/'_COMPLETION.json',dict(cases=4096,updates=updates,records=records,readout_sha256=old.digest((out/'READOUT.json').read_bytes()),
               outcomes_sha256=old.digest((out/'all_start_outcomes.npz').read_bytes())))
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--references',required=True);p.add_argument('--technical-root',required=True);p.add_argument('--shards',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();r=aggregate(a.input,a.references,a.technical_root,a.shards,a.out)
    print(json.dumps({k:r[k] for k in ('status','cases','updates','primary')},indent=2))


if __name__=='__main__':main()
