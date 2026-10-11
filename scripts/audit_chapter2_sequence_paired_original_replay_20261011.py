"""Compare one discovery-history replay candidate with frozen A/I crossings.

The imported checkout generates diploid states under the frozen task and RNG
specification. This companion checks whether its eight paired demographic
repeats agree with already frozen trait-crossing events. Supplied case-file
agreement cannot authenticate the historical archive, source or runtime.

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
    ROOT, replay, unverified_historical_identity
)
from scripts.model3_temporal_order import first_sustained,order_label

FROZEN_RESULT=ROOT/"data/results/model3_persistent_isolation_summary_20261005.json"
FROZEN_SEQUENCE_DIAGNOSTIC=ROOT/"data/design/model3_temporal_order_diagnostic_20261005.json"
REPEAT_SEEDS=range(7101,7109)
THRESHOLDS=(.025,.05,.1)
STATUS_PAIRED="POSTDISCOVERY_PAIRED_REPLAY_CANDIDATE_HISTORICAL_IDENTITY_UNVERIFIED"


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
            # A legacy boolean from a case reader is not an authentication
            # contract. This companion independently establishes no identity.
            comparison={**record["verification"],**unverified_historical_identity()}
            hashes.append({"rep":rep,"arm":arm,
                "replay_trace_sha256":record["source_trace_sha256"],
                "archive_verified":False,"verification":comparison})
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
    comparisons=[r["verification"] for r in hashes]
    records_agree=(len(comparisons)==16 and all(
        v.get("supplied_case_record_verified") is True for v in comparisons))
    prefixes_agree=(records_agree and all(
        v.get("replay_matches_supplied_prefix") is True for v in comparisons))
    verification={
        **unverified_historical_identity(),
        "case_records_expected":16,
        "case_records_compared":sum(
            v.get("supplied_case_record_verified") is True for v in comparisons),
        "all_supplied_case_records_agree":records_agree,
        "all_supplied_trace_prefixes_agree":prefixes_agree,
        "all_full_supplied_records_reproduced":prefixes_agree and all(
            v.get("full_supplied_record_reproduced") is True for v in comparisons),
        "reason":"This companion aggregates supplied-case comparisons and frozen crossing agreement; it authenticates no historical archive, source, runtime or annual genomes.",
    }
    return {
        "schema":"chapter2_sequence_paired_replay_candidate_v2",
        "status":STATUS_PAIRED,
        "history_seed":seed,"setting":setting,"mutation_rate":.01,
        "n_original_demographic_repeats":len(REPEAT_SEEDS),
        "n_original_visitor_history_clusters":1,
        "years_replayed":years,"n_original_near_and_far_replays":16,
        "all_six_frozen_original_events_reproduced":all(
            e["original_event_agrees_with_prefix_replay"] for e in events),
        "direct_archive_NPZ_identity_verified":False,
        "verification":verification,
        "original_10_column_trace_sha_by_case":hashes,
        "original_observed_crossings":events,
        "annual_pooled_trait_delta_from_founder_far":curves[
            "far_change_from_founders"].tolist(),
        "annual_pooled_far_minus_near_trait_delta":curves[
            "paired_far_minus_near"].tolist(),
        "sampled_actual_genotype_local_gradients":focal,
        "scientific_limit":"This current-checkout replay candidate tests correspondence with frozen trait-crossing timing for one history. Supplied NPZ/receipt agreement does not authenticate the historical archive, source, runtime or original annual genomes. Sampled gradients are individual focal W assays, not population-wide gradients or causal effects of inherited order.",
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--years",type=int,default=100)
    parser.add_argument("--gradient-until",type=int,default=50)
    parser.add_argument("--sample-n",type=int,default=4)
    parser.add_argument("--archive-root",type=Path,default=None,
                        help="Parent of supplied case files; comparison does not authenticate historical origin")
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
        "verification":d["verification"],
        "source_events":d["original_observed_crossings"],
    },sort_keys=True))


if __name__=="__main__":main()
