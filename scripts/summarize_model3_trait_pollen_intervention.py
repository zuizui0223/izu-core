"""Full-design paired-history contrasts for exploratory trait interventions."""
from pathlib import Path
import hashlib,json
from itertools import product
import numpy as np


def main():
    root=Path(__file__).resolve().parents[1]
    plan=json.loads((root/'data/design/model3_trait_pollen_intervention_20261005.json').read_text(encoding='utf-8'))
    path=root/'outputs/model3_trait_pollen_intervention_20261005/records.json'
    receiptpath=root/'data/results/model3_trait_pollen_intervention_20261005.json'
    target=root/'data/results/model3_trait_pollen_intervention_summary_20261005.json'
    if target.exists():raise ValueError('preserve prior summary')
    receipt=json.loads(receiptpath.read_text(encoding='utf-8'))
    assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['records_sha256']
    rows=json.loads(path.read_text(encoding='utf-8'))
    keys=['setting','history_seed','arm','period','investment','capacity']
    indexed={tuple(r[k] for k in keys):r for r in rows}
    expected=set(product(plan['settings'],range(76001,76065),plan['arms'],plan['visitor_snapshots'],plan['investment_values'],plan['capacity_values']))
    assert set(indexed)==expected and len(rows)==len(indexed)==6912
    metrics=plan['metrics'];summaries=[]
    draws=np.random.default_rng(8102026).integers(0,64,(5000,64))
    for setting,arm,period in product(plan['settings'],plan['arms'],plan['visitor_snapshots']):
        values=np.array([[[[indexed[(setting,seed,arm,period,i,a)][metric] for metric in metrics]
            for a in plan['capacity_values']] for i in plan['investment_values']] for seed in range(76001,76065)],dtype=float)
        assert np.isfinite(values).all()
        contrasts=[]
        for j,value in enumerate(plan['investment_values']):
            contrasts.append(('capacity_high_minus_low',value,values[:,j,2]-values[:,j,0]))
        for j,value in enumerate(plan['capacity_values']):
            contrasts.append(('investment_high_minus_low',value,values[:,2,j]-values[:,0,j]))
        contrasts.append(('interaction',None,values[:,2,2]-values[:,2,0]-values[:,0,2]+values[:,0,0]))
        results=[]
        for kind,fixed,x in contrasts:
            boot=x[draws].mean(axis=1);bounds=np.quantile(boot,[.025,.975],axis=0)
            results.append(dict(contrast=kind,fixed_trait_value=fixed,history_count=64,
                metrics={metric:dict(mean=float(x[:,j].mean()),interval=bounds[:,j].tolist()) for j,metric in enumerate(metrics)}))
        summaries.append(dict(setting=setting,arm=arm,period=period,
            cell_means=[dict(investment=i,capacity=a,metrics=dict(zip(metrics,values[:,ii,ai].mean(axis=0).tolist())))
                for ii,i in enumerate(plan['investment_values']) for ai,a in enumerate(plan['capacity_values'])],contrasts=results))
    result=dict(status='complete_exploratory_summary',records=6912,summaries=summaries,
        records_sha256=receipt['records_sha256'],analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limits=plan['limits'])
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],cells=len(summaries),contrasts=sum(len(s['contrasts']) for s in summaries))))


if __name__=='__main__':main()
