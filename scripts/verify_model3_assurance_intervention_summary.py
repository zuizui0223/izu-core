"""Independent row-wise reconstruction of full capacity-intervention readout."""
from pathlib import Path
import hashlib,json
import numpy as np


def verify_estimate(reported,groups,counts):
    sample=np.array([np.mean(group,axis=0) for group in groups if group])
    assert reported['histories']==len(sample)
    assert reported['missing_histories']==64-len(sample)
    assert reported['eligible_replicates']==sum(counts)
    if not len(sample):
        assert reported['traits']=={}
        return
    draws=np.random.default_rng(6102026).integers(0,len(sample),(5000,len(sample)))
    ci=np.quantile(sample[draws].mean(axis=1),[.025,.975],axis=0)
    for j,name in enumerate(['matching','investment','capacity']):
        np.testing.assert_allclose(reported['traits'][name]['mean'],sample[:,j].mean(),rtol=1e-12,atol=1e-12)
        np.testing.assert_allclose(reported['traits'][name]['interval'],ci[:,j],rtol=1e-12,atol=1e-12)


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_assurance_intervention_20261005'
    summarypath=root/'data/results/model3_assurance_intervention_summary_20261005.json'
    resultpath=root/'data/results/model3_assurance_intervention_verified_20261005.json'
    summary=json.loads(summarypath.read_text())
    assert summary['integrity']['checked_cases']==8192
    assert summary['integrity']['zero_mutation_matched_pairs_identical']==2048
    assert len(summary['results'])==12
    raw={};initial=None
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            for seed in range(76001,76065):
                for rep in range(7101,7109):
                    for arm in ['near','far']:
                        for mode in ['fixed','evolving']:
                            key=(setting,rate,seed,rep,arm,mode)
                            p=out/f'{setting}_u{rate}_h{seed}_r{rep}_{arm}_{mode}.npz'
                            receipt=json.loads(p.with_suffix('.json').read_text())
                            assert receipt['task']==list(key)
                            assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
                            with np.load(p) as z:
                                raw[key]=z['trace'][[200,400,1000],:4].copy()
                                founder=z['trace'][0,1:4]
                                if initial is None:initial=founder.copy()
                                np.testing.assert_array_equal(founder,initial)
    checked=0
    for cell in summary['results']:
        setting,rate,period=cell['setting'],cell['mutation_rate'],cell['period']
        index=[200,400,1000].index(period)
        for mode in ['fixed','evolving']:
            entry=cell['modes'][mode]
            for contrast in ['far_minus_near','near','far']:
                groups=[];counts=[];alive_total=0
                for seed in range(76001,76065):
                    group=[]
                    for rep in range(7101,7109):
                        near=raw[(setting,rate,seed,rep,'near',mode)][index]
                        far=raw[(setting,rate,seed,rep,'far',mode)][index]
                        if contrast=='far_minus_near':
                            if near[0]>0 and far[0]>0:group.append(far[1:]-near[1:])
                        else:
                            row=near if contrast=='near' else far
                            if row[0]>0:group.append(row[1:]-initial);alive_total+=1
                    groups.append(group);counts.append(len(group))
                report=entry['far_minus_near'] if contrast=='far_minus_near' else entry['change_from_founders'][contrast]
                verify_estimate(report,groups,counts);checked+=1
                if contrast!='far_minus_near':assert entry['occupancy'][contrast]==alive_total/512
        groups=[];counts=[]
        for seed in range(76001,76065):
            group=[]
            for rep in range(7101,7109):
                fnear=raw[(setting,rate,seed,rep,'near','fixed')][index]
                ffar=raw[(setting,rate,seed,rep,'far','fixed')][index]
                enear=raw[(setting,rate,seed,rep,'near','evolving')][index]
                efar=raw[(setting,rate,seed,rep,'far','evolving')][index]
                if all(x[0]>0 for x in [fnear,ffar,enear,efar]):
                    group.append((efar[1:]-enear[1:])-(ffar[1:]-fnear[1:]))
            groups.append(group);counts.append(len(group))
        verify_estimate(cell['isolation_effect_evolving_minus_fixed'],groups,counts);checked+=1
    result=dict(status='verified',raw_cases=len(raw),estimates=checked,summary_sha256=hashlib.sha256(summarypath.read_bytes()).hexdigest(),
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if resultpath.exists():assert json.loads(resultpath.read_text())==result
    else:resultpath.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
