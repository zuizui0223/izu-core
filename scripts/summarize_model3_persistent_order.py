"""Frozen sustained-isolation endpoints and exploratory temporal-order diagnostic."""
from pathlib import Path
from collections import Counter
import hashlib,json,zipfile
import numpy as np
from scripts.run_model3_persistent_isolation import tasks
from scripts.summarize_model3_full_mutation import read_case
from scripts.model3_temporal_order import first_sustained,order_label

ROOT=Path(__file__).resolve().parents[1]


def mean_available(values,axis):
    counts=np.isfinite(values).sum(axis=axis)
    return np.divide(np.nansum(values,axis=axis),counts,out=np.full(counts.shape,np.nan),where=counts>0)


def main():
    out=ROOT/'outputs/model3_persistent_isolation_20261005'
    old=ROOT/'outputs/model3_full_mutation_20261004'
    declared=tasks(str(out),'core',64,8);expected={t[1]:list(t[2:]) for t in declared}
    complete=out/'core_64_8_complete.json'
    if not complete.exists():raise ValueError('campaign incomplete; no partial biological readout')
    done=json.loads(complete.read_text());assert done['status']=='completed' and done['n_cases']==2048
    assert set(done['keys'])==set(expected)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=json.loads((out/'sources.json').read_text())
    with zipfile.ZipFile(out/'sources.zip') as archive:
        for name,digest in manifest.items():
            assert hashlib.sha256(archive.read(name)).hexdigest()==digest==sha(ROOT/name)
    planpath=ROOT/'data/design/model3_temporal_order_diagnostic_20261005.json'
    plan=json.loads(planpath.read_text());rows=[];endpoints=[];curves={}
    samples=np.random.default_rng(4102026).integers(0,64,size=(5000,64))
    resultpath=ROOT/'data/results/model3_persistent_isolation_summary_20261005.json'
    if resultpath.exists():raise ValueError('preserve previous summary')
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            arms=[]
            for seed in range(76001,76065):
                reps=[]
                for rep in range(7101,7109):
                    key=f'persistent_core_{setting}_u{rate}_h{seed}_r{rep}_far'
                    receipt=json.loads((out/(key+'.json')).read_text())
                    assert receipt['task']==expected[key] and sha(out/(key+'.npz'))==receipt['sha256']
                    with np.load(out/(key+'.npz')) as archive:far=archive['trace'].copy()
                    assert far.shape==(1001,10)
                    prefix=key.removeprefix('persistent_')
                    near=read_case(old,prefix[:-3]+'near')
                    oldfar=read_case(old,prefix)
                    assert np.array_equal(far[:201],oldfar[:201],equal_nan=True)
                    reps.append([near,far])
                arms.append(reps)
            data=np.array(arms) # history,replicate,arm,period,statistic
            occupied=data[:,:,:,:,0]>0
            paired=occupied[:,:,0]&occupied[:,:,1]
            gap=np.where(paired[:,:,:,None],data[:,:,1,:,1:4]-data[:,:,0,:,1:4],np.nan)
            contrasts={'paired_far_minus_near':mean_available(gap,1)}
            for arm,name in enumerate(['near','far']):
                delta=data[:,:,arm,:,1:4]-data[:,:,arm,0,1:4][:,:,None,:]
                contrasts[name+'_change_from_founders']=mean_available(np.where(occupied[:,:,arm,:,None],delta,np.nan),1)
            for name,values in contrasts.items():
                curves[f'{setting}_u{rate}_{name}']=values
                for threshold in plan['threshold_sensitivity']:
                    events=[]
                    for h,v in enumerate(values):
                        ti=first_sustained(-v[:,1],threshold,plan['sustained_periods'])
                        ta=first_sustained(v[:,2],threshold,plan['sustained_periods'])
                        events.append(dict(history_seed=76001+h,investment_time=ti,assurance_time=ta,
                                           order=order_label(ta,ti,plan['tie_tolerance_periods'])))
                    counts=dict(Counter(e['order'] for e in events))
                    both=sum(counts.get(k,0) for k in ['assurance_first','investment_first','near_simultaneous'])
                    rows.append(dict(setting=setting,mutation_rate=rate,contrast=name,threshold=threshold,
                        events=events,counts=counts,both_reached=both,total_histories=64,
                        order_proportions_among_both={k:counts.get(k,0)/both if both else None
                            for k in ['assurance_first','investment_first','near_simultaneous']}))
            for period in [200,1000]:
                traits={}
                for column,name in enumerate(['matching','investment','assurance']):
                    h=contrasts['paired_far_minus_near'][:,period,column]
                    boot=mean_available(h[samples],1)
                    ci=np.quantile(boot,[.025,.975]) if np.isfinite(boot).all() else [np.nan,np.nan]
                    traits[name]=dict(mean_gap=float(mean_available(h,0)),interval=[float(x) if np.isfinite(x) else None for x in ci],
                        halfwidth=float((ci[1]-ci[0])/2) if np.isfinite(ci).all() else None)
                endpoints.append(dict(setting=setting,mutation_rate=rate,period=period,traits=traits,
                    paired_occupancy=float(paired[:,:,period].mean()),near_occupancy=float(occupied[:,:,0,period].mean()),
                    far_occupancy=float(occupied[:,:,1,period].mean())))
    curvepath=out/'temporal_order_curves.npz'
    if curvepath.exists():raise ValueError('preserve prior curves')
    np.savez_compressed(curvepath,**curves)
    result=dict(status='completed_summary',verified_new_cases=2048,verified_near_references=2048,
        first_200_updates_match=True,endpoints=endpoints,temporal_order=rows,
        plan_sha256=sha(planpath),curve_sha256=sha(curvepath),source_manifest_sha256=sha(out/'sources.json'),
        analysis_source_sha256=sha(Path(__file__)),claim_ceiling=plan['claim_ceiling'])
    resultpath.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(endpoints=endpoints,diagnostic_rows=len(rows)),indent=2))


if __name__=='__main__':main()
