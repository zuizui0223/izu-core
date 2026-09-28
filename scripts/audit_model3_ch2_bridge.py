"""Retrospective Ch2 question audit of every frozen Model 3 transport case."""
import argparse
from hashlib import sha256
from pathlib import Path
import json
import numpy as np
from scripts.model3_island.design import compile_design,digest,canonical,source_hashes
from scripts.model3_island.summarize import decompose_crossed


def _label(x,epsilon):
    if not np.isfinite(x).all(): return 'undefined'
    pos=bool(np.any(x>epsilon)); neg=bool(np.any(x < -epsilon))
    return 'mixed' if pos and neg else 'positive' if pos else 'negative' if neg else 'neutral'


def classify_histories(values,epsilon):
    x=np.asarray(values,float)
    if x.ndim!=3 or x.shape[0]<2 or min(x.shape[1:])<1 or not np.isfinite(epsilon) or epsilon<0:
        raise ValueError('need starts x histories x repeats and nonnegative deadband')
    labels=[_label(x[:,i,:].mean(axis=1),epsilon) for i in range(x.shape[1])]
    counts={k:labels.count(k) for k in ('mixed','positive','negative','neutral','undefined')}
    eligible=x.shape[1]-counts['undefined']
    half=np.sqrt(np.log(40)/(2*eligible)) if eligible else None
    p=counts['mixed']/eligible if eligible else None
    return dict(counts=counts,n_histories=x.shape[1],n_eligible=eligible,
        mixed_fraction=p,mixed_fraction_hoeffding_95=None if p is None else [max(0.,p-half),min(1.,p+half)],
        repeat_disagreements=sum(len({_label(x[:,i,j],epsilon) for j in range(x.shape[2])})>1 for i in range(x.shape[1])),
        labels=labels,epsilon=float(epsilon),
        scope='three starting populations, repeat-mean descriptive labels; not noise-free branching probability')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args(); root=Path('data/results/model3_island_v2')
    d=json.loads(Path('data/design/model3_island_v2.json').read_text())
    assert source_hashes()==d['source_hashes']
    audit=json.loads(Path('data/results/model3_island_v2_audit.json').read_text())
    assert audit['status']=='passed' and audit['manifest_hash']==digest(d)
    cases=[c for c in compile_design(d) if c['family']=='transport' and c['cohort']!='pilot']
    assert len(cases)==3072
    tensors={}; initial={}; visitor={}; receipts=[]
    for cohort in ('production','heldout'):
        for dist in (0,3):
            for mode in ('individual','density'):
                tensors[cohort,dist,mode]=np.full((3,128,2),np.nan)
    for c in cases:
        folder=root/c['case_id']; raw=(folder/'arrays.npz').read_bytes()
        r=json.loads((folder/'receipt.json').read_text())
        assert r['status']=='complete' and r['case_hash']==digest(c) and r['manifest_hash']==digest(d)
        assert sha256(raw).hexdigest()==r['arrays_sha256']
        assert json.loads((folder/'input.json').read_text())==c
        cohort=c['cohort'];cell=c['cell']['id'];dist=int(cell.split('_')[1][1:]);start=[3,5,7].index(int(cell.split('_')[2][1:]))
        hi=d['cohorts'][cohort].index(c['history_seed']);di=d['demographic_seeds'].index(c['demographic_seed'])
        with np.load(folder/'arrays.npz',allow_pickle=False) as a:
            for mode,key,pop in [('individual','trait_mean','population'),('density','density_traits','density_mass')]:
                x=a[key];valid=a[pop][-1]>0 and np.isfinite(x[[0,-1],1]).all()
                tensors[cohort,dist,mode][start,hi,di]=float(x[-1,1]-x[0,1]) if valid else np.nan
            k=(cohort,start,hi,di)
            if dist==0:initial[k]=a['initial_genotypes'].copy()
            else:
                # compile order is distance 0 before distance 3
                assert np.array_equal(initial[k],a['initial_genotypes'])
            vk=(cohort,dist,hi)
            vc=a['visitor_count']
            if vk in visitor: assert np.array_equal(visitor[vk],vc)
            else:visitor[vk]=vc.copy()
        receipts.append({'case_id':c['case_id'],'arrays_sha256':r['arrays_sha256']})
    reports=[]
    for cohort in ('production','heldout'):
        for mode in ('individual','density'):
            for label,x in [('near_change',tensors[cohort,0,mode]),('isolated_change',tensors[cohort,3,mode]),('isolation_effect',tensors[cohort,3,mode]-tensors[cohort,0,mode])]:
                reports.append(dict(cohort=cohort,model=mode,endpoint=label,
                    mean=float(np.nanmean(x)),mean_by_start=np.nanmean(x,axis=(1,2)).tolist(),
                    classification=[classify_histories(x,e) for e in (0,.01,.05)],
                    decomposition=decompose_crossed(x,{'S':[1/3]*3,'C':[1/128]*128})))
    payload=dict(status='retrospective_audit_complete',manifest_hash=digest(d),cases_checked=len(cases),
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),reports=reports,receipts=receipts,
        visitor_counts={f'{cohort}_d{dist}':float(np.mean([v.mean() for k,v in visitor.items() if k[:2]==(cohort,dist)])) for cohort in ('production','heldout') for dist in (0,3)},
        ceilings=['old endpoint was service; new endpoint is inherited investment','previously inspected cohorts are not fresh confirmation','two repeats cannot identify latent mixed-sign probabilities','not a richness-matched or visitor-averaged experiment','numerical convergence remains unestablished'])
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(canonical(payload))
    print(json.dumps({'status':payload['status'],'cases_checked':len(cases),'reports':[{k:r[k] for k in ('cohort','model','endpoint','mean')}|{'mixed':[q['counts']['mixed'] for q in r['classification']]} for r in reports]}))

if __name__=='__main__': main()
