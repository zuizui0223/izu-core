"""Precision-gated summaries for the fixed full-model campaign."""
from pathlib import Path
from functools import lru_cache
import argparse,json,hashlib
import numpy as np
from scripts.run_model3_full_mutation import tasks,ROOT


@lru_cache(maxsize=1)
def expected_receipts():
    declared=tasks('', 'core',64,8)+tasks('', 'benchmark')+tasks('', 'density')
    return {t[1]:list(t[2:]) for t in declared}


def read_case(out,key):
    receipt=json.loads((out/(key+'.json')).read_text())
    if key not in expected_receipts() or receipt.get('task')!=expected_receipts()[key]:
        raise ValueError('case task mismatch '+key)
    path=out/(key+'.npz')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt['sha256']:raise ValueError('case hash mismatch '+key)
    with np.load(path) as archive:return archive['trace'].copy()


def core_summary(out,histories,repeats,mode='core'):
    all_tasks=tasks(out,mode,histories,repeats)
    missing=[t[1] for t in all_tasks if not (out/(t[1]+'.json')).exists()]
    if missing:raise ValueError(f'incomplete {mode}: {len(missing)} cases')
    hcount=4 if mode=='benchmark' else histories
    rcount=4 if mode=='benchmark' else repeats
    rng=np.random.default_rng(4102026)
    resamples=rng.integers(0,hcount,size=(5000,hcount))
    rows=[]
    for setting in ['assurance_cost','prior_selfing']:
     for rate in [0.,.01]:
      paired=[]
      for h in range(76001,76001+hcount):
       records=[]
       for r in range(7101,7101+rcount):
        records.append([read_case(out,f'{mode}_{setting}_u{rate}_h{h}_r{r}_{arm}') for arm in ['near','far']])
       paired.append(records)
      data=np.array(paired) #history, repeat, arm, period, statistic
      for t in [200,400,1000]:
       occupied=(data[:,:,0,t,0]>0)&(data[:,:,1,t,0]>0)
       row=dict(setting=setting,mutation_rate=rate,period=t,common_periods=max(0,t-200),
         history_count=hcount,repeats=rcount,paired_occupancy=float(occupied.mean()),
         near_occupancy=float((data[:,:,0,t,0]>0).mean()),far_occupancy=float((data[:,:,1,t,0]>0).mean()),traits={})
       for column,name in enumerate(['access','investment','assurance'],1):
        gap=np.where(occupied,data[:,:,1,t,column]-data[:,:,0,t,column],np.nan)
        sums=np.nansum(gap,axis=1);counts=np.sum(np.isfinite(gap),axis=1)
        hist_mean=np.divide(sums,counts,out=np.full(hcount,np.nan),where=counts>0)
        boot=np.nanmean(hist_mean[resamples],axis=1)
        ci=np.quantile(boot,[.025,.975]) if np.isfinite(boot).all() else [np.nan,np.nan]
        row['traits'][name]=dict(mean_gap=float(np.nanmean(hist_mean)),interval=list(ci),
          halfwidth=float((ci[1]-ci[0])/2),history_effects=hist_mean.tolist(),
          near_mean=float(np.nanmean(data[:,:,0,t,column])),
          far_mean=float(np.nanmean(data[:,:,1,t,column])),
          near_change_from_founders=float(np.nanmean(data[:,:,0,t,column]-data[:,:,0,0,column])),
          far_change_from_founders=float(np.nanmean(data[:,:,1,t,column]-data[:,:,1,0,column])),
          near_mean_allele_count=float(np.nanmean(data[:,:,0,t,column+6])),
          far_mean_allele_count=float(np.nanmean(data[:,:,1,t,column+6])),
          mean_last100_change_near=float(np.nanmean(data[:,:,0,t,column]-data[:,:,0,t-100,column])),
          mean_last100_change_far=float(np.nanmean(data[:,:,1,t,column]-data[:,:,1,t-100,column])))
       rows.append(row)
    gates=[r['paired_occupancy']>=.9 and all(np.isfinite(r['traits'][k]['halfwidth']) and r['traits'][k]['halfwidth']<=.025 for k in ['investment','assurance']) for r in rows if r['period'] in [200,1000]]
    return dict(mode=mode,n_cases=len(all_tasks),histories=hcount,repeats=rcount,precision_all_pass=all(gates),precision_gates_passed=sum(gates),precision_gates_total=len(gates),rows=rows,
      claim_boundary='history-cluster bootstrap on paired survivors; precision diagnostic, not attractor evidence; adaptive precision intervals are descriptive')


