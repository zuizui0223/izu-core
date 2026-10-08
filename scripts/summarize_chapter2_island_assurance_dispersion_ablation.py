"""Read all declared A-dispersion ablation trajectories; no pseudo-replication."""
from __future__ import annotations
from itertools import product
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scripts.run_chapter2_island_assurance_dispersion_ablation import (
    load_protocol,historical_groups
)

def summarize(d,rows):
    by={}
    for r in rows:
        key=(r["setting"],r["history"],r["background"],
             r["q"],r["mutation"],r["post"],r["budget"],r["repeat"])
        if key in by or r["occupied"]!=int(r["end_n"]>0):
            raise AssertionError("duplicate or malformed poststress case")
        by[key]=r
    expected={
        (setting,h,bg,q,mu,post,budget,rep)
        for setting,h in historical_groups(d)
        for bg,q,mu,post,budget,rep in product(
            d["backgrounds"],d["assurance_dispersion_scale"],
            d["post_mutation_rate"],d["post_visitor_environments"],
            d["post_ovule_budgets"],d["post_rng_repeats"])
    }
    if set(by)!=expected or len(rows)!=d["n_poststress_trajectories"]:
        raise AssertionError("incomplete or extra ablation trajectories")
    out=[]
    for setting,bg,mu in product(
        d["settings"],d["backgrounds"],d["post_mutation_rate"]
    ):
        by_q={}
        histories=[]
        for h in d["history_seeds"]:
            hvals={}
            for q in d["assurance_dispersion_scale"]:
                r=[by[setting,h,bg,q,mu,post,b,rep]
                   for post,b,rep in product(
                    d["post_visitor_environments"],d["post_ovule_budgets"],
                    d["post_rng_repeats"])]
                # The source assay keeps exactly the same mean at all q.
                hvals[q]=r
            mean0=hvals[0.0][0]["a_mean"]
            if any(abs(hvals[q][0]["a_mean"]-mean0)>1e-12 for q in hvals):
                raise AssertionError("assurance mean changed across q")
            v1=hvals[1.0][0]["a_var_initial"]
            if abs(hvals[.5][0]["a_var_initial"]-v1/4)>1e-12:
                raise AssertionError("variance did not scale 1/4")
            if any(abs(x["a_var_initial"])>1e-12 for x in hvals[0.0]):
                raise AssertionError("q0 not genetically homogeneous in A")
            if mu==0 and any(x["a_var_end"] is not None and
                             abs(x["a_var_end"])>1e-12 for x in hvals[0.0]):
                raise AssertionError("no mutation q0 recreated A variation")
            histories.append({
                "history":h,
                "occupancy_by_q":{str(q):float(np.mean([
                    x["occupied"] for x in hvals[q]
                ])) for q in hvals},
            })
        treatments={}
        for q in d["assurance_dispersion_scale"]:
            sub=[by[setting,h,bg,q,mu,post,b,rep]
                 for h,post,b,rep in product(
                    d["history_seeds"],d["post_visitor_environments"],
                    d["post_ovule_budgets"],d["post_rng_repeats"])]
            treatments[str(q)]={
                "n_trajectories":len(sub),
                "terminal_occupancy":float(np.mean([x["occupied"] for x in sub])),
                "immediate_viable_maternal_per_plant":float(np.mean([
                    x["initial_viable"] for x in sub
                ])),
            }
        out.append({
            "setting":setting,"recipient_background":bg,
            "post_mutation_rate":mu,
            "treatments":treatments,
            "occupancy_delta_q0_minus_q1":treatments["0.0"]["terminal_occupancy"]-treatments["1.0"]["terminal_occupancy"],
            "occupancy_delta_q05_minus_q1":treatments["0.5"]["terminal_occupancy"]-treatments["1.0"]["terminal_occupancy"],
            "independent_histories":len(d["history_seeds"]),
            "history_occupancy":histories,
        })
    return {
        "status":"completed_post_outcome_dispersion_ablation_descriptive",
        "independent_visitor_histories":len(d["history_seeds"]),
        "n_postshock_trajectories":len(rows),
        "n_matched_condition_sets":len(rows)//3,
        "result":out,
        "boundaries":[
            "Variance q^2 and cross-trait genetic covariance q both change.",
            "Four previously exposed visitor histories, technical screen only.",
            "Postmutation0 removes mutation at all three traits, not just assurance.",
            "No preregistered hypothesis success rule and no natural island calibration.",
            "Earlier preregistered mutational priority, payoff and allele-swap failures remain failures."
        ],
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--shard-count",type=int,default=4)
    a=p.parse_args()
    d,_,_=load_protocol()
    rows=[];hashes={}
    for i in range(a.shard_count):
        path=a.input/f"assurance_dispersion_shard_{i:02d}.json"
        raw=path.read_bytes();hashes[path.name]=hashlib.sha256(raw).hexdigest()
        rows.extend(json.loads(raw))
    out=summarize(d,rows)
    out["shard_sha256"]=hashes
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":out["status"],"trajectories":out["n_postshock_trajectories"]}))

if __name__=="__main__":main()
