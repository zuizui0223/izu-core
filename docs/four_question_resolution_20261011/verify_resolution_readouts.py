"""Independent all-start pairing, interval and practical-bound arithmetic."""
import json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent

def sha(p):
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()

def score(r):return {'assurance_first':1,'investment_first':-1}.get(r['events']['0.05']['category'],0)

def interval(x,family,seed):
    rng=np.random.default_rng(seed);estimates=[]
    for block in x:
        indices=rng.integers(0,len(block),size=(19999,len(block)))
        estimates.append(np.take(block,indices).mean(axis=1))
    return np.quantile(np.mean(estimates,axis=0),[.025/family,1-.025/family])

def main():
    checked={}
    for study,total in (('boundary',6144),('history',3072)):
        p=ROOT/(study+'_records.json');record=json.loads(p.read_text());report=json.loads((ROOT/(study+'_readout.json')).read_text())
        assert record['status']==report['status']=='complete_verified' and record['cases']==len(record['records'])==total
        assert report['records_sha256']==sha(p);rows=record['records']
        if study=='boundary':
            assert report['interval_family']==12 and len(report['groups'])==12
            indexed={}
            for ix,g in enumerate(report['groups']):
                rs=sorted([r for r in rows if all(r['task'][k]==g[k] for k in ('block','supply','composition','width'))],key=lambda r:r['task']['replicate'])
                assert len(rs)==512 and [r['task']['replicate'] for r in rs]==list(range(512))
                x=np.array([[score(r) for r in rs]])
                assert x.mean()==g['D'];np.testing.assert_allclose(interval(x,12,2026101191+ix),g['simultaneous_interval'],atol=1e-14,rtol=0)
                indexed[(g['block'],g['supply'],g['composition'],g['width'])]=g
            expected=[]
            for supply,composition in ((0.,'empty'),(.125,'matched'),(.125,'separated')):
                if all(indexed[(b,supply,composition,.046875)]['simultaneous_interval'][1]<0 and indexed[(b,supply,composition,.078125)]['simultaneous_interval'][0]>0 for b in ('main','confirmation')):expected.append(dict(supply=supply,composition=composition,band=[.046875,.078125],resolution=.03125))
            assert expected==report['replicated_transition_bands']
        else:
            lookup={(r['task']['block'],r['task']['replicate'],r['task']['arm']):r for r in rows};assert len(lookup)==3072
            first=np.array([[score(lookup[(b,i,'A_access_first')]['preparation'])-score(lookup[(b,i,'I_access_first')]['preparation']) for i in range(512)] for b in ('main','confirmation')])
            f=report['first_stage'];assert first.mean()==f['order_score_difference']
            ci=2*interval(first/2,1,2026101291);np.testing.assert_allclose(ci,f['interval'],atol=1e-14,rtol=0);assert f['intended_shift']==bool(ci[0]>0)
            assert report['primary_family']==4 and len(report['contexts'])==2
            for ix,context in enumerate(report['contexts']):
                target=context['target'];assert target==(1.05,1.5)[ix] and context['starts_per_arm']==1024
                def future(b,i,a):return next(r for r in lookup[(b,i,a)]['future'] if r['target']==target)
                for m,metric in enumerate(('survived','occupied_updates')):
                    scale=1 if metric=='survived' else 200
                    x=np.array([[(float(future(b,i,'A_access_first')[metric])-float(future(b,i,'I_access_first')[metric]))/scale for i in range(512)] for b in ('main','confirmation')])
                    output=context['primary'][metric];assert output['scale']==scale and x.mean()==output['estimate']
                    np.testing.assert_allclose(interval(x,4,2026101391+2*ix+m),output['bootstrap_interval'],atol=1e-14,rtol=0)
                    radius=math.sqrt(2*math.log(8/.05)/1024);bound=[max(-1.,x.mean()-radius),min(1.,x.mean()+radius)]
                    np.testing.assert_allclose(bound,output['hoeffding_interval'],atol=1e-14,rtol=0)
                    assert output['effect_bounded_within_margin']==bool(bound[0]>-.1 and bound[1]<.1) and not output['exact_equivalence']
                for arm,stats in context['descriptive'].items():
                    rs=[future(b,i,arm) for b in ('main','confirmation') for i in range(512)]
                    for k,value in stats.items():np.testing.assert_allclose(np.mean([r[k] for r in rs]),value,atol=1e-12,rtol=1e-14)
        checked[study]=dict(cases=total,status='independent_all_start_arithmetic_verified',records_sha256=sha(p))
    out=ROOT/'independent_readout_verification.json'
    if out.exists():assert json.loads(out.read_text())==checked
    else:out.write_text(json.dumps(checked,indent=2)+'\n')
    print('all independent resolution arithmetic passed',flush=True)

if __name__=='__main__':main()
