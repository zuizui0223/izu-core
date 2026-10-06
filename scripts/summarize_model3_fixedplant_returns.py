"""Full precision-gated fixed-plant return comparisons, paired by visitor history."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_fixedplant_returns_20261005'
    receipt=root/'data/results/model3_fixedplant_returns_20261005.json'
    target=root/'data/results/model3_fixedplant_returns_summary_20261005.json'
    if not receipt.exists():raise ValueError('incomplete diagnostic; no partial readout')
    if target.exists():raise ValueError('preserve previous summary')
    result=json.loads(receipt.read_text(encoding='utf-8'))
    assert result['status']=='precision_passed' and result['cases']==768 and result['failed_cases']==0
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for name,key in [('sources.json','sources_sha256'),('records.json','records_sha256'),('individual_arrays.npz','arrays_sha256')]:
        assert sha(out/name)==result[key]
    sources=json.loads((out/'sources.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(out/'sources.zip') as archive:
        for name,digest in sources.items():assert sha(root/name)==hashlib.sha256(archive.read(name)).hexdigest()==digest
    rows=json.loads((out/'records.json').read_text(encoding='utf-8'))
    lookup={(r['setting'],r['history_seed'],r['arm'],r['period']):r for r in rows}
    expected={(s,h,a,t) for s in ['assurance_cost','prior_selfing'] for h in range(76001,76065) for a in ['near','far'] for t in [0,200,400]}
    assert len(rows)==len(lookup)==768 and set(lookup)==expected
    with np.load(out/'individual_arrays.npz') as arrays:
        assert len(arrays.files)==768
        for (s,h,a,t),row in lookup.items():
            array=arrays[f'{s}_h{h}_{a}_t{t}']
            assert array.shape==(3,48) and np.isfinite(array).all()
            assert np.all(array[2]<=1e-4+1e-3*np.abs(array[0]))
            assert np.isclose(array[0].mean(),row['mean_gradient'])
            assert np.isclose((array[0]<0).mean(),row['negative_fraction'])
            assert np.isclose(array[1].mean(),row['mean_outcross_gradient'])
            assert np.isclose(array[2].max(),row['max_step_error'])
            if t==0:
                partner=lookup[s,h,'far' if a=='near' else 'near',t]
                for name in ['mean_gradient','raw_deficit','viable_deficit','received_pollen']:
                    assert row[name]==partner[name]
    draws=np.random.default_rng(8102026).integers(0,64,(5000,64))
    summaries=[]
    for setting in ['assurance_cost','prior_selfing']:
        for period in [0,200,400]:
            entry=dict(setting=setting,period=period,metrics={})
            for metric in ['mean_gradient','negative_fraction','mean_outcross_gradient','received_pollen','raw_deficit','viable_deficit']:
                near=np.array([lookup[setting,h,'near',period][metric] for h in range(76001,76065)])
                far=np.array([lookup[setting,h,'far',period][metric] for h in range(76001,76065)])
                diff=far-near
                entry['metrics'][metric]=dict(near_mean=float(near.mean()),far_mean=float(far.mean()),
                    far_minus_near=float(diff.mean()),interval=np.quantile(diff[draws].mean(axis=1),[.025,.975]).tolist())
            summaries.append(entry)
    target.write_text(json.dumps(dict(status='verified_complete',cases=768,records_sha256=result['records_sha256'],
        analysis_sha256=sha(Path(__file__)),summaries=summaries,
        claim_ceiling='Paired visitor histories at identical plant state and capacity0.5; instantaneous contribution gradient, not realized evolution. Visitor richness and composition change together. Descriptive intervals, no multiplicity correction.'),indent=2)+'\n',encoding='utf-8')
    print(json.dumps([r for r in summaries if r['period']==400],indent=2))


if __name__=='__main__':main()
