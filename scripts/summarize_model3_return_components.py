"""Exploratory arithmetic decomposition of previously verified fixed-plant gradients."""
from pathlib import Path
import hashlib, json
import numpy as np


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'outputs/model3_fixedplant_returns_20261005'
    receipt=json.loads((root/'data/results/model3_fixedplant_returns_20261005.json').read_text(encoding='utf-8'))
    target=root/'data/results/model3_return_components_20261005.json'
    if target.exists():
        raise ValueError('preserve existing result')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert receipt['status']=='precision_passed' and receipt['cases']==768
    assert sha(source/'individual_arrays.npz')==receipt['arrays_sha256']
    assert sha(source/'records.json')==receipt['records_sha256']
    records=json.loads((source/'records.json').read_text(encoding='utf-8'))
    lookup={(r['setting'],r['history_seed'],r['arm'],r['period']):r for r in records}
    draws=np.random.default_rng(8102026).integers(0,64,(5000,64))
    rows=[]
    with np.load(source/'individual_arrays.npz') as arrays:
        assert len(arrays.files)==len(lookup)==768
        for setting in ['assurance_cost','prior_selfing']:
            for period in [0,200,400]:
                values={}
                for arm in ['near','far']:
                    v=[]
                    for h in range(76001,76065):
                        a=arrays[f'{setting}_h{h}_{arm}_t{period}']
                        assert a.shape==(3,48) and np.isfinite(a).all()
                        total,cross=a[:2].mean(axis=1)
                        rec=lookup[setting,h,arm,period]
                        assert np.isclose(total,rec['mean_gradient']) and np.isclose(cross,rec['mean_outcross_gradient'])
                        v.append([cross,total-cross,total])
                    values[arm]=np.array(v)
                for j,name in enumerate(['outcross_contribution','viable_selfed_contribution','total_contribution']):
                    d=values['far'][:,j]-values['near'][:,j]
                    rows.append(dict(setting=setting,period=period,component=name,near=float(values['near'][:,j].mean()),far=float(values['far'][:,j].mean()),difference=float(d.mean()),interval=np.quantile(d[draws].mean(axis=1),[.025,.975]).tolist()))
                for v in values.values():
                    assert np.allclose(v[:,0]+v[:,1],v[:,2],atol=1e-12,rtol=0)
    target.write_text(json.dumps(dict(status='complete',classification='exploratory secondary decomposition',source_arrays_sha256=receipt['arrays_sha256'],script_sha256=sha(Path(__file__)),rows=rows,scope='Gradients of offspring contributions with respect to investment at fixed capacity0.5. Each component includes allocation costs; not pure benefit/cost or causal mediation. Paired-history descriptive intervals.'),indent=2),encoding='utf-8')
    print(json.dumps([r for r in rows if r['period']==400],indent=2))


if __name__=='__main__':
    main()
