"""Post-outcome deterministic pollen-return assay on old 8 artificial histories.

NO new biological cases, descendant continuations, seeds, or t-star claims.
Full genetic return includes maternal + paternal source ledger contributions.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.explore_chapter2_pollinator_recovery_20261018 import (
    FOUNDER_IDS, VISITOR_IDS, POLICIES, EXTIRPATION, HISTORICAL_HORIZON,
    seeded, streams, make_founders, make_visitors, configuration,
    historical_snapshots, investment_mean, support_bound,
    empty_visitors, step, source_identity,
)
from scripts.model3_island.reproduction import reproduce

TEST_TIMES = (30,35,38,39,45)


def focal_gradient(state,visitors,cfg,trait,h):
    """One source-native focal (not rare-mutant) log relative-fitness slope."""
    if len(state.ids)<2 or (trait==2 and cfg.assurance_mode=="fixed"):
        return None
    allowed=np.flatnonzero(np.all(
        (state.alleles[:,trait,:]>=h)&(state.alleles[:,trait,:]<=1-h),
        axis=1))
    if not len(allowed):
        return None
    k=int(allowed[len(allowed)//2])
    logs=[]
    for direction in (-1,1):
        a=state.alleles.copy()
        a[k,trait,:]+=direction*h
        ledger=reproduce(replace(state,alleles=a),visitors,cfg)
        w=(ledger.maternal+ledger.paternal)/2
        if not (w[k]>0 and w.mean()>0):
            return None
        logs.append(float(np.log(w[k]/w.mean())))
    return (logs[1]-logs[0])/(2*h)


def assayed_source():
    rows=[]
    for fi,fseed in enumerate(FOUNDER_IDS):
        founder=make_founders(fseed)
        target=investment_mean(founder)
        founder_A_target=float(founder.alleles[:,2,:].mean())
        for vi,vseed in enumerate(VISITOR_IDS):
            full,sparse=make_visitors(vseed)
            master=seeded(1,fi,vi)
            for policy in POLICIES:
                cfg=configuration(policy)
                expected=historical_snapshots(founder,full,sparse,policy,master)
                state=founder
                rng=streams(master)
                for t in range(HISTORICAL_HORIZON+1):
                    if t in (10,30,45):
                        source=expected[t]
                        for name in ("ids","alleles","allele_origin",
                                     "mutation_flags","birth_years"):
                            np.testing.assert_array_equal(
                                getattr(state,name),getattr(source,name))
                    if t in TEST_TIMES:
                        n=len(state.ids)
                        if n:
                            r=reproduce(state,full,cfg)
                            absent=reproduce(state,empty_visitors(),cfg)
                            a=(state.alleles[:,2,:].mean(axis=1)
                               if policy=="evolving"
                               else np.full(n,cfg.fixed_assurance))
                            fault_floor=float((1-cfg.depression)*
                                np.sum(r.ovules*a)/np.sum(r.ovules))
                            grad={}
                            for name,idx in (("I",1),("A",2)):
                                slopes=[focal_gradient(state,full,cfg,idx,h)
                                        for h in (.005,.0025)]
                                grad[name]=dict(
                                    slopes=slopes,
                                    sign=("undefined" if None in slopes
                                        else "positive" if min(slopes)>1e-6
                                        else "negative" if max(slopes)<-1e-6
                                        else "mixed_or_near_zero"))
                            rows.append(dict(
                                founder=fi,visitor=vi,policy=policy,t=t,
                                census=n,founder_I_target=target,
                                high_I_support_closed=support_bound(state,target),
                                max_retained_I=float(state.alleles[:,1,:].max()),
                                ancestral_founder_A_mean=founder_A_target,
                                min_retained_A_allele=float(state.alleles[:,2,:].min()),
                                max_retained_A_allele=float(state.alleles[:,2,:].max()),
                                ancestral_low_A_target_structurally_closed=(
                                    bool(state.alleles[:,2,:].min()>founder_A_target+1e-12)
                                    if policy=="evolving" else None),
                                expected_outcross_return_gain=float(
                                    r.outcross.sum()-absent.outcross.sum()),
                                maternal_no_service_fraction=fault_floor,
                                full_genetic_focal_gradients=grad,
                            ))
                        else:
                            rows.append(dict(founder=fi,visitor=vi,policy=policy,
                                             t=t,census=0,high_I_support_closed=None))
                    if t==HISTORICAL_HORIZON:break
                    visitors=(full if t<5 else sparse if t<EXTIRPATION
                              else empty_visitors())
                    state=step(state,visitors,cfg,rng,year=t)
    if len(rows)!=len(FOUNDER_IDS)*len(VISITOR_IDS)*len(POLICIES)*len(TEST_TIMES):
        raise AssertionError("source readout coverage")
    one={r["t"]:r for r in rows if
         (r["founder"],r["visitor"],r["policy"])==(0,0,"evolving")}
    if one[38]["high_I_support_closed"] is not False:
        raise AssertionError("source should retain access at 38")
    if one[39]["high_I_support_closed"] is not True:
        raise AssertionError("source should lose high-I support at 39")
    return dict(
        status="EXPLORATORY_SOURCE_ONLY_GENOTYPE_POLLEN_ASSAY_NOT_RESTORATION",
        new_biological_histories=0,new_random_future_paths=0,
        existing_historical_paths=8,
        original_source_sha256=source_identity(),
        auditor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        focal_assay_scope="one finite adult, two central-difference widths, not rare-mutant invasion",
        return_pollen_assay_scope="same saved plant genotypes, functional visitors full versus absent",
        t39_source_example=one[39],path_rows=rows,
        A_support_assay_scope=(
            "Ancestral founder-A-mean reachability only in the evolving-A history: "
            "min surviving A allele exceeding founder mean A under no A mutation or seed immigration. "
            "This is a target-specific sufficient bound, not realized selection response."),
    )


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    x=p.parse_args()
    if x.out.exists():p.error("no overwrite")
    z=assayed_source()
    x.out.parent.mkdir(parents=True,exist_ok=True)
    with x.out.open("x",encoding="utf-8") as f:
        json.dump(z,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")
    print(json.dumps({"status":z["status"],
                      "t39_source_example":z["t39_source_example"]},
                     sort_keys=True,allow_nan=False))


if __name__=="__main__":main()
