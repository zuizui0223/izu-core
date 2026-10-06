"""Independent stored-curve readout check, with explicit missing-data handling."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/model3_replenishment_evolution_20261005'


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def finite_mean(a,axis):
    n=np.isfinite(a).sum(axis=axis)
    return np.divide(np.nansum(a,axis=axis),n,out=np.full(n.shape,np.nan),where=n>0)


def crossing(values,threshold):
    # Deliberately do not call the production convolution helper.
    for t in range(len(values)-19):
        window=values[t:t+20]
        if np.isfinite(window).all() and (window>=threshold).all(): return t
    return None


def label(a,i):
    if a is None:return 'neither' if i is None else 'investment_only'
    if i is None:return 'assurance_only'
    if abs(a-i)<=5:return 'near_simultaneous'
    return 'assurance_first' if a<i else 'investment_first'


def main():
    path=ROOT/'data/results/model3_replenishment_evolution_summary_20261005.json'
    result=json.loads(path.read_text());assert result['status']=='complete_all_declared_rates'
    assert digest(OUT/'evolution_curves.npz')==result['array_sha256']
    assert digest(ROOT/'data/design/model3_replenishment_evolution_20261005.json')==result['source_plan_sha256']
    assert digest(ROOT/'scripts/summarize_model3_replenishment_evolution.py')==result['analysis_sha256']
    arrays=np.load(OUT/'evolution_curves.npz');events=0
    assert len(result['temporal_order'])==156 and len(result['endpoints'])==156
    for row in result['temporal_order']:
        vals=arrays[f"{row['setting']}_d{row['distance']:.2f}_{row['contrast']}"]
        assert vals.shape==(64,1001,3);counts=Counter()
        for values,event in zip(vals,row['events']):
            a=crossing(values[:,2],row['threshold']);i=crossing(-values[:,1],row['threshold'])
            assert [a,i]==[event['capacity_time'],event['investment_time']]
            assert label(a,i)==event['order'];counts[label(a,i)]+=1;events+=1
        assert dict(counts)==row['counts'] and sum(counts.values())==64
    samples=np.random.default_rng(4102026).integers(0,64,size=(5000,64));maxerr=0.
    for row in result['endpoints']:
        key=f"{row['setting']}_d{row['distance']:.2f}"
        vals=arrays[key+'_'+row['contrast']][:,row['update']]
        for j,name in enumerate(['matching','investment','capacity']):
            v=vals[:,j];estimate=row['traits'][name]
            actual=finite_mean(v,0);boots=finite_mean(v[samples],1)
            ci=np.quantile(boots,[.025,.975]) if np.isfinite(boots).all() else [np.nan,np.nan]
            stored=np.array([estimate['mean'],*estimate['pointwise_interval']],dtype=float)
            expected=np.array([actual,*ci]);np.testing.assert_allclose(stored,expected,atol=1e-13,rtol=0,equal_nan=True)
            delta=np.abs(stored-expected);maxerr=max(maxerr,float(np.nanmax(delta)) if np.isfinite(delta).any() else 0.)
            assert estimate['histories_observed']==int(np.isfinite(v).sum())
        assert row['occupied_cases']==int(arrays[key+'_occupancy'][:,row['update']].sum())
        assert row['paired_cases']==int(arrays[key+'_paired_occupancy'][:,row['update']].sum())
    assert events==9984
    receipt=dict(status='verified_all_curve_readouts',temporal_records=events,endpoint_rows=156,
                 max_numeric_difference=maxerr,summary_sha256=digest(path),
                 scope='Independently derives events and intervals from stored curves. Raw-case checks belong to the complete-campaign summarizer; no independent biological-model implementation claimed.')
    (ROOT/'data/results/model3_replenishment_readout_verified_20261005.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))


if __name__=='__main__':main()
