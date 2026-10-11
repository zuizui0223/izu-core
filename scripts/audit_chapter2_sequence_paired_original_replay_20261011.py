"""Same 64-history frozen cohort: paired ORIGINAL ABM prefix and A/I crossings.

Unlike the archived 10-column means, we actively replay original full diploid
plant states and original keyed RNG. This companion checks that all eight
nested demographic repeats reconstruct the ALREADY FROZEN trait crossing
events. It does not infer individual source-gradient signs from archived means.

The selected source history 76001 in assurance_cost/.01 has all three
original threshold crossing times within the first 63 updates; replaying
the first 100 updates suffices to check its six crossing events without
running 1000 updates for each original repeat.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_sequence_source_genome_replay_20261011 import (
    ROOT, replay, STATUS
)
from scripts.model3_temporal_order import first_sustained,order_label

FROZEN_RESULT=ROOT/"data/results/model3_persistent_isolation_summary_20261005.json"
FROZEN_SEQUENCE_DIAGNOSTIC=ROOT/"data/design/model3_temporal_order_diagnostic_20261005.json"
REPEAT_SEEDS=range(7101,7109)
THRESHOLDS=(.025,.05,.1)
STATUS_PAIRED="POSTDISCOVERY_ORIGINAL_GENOME_REPLAY_FROZEN_ORDER_HISTORY_MATCH_NOT_NEW_COHORT"


def mean_available(values,axis):
    n=np.isfinite(values).sum(axis=axis)
    return np.divide(np.nansum(values,axis=axis),n,
        out=np.full(n.shape,np.nan,dtype=float),where=n>0)


def original_expected(seed,setting,threshold,contrast):
    old=json.loads(FROZEN_RESULT.read_text(encoding="utf-8"))
    assert old["status"]=="completed_summary" and old["verified_new_cases"]==2048
    matching=[x for x in old["temporal_order"] if
        x["setting"]==setting and x["mutation_rate"]==.01 and
        x["threshold"]==threshold and x["contrast"]==contrast]
    if len(matching)!=1:
        raise AssertionError("frozen historical source crossing row missing")
    found=[e for e in matching[0]["events"] if e["history_seed"]==seed]
    if len(found)!=1:
        raise AssertionError("frozen original history seed not found")
    return found[0]


def original_order_pair_100_updates(*,seed=76001,setting="assurance_cost",
                                     years=100,gradient_until=0,
                                     sample_n=2,archive_root=None,
                                     require_all_frozen_crossings=True):
    if seed!=76001 or setting!="assurance_cost":
        # Do not use 100-year right censoring to validate unknown later 1000-y
        # crossings; this routine is the intentionally preidentified anchor.
        raise ValueError("100-update exact order anchor restricted to assurance_cost history76001")
    if not 63<=years<=1000:
        raise ValueError("must preserve sufficient 20-year sustained crossing window")
    plan=json.loads(FROZEN_SEQUENCE_DIAGNOSTIC.read_text())
    if plan["sustained_periods"]!=20 or plan["tie_tolerance_periods"]!=5:
        raise AssertionError("temporal-order protocol changed")
    data=np.zeros((8,2,years+1,10),dtype=float)
    hashes=[];focal=[]
    for idx,rep in enumerate(REPEAT_SEEDS):
        for j,arm in enumerate(("near","far")):
            record=replay(setting,seed,rep,arm,years=years,
                          gradient_until=gradient_until,sample_n=sample_n,
                          archive_root=archive_root)
            data[idx,j]=np.asarray(record["trace"],dtype=float)
            hashes.append({"rep":rep,"arm":arm,
                "replay_trace_sha256":record["source_trace_sha256"],
                "archive_verified":record["verification"][
                    "verified_against_exact_original_archive"]})
            focal.append({"rep":rep,"arm":arm,
                "sampled_local_focal_selection":record["sampled_local_focal_selection"]})
    occupied=data[:,:,:,0]>0
    paired=occupied[:,0]&occupied[:,1]
    gap=np.where(paired[:,:,None],
                 data[:,1,:,1:4]-data[:,0,:,1:4],np.nan)
    far_change=data[:,1,:,1:4]-data[:,1,0,1:4][:,None,:]
    far_change=np.where(occupied[:,1,:,None],far_change,np.nan)
    curves={
        "far_change_from_founders":mean_available(far_change,axis=0),
        "paired_far_minus_near":mean_available(gap,axis=0)
    }
    events=[]
    for contrast,v in curves.items():
        for threshold in THRESHOLDS:
            tI=first_sustained(-v[:,1],threshold,20)
            tA=first_sustained(v[:,2],threshold,20)
            category=order_label(tA,tI,5)
            historical=original_expected(seed,setting,threshold,contrast)
            matched=(tI==historical["investment_time"] and
                     tA==historical["assurance_time"] and
                     category==historical["order"])
            if require_all_frozen_crossings and not matched:
                raise AssertionError(
                    f"historical source event replay mismatch {contrast} {threshold}: "
                    f"got {tA},{tI},{category}, expected {historical}"
                )
            events.append({
                "contrast":contrast,
                "threshold":threshold,
                "replayed_investment_crossing":tI,
                "replayed_assurance_crossing":tA,
                "replayed_category":category,
                "historical_1000_update_event":historical,
                "original_event_agrees_with_prefix_replay":matched,
            })
    return {
        "schema":"chapter2_sequence_paired_original_prefix_source_verification_v1",
        "status":STATUS_PAIRED,
        "history_seed":seed,"setting":setting,"mutation_rate":.01,
        "n_original_demographic_repeats":len(REPEAT_SEEDS),
        "n_original_visitor_history_clusters":1,
        "years_replayed":years,"n_original_near_and_far_replays":16,
        "all_six_frozen_original_events_reproduced":all(
            e["original_event_agrees_with_prefix_replay"] for e in events),
        "direct_archive_NPZ_identity_verified":all(
            r["archive_verified"] for r in hashes),
        "original_10_column_trace_sha_by_case":hashes,
        "original_observed_crossings":events,
        "annual_pooled_trait_delta_from_founder_far":curves[
            "far_change_from_founders"].tolist(),
        "annual_pooled_far_minus_near_trait_delta":curves[
            "paired_far_minus_near"].tolist(),
        "sampled_actual_genotype_local_gradients":focal,
        "scientific_limit":"This exact original-model history replay tests correspondence with frozen observed trait-crossing timing, not the causal role of the selected preceding trait, not all 64 histories, not archive NPZ byte identity unless raw receipts supplied. Any sampled gradient is individual focal W and not the whole population or spontaneous mutation causal effect.",
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--years",type=int,default=100)
    parser.add_argument("--gradient-until",type=int,default=50)
    parser.add_argument("--sample-n",type=int,default=4)
    parser.add_argument("--archive-root",type=Path,default=None)
    args=parser.parse_args()
    d=original_order_pair_100_updates(
        years=args.years,gradient_until=args.gradient_until,
        sample_n=args.sample_n,archive_root=args.archive_root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":d["status"],
        "history":d["history_seed"],
        "n_original_replayed_cases":d["n_original_near_and_far_replays"],
        "all_six_events_match_original_frozen_source":d[
            "all_six_frozen_original_events_reproduced"],
        "archive_NPZ_identity_verified":d["direct_archive_NPZ_identity_verified"],
        "source_events":d["original_observed_crossings"],
    },sort_keys=True))


if __name__=="__main__":main()
