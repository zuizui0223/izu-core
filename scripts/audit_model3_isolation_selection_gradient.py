"""Local selection along an arrival-distance gradient; plants never evolve."""
from pathlib import Path
from dataclasses import replace
import hashlib,itertools,json
import numpy as np
from scripts.run_model3_persistent_isolation import config
from scripts.model3_island.run import history_from_spec
from scripts.model3_island.selection import syndrome_thresholds

ROOT=Path(__file__).resolve().parents[1]

def main():
    design_path=ROOT/'data/design/model3_isolation_selection_gradient_20261005.json'
    d=json.loads(design_path.read_text(encoding='utf-8'))
    for p,sha in d['source_sha256'].items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
    out=ROOT/'outputs/model3_isolation_selection_gradient_20261005';out.mkdir(parents=True,exist_ok=True)
    if (out/'gradients.npz').exists():raise ValueError('preserve completed diagnostic')
    decision=json.loads((ROOT/'data/design/model3_joint_syndrome_rare_mutant_20261004.json').read_text())
    states=np.array(list(itertools.product(*(decision['resident_states'][k] for k in ['access','investment','assurance']))))
    shape=(len(d['settings']),len(d['distances']),len(d['history_seeds']),len(d['snapshots']),len(states),2)
    values=np.empty(shape);counts=np.empty(shape[1:4],dtype=int)
    configs=[config(s,0.) for s in d['settings']]
    for di,distance in enumerate(d['distances']):
        c=replace(configs[0],years=d['history_duration'],visitor_arrival=replace(configs[0].visitor_arrival,distance=distance))
        for hi,seed in enumerate(d['history_seeds']):
            h=history_from_spec(c,{'kind':'assembly'},seed)
            for ti,t in enumerate(d['snapshots']):
                visitors=h.visitors[t];counts[di,hi,ti]=len(visitors.ids)
                for si,cfg in enumerate(configs):
                    q=syndrome_thresholds(states,visitors,cfg)
                    values[si,di,hi,ti,:,0]=q['investment_gradient']
                    values[si,di,hi,ti,:,1]=q['assurance_gradient']
        print('distance',distance,'completed',flush=True)
    assert np.isfinite(values).all()
    # Initial communities must match across distance treatments.
    assert np.array_equal(values[:,:,:,0],np.broadcast_to(values[:,0:1,:,0],values[:,:,:,0].shape))
    means=values.mean(axis=2);rng=np.random.default_rng(105760)
    draws=rng.integers(0,64,size=(1999,64));weights=np.array([np.bincount(v,minlength=64) for v in draws])/64
    intervals=np.empty(means.shape+(2,))
    for si in range(len(configs)):
        boot=np.einsum('bh,dhtsk->bdtsk',weights,values[si],optimize=True)
        intervals[si]=np.moveaxis(np.quantile(boot,[.025,.975],axis=0),0,-1)
    np.savez_compressed(out/'gradients.npz',gradients=values,counts=counts,states=states,means=means,intervals=intervals,distances=d['distances'],snapshots=d['snapshots'])
    rows=[]
    for si,setting in enumerate(d['settings']):
        for ti,t in enumerate(d['snapshots']):
            for pi,state in enumerate(states):
                row=dict(setting=setting,snapshot=t,state=state.tolist())
                for ki,name in enumerate(['investment_decrease','capacity_increase']):
                    y=means[si,:,ti,pi,ki];target=y<0 if ki==0 else y>0
                    row[name]=dict(already_favoured_at_zero=bool(target[0]),
                        first_target_distance=float(np.array(d['distances'])[target][0]) if target.any() else None,
                        entry_brackets=[[d['distances'][j-1],d['distances'][j]] for j in range(1,len(target)) if target[j] and not target[j-1]],
                        exit_brackets=[[d['distances'][j-1],d['distances'][j]] for j in range(1,len(target)) if target[j-1] and not target[j]])
                rows.append(row)
    result=dict(classification=d['classification'],status='complete',histories=len(d['distances'])*64,gradient_values=values.size,
                rows=rows,source_design_sha256=hashlib.sha256(design_path.read_bytes()).hexdigest(),arrays_sha256=hashlib.sha256((out/'gradients.npz').read_bytes()).hexdigest(),
                scope=d['limits'],uncertainty=d['uncertainty'])
    (ROOT/'data/results/model3_isolation_selection_gradient_20261005.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    print('completed',values.shape,flush=True)

if __name__=='__main__':main()
