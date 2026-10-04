"""Predeclared n5/40-period integrated compressed-solver admission probe."""
import hashlib,json,time,zipfile
from pathlib import Path
import numpy as np
from scripts.run_model3_full_mutation import ROOT,config,exposure,atomic_json
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.density import project_state,density_step
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_compressed_step import compressed_step
from scripts.model3_core_rounding import rounded


def main():
    out=ROOT/'outputs/model3_precision_feasibility/integrated_n5_40'
    out.mkdir(parents=True,exist_ok=True)
    sources=sorted(set(list((ROOT/'scripts/model3_island').glob('*.py'))+
        list((ROOT/'scripts').glob('model3_compressed*.py'))+[
        ROOT/'scripts/model3_core_rounding.py',Path(__file__),
        ROOT/'scripts/run_model3_full_mutation.py',
        ROOT/'data/design/model3_ch2_bridge_20260927.json',
        ROOT/'docs/superpowers/plans/2026-10-04-model3-rounded-integration-probe.md']))
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    if (out/'sources.json').exists():
        raise ValueError('existing probe output must not be overwritten')
    atomic_json(out/'sources.json',hashes)
    with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sources:z.write(p,p.relative_to(ROOT).as_posix())
    axes=([0,.25,.5,.75,1],)*3;grid=make_tensor_grid(axes)
    founders=founders_from_spec(dict(count=48,draw_count=48,means=[.5]*3,sd=.15,birth_year=0),74001)
    _,initial=project_state(founders,grid)
    traits=grid.genotypes.mean(axis=2);results=[]
    for setting in ['assurance_cost','prior_selfing']:
      for arm in ['near','far']:
       for scheme in ['jump','heat_fv']:
        key=f'{setting}_{arm}_{scheme}';c=config(setting,.01);h=exposure(76001,arm)
        state,_=rounded((initial.reshape(15,15,15),[np.eye(15)]*3))
        baseline=initial.copy();records=[];start=time.monotonic();failure=None
        for t in range(40):
            local=[]
            def reduce(value,stage):
                value,receipt=rounded(value,relative_l1=1e-8)
                local.append(dict(stage=stage,**receipt));return value
            try:
                baseline,_=density_step(baseline,grid,h.visitors[t],h.seed_candidates[t],c,
                    mutation_scheme=scheme,inheritance_backend='tensor')
                state=compressed_step(state,axes,h.visitors[t],c,scheme=scheme,rounding=reduce)
                dense=np.einsum('abc,ia,jb,kc->ijk',state[0],*state[1]).ravel()
                bm=float(baseline.sum());cm=float(dense.sum())
                gap=float(np.max(np.abs(baseline@traits/bm-dense@traits/cm))) if bm>0 and cm>0 else None
                records.append(dict(period=t+1,path_l1=float(np.abs(dense-baseline).sum()/max(bm,1e-300)),
                    mass_gap=abs(bm-cm),trait_gap=gap,
                    negative_mass=float(-dense[dense<0].sum()/max(bm,1e-300)),
                    occupancy_mismatch=bool((bm>0)!=(cm>0)),ranks=list(state[0].shape),local=local))
            except (ArithmeticError,ValueError,MemoryError) as error:
                failure=dict(period=t+1,type=type(error).__name__,message=str(error),local=local)
                break
        passed=failure is None and len(records)==40 and all(
            r['path_l1']<=1e-5 and r['mass_gap']<=1e-5 and r['negative_mass']<=1e-10
            and not r['occupancy_mismatch'] and (r['trait_gap'] is None or r['trait_gap']<=1e-6) for r in records)
        arrays=out/(key+'.npz')
        np.savez_compressed(arrays,baseline=baseline,core=state[0],**{f'factor{k}':f for k,f in enumerate(state[1])})
        result=dict(key=key,passed=passed,failure=failure,records=records,seconds=time.monotonic()-start,
                    checkpoint_sha256=hashlib.sha256(arrays.read_bytes()).hexdigest())
        atomic_json(out/(key+'.json'),result);results.append(result)
        print(key,'passed',passed,'completed periods',len(records),'failure',failure and failure['message'],flush=True)
    atomic_json(out/'summary.json',dict(scope='coarse-grid integrated solver admission only',results=results))


if __name__=='__main__':main()
