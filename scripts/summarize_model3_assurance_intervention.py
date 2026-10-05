"""Full-campaign-only paired intervention readout; extinction is reported separately."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scripts.run_model3_assurance_intervention import tasks, founders
from scripts.audit_model3_assurance_intervention import audit


def require_complete(out):
    marker=out/'complete.json'
    if not marker.exists():raise ValueError('incomplete campaign: no biological readout')
    record=json.loads(marker.read_text(encoding='utf-8'))
    expected={f'{s}_u{u}_h{h}_r{r}_{a}_{m}' for s,u,h,r,a,m in tasks()}
    if record['status']!='completed' or record['n_cases']!=8192 or len(record['keys'])!=8192 or set(record['keys'])!=expected:
        raise ValueError('incomplete or mismatched campaign')


def history_means(values,mask):
    counts=mask.sum(axis=1)
    total=np.where(mask[...,None],values,0).sum(axis=1)
    result=np.divide(total,counts[:,None],out=np.full(total.shape,np.nan),where=counts[:,None]>0)
    return result,counts


def interaction(values,alive):
    differences=(values[:,:,1,1]-values[:,:,1,0])-(values[:,:,0,1]-values[:,:,0,0])
    return history_means(differences,alive.all(axis=(2,3)))


def estimate(values,counts):
    estimable=np.isfinite(values).all(axis=1)
    sample=values[estimable]
    result=dict(histories=int(estimable.sum()),eligible_replicates=int(counts.sum()),
                missing_histories=int((~estimable).sum()),traits={})
    if not len(sample):return result
    draws=np.random.default_rng(6102026).integers(0,len(sample),(5000,len(sample)))
    boot=sample[draws].mean(axis=1)
    for j,name in enumerate(['matching','investment','capacity']):
        result['traits'][name]=dict(mean=float(sample[:,j].mean()),
            interval=np.quantile(boot[:,j],[.025,.975]).tolist())
    return result


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_assurance_intervention_20261005'
    require_complete(out)
    receipt=audit(root)
    assert receipt['checked_cases']==8192 and receipt['zero_mutation_matched_pairs_identical']==2048
    target=root/'data/results/model3_assurance_intervention_summary_20261005.json'
    if target.exists():raise ValueError('preserve existing summary')
    initial=founders().alleles.mean(axis=2).mean(axis=0)
    results=[]
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            # history, demographic repeat, capacity mode, isolation, endpoint, statistic
            data=np.empty((64,8,2,2,3,4))
            for hi,seed in enumerate(range(76001,76065)):
                for ri,rep in enumerate(range(7101,7109)):
                    for mi,mode in enumerate(['fixed','evolving']):
                        for ai,arm in enumerate(['near','far']):
                            path=out/f'{setting}_u{rate}_h{seed}_r{rep}_{arm}_{mode}.npz'
                            with np.load(path) as z:data[hi,ri,mi,ai]=z['trace'][[200,400,1000],:4]
            for pi,period in enumerate([200,400,1000]):
                alive=data[:,:,:,:,pi,0]>0
                values=data[:,:,:,:,pi,1:4]
                cell=dict(setting=setting,mutation_rate=rate,period=period,modes={})
                for mi,mode in enumerate(['fixed','evolving']):
                    entry=dict(occupancy={arm:float(alive[:,:,mi,ai].mean()) for ai,arm in enumerate(['near','far'])},
                               change_from_founders={})
                    means,counts=history_means(values[:,:,mi,1]-values[:,:,mi,0],alive[:,:,mi].all(axis=2))
                    entry['far_minus_near']=estimate(means,counts)
                    for ai,arm in enumerate(['near','far']):
                        means,counts=history_means(values[:,:,mi,ai]-initial,alive[:,:,mi,ai])
                        entry['change_from_founders'][arm]=estimate(means,counts)
                    cell['modes'][mode]=entry
                means,counts=interaction(values,alive)
                cell['isolation_effect_evolving_minus_fixed']=estimate(means,counts)
                results.append(cell)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    result=dict(status='completed_verified_summary',integrity=receipt,results=results,
        design_sha256=sha(root/'data/design/model3_assurance_intervention_20261005.json'),
        analysis_sha256=sha(Path(__file__)),
        claim_ceiling='Single fixed capacity0.5 and matched zero-assurance-variance founders. Conditional-survival contrasts, descriptive history bootstrap, no mediation fraction. Interaction uses same four surviving cells. Zero mutation is a structural negative control.')
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'endpoint_cells':len(results)}))


if __name__=='__main__':main()
