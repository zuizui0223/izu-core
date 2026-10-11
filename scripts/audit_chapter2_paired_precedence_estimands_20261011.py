"""Paired audit of *which* evolutionary order the historical trajectories measure.

Re-read the complete, already public 2026-10-05 Model3 temporal-order readout.
The same 64 visitor histories have two different order estimands:

(1) Within far/island population, trait change relative to its founders.
(2) The FAR-minus-NEAR divergence (incremental island/isolation response).

These are not interchangeable, and an order-label change can include
threshold noncrossing or ties, not only a strict A-first ↔ I-first reversal.

This script does not rerun, simulate or independently confirm ecology; it
recomputes a complete 2 mating × 2 mutation × 3 threshold paired cross-tab.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import json
import math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/results/model3_persistent_isolation_summary_20261005.json"
SETTINGS=("assurance_cost","prior_selfing")
MUTATION=(0.,.01)
THRESHOLDS=(.025,.05,.1)
WITHIN="far_change_from_founders"
DIVERGENCE="paired_far_minus_near"
LABELS=("assurance_first","investment_first","near_simultaneous",
        "assurance_only","investment_only","neither")
STATUS="POSTDISCOVERY_PAIRED_ORDER_REFERENCE_READING_NOT_CAUSAL_ORDER_INTERVENTION"


def load_frozen_readout(path=SOURCE):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    if (d.get("status")!="completed_summary"
            or d.get("verified_new_cases")!=2048
            or d.get("verified_near_references")!=2048
            or d.get("first_200_updates_match") is not True
            or len(d["temporal_order"])!=36):
        raise ValueError("requires complete verified 2026-10-05 source readout")
    return d


def aligned_events(data,setting,mutation,threshold):
    entries=[x for x in data["temporal_order"]
             if x["setting"]==setting and x["mutation_rate"]==mutation
             and x["threshold"]==threshold]
    assert len(entries)==3, "source must include far/near and paired estimands"
    source_by={x["contrast"]:x for x in entries}
    if WITHIN not in source_by or DIVERGENCE not in source_by:
        raise ValueError("source contrasts absent")
    a,b=source_by[WITHIN],source_by[DIVERGENCE]
    x={e["history_seed"]:e for e in a["events"]}
    y={e["history_seed"]:e for e in b["events"]}
    keys=list(range(76001,76065))
    if sorted(x)!=keys or sorted(y)!=keys:
        raise AssertionError("64 history units not perfectly paired")
    if any(e["order"] not in LABELS for e in [*x.values(),*y.values()]):
        raise ValueError("unrecognized original order category")
    if Counter(x[k]["order"] for k in keys)!=a["counts"]:
        raise AssertionError("within-arm source class counts altered")
    if Counter(y[k]["order"] for k in keys)!=b["counts"]:
        raise AssertionError("far-near source class counts altered")
    pairs=[]
    for k in keys:
        first=x[k];second=y[k]
        pairs.append({
            "history_seed":k,
            "far_from_founder_order":first["order"],
            "far_minus_near_order":second["order"],
            "within_A_crossing":first["assurance_time"],
            "within_I_crossing":first["investment_time"],
            "divergence_A_crossing":second["assurance_time"],
            "divergence_I_crossing":second["investment_time"],
            "within_lag_I_minus_A":(
                first["investment_time"]-first["assurance_time"]
                if first["investment_time"] is not None and first["assurance_time"] is not None
                else None),
            "divergence_lag_I_minus_A":(
                second["investment_time"]-second["assurance_time"]
                if second["investment_time"] is not None and second["assurance_time"] is not None
                else None)
        })
    return pairs


def summarize_pairs(pairs):
    tab={k:{q:0 for q in LABELS} for k in LABELS}
    for p in pairs:
        tab[p["far_from_founder_order"]][p["far_minus_near_order"]]+=1
    assert sum(sum(q.values()) for q in tab.values())==64
    strict_reversed=sum(
        x["far_from_founder_order"]=="assurance_first" and
        x["far_minus_near_order"]=="investment_first"
        for x in pairs
    )+sum(
        x["far_from_founder_order"]=="investment_first" and
        x["far_minus_near_order"]=="assurance_first"
        for x in pairs
    )
    reclassified=sum(p["far_from_founder_order"]!=p["far_minus_near_order"] for p in pairs)
    within_lags=[p["within_lag_I_minus_A"] for p in pairs if p["within_lag_I_minus_A"] is not None]
    divergence_lags=[p["divergence_lag_I_minus_A"] for p in pairs if p["divergence_lag_I_minus_A"] is not None]
    return {
        "within_far_counts":dict(Counter(p["far_from_founder_order"] for p in pairs)),
        "incremental_far_minus_near_counts":dict(Counter(p["far_minus_near_order"] for p in pairs)),
        "order_cross_tab_6x6":tab,
        "reclassified_any_reason":reclassified,
        "strict_opposite_order":strict_reversed,
        "reclassified_but_not_strict_opposite":reclassified-strict_reversed,
        "within_both_crossing_n":len(within_lags),
        "divergence_both_crossing_n":len(divergence_lags),
        "within_median_lag_I_minus_A":float(np.median(within_lags)) if within_lags else None,
        "divergence_median_lag_I_minus_A":float(np.median(divergence_lags)) if divergence_lags else None,
        "n_original_independent_history_clusters":64,
    }


def audit():
    d=load_frozen_readout()
    rows=[]
    for setting in SETTINGS:
        for mutation in MUTATION:
            for threshold in THRESHOLDS:
                pairs=aligned_events(d,setting,mutation,threshold)
                rows.append({
                    "setting":setting,"mutation_rate":mutation,
                    "crossing_threshold":threshold,
                    "sustained_updates":20,"near_simultaneous_tolerance":5,
                    "paired_summary":summarize_pairs(pairs),
                    "paired_history_records":pairs,
                })
    return {
        "schema":"model3_two_precedence_estimands_paired_complete_v1",
        "status":STATUS,
        "source_json":SOURCE.relative_to(ROOT).as_posix(),
        "source_verified_cases":d["verified_new_cases"],
        "analysis_count":len(rows),
        "n_new_evolutionary_histories":0,
        "n_independent_ecological_systems":0,
        "interpretation_ceiling":[
            "Founder-relative change and far-minus-near divergence are different estimands.",
            "A category change can include ties and censored thresholds; it is not always a strict biological order reversal.",
            "51/64 assurance-first is a setting- and threshold-specific historical observation, not a universal mating-system evolutionary sequence.",
            "Prior-selfing and delayed selfing jointly change direct assurance cost in this historical comparison; do not attribute setting differences to selfing timing alone.",
            "Timing of trait crossing does not demonstrate when selection coefficients changed sign, or manipulate visitor-loss onset.",
            "Time order does not establish a necessary causal pathway from selfing evolution to floral investment decrease or a fitness benefit of the order.",
        ],
        "results":rows,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    d=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{
        "setting":r["setting"],
        "mutation_rate":r["mutation_rate"],
        "threshold":r["crossing_threshold"],
        "within":r["paired_summary"]["within_far_counts"],
        "far_minus_near":r["paired_summary"]["incremental_far_minus_near_counts"],
        "reclassified":r["paired_summary"]["reclassified_any_reason"],
        "strict_opposite_order":r["paired_summary"]["strict_opposite_order"],
    } for r in d["results"]],sort_keys=True))


if __name__=="__main__":
    main()
