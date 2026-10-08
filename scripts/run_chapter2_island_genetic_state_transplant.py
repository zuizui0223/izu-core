"""Declared 2026-10-08 2x2 allele-state transplant pilot (archived biology)."""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse, json, hashlib, os, time
import numpy as np
from scripts.run_chapter2_assurance_generality import config, founders, load_design
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.population import advance, subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'data/design/chapter2_island_genetic_state_transplant_pilot_20261008.json'


def load_pilot():
    d=json.loads(DESIGN.read_text(encoding='utf-8'))
    assert d['status']=='exploratory_allele_distribution_transplant_protocol_before_outcomes'
    assert len(d['history_seeds'])==4 and d['n_postshock_trajectories']==512
    source=load_design(ROOT/'data/design/chapter2_assurance_generality_20261006.json')
    return d,source


def history_state(d,source,setting,h,pre):
    c=config(source,setting,.01,'evolving')
    current=founders(source)
    seed=int(np.random.SeedSequence([h,d['nested_demographic_repeats'][0]]).generate_state(1)[0])
    rng={name:stream(seed,name,0) for name in STREAM_IDS}
    incoming=exposure(h,pre)
    for t in range(d['prehistory_updates']):
        ledger=reproduce(current,incoming.visitors[t],c)
        current,_=advance(current,ledger,incoming.seed_candidates[t],c,rng,
                          year=t,mutation_traits=(True,True,True))
    if len(current.ids)<d['shock_n']:
        raise ValueError('prehistory has fewer than eight plants')
    bottleneck_seed=int(np.random.SeedSequence([
        h,d['nested_demographic_repeats'][0],117
    ]).generate_state(1)[0])
    selection=np.random.default_rng(bottleneck_seed).choice(
        len(current.ids),size=d['shock_n'],replace=False
    )
    return subset(current,selection)


def rank_order(state,k):
    return np.argsort(state.alleles[:,k,:].mean(axis=1),kind='stable')


def crossed_state(recipient,investment_donor,assurance_donor):
    arrays={name:getattr(recipient,name).copy() for name in (
        'alleles','allele_origin','mutation_flags'
    )}
    for k,donor in ((1,investment_donor),(2,assurance_donor)):
        rec_order=rank_order(recipient,k)
        donor_order=rank_order(donor,k)
        for name in arrays:
            arrays[name][rec_order,k,:]=getattr(donor,name)[donor_order,k,:]
    return replace(recipient,**arrays)


def run_pair(d,source,job):
    setting,h=job
    ENV=('near','far')
    base={pre:history_state(d,source,setting,h,pre) for pre in ENV}
    c=config(source,setting,.01,'evolving')
    results=[]
    for background in ENV:
        recipient=base[background]
        for i_donor,a_donor in product(ENV,repeat=2):
            intervention=crossed_state(recipient,base[i_donor],base[a_donor])
            native=i_donor==background and a_donor==background
            if native:
                for name in ('alleles','allele_origin','mutation_flags','ids','birth_years'):
                    if not np.array_equal(getattr(intervention,name),getattr(recipient,name)):
                        raise AssertionError('Native alleles not exact')
            rows=[]
            for post,budget in product(d['post_visitor_arms'],d['ovule_budgets']):
                pconfig=replace(c,capacity=d['post_capacity'],ovule_budget=float(budget))
                future=exposure(h+d['post_visitor_seed_offset'],post)
                initial=reproduce(intervention,future.visitors[0],pconfig)
                n=d['shock_n']
                maternal=float(initial.maternal.sum()/n)
                female=float(initial.outcross.sum()/n)
                exported=float(initial.exported.sum()/n)
                master=int(np.random.SeedSequence([
                    h,d['nested_demographic_repeats'][0],
                    d['four_settings'].index(setting),
                    d['post_visitor_arms'].index(post),
                    d['ovule_budgets'].index(budget),713
                ]).generate_state(1)[0])
                rng={name:stream(master,name,0) for name in STREAM_IDS}
                current=intervention
                first_extinction=None
                for step in range(d['post_updates']):
                    ledger=reproduce(current,future.visitors[step],pconfig)
                    current,_=advance(current,ledger,future.seed_candidates[step],pconfig,rng,
                                      year=d['prehistory_updates']+step,
                                      mutation_traits=(True,True,True))
                    if len(current.ids)==0 and first_extinction is None:
                        first_extinction=step+1
                rows.append(dict(
                    post=post,budget=budget,viable_maternal=maternal,
                    female_outcross=female,pollen_export=exported,
                    occupied=int(bool(len(current.ids))),final_n=len(current.ids),
                    first_extinction=first_extinction
                ))
            results.append(dict(
                setting=setting,history=h,repeat=d['nested_demographic_repeats'][0],
                background=background,I_donor=i_donor,A_donor=a_donor,
                donor_genotype_sha256=hashlib.sha256(intervention.alleles.tobytes()).hexdigest(),
                starting_phenotype=intervention.alleles.mean(axis=(0,2)).tolist(),
                native=native,cases=rows
            ))
    return results


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--shard-index',type=int,default=0)
    p.add_argument('--shard-count',type=int,default=1)
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    d,source=load_pilot()
    jobs=list(product(d['four_settings'],d['history_seeds']))
    selected=[job for i,job in enumerate(jobs) if i%a.shard_count==a.shard_index]
    if a.dry_run:
        print(json.dumps({'historical_pairs':len(selected),'genetic_states':len(selected)*8,
                          'postshock_cases':len(selected)*32}))
        return
    a.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    allrows=[]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(run_pair,d,source,job) for job in selected]
        for f in as_completed(futures):
            allrows.extend(f.result())
    allrows.sort(key=lambda r:(
        d['four_settings'].index(r['setting']),r['history'],r['background'],r['I_donor'],r['A_donor']
    ))
    assert len(allrows)==8*len(selected) and sum(len(r['cases']) for r in allrows)==32*len(selected)
    path=a.out/f"transplant_shard_{a.shard_index:02d}.json"
    data=(json.dumps(allrows,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    tmp=path.with_suffix('.tmp')
    tmp.write_bytes(data)
    os.replace(tmp,path)
    print(json.dumps({'historical_pairs':len(selected),'genetic_states':len(allrows),
                      'postshock_cases':sum(len(r['cases']) for r in allrows),
                      'sha256':hashlib.sha256(data).hexdigest(),
                      'elapsed_s':round(time.monotonic()-start,2)}))


if __name__=='__main__':
    main()
