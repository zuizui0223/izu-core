"""Paired completed sustained-isolation versus common-environment experiment."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scripts.run_model3_persistent_isolation import tasks
from scripts.summarize_model3_full_mutation import read_case


def main():
    root=Path(__file__).resolve().parents[1]
    persistent=root/'outputs/model3_persistent_isolation_20261005'
    common=root/'outputs/model3_full_mutation_20261004'
    target=root/'data/results/model3_exposure_experiment_comparison_20261005.json'
    if target.exists():raise ValueError('preserve existing comparison')
    declared={t[1]:list(t[2:]) for t in tasks(str(persistent),'core',64,8)}
    marker=json.loads((persistent/'core_64_8_complete.json').read_text(encoding='utf-8'))
    assert marker['status']=='completed' and marker['n_cases']==2048 and set(marker['keys'])==set(declared)
    draws=np.random.default_rng(7102026).integers(0,64,(5000,64))
    rows=[];checks=0
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            data=[]
            for seed in range(76001,76065):
                history=[]
                for rep in range(7101,7109):
                    key=f'core_{setting}_u{rate}_h{seed}_r{rep}_far'
                    path=persistent/('persistent_'+key+'.npz')
                    receipt=json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
                    assert receipt['task']==declared['persistent_'+key]
                    assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['sha256']
                    with np.load(path) as z:continued=z['trace'].copy()
                    equalized=read_case(common,key)
                    near=read_case(common,key[:-3]+'near')
                    assert np.array_equal(continued[:201],equalized[:201],equal_nan=True)
                    checks+=1
                    history.append(np.stack([continued[[200,400,1000],:4],equalized[[200,400,1000],:4],near[[200,400,1000],:4]]))
                data.append(history)
            data=np.asarray(data) # history,repeat,experiment,endpoint,statistic
            for pi,period in enumerate([200,400,1000]):
                alive=data[:,:,:,pi,0]>0
                # Same three surviving cells for all comparisons in this row.
                eligible=alive.all(axis=2);counts=eligible.sum(axis=1)
                traits=data[:,:,:,pi,1:4]
                cell=dict(setting=setting,mutation_rate=rate,period=period,
                    eligible_triplets=int(eligible.sum()),missing_triplets=int((~eligible).sum()),
                    occupancy={name:float(alive[:,:,i].mean()) for i,name in enumerate(['sustained_far','equalized_far','near'])},comparisons={})
                for label,left,right in [('sustained_far_minus_near',0,2),('equalized_far_minus_near',1,2),('sustained_minus_equalized',0,1)]:
                    diff=np.where(eligible[...,None],traits[:,:,left]-traits[:,:,right],0)
                    means=np.divide(diff.sum(axis=1),counts[:,None],out=np.full((64,3),np.nan),where=counts[:,None]>0)
                    assert np.isfinite(means).all(), 'No eligible members in a history; explicit reporting required'
                    ci=np.quantile(means[draws].mean(axis=1),[.025,.975],axis=0)
                    cell['comparisons'][label]={name:dict(mean=float(means[:,j].mean()),interval=ci[:,j].tolist()) for j,name in enumerate(['matching','investment','capacity'])}
                if period==200:
                    assert all(v['mean']==0 and v['interval']==[0.,0.] for v in cell['comparisons']['sustained_minus_equalized'].values())
                rows.append(cell)
    result=dict(status='verified_paired_experiment_comparison',first_phase_pairs_verified=checks,
        results=rows,analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        claim_ceiling='Exploratory paired comparison of completed frozen exposures; descriptive history-bootstrap intervals, no multiplicity adjustment. Shared-survivor estimand, no equilibrium or irreversibility inference. Equalization is an intervention, not spontaneous recovery.')
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps([r for r in rows if r['setting']=='assurance_cost' and r['mutation_rate']==.01 and r['period']==1000],indent=2))


if __name__=='__main__':main()
