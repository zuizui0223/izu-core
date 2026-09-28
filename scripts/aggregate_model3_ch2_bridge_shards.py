"""Aggregate all frozen bridge execution shards into the prospective Chapter 2 answer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest
from scripts.model3_island.summarize import decompose_crossed
from scripts.summarize_model3_ch2_bridge_production import _bootstrap_mean, _history_labels

INTERVENTIONS=("natural","richness_matched","visitor_pooled","large_plant_capacity")
MODES=("individual","density")


def _arr(x):
    return np.asarray(x,dtype=float)


def aggregate(parent, files):
    shards=[json.loads(Path(p).read_text()) for p in files]
    if not shards:
        raise ValueError("no shard extracts")
    expected_n={s["execution_shard"]["count"] for s in shards}
    if len(expected_n)!=1:
        raise ValueError("inconsistent shard counts")
    n=expected_n.pop()
    by_index={s["execution_shard"]["index"]:s for s in shards}
    if set(by_index)!=set(range(n)):
        raise ValueError(f"missing or duplicate shards: have {sorted(by_index)} expected 0..{n-1}")
    parent_hash=digest(parent)
    if any(s["parent_design_hash"]!=parent_hash for s in shards):
        raise ValueError("parent design hash mismatch")

    histories=list(parent["history_seeds"]); starts=list(parent["starts"]); demos=list(parent["demographic_seeds"])
    pos={h:i for i,h in enumerate(histories)}
    shape=(len(starts),len(histories),len(demos))
    tensors={(i,m):np.full(shape,np.nan) for i in INTERVENTIONS for m in MODES}
    near_occ={(i,m):np.full(shape,np.nan) for i in INTERVENTIONS for m in MODES}
    far_occ={(i,m):np.full(shape,np.nan) for i in INTERVENTIONS for m in MODES}
    visitor={arm:[None]*len(histories) for arm in parent["arms"]}
    seen=set(); cases=0; roots=[]

    for si in range(n):
        s=by_index[si]
        if s["status"]!="complete_bridge_shard_extract":
            raise ValueError(f"shard {si} incomplete")
        if s["starts"]!=starts or s["demographic_seeds"]!=demos:
            raise ValueError("factor support changed")
        hs=s["history_seeds"]
        for local,h in enumerate(hs):
            if h not in pos or h in seen:
                raise ValueError(f"history duplication/out of parent support: {h}")
            seen.add(h); global_i=pos[h]
            for intervention in INTERVENTIONS:
                for mode in MODES:
                    block=s["contrasts"][intervention][mode]
                    tensors[intervention,mode][:,global_i,:]=_arr(block["values"])[:,local,:]
                    near_occ[intervention,mode][:,global_i,:]=_arr(block["near_occupancy"])[:,local,:]
                    far_occ[intervention,mode][:,global_i,:]=_arr(block["far_occupancy"])[:,local,:]
            for arm in parent["arms"]:
                visitor[arm][global_i]=np.asarray(s["visitor_count"][arm][local],int)
        cases+=s["cases_verified"];roots.append({"index":si,"root":s["receipt_arrays_hash_root"],"shard_design_hash":s["shard_design_hash"]})

    if seen!=set(histories):
        raise ValueError("history union is incomplete")
    if cases!=parent["cases"]:
        raise ValueError(f"case union {cases} != parent {parent['cases']}")
    if any(v is None for xs in visitor.values() for v in xs):
        raise ValueError("visitor histories incomplete")

    # Annual response-blind richness-matching identity check.
    for h in range(len(histories)):
        if not np.array_equal(visitor["matched_near"][h],visitor["matched_far"][h]):
            raise ValueError(f"matched richness differs at history {histories[h]}")

    rng=np.random.default_rng(927032)
    resamples=rng.integers(0,len(histories),size=(1999,len(histories)))
    reports=[]
    for intervention in INTERVENTIONS:
        for mode in MODES:
            x=tensors[intervention,mode]
            reports.append({
                "intervention":intervention,
                "model":mode,
                "paired_far_minus_near":_bootstrap_mean(x,resamples),
                "mean_by_start":[None if not np.isfinite(x[k]).any() else float(np.nanmean(x[k])) for k in range(len(starts))],
                "finite_cells":int(np.isfinite(x).sum()),
                "total_cells":int(x.size),
                "classification":[_history_labels(x,e) for e in parent["thresholds"]],
                "decomposition":decompose_crossed(x,{
                    "S":(np.ones(len(starts))/len(starts)).tolist(),
                    "C":(np.ones(len(histories))/len(histories)).tolist(),
                }),
                "near_terminal_occupancy":float(np.nanmean(near_occ[intervention,mode])),
                "far_terminal_occupancy":float(np.nanmean(far_occ[intervention,mode])),
            })

    visitor_summary={}
    for arm,xs in visitor.items():
        cvs=[]
        for x in xs:
            mean=float(np.mean(x))
            cvs.append(np.nan if mean<=0 else float(np.std(x)/mean))
        visitor_summary[arm]={
            "mean_count":float(np.mean([np.mean(x) for x in xs])),
            "empty_year_fraction":float(np.mean([np.mean(x==0) for x in xs])),
            "mean_history_cv":None if not np.isfinite(cvs).any() else float(np.nanmean(cvs)),
        }

    def report(intervention,mode):
        return next(r for r in reports if r["intervention"]==intervention and r["model"]==mode)

    comparisons={}
    for mode in MODES:
        natural=report("natural",mode)
        comparisons[mode]={}
        for other in ("richness_matched","visitor_pooled","large_plant_capacity"):
            o=report(other,mode)
            comparisons[mode][f"natural_vs_{other}_mixed_fraction"]={
                str(e):[
                    natural["classification"][k]["mean8_mixed_fraction"],
                    o["classification"][k]["mean8_mixed_fraction"],
                ]
                for k,e in enumerate(parent["thresholds"])
            }

    # Predeclared question closure: factual status only, never pass/fail on direction.
    result={
        "schema_version":"1.0",
        "status":"complete_prospective_model3_ch2_bridge",
        "parent_design_hash":parent_hash,
        "cases_verified":cases,
        "execution_shards":roots,
        "endpoint":"paired far-minus-near terminal-minus-initial inherited investment change",
        "reports":reports,
        "comparisons":comparisons,
        "visitor_summary":visitor_summary,
        "question_status":{
            "dynamic_response_blind_realized_richness_matching":"evaluated",
            "finite_visitor_environment_vs_finite_plant_population":"evaluated",
            "density_vs_individual_under_each_intervention":"evaluated",
            "legacy_model2_controls_reproduced_in_model3":"results_must_be_interpreted_from_report_not_assumed",
        },
        "claim_boundaries":parent["claim_exclusions"]+[
            "annual richness matching changes identity persistence as well as count",
            "pooled visitor histories average composition and nonlinear reproductive environment; not island number or lifespan",
            "large plant capacity changes finite demographic realization only; not visitor-community sampling",
            "mixed fractions are descriptive independent-history labels, not natural prevalence or latent branch probabilities",
            "no result sign, mixed fraction, rank ordering, or Model 2 agreement was a success criterion",
        ],
    }
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--parent-design",required=True)
    p.add_argument("--input-dir",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    parent=json.loads(Path(a.parent_design).read_text())
    files=sorted(Path(a.input_dir).rglob("shard_summary.json"))
    result=aggregate(parent,files)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(canonical(result))
    compact={
        "status":result["status"],
        "cases_verified":result["cases_verified"],
        "reports":[{
            "intervention":r["intervention"],"model":r["model"],
            "mean":r["paired_far_minus_near"].get("mean"),
            "mixed":[q["mean8_counts"]["mixed"] for q in r["classification"]],
            "undefined":[q["mean8_counts"]["undefined"] for q in r["classification"]],
            "repeat_disagreement":[q["any_repeat_label_disagreements"] for q in r["classification"]],
        } for r in result["reports"]],
        "visitor_summary":result["visitor_summary"],
    }
    print(json.dumps(compact,indent=2))


if __name__=="__main__":
    main()
