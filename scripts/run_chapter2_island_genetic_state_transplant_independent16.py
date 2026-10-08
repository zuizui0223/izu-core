"""Frozen new-visitor 16-history allele-state transplant replication.

Reuses the exact paired diploid-locus transplant method of the preceding
four-history exploratory pilot, but neither reuses seeds nor treats stress
cases as independent ecological histories.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import argparse, json, hashlib, os
from scripts.run_chapter2_island_genetic_state_transplant import load_pilot, run_pair

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'data/design/chapter2_island_genetic_state_transplant_independent16_20261008.json'


def load_frozen():
    protocol=json.loads(DESIGN.read_text(encoding='utf-8'))
    if protocol['status']!='independent_16history_allele_transplant_gate_frozen_before_new_outcomes':
        raise ValueError('unexpected independent16 design state')
    if protocol['expected_post_stress_trajectories']!=2048:
        raise ValueError('unexpected declared case count')
    d,source=load_pilot()
    d=dict(d)
    d['history_seeds']=list(range(protocol['new_visitor_history_seeds']['first'],
                                  protocol['new_visitor_history_seeds']['last']+1))
    d['nested_demographic_repeats']=list(protocol['new_nested_demographic_repeat_seeds'])
    d['n_postshock_trajectories']=protocol['expected_post_stress_trajectories']
    assert d['ovule_budgets']==protocol['post_ovule_budgets']
    assert d['four_settings']==protocol['settings']
    assert len(d['history_seeds'])==16
    return protocol,d,source


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--shard-index',type=int,required=True)
    p.add_argument('--shard-count',type=int,default=8)
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    protocol,d,source=load_frozen()
    jobs=list(product(d['four_settings'],d['history_seeds']))
    assert len(jobs)==protocol['expected_historical_pairs']==64
    if a.shard_count<=0 or not 0<=a.shard_index<a.shard_count:
        raise ValueError('invalid shard')
    selected=[g for i,g in enumerate(jobs) if i%a.shard_count==a.shard_index]
    if a.dry_run:
        print(json.dumps({'historical_pairs':len(selected),'genetic_states':8*len(selected),
                          'poststress_cases':32*len(selected)}))
        return
    a.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(run_pair,d,source,g) for g in selected]
        for f in as_completed(futures): rows.extend(f.result())
    rows.sort(key=lambda x:(d['four_settings'].index(x['setting']),x['history'],
                            x['background'],x['I_donor'],x['A_donor']))
    if len(rows)!=8*len(selected) or sum(len(x['cases']) for x in rows)!=32*len(selected):
        raise RuntimeError('incomplete history-to-postshock grid')
    path=a.out/f"independent16_transplant_shard_{a.shard_index:02d}.json"
    raw=(json.dumps(rows,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    tmp=path.with_suffix('.tmp')
    tmp.write_bytes(raw);os.replace(tmp,path)
    print(json.dumps({'group_pairs':len(selected),'states':len(rows),'cases':32*len(selected),
                      'sha256':hashlib.sha256(raw).hexdigest()}))


if __name__=='__main__': main()
