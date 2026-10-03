"""Summarize prospectively frozen transfer to new synthetic visitor histories."""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np


PAIRS={
    "natural":("near","far"),
    "visitor_pooled":("pool_near","pool_far"),
    "large_plant_capacity":("large_near","large_far"),
}


def _varcomp(x):
    x=np.asarray(x,float); a,b,n=x.shape
    gm=x.mean(); ms=x.mean(axis=(1,2)); mh=x.mean(axis=(0,2)); cell=x.mean(axis=2)
    ss_h=a*n*np.sum((mh-gm)**2)
    ss_sh=n*np.sum((cell-ms[:,None]-mh[None,:]+gm)**2)
    ss_e=np.sum((x-cell[:,:,None])**2)
    ms_h=ss_h/(b-1); ms_sh=ss_sh/((a-1)*(b-1)); ms_e=ss_e/(a*b*(n-1))
    raw_h=(ms_h-ms_sh)/(a*n)
    raw_sh=(ms_sh-ms_e)/n
    h=max(0.0,float(raw_h)); sh=max(0.0,float(raw_sh))
    structured=h+sh
    reliability=structured/(structured+float(ms_e)/n) if structured>0 else 0.0
    return {
        "sigma_history_raw":float(raw_h),
        "sigma_start_by_history_raw":float(raw_sh),
        "sigma_history":h,
        "sigma_start_by_history":sh,
        "history_structured_variance":structured,
        "sigma_demographic_residual":float(ms_e),
        "four_repeat_mean_reliability":float(reliability),
    }


def _label(v,eps):
    v=np.asarray(v,float)
    pos=bool(np.any(v>eps)); neg=bool(np.any(v<-eps))
    return "mixed" if pos and neg else "positive" if pos else "negative" if neg else "neutral"


def _labels(x,eps):
    m=x.mean(axis=2)
    labs=[_label(m[:,h],eps) for h in range(m.shape[1])]
    return {k:labs.count(k) for k in ("negative","mixed","positive","neutral")}


