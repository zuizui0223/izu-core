"""Read only a complete replenishment campaign; keep all rates and censoring."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import numpy as np
from scripts.model3_temporal_order import first_sustained, order_label
from scripts.summarize_model3_persistent_order import mean_available

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/model3_replenishment_evolution_20261005'
PLAN=ROOT/'data/design/model3_replenishment_evolution_20261005.json'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def read(setting,distance,seed,rep):
    if distance==0:
        folder=ROOT/'outputs/model3_full_mutation_20261004'
        key=f'core_{setting}_u0.01_h{seed}_r{rep}_near'
        task=['abm',setting,.01,seed,rep,'near',0,'jump',False]
    elif distance==3:
        folder=ROOT/'outputs/model3_persistent_isolation_20261005'
        key=f'persistent_core_{setting}_u0.01_h{seed}_r{rep}_far'
        task=['abm',setting,.01,seed,rep,'far',0,'jump',False]
    else:
        folder=OUT;key=f'{setting}_d{distance:.2f}_h{seed}_r{rep}'
        task=[setting,distance,seed,rep]
    p=folder/(key+'.npz');r=json.loads((folder/(key+'.json')).read_text())
    assert r['task']==task and sha(p)==r['sha256'],key
    with np.load(p) as a: trace=a['trace'].copy()
    assert trace.shape==(1001,10)
    alive=trace[:,0]>0
    assert np.isfinite(trace[:,0]).all() and np.isfinite(trace[alive]).all()
    assert np.isnan(trace[~alive,1:]).all()
    return trace


def group(setting,d,plan):
    return np.array([[read(setting,d,h,r) for r in plan['demographic_repeats']]
                     for h in plan['history_seeds']])


def main():
    plan=json.loads(PLAN.read_text());status=json.loads((OUT/'progress.json').read_text())
    if status['status']!='complete' or status['completed']!=plan['new_cases']:
        raise RuntimeError('Incomplete declared campaign; no outcome readout permitted')
    for name,digest in plan['source_sha256'].items(): assert sha(ROOT/name)==digest
    bootstrap=np.random.default_rng(4102026).integers(0,64,size=(5000,64))
    curves={};endpoints=[];events=[];verified=0
    for setting in plan['settings']:
        baseline=group(setting,0,plan)
        for distance in plan['distance_coordinates']:
            data=baseline if distance==0 else group(setting,distance,plan)
            verified+=512; alive=data[...,0]>0;paired=alive&(baseline[...,0]>0)
            changes=data[...,1:4]-data[:,:,0:1,1:4]
            contrasts={'from_founders':mean_available(np.where(alive[...,None],changes,np.nan),1),
                       'minus_high_supply':mean_available(np.where(paired[...,None],data[...,1:4]-baseline[...,1:4],np.nan),1)}
            key=f'{setting}_d{distance:.2f}'
            curves[key+'_occupancy']=alive.sum(axis=1)
            curves[key+'_paired_occupancy']=paired.sum(axis=1)
            for contrast,values in contrasts.items():
                curves[key+'_'+contrast]=values
                for threshold in plan['temporal_readout']['thresholds']:
                    rows=[]
                    for h,vals in zip(plan['history_seeds'],values):
                        ti=first_sustained(-vals[:,1],threshold,20)
                        ta=first_sustained(vals[:,2],threshold,20)
                        rows.append(dict(history_seed=h,investment_time=ti,capacity_time=ta,
                                         order=order_label(ta,ti,5)))
                    events.append(dict(setting=setting,distance=distance,
                                       replenishment=.24*float(np.exp(-distance)),contrast=contrast,
                                       threshold=threshold,counts=dict(Counter(x['order'] for x in rows)),events=rows))
                for t in plan['endpoints']:
                    estimates={}
                    for j,name in enumerate(['matching','investment','capacity']):
                        h=values[:,t,j];resampled=mean_available(h[bootstrap],1)
                        interval=np.quantile(resampled,[.025,.975]) if np.isfinite(resampled).all() else [np.nan,np.nan]
                        estimates[name]={'mean':float(mean_available(h,0)),
                                         'pointwise_interval':list(map(float,interval)),
                                         'histories_observed':int(np.isfinite(h).sum())}
                    endpoints.append(dict(setting=setting,distance=distance,replenishment=.24*float(np.exp(-distance)),
                                          contrast=contrast,update=t,traits=estimates,
                                          occupied_cases=int(alive[:,:,t].sum()),paired_cases=int(paired[:,:,t].sum()),total_cases=512))
    assert verified==13312
    target=OUT/'evolution_curves.npz';np.savez_compressed(target,**curves)
    def clean(value):
        if isinstance(value,float) and not np.isfinite(value):return None
        if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
        if isinstance(value,list):return [clean(v) for v in value]
        return value
    result=clean(dict(status='complete_all_declared_rates',verified_cases=verified,new_cases=11264,
                      reused_endpoint_cases=2048,endpoints=endpoints,temporal_order=events,
                      source_plan_sha256=sha(PLAN),array_sha256=sha(target),analysis_sha256=sha(Path(__file__)),
                      scope='Positive-mutation finite ABM at fixed capacity48; no intermediate-rate deterministic or PDE result.'))
    (ROOT/'data/results/model3_replenishment_evolution_summary_20261005.json').write_text(
        json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(f'Verified {verified} cases; {len(endpoints)} endpoint rows; {len(events)*64} temporal records')


if __name__=='__main__':main()
