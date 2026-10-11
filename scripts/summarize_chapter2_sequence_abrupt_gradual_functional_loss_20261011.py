"""Fail-closed, history-clustered source readout of complete timing cohort.

No analysis from smoke/partial samples. Verify all 1,024 SHA receipts and
16 completed shard manifests. Independently check every matched abrupt/
gradual case pair and cluster over the 16 independent artificial visitor
functional profiles, treating the four demographic repeats as nested.
"""
from __future__ import annotations
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.run_chapter2_sequence_abrupt_gradual_batch_20261011 import tasks,key,source_identity
from scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import contract

SCHEDULES=("abrupt","gradual")
METRICS=("A_crossed_by100","I_crossed_by100","A_first",
         "I_first","near_simultaneous","A_only","I_only","neither",
         "persistence100","persistence400")
STATUS="COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY"


def read_all(folder):
    root=Path(folder)
    d,digest=contract()
    source_digest=source_identity()["digest"]
    for index in range(16):
        path=root/f"shard_{index:02d}_complete.json"
        if not path.is_file():raise FileNotFoundError(f"missing completed shard: {path}")
        s=json.loads(path.read_text())
        exact_keys=[key(c) for j,c in enumerate(tasks()) if j%16==index]
        if (s["status"]!="COMPLETE_FROZEN_SHARD" or
            s["shard_index"]!=index or s["shard_count"]!=16 or
            s["case_count"]!=64 or s["design_sha256"]!=digest or
            s.get("source_identity_sha256")!=source_digest or
            s.get("case_keys")!=exact_keys):
            raise ValueError("incomplete or mismatched execution provenance")
    records={}
    for case in tasks():
        k=key(case)
        data=root/(k+".json")
        receipt=root/(k+".receipt.json")
        if not data.is_file() or not receipt.is_file():
            raise FileNotFoundError(f"undeclared/missing full source case {k}")
        r=json.loads(receipt.read_text())
        if r.get("sha256")!=sha256(data.read_bytes()).hexdigest():
            raise ArithmeticError("full source case SHA256 mismatch: "+k)
        if (r.get("case")!=list(case) or r.get("design_sha256")!=digest or
            r.get("source_identity_sha256")!=source_digest or
            r.get("full_declared_case") is not True):
            raise ValueError("partial/altered biological source cell: "+k)
        x=json.loads(data.read_text())
        if (x["case_key"]!=k or x["years"]!=400 or
            x["full_declared_case"] is not True or
            x["frozen_design_sha256"]!=digest or
            x["history_profile_seed"]!=case[0] or
            x["nested_demography_seed"]!=case[1] or
            x["mating_timing"]!=case[2] or
            x["direct_assurance_cost"]!=case[3] or
            x["mutation_rate"]!=case[4] or
            x["schedule"]!=case[5]):
            raise ValueError("full source setting or source hash differs")
        if len(x["trace"])!=401 or len(x["pollen_and_price_series"])!=400:
            raise ValueError("full 400-year genetic history incomplete")
        records[case]=x
    if len(records)!=1024:
        raise ValueError("full cohort is not complete")
    return records


def metrics_for_record(x):
    order=x["order"]
    trace=np.asarray(x["trace"],dtype=float)
    values={
        "A_crossed_by100":float(order["A_crossed_by100"]),
        "I_crossed_by100":float(order["I_crossed_by100"]),
        "A_first":float(order["order"]=="assurance_first"),
        "I_first":float(order["order"]=="investment_first"),
        "near_simultaneous":float(order["order"]=="near_simultaneous"),
        "A_only":float(order["order"]=="assurance_only"),
        "I_only":float(order["order"]=="investment_only"),
        "neither":float(order["order"]=="neither"),
        "persistence100":float(trace[100,0]>0),
        "persistence400":float(trace[400,0]>0),
    }
    if sum(values[k] for k in (
            "A_first","I_first","near_simultaneous","A_only","I_only","neither"))!=1:
        raise AssertionError("source history lacks exactly one sequence/censoring class")
    return values


def clustered_summary(records):
    profiles=sorted({case[0] for case in records})
    if len(profiles)!=16:raise AssertionError("synthetic visitor-profile unit count incorrect")
    rng=np.random.default_rng(48272026)
    draw=rng.integers(0,len(profiles),size=(9999,len(profiles)))
    by_setting=[]
    for timing in ("delayed","prior"):
        for cost in (0.,.5):
            for mutation in (0.,.01):
                paired=[]; abrupt_observed=[]; gradual_observed=[]
                for profile in profiles:
                    changes=[]; a_rep=[];g_rep=[]
                    for rep in range(49271001,49271005):
                        a=metrics_for_record(records[(profile,rep,timing,cost,mutation,"abrupt")])
                        g=metrics_for_record(records[(profile,rep,timing,cost,mutation,"gradual")])
                        changes.append({k:a[k]-g[k] for k in METRICS})
                        a_rep.append(a);g_rep.append(g)
                    paired.append([np.mean([v[k] for v in changes]) for k in METRICS])
                    abrupt_observed.append([np.mean([v[k] for v in a_rep]) for k in METRICS])
                    gradual_observed.append([np.mean([v[k] for v in g_rep]) for k in METRICS])
                matrix=np.array(paired)
                a_obs=np.array(abrupt_observed)
                g_obs=np.array(gradual_observed)
                bootstrap=matrix[draw].mean(axis=1)
                metrics={}
                for j,k in enumerate(METRICS):
                    metrics[k]={
                        "P_abrupt":float(a_obs[:,j].mean()),
                        "P_gradual":float(g_obs[:,j].mean()),
                        "abrupt_minus_gradual":float(matrix[:,j].mean()),
                        "descriptive_history_profile_bootstrap95":[float(q) for q in np.quantile(
                            bootstrap[:,j],[.025,.975])],
                    }
                by_setting.append({
                    "timing":timing,"direct_assurance_cost":cost,
                    "mutation_rate":mutation,
                    "independent_synthetic_visitor_profile_units":16,
                    "nested_repeats_per_profile":4,
                    "outcomes":metrics
                })
    return {
        "schema":"chapter2_sequence_abrupt_gradual_full_source_readout_v1",
        "status":STATUS,
        "design_sha256":contract()[1],
        "verified_source_identity_sha256":source_identity()["digest"],
        "total_verified_trajectory_cases":1024,
        "n_independent_synthetic_visitor_profiles":16,
        "n_nested_demographic_replicates_per_profile":4,
        "n_natural_plant_islands":0,
        "n_paired_setting_blocks":8,
        "confidence_note":"Bootstrap across 16 synthetic functional visitor profile clusters, with only 4 nested demographic repeats. This does not estimate natural ecological variation and does not establish a historical evolutionary order mechanism.",
        "scientific_warning":"Fixed-reference pollen integrals were equated, but realized pollen can differ as X, I, A and census evolve. Assigned visitor chronology is not an assigned A/I inherited mutation order. No after-outcome window/parameter selection.",
        "results":by_setting,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    r=clustered_summary(read_all(args.input_root))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "verified":r["total_verified_trajectory_cases"],
        "independent_source_profiles":r["n_independent_synthetic_visitor_profiles"]
    },sort_keys=True))

if __name__=="__main__":main()