def _split_corrs(x):
    idx=range(x.shape[2]); vals=[]
    for comb in combinations(idx,x.shape[2]//2):
        if 0 not in comb:
            continue
        a=np.asarray(comb,int)
        b=np.asarray([i for i in idx if i not in comb],int)
        va=x[:,:,a].mean(axis=(0,2))
        vb=x[:,:,b].mean(axis=(0,2))
        vals.append(float(np.corrcoef(va,vb)[0,1]))
    if len(vals)!=3:
        raise ValueError(f"expected 3 unique 2-versus-2 splits, got {len(vals)}")
    return vals


def _load(folder,design):
    histories=[int(x) for x in design["execution"]["visitor_history_seeds"]]
    starts=[float(x) for x in design["execution"]["starts"]]
    demos=[int(x) for x in design["execution"]["demographic_seeds"]]
    hi={h:i for i,h in enumerate(histories)}
    si={s:i for i,s in enumerate(starts)}
    di={d:i for i,d in enumerate(demos)}
    arms=set(design["execution"]["arms"])
    values={arm:np.full((len(starts),len(histories),len(demos)),np.nan) for arm in arms}
    pops={arm:np.full((len(starts),len(histories),len(demos)),np.nan) for arm in arms}
    docs=[json.loads(p.read_text()) for p in sorted(Path(folder).glob("*.json"))]
    docs=[d for d in docs if d.get("status")=="complete_new_visitor_history_validation_shard"]
    if len(docs)!=16:
        raise ValueError(f"expected 16 validation shards, got {len(docs)}")
    seen=set()
    for d in docs:
        for row in d["rows"]:
            key=(int(row["history_seed"]),float(row["start"]),row["arm"],int(row["demographic_seed"]))
            if key in seen:
                raise ValueError(f"duplicate {key}")
            seen.add(key)
            arm=row["arm"]
            idx=(si[float(row["start"])],hi[int(row["history_seed"])],di[int(row["demographic_seed"])])
            values[arm][idx]=np.nan if row["investment_change"] is None else float(row["investment_change"])
            pops[arm][idx]=int(row["terminal_population"])
    if not all(np.isfinite(v).all() for v in values.values()):
        raise ValueError("incomplete validation tensor")
    effects={name:values[far]-values[near] for name,(near,far) in PAIRS.items()}
    return histories,effects,pops


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--design",type=Path,required=True)
    p.add_argument("--input-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    design=json.loads(a.design.read_text(encoding="utf-8"))
    if design["status"]!="prospective_frozen_before_new_visitor_history_execution":
        raise ValueError("frozen environmental validation design required")
    histories,effects,pops=_load(a.input_dir,design)

    reports={}
    for name,x in effects.items():
        vc=_varcomp(x)
        reports[name]={
            "mean_effect":float(x.mean()),
            "variance_components":vc,
            "labels_eps0":_labels(x,0.0),
            "labels_eps0_01":_labels(x,0.01),
            "balanced_2v2_split_history_correlations":_split_corrs(x),
        }

    seed=int(design["primary_validation"]["inference"].split()[-1])
    rng=np.random.default_rng(seed)
    boots={name:[] for name in PAIRS}
    diffs={"large_minus_natural":[],"pooled_minus_natural":[]}
    for _ in range(1999):
        ix=rng.integers(0,len(histories),len(histories))
        rel={}
        for name,x in effects.items():
            rel[name]=_varcomp(x[:,ix,:])["four_repeat_mean_reliability"]
            boots[name].append(rel[name])
        diffs["large_minus_natural"].append(rel["large_plant_capacity"]-rel["natural"])
        diffs["pooled_minus_natural"].append(rel["visitor_pooled"]-rel["natural"])

    for name in PAIRS:
        reports[name]["variance_components"]["four_repeat_mean_reliability_bootstrap95"]=np.quantile(
            boots[name],[.025,.975]
        ).tolist()

    paired={
        "large_capacity_minus_natural_reliability":{
            "estimate":reports["large_plant_capacity"]["variance_components"]["four_repeat_mean_reliability"]-reports["natural"]["variance_components"]["four_repeat_mean_reliability"],
            "bootstrap95":np.quantile(diffs["large_minus_natural"],[.025,.975]).tolist(),
        },
        "visitor_pooled_minus_natural_reliability":{
            "estimate":reports["visitor_pooled"]["variance_components"]["four_repeat_mean_reliability"]-reports["natural"]["variance_components"]["four_repeat_mean_reliability"],
            "bootstrap95":np.quantile(diffs["pooled_minus_natural"],[.025,.975]).tolist(),
        },
    }
    occupancy={
        arm:{
            "occupied_fraction":float(np.mean(v>0)),
            "min_terminal_population":int(np.min(v)),
            "mean_terminal_population":float(np.mean(v)),
        } for arm,v in pops.items()
    }
    reliabilities={name:reports[name]["variance_components"]["four_repeat_mean_reliability"] for name in PAIRS}
    ordering=bool(reliabilities["large_plant_capacity"]>reliabilities["natural"]>reliabilities["visitor_pooled"])
    occupancy_ok=all(v["occupied_fraction"]>=.95 for v in occupancy.values())
    strong=bool(
        ordering and occupancy_ok
        and paired["large_capacity_minus_natural_reliability"]["bootstrap95"][0]>0
        and paired["visitor_pooled_minus_natural_reliability"]["bootstrap95"][1]<0
    )
    out={
        "schema_version":"1.0",
        "date":design["date"],
        "status":"complete_prospectively_frozen_new_visitor_history_validation",
        "design":str(a.design),
        "provenance":{
            "visitor_history_seeds":[histories[0],histories[-1]],
            "n_visitor_histories":len(histories),
            "demographic_seeds":design["execution"]["demographic_seeds"],
            "starts":design["execution"]["starts"],
            "finite_arm_trajectories":sum(v.size for v in pops.values()),
            "paired_effect_cells_per_intervention":effects["natural"].size,
        },
        "reports":reports,
        "paired_bootstrap_differences":paired,
        "terminal_occupancy":occupancy,
        "primary_decision":{
            "observed_ordering":"large_plant_capacity > natural > visitor_pooled",
            "observed_reliability":reliabilities,
            "observed_ordering_holds":ordering,
            "occupancy_rule_holds":occupancy_ok,
            "strong_success":strong,
            "weak_success":bool(ordering and occupancy_ok and not strong),
            "failure":bool(not ordering),
        },
        "claim_boundary":design["claim_boundary"],
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"primary_decision":out["primary_decision"],"paired":paired},indent=2))


if __name__=="__main__":
    main()
