"""Verify what the frozen 200/800 intervention actually equates."""
from pathlib import Path
import hashlib,json
import numpy as np
from scripts.run_model3_full_mutation import config,exposure


def same(a,b):
    return all(np.array_equal(getattr(a,k),getattr(b,k))
               for k in ['ids','optima','breadths','effectiveness'])


def main():
    root=Path(__file__).resolve().parents[1];rows=[]
    for seed in range(76001,76065):
        near,far=exposure(seed,'near'),exposure(seed,'far')
        assert len(near.visitors)==len(far.visitors)==1000
        assert same(near.visitors[0],far.visitors[0])
        assert all(same(a,b) for a,b in zip(near.visitors[200:],far.visitors[200:]))
        assert all(len(p.ids)==0 for h in [near,far] for p in h.seed_candidates)
        changed=sum(not same(a,b) for a,b in zip(near.visitors[:200],far.visitors[:200]))
        temporal=sum(not same(a,b) for a,b in zip(near.visitors[200:999],near.visitors[201:]))
        assert changed>0 and temporal>0
        rows.append(dict(seed=seed,first_phase_different_snapshots=changed,
            common_phase_temporal_changes=temporal,common_phase_identical_snapshots=800))
    c=config('assurance_cost',.01)
    paths=['scripts/run_model3_full_mutation.py','scripts/model3_island/history.py',
           'scripts/audit_model3_common_environment_design.py','data/design/model3_ch2_bridge_20260927.json']
    result=dict(status='passed',histories=64,rows=rows,
        common_phase_matched_fields=['ids','optima','breadths','effectiveness'],
        initialization='same four visitor types and same plant founder specification',
        mean_established_arrivals_first_phase={'near':c.visitor_arrival.supply*c.visitor_arrival.establishment,
           'far':c.visitor_arrival.supply*c.visitor_arrival.establishment*float(np.exp(-3/c.visitor_arrival.scale))},
        interpretation='controlled visitor-history equalization after 200 updates; not continuous isolation or natural reconnection',
        excluded_claims=['geologically calibrated duration','equilibrium','irreversibility','oceanic versus continental island contrast'],
        sources={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths})
    path=root/'data/results/model3_common_environment_design_audit_20261005.json'
    if path.exists():raise ValueError('preserve existing audit')
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Verified64 histories:51,200 identical post-transfer snapshots, ongoing temporal change, no seed arrivals.')


if __name__=='__main__':main()