def density_summary(out):
    rows=[]
    for setting in ['assurance_cost','prior_selfing']:
     for rate in [0.,.01]:
      for seed in range(76001,76005):
       for arm in ['near','far']:
        all_traces={}
        for scheme in (['jump'] if rate==0 else ['jump','heat_fv']):
         for n in [5,7,9]:
          all_traces[n,scheme]=read_case(out,f'density_{setting}_u{rate}_h{seed}_{arm}_n{n}_{scheme}')
         a,b=all_traces[7,scheme],all_traces[9,scheme]
         coarse=all_traces[5,scheme]
         gap=float(np.nanmax(np.abs(a[-1,1:4]-b[-1,1:4])))
         rows.append(dict(setting=setting,mutation_rate=rate,history_seed=seed,arm=arm,scheme=scheme,
           terminal_grid_gap=gap,terminal_grid_pass=bool(gap<.01),
           terminal_grid_gap_5_to_7=float(np.nanmax(np.abs(coarse[-1,1:4]-a[-1,1:4]))),
           full_trajectory_max_grid_gap_5_to_7=float(np.nanmax(np.abs(coarse[:,1:4]-a[:,1:4]))),
           full_trajectory_max_grid_gap=float(np.nanmax(np.abs(a[:,1:4]-b[:,1:4]))),
           terminal_traits=b[-1,1:4].tolist(),terminal_mass=float(b[-1,0]),
           last100_trait_changes=(b[-1,1:4]-b[-101,1:4]).tolist()))
        if rate:
         a,b=all_traces[9,'jump'],all_traces[9,'heat_fv']
         rows.append(dict(setting=setting,mutation_rate=rate,history_seed=seed,arm=arm,comparison='jump_vs_heat_fv',
             terminal_approximation_gap=float(np.nanmax(np.abs(a[-1,1:4]-b[-1,1:4]))),
             full_trajectory_max_approximation_gap=float(np.nanmax(np.abs(a[:,1:4]-b[:,1:4])))))
    return dict(rows=rows,grid_gate='7-to-9-node terminal means <.01; 5-to-7 and complete trajectory gaps reported separately',claim_boundary='three-locus joint density; failed grid gates forbid quantitative fidelity claims')


def benchmark_comparison(out):
    """Paired comparisons using the same projected founders and visitor histories.

    Four histories are a bounded numerical/engine comparison, not an estimate
    of the prevalence or distribution of effects across natural islands.
    """
    rows=[]
    for setting in ['assurance_cost','prior_selfing']:
     for rate in [0.,.01]:
      for seed in range(76001,76005):
       for arm in ['near','far']:
        abm=np.array([read_case(out,f'benchmark_{setting}_u{rate}_h{seed}_r{rep}_{arm}')
                      for rep in range(7101,7105)])
        density=read_case(out,f'density_{setting}_u{rate}_h{seed}_{arm}_n9_jump')
        heat=read_case(out,f'density_{setting}_u{rate}_h{seed}_{arm}_n9_heat_fv') if rate else density
        for t in [200,400,1000]:
         rows.append(dict(setting=setting,mutation_rate=rate,history_seed=seed,arm=arm,period=t,
           abm_occupancy=float(np.mean(abm[:,t,0]>0)),
           abm_mean_traits=np.nanmean(abm[:,t,1:4],axis=0).tolist(),
           density_traits=density[t,1:4].tolist(),
           heat_traits=heat[t,1:4].tolist(),
           abm_minus_density=(np.nanmean(abm[:,t,1:4],axis=0)-density[t,1:4]).tolist(),
           density_minus_heat=(density[t,1:4]-heat[t,1:4]).tolist(),
           abm_minus_heat=(np.nanmean(abm[:,t,1:4],axis=0)-heat[t,1:4]).tolist(),
           abm_replicate_traits=abm[:,t,1:4].tolist()))
    return dict(rows=rows,claim_boundary='four matched histories, four ABM replicates; numerical grid gates must be read alongside these descriptive contrasts')


def sanitize(x):
    if isinstance(x,dict):return {k:sanitize(v) for k,v in x.items()}
    if isinstance(x,list):return [sanitize(v) for v in x]
    if isinstance(x,(float,np.floating)) and not np.isfinite(x):return None
    return x


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mode',choices=['core','benchmark','density','comparison'],required=True)
    p.add_argument('--histories',type=int,default=32);p.add_argument('--repeats',type=int,default=4)
    a=p.parse_args();out=Path(a.out)
    if a.mode=='density':result=density_summary(out)
    elif a.mode=='comparison':result=benchmark_comparison(out)
    else:result=core_summary(out,a.histories,a.repeats,a.mode)
    path=out/f'summary_{a.mode}_{a.histories}_{a.repeats}.json'
    path.write_text(json.dumps(sanitize(result),indent=2,allow_nan=False)+'\n')
    print({k:v for k,v in result.items() if k!='rows'})

if __name__=='__main__':main()
