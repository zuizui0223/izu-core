"""Admit the full source-linked seed viability factorial before any history-level test."""
from __future__ import annotations
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.chapter2_postzygotic_factorial_common import (
    frozen,hashes,folder,verify_registry,old_state_and_future,sha,
)
from scripts.chapter2_order_prehistory_runner import case_key
from scripts.plan_chapter2_order_expression_identification import log_budget_weights
from scripts.chapter2_postzygotic_viability_gate import analyze_factorial_schedule_interactions

GATES=("baseline","attenuate_self","attenuate_outcross","attenuate_both")
METRICS=("occupied","selfed_recruits","outcross_recruits",
         "t0_maternal_viable","t0_selfed_viable","t0_female_outcross",
         "t0_expected_pollen_export")


def audit_all(pre_root:Path,post_root:Path,new_root:Path):
    d,tasks=frozen()
    shape=(64,4,2,2,2,7,2,2,4)
    grid={k:np.full(shape,np.nan) for k in METRICS}
    sources=0
    for shard in range(64):
        group=verify_registry(pre_root,post_root,shard,tasks,d)
        pre=folder(pre_root,"budget-window-pre-shard-",shard)
        post=folder(post_root,"budget-window-post-shard-",shard)
        root=folder(new_root,"factorial-shard-",shard)
        receipt=json.loads((root/f"factorial_shard_{shard:02}.json").read_text())
        if (receipt["status"]!="complete_raw_32_source_2688_futures"
            or receipt["shard"]!=shard or receipt["visitor_history"]!=38110901+shard
            or receipt["keys"]!=sorted(case_key(t) for t in group)
            or receipt["count"]!=2688 or receipt["hashes"]!=hashes()):
            raise AssertionError("Incomplete or altered new shard registry")
        for t in group:
            name=case_key(t)
            # Full ancestral genetic lineage and the original future are
            # reauthenticated; source extinction is not discarded.
            _,state_sha,baseline=old_state_and_future(pre,post,t,d)
            path=root/f"viability_{name}.json"
            if sha(path)!=(root/f"viability_{name}.sha256").read_text().strip():
                raise AssertionError("Corrupt intervention archive")
            v=json.loads(path.read_text())
            if (v["status"]!="raw_futures_no_adjudication"
                or v["hashes"]!=hashes() or v["state_sha256"]!=state_sha
                or v["old_future_sha256"]!=sha(post/f"{name}.json")
                or v["task"]!={f:k for f,k in vars(t).items()}
                or len(v["futures"])!=84):
                raise AssertionError("New source / old source provenance mismatch")
            old={(x["regime"],float(x["budget"]),x["future_visitor"]):x
                 for x in baseline["postshock"]}
            found=set()
            for arm,rows in [("baseline",baseline["postshock"]),
                             ("perturbed",v["futures"])]:
                for x in rows:
                    gate=arm if arm=="baseline" else x["gate"]
                    key=(gate,x["regime"],float(x["budget"]),x["future_visitor"])
                    if gate not in GATES or key in found:
                        raise AssertionError("Unknown or duplicate intervention")
                    found.add(key)
                    ref=old[(x["regime"],float(x["budget"]),x["future_visitor"])]
                    if (x["t0_population"]!=ref["t0_population"]
                        or x["future_expression_offsets"]!=[0,0]
                        or x["future_assurance_mode"]!="evolving"):
                        raise AssertionError("Intervention has mutated source/future baseline")
                    n=x["t0_population"]
                    immediate=x["immediate_reproductive_payoff"]
                    if not isinstance(n,int) or (n==0)!=(immediate is None):
                        raise AssertionError("Invalid/pre-extinct source accounting")
                    idx=(t.visitor_history-38110901,
                         d["reproductive_settings"].index(t.setting),
                         d["environmental_settings"].index(t.environment),
                         ["assurance_first","investment_first"].index(t.expression_order),
                         d["nested_demographic_repeats"].index(t.demographic_repeat),
                         d["postshock"]["budgets"].index(float(x["budget"])),
                         d["postshock"]["future_environments"].index(x["future_visitor"]),
                         d["postshock"]["arms"].index(x["regime"]),GATES.index(gate))
                    z={
                        "occupied":x["occupied"],
                        "selfed_recruits":x["selfed_recruits"],
                        "outcross_recruits":x["outcross_recruits"],
                        "t0_maternal_viable":n*immediate["maternal_viable_per_plant"] if n else 0,
                        "t0_selfed_viable":n*immediate["viable_selfed_per_plant"] if n else 0,
                        "t0_female_outcross":n*immediate["female_outcross_per_plant"] if n else 0,
                        "t0_expected_pollen_export":n*immediate["paternal_export_per_plant"] if n else 0,
                    }
                    for metric,value in z.items():
                        if (not np.isfinite(value) or value<0 or
                            (metric=="occupied" and value not in (0,1))):
                            raise AssertionError("Invalid future scientific outcome")
                        grid[metric][idx]=value
                    if gate!="baseline":
                        ref_export=(n*ref["immediate_reproductive_payoff"]["paternal_export_per_plant"]
                                    if n else 0)
                        if not np.isclose(z["t0_expected_pollen_export"],ref_export,
                                          rtol=0,atol=1e-9):
                            raise AssertionError("Forbidden pollen-export intervention")
            if len(found)!=112:
                raise AssertionError("Missing full 28-baseline + 84-factorial grid")
            sources+=1
        if len(list(root.glob("viability_*.json")))!=32 or len(list(
                root.glob("viability_*.sha256")))!=32:
            raise AssertionError("Incorrect number of complete future cases")
    if sources!=2048 or any(not np.isfinite(z).all() for z in grid.values()):
        raise AssertionError("Incomplete 229376-future full cohort")
    return d,grid


