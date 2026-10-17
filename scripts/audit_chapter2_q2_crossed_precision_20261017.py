"""Retrospective two-axis precision diagnostic from the 384 original Q2 archives.

Read-only source receipts; no Model 3 reproduction, seed additions or p-value tuning.
Original bootstrap and frozen co-primary decision must match signed readout.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
from statistics import NormalDist
import argparse
import hashlib
import io
import json
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OFFICIAL=ROOT/"docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json"
LABELS=("assurance_first","investment_first","near_simultaneous",
        "assurance_only","investment_only","neither")
POLICIES=("dense_reachable","sparse_reachable","dense_unreachable")


def original_cases(archives:Path)->dict:
    cases={}
    for i in range(32):
        with zipfile.ZipFile(Path(archives)/f"q2_original_shard_{i}_actions.zip") as wrapper:
            if wrapper.namelist()!=[f"original-shard-{i}.zip"]:
                raise ValueError("Unexpected outer source-shard inventory")
            inner=wrapper.read(f"original-shard-{i}.zip")
        with zipfile.ZipFile(io.BytesIO(inner)) as z:
            receipts=sorted(x for x in z.namelist() if x.endswith(".json") and "/f860" in x)
            if len(receipts)!=12:
                raise ValueError("Original 12-case shard missing/duplicated")
            for member in receipts:
                r=json.loads(z.read(member))
                task=tuple(r["task"])
                key=f"f{task[0]}_v{task[1]}_{task[2]}_{task[3]}"
                if (task in cases or r["case"]!=key or r["censuses"]!=201
                    or r["status"]!="full_source_case_not_independently_read_back"):
                    raise ValueError("Foreign/duplicate historical case")
                if hashlib.sha256(z.read(member[:-5]+".npz")).hexdigest()!=r["sha256"]:
                    raise ValueError("Original source NPZ SHA256 mismatch")
                cases[task]=r["events"]
    f=sorted({x[0] for x in cases})
    v=sorted({x[1] for x in cases})
    if len(cases)!=384 or f!=list(range(860101,860109)) or v!=list(range(860201,860209)):
        raise ValueError("Not 384 exact 8x8x2x3 original study")
    return cases


def far_grid(cases:dict)->np.ndarray:
    grid=np.empty((8,8,2))
    rank=lambda e: int(e["label"]=="assurance_first")-int(e["label"]=="investment_first")
    for i,f in enumerate(range(860101,860109)):
        for j,v in enumerate(range(860201,860209)):
            d=cases[f,v,"far","dense_reachable"]
            s=cases[f,v,"far","sparse_reachable"]
            grid[i,j]=[rank(d)-rank(s),int(d["I_event"])-int(s["I_event"])]
    return grid


def variance_proxy(x:np.ndarray)->dict:
    """Interaction vs finite-history noise UNIDENTIFIED with one path per cell."""
    x=np.asarray(x,dtype=float)
    if x.ndim!=2 or min(x.shape)<3 or not np.isfinite(x).all():
        raise ValueError("Need two complete independent axes")
    f,v=x.shape
    rf=x.mean(axis=1)
    cv=x.mean(axis=0)
    global_mean=float(x.mean())
    residual=x-rf[:,None]-cv[None,:]+global_mean
    vf=float(rf.var(ddof=1))
    vv=float(cv.var(ddof=1))
    mr=float((residual**2).sum()/((f-1)*(v-1)))
    return {
        "mean":global_mean,
        "founder_mean_range":[float(rf.min()),float(rf.max())],
        "visitor_mean_range":[float(cv.min()),float(cv.max())],
        "raw_founder_mean_variance":vf,"raw_visitor_mean_variance":vv,
        "interaction_plus_path_noise_MS":mr,
        "nonnegative_ANOVA_moment_components":{
            "founder":max(0,vf-mr/v),
            "visitor":max(0,vv-mr/f),
            "interaction_plus_path_noise":mr},
        "ANOVA_moment_negative_clipped_to_zero":{"founder":vf<mr/v,"visitor":vv<mr/f},
        "double_counting_adverse_proxy":{"founder":vf,"visitor":vv,"interaction":mr},
        "not_identified":"One stochastic path per founder×visitor cell: interaction and within-cell RNG noise are inseparable; founder variance dominance not proven."
    }


def assumption_mde(proxy:dict,nf:int,nv:int)->float:
    if nf<3 or nv<3 or any(not np.isfinite(x) or x<0 for x in proxy.values()):
        raise ValueError("Invalid assumption-only sample/variance")
    var=proxy["founder"]/nf+proxy["visitor"]/nv+proxy["interaction"]/(nf*nv)
    # 2-sided Bonferroni 97.5% intervals, 2 co-primaries; >=0.9 success
    # on each endpoint conservatively implies >=0.8 joint (union bound).
    multiplier=NormalDist().inv_cdf(.9875)+NormalDist().inv_cdf(.90)
    return float(multiplier*np.sqrt(var))


def audit(archives:Path,official:Path=OFFICIAL)->dict:
    q=json.loads(Path(official).read_text(encoding="utf-8"))
    cases=original_cases(archives)
    x=far_grid(cases)
    names=("carrier_order_score_delta","carrier_I_event_delta")
    for k,name in enumerate(names):
        if float(x[:,:,k].mean())!=q["coprimary"][name]["estimate"]:
            raise ValueError("Original registered effect differs")
    for arm in ("far","near"):
        for policy in POLICIES:
            c=Counter(cases[f,v,arm,policy]["label"]
                      for f in range(860101,860109) for v in range(860201,860209))
            if [c[label] for label in LABELS]!=q["original_six_class_cells"][arm][policy]["counts"]:
                raise ValueError("Original six-class cell differs")
    rng=np.random.default_rng(910763)
    b=np.empty((9999,2))
    for k in range(len(b)):
        fi=rng.integers(0,8,8)
        vi=rng.integers(0,8,8)
        b[k]=x[np.ix_(fi,vi)].mean((0,1))
    lohi=np.quantile(b,[.0125,.9875],axis=0)
    for k,name in enumerate(names):
        if not np.allclose(lohi[:,k],q["coprimary"][name]["simultaneous_familywise_CI"],rtol=0,atol=1e-15):
            raise ValueError("Preregistered two-way bootstrap differs")
    diagnostics={name:variance_proxy(x[:,:,k]) for k,name in enumerate(names)}
    scenarios={str(n):{name:assumption_mde(diagnostics[name]["double_counting_adverse_proxy"],n,n)
                       for name in names} for n in (8,12,16,24,32,48,64)}
    return {
        "schema":"chapter2_q2_384_retrospective_crossed_precision_v1",
        "status":"RETROSPECTIVE_NOT_PROSPECTIVE_POWER",
        "original_actions_run":38918737325,
        "source_case_sha_verified":384,
        "original_9999_bootstrap_exact":True,
        "original_both_primary_inconclusive":True,
        "observed":dict(zip(names,x.mean((0,1)).tolist())),
        "intervals":dict(zip(names,lohi.T.tolist())),
        "founder_conditional_means":{name:x[:,:,k].mean(1).tolist() for k,name in enumerate(names)},
        "visitor_conditional_means":{name:x[:,:,k].mean(0).tolist() for k,name in enumerate(names)},
        "variance_diagnostics":diagnostics,
        "future_n_by_n_assumption_only_mde":scenarios,
        "exclusions":"No biological new runs or changed readouts, no estimate of actual post hoc power, no identified founder variance dominance or finite-drift causal contribution.",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archives",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--official",type=Path,default=OFFICIAL)
    args=p.parse_args()
    if args.out.exists():p.error("Refuse overwrite")
    report=audit(args.archives,args.official)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"source_cases":384}))
if __name__=="__main__":
    main()
