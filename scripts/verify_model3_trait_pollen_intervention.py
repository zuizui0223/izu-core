"""Reconstruct contrasts from row keys, independently of summary array layout."""
from pathlib import Path
from itertools import product
import hashlib,json,zipfile
import numpy as np


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_trait_pollen_intervention_20261005'
    target=root/'data/results/model3_trait_pollen_intervention_verified_20261005.json'
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=json.loads((root/'data/results/model3_trait_pollen_intervention_20261005.json').read_text())
    summarypath=root/'data/results/model3_trait_pollen_intervention_summary_20261005.json'
    summary=json.loads(summarypath.read_text())
    assert sha(out/'records.json')==receipt['records_sha256']==summary['records_sha256']
    assert sha(out/'sources.json')==receipt['source_manifest_sha256']
    with zipfile.ZipFile(out/'sources.zip') as z:
        for name,digest in json.loads((out/'sources.json').read_text()).items():
            assert sha(root/name)==hashlib.sha256(z.read(name)).hexdigest()==digest
    rows=json.loads((out/'records.json').read_text())
    keys=['setting','history_seed','arm','period','investment','capacity']
    expected=set(product(['assurance_cost','prior_selfing'],range(76001,76065),['near','far'],[0,200,400],[.25,.5,.75],[.25,.5,.75]))
    assert {tuple(x[k] for k in keys) for x in rows}==expected and len(rows)==6912
    for row in rows:
        for label in ['raw','viable']:
            np.testing.assert_allclose(row[label+'_deficit'],1-row['natural_'+label]/row['saturated_'+label],rtol=0,atol=2e-15)
    assert len(summary['summaries'])==12
    checked=0
    for cell in summary['summaries']:
        subset=[x for x in rows if all(x[k]==cell[k] for k in ['setting','arm','period'])]
        assert len(subset)==576 and len(cell['contrasts'])==7
        for mean in cell['cell_means']:
            selected=[x for x in subset if x['investment']==mean['investment'] and x['capacity']==mean['capacity']]
            for metric,value in mean['metrics'].items():
                np.testing.assert_allclose(value,np.mean([x[metric] for x in selected]),rtol=1e-12,atol=1e-12)
        for contrast in cell['contrasts']:
            terms=[]
            for seed in range(76001,76065):
                d={(x['investment'],x['capacity']):x for x in subset if x['history_seed']==seed}
                fixed=contrast['fixed_trait_value'];kind=contrast['contrast']
                if kind=='capacity_high_minus_low':pairs=[(1,(fixed,.75)),(-1,(fixed,.25))]
                elif kind=='investment_high_minus_low':pairs=[(1,(.75,fixed)),(-1,(.25,fixed))]
                elif kind=='interaction':pairs=[(1,(.75,.75)),(-1,(.75,.25)),(-1,(.25,.75)),(1,(.25,.25))]
                else:raise ValueError('unknown contrast')
                terms.append([sum(sign*d[key][metric] for sign,key in pairs) for metric in contrast['metrics']])
            a=np.array(terms)
            draws=np.random.default_rng(8102026).integers(0,64,(5000,64))
            ci=np.quantile(a[draws].mean(1),[.025,.975],axis=0)
            for j,(metric,reported) in enumerate(contrast['metrics'].items()):
                np.testing.assert_allclose(reported['mean'],a[:,j].mean(),atol=1e-12,rtol=1e-12)
                np.testing.assert_allclose(reported['interval'],ci[:,j],atol=1e-12,rtol=1e-12)
            checked+=1
    result=dict(status='verified',records=len(rows),contrasts=checked,summary_sha256=sha(summarypath),
        records_sha256=sha(out/'records.json'),verifier_sha256=sha(Path(__file__)))
    if target.exists():assert json.loads(target.read_text())==result
    else:target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