def paired(value:np.ndarray,indices:np.ndarray):
    if value.shape!=(64,) or not np.isfinite(value).all():
        raise ValueError("Not 64 independent visitor-history pairs")
    lo,hi=np.percentile(value[indices].mean(axis=1),[2.5,97.5])
    return {"mean":float(value.mean()),"bootstrap95":[float(lo),float(hi)]}


def adjudicate(d,grid):
    w=log_budget_weights(d)
    weights=np.array([w[float(b)] for b in d["postshock"]["budgets"]])
    draws=np.random.default_rng(2026100927).integers(0,64,size=(9999,64))
    outcomes={}
    for regime_index,regime in enumerate(d["postshock"]["arms"]):
        channels={}
        for metric,a in grid.items():
            # First pool nested demographic repeats and paired future visitors.
            groups=a[:,:,:,:,:,:,:,regime_index,:].mean(axis=(4,6))
            if groups.shape!=(64,4,2,2,7,4):
                raise AssertionError("Unexpected averaging dimensions")
            weighted=np.tensordot(groups,weights,axes=([4],[0]))
            effect=weighted[:,:,:,0,:]-weighted[:,:,:,1,:]
            both=effect.mean(axis=(1,2))
            terms=analyze_factorial_schedule_interactions(both)
            channels[metric]={
                "schedule_by_gate":{g:paired(both[:,i],draws)
                                     for i,g in enumerate(GATES)},
                "factorial":{term:paired(v,draws) for term,v in terms.items()},
                "near_by_gate":{g:paired(effect[:,:,0,i].mean(axis=1),draws)
                                for i,g in enumerate(GATES)},
                "far_by_gate":{g:paired(effect[:,:,1,i].mean(axis=1),draws)
                               for i,g in enumerate(GATES)},
            }
        outcomes[regime]=channels
    primary=outcomes["eight_founders_capacity8"]["occupied"]["factorial"][
        "primary_selfed_viability_sensitivity"]
    mean=primary["mean"]
    low,high=primary["bootstrap95"]
    if abs(mean)>=0.005 and (low>0 or high<0):
        decision="nonzero_controlled_self_viability_sensitivity"
    elif low>-0.005 and high<0.005:
        decision="controlled_self_viability_sensitivity_practically_equivalent"
    else:
        decision="inconclusive"
    return {
        "status":"all_2048_diploid_sources_229376_future_cells_admitted",
        "n_independent_visitor_histories":64,
        "n_archived_baseline_futures":57344,
        "n_new_perturbed_futures":172032,
        "n_all_future_cells":229376,
        "experiment_hashes":hashes(),
        "primary":{**primary,"decision":decision,
                    "predeclared_min_abs":0.005},
        "bootstrap":{"draws":9999,"unit":"visitor_history","seed":2026100927},
        "by_regime":outcomes,
        "cautions":[
            "Old, already outcome-exposed historical states were reused under a prospectively declared NEW viability intervention.",
            "Conditional sensitivity to seed viability is not natural genetic-order mediation.",
            "Source-genotype history and genome-wide parental covariance not manipulated.",
            "Original pooled interaction was practically equivalent; fixed resource-window follow-up failed confirmation.",
            "Synthetic stress is not calibrated for natural Izu population persistence.",
            "The 229376 future trajectories are correlated branches, never 229376 independent ecological replicates."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory",type=Path,required=True)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--perturbed",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--execute-frozen-cohort",action="store_true")
    args=p.parse_args()
    if not args.execute_frozen_cohort:
        raise PermissionError("Prospective factorial adjudication requires explicit authorization")
    d,m=audit_all(args.prehistory,args.baseline,args.perturbed)
    result=adjudicate(d,m)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":result["status"],"primary":result["primary"]}))


if __name__=="__main__":
    main()
