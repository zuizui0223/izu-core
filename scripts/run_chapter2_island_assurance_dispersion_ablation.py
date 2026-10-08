"""Exploratory A-locus dispersion ablation with EXACT posthistory assurance mean."""
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse,hashlib,json,os
import numpy as np
from scripts.run_chapter2_assurance_generality import config
from scripts.run_chapter2_island_genetic_state_transplant import history_state
from scripts.run_chapter2_island_genetic_state_transplant_independent16 import load_frozen
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream,STREAM_IDS

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_island_assurance_dispersion_ablation_20261008.json"

def load_protocol():
    d=json.loads(DESIGN.read_text(encoding="utf-8"))
    _,parent,source=load_frozen()
    if d["status"]!="post_outcome_allelic_dispersion_ablation_exploratory_before_execution":
        raise ValueError("unexpected experiment status")
    if d["historical_demographic_repeat"]!=parent["nested_demographic_repeats"][0]:
        raise AssertionError("historical repeat mismatch")
    if d["settings"]!=parent["four_settings"] or d["n_poststress_trajectories"]!=3072:
        raise AssertionError("unexpected source/design")
    return d,parent,source

def historical_groups(d):
    return list(product(d["settings"],d["history_seeds"]))

def simulate_group(group,d,parent,source):
    setting,h=group
    cfg=config(source,setting,.01,"evolving")
    bases={bg:history_state(parent,source,setting,h,bg) for bg in d["backgrounds"]}
    output=[]
    for bg in d["backgrounds"]:
        base=bases[bg]
        original=base.alleles[:,2,:]
        mean=float(original.mean());variance=float(original.var())
        for q in d["assurance_dispersion_scale"]:
            alleles=base.alleles.copy()
            alleles[:,2,:]=mean+q*(original-mean)
            assert abs(float(alleles[:,2,:].mean())-mean)<1e-12
            assert abs(float(alleles[:,2,:].var())-q*q*variance)<1e-12
            if q==1 and not np.array_equal(alleles,base.alleles):
                raise AssertionError("native control drift")
            state=replace(base,alleles=alleles)
            for mu,post,budget in product(
                d["post_mutation_rate"],d["post_visitor_environments"],d["post_ovule_budgets"]
            ):
                pcfg=replace(cfg,capacity=d["post_capacity"],
                             mutation_rate=mu,ovule_budget=budget)
                hist=exposure(h+d["post_visitor_seed_offset"],post)
                viable=float(reproduce(state,hist.visitors[0],pcfg).maternal.sum()/d["post_capacity"])
                for rep in d["post_rng_repeats"]:
                    master=int(np.random.SeedSequence([
                        h,d["historical_demographic_repeat"],d["settings"].index(setting),
                        d["post_visitor_environments"].index(post),
                        d["post_ovule_budgets"].index(budget),
                        713,rep,20261008,241
                    ]).generate_state(1)[0])
                    rng={name:stream(master,name,0) for name in STREAM_IDS}
                    cur=state;ext=None
                    for t in range(d["post_updates"]):
                        ledger=reproduce(cur,hist.visitors[t],pcfg)
                        cur,_=advance(cur,ledger,hist.seed_candidates[t],pcfg,rng,
                                      year=d["historical_updates"]+t,mutation_traits=(True,True,True))
                        if ext is None and len(cur.ids)==0: ext=t+1
                    output.append(dict(setting=setting,history=h,background=bg,q=q,mutation=mu,
                        post=post,budget=budget,repeat=rep,occupied=int(bool(len(cur.ids))),
                        end_n=len(cur.ids),first_extinction=ext,initial_viable=viable,a_mean=mean,
                        a_var_initial=q*q*variance,
                        a_var_end=float(cur.alleles[:,2,:].var()) if len(cur.ids) else None))
    expected=(len(d["backgrounds"])*len(d["assurance_dispersion_scale"])*
              len(d["post_mutation_rate"])*len(d["post_visitor_environments"])*
              len(d["post_ovule_budgets"])*len(d["post_rng_repeats"]))
    if len(output)!=expected: raise RuntimeError("missing group states")
    return output

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--shard-index",type=int,default=0)
    p.add_argument("--shard-count",type=int,default=4)
    p.add_argument("--workers",type=int,default=2)
    p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    d,parent,source=load_protocol()
    if not 0<=a.shard_index<a.shard_count: raise ValueError("invalid shard")
    groups=[g for i,g in enumerate(historical_groups(d)) if i%a.shard_count==a.shard_index]
    if a.dry_run:
        print(json.dumps({"groups":len(groups),"poststress":len(groups)*192}))
        return
    a.out.mkdir(parents=True,exist_ok=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(simulate_group,g,d,parent,source) for g in groups]
        rows=[row for future in as_completed(futures) for row in future.result()]
    rows.sort(key=lambda r:(d["settings"].index(r["setting"]),r["history"],
        r["background"],r["q"],r["mutation"],r["post"],r["budget"],r["repeat"]))
    if len(rows)!=len(groups)*192: raise RuntimeError("incomplete shard")
    raw=(json.dumps(rows,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    path=a.out/f"assurance_dispersion_shard_{a.shard_index:02d}.json"
    tmp=path.with_suffix(".tmp");tmp.write_bytes(raw);os.replace(tmp,path)
    print(json.dumps({"cases":len(rows),"sha256":hashlib.sha256(raw).hexdigest()}))

if __name__=="__main__":main()
