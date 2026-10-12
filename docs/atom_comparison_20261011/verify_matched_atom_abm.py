"""Independently reconstruct every matched descriptive event and checkpoint.

Uses archived trajectory arrays, not producer event helpers. This is not a
fresh evolutionary simulation or a raw-genome reconstruction of every mean.
"""
from pathlib import Path
from collections import Counter
import hashlib,json
import numpy as np

BASE=Path(__file__).resolve().parents[2]
NUM=BASE/'work/resolution_20261011/atom_cell_numerical'
ABM=BASE/'work/EL_order_boundary_20261007/assurance_causal_campaign_20261008/archives'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def events(means,delta):
    def onset(column,direction):
        streak=0
        for t,value in enumerate(means[:,column]):
            gain=direction*(value-means[0,column])
            streak=streak+1 if np.isfinite(gain) and gain>=delta else 0
            if streak==20:return t-19
        return None
    a,i=onset(2,1),onset(1,-1)
    if a is None:label='neither' if i is None else 'investment_only'
    elif i is None:label='assurance_only'
    elif abs(a-i)<=5:label='near_simultaneous'
    else:label='assurance_first' if a<i else 'investment_first'
    return dict(assurance_time=a,investment_time=i,category=label)


def main():
    data=json.loads((NUM/'matched_comparison.json').read_text())
    reg=json.loads((NUM/'registration.json').read_text())
    admitted=json.loads((NUM/'admission.json').read_text())
    assert data['status']=='all_ten_contexts_accounted'
    expected={r['context'] for r in admitted['contexts'] if r['admitted']}
    assert len(expected)==len(data['rows'])==10
    assert {r['context'] for r in data['rows']}==expected
    names=set();event_checks=0;checkpoint_checks=0;density_hashes={}
    for row in data['rows']:
        assert row['status']=='admitted_descriptive_comparison'
        means=[];population=[]
        for replicate in range(32):
            name=row['context'].replace('_r0_',f'_r{replicate}_')+'.npz'
            p=ABM/name;assert sha(p)==data['abm_archive_sha256'][name]
            names.add(name)
            with np.load(p,allow_pickle=False) as a:
                means.append(a['means'].copy());population.append(a['population'].copy())
        means=np.array(means);population=np.array(population)
        assert means.shape==(32,201,3) and population.shape==(32,201)
        job=next(j for j in reg['jobs'] if j['task']['key']==row['context'] and j['nodes']==257)
        key=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        p=NUM/'archives'/(key+'.npz');density_hashes[p.name]=sha(p)
        with np.load(p,allow_pickle=False) as a:density=a['trace'].copy()
        assert {e['threshold'] for e in row['events']}=={.025,.05,.1}
        for e in row['events']:
            assert events(density[:,1:4],e['threshold'])==e['density']
            counts=Counter(events(m,e['threshold'])['category'] for m in means)
            assert sum(e['abm_counts'].values())==32
            assert all(counts[k]==n for k,n in e['abm_counts'].items())
            event_checks+=33
        for c in row['checkpoints']:
            t=c['year'];live=population[:,t]>0
            assert c['all_starts']==32 and c['living_abm_starts']==int(live.sum())
            assert c['abm_occupied_fraction']==float(live.mean())
            np.testing.assert_allclose(c['density'],density[t],atol=1e-12,rtol=0,equal_nan=True)
            if live.any():np.testing.assert_allclose(c['abm_living_mean_traits'],means[live,t].mean(axis=0),atol=1e-12,rtol=0)
            else:assert c['abm_living_mean_traits'] is None
            checkpoint_checks+=1
    assert names==set(data['abm_archive_sha256']) and len(names)==320
    assert event_checks==990 and checkpoint_checks==40
    result=dict(status='all320_abm_and10_density_descriptive_readouts_independently_recomputed',
        matched_comparison_sha256=sha(NUM/'matched_comparison.json'),abm_archives=320,density_archives=10,
        event_checks=event_checks,checkpoint_checks=checkpoint_checks,density_archive_sha256=density_hashes,
        verifier_sha256=sha(__file__),scope='Archived trajectory-array event and checkpoint recomputation; no additional ecological test or raw-genome mean reconstruction')
    out=NUM/'matched_comparison_independent_verification.json'
    if out.exists():assert json.loads(out.read_text())==result
    else:out.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],event_checks,checkpoint_checks)


if __name__=='__main__':main()
