"""Fail-closed, outcome-free prospective K study contract at fixed B=48."""
from __future__ import annotations
import json
from pathlib import Path

SPEC=Path(__file__).resolve().parents[1]/"data/design/chapter2_k_fixedB48_independent_20261009.json"

def frozen(path=SPEC):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    h=d["independent_cohort"]; m=d["fixed_biological_model"]
    g=d["complete_grid"]; p=d["primary"]
    if d["status"]!="FROZEN_BEFORE_NEW_INDEPENDENT_OUTCOMES":
        raise AssertionError("Unfrozen or outcome-exposed K/B design")
    if (h["visitor_history_first"],h["visitor_history_last"],
            h["independent_history_clusters"])!=(41110901,41110964,64):
        raise AssertionError("Independent study cohort altered")
    if (h["demographic_repeat_ids"]!=[41111901,41111902]
            or h["complete_diploid_t400_source_count"]!=2048
            or h["exclude_early_extinction"] or h["no_outcome_based_selection"] is not True
            or not h["no_seed_reuse_or_prior_source_trajectories"]):
        raise AssertionError("New source independence/unbiased selection changed")
    for a,b in h["previous_exposed_history_ranges"]:
        if not (h["visitor_history_last"]<a or h["visitor_history_first"]>b):
            raise AssertionError("Reused earlier visitor histories")
    if (m["K_values"]!=[8,48] or m["fixed_B"]!=48
            or m["arm_names"]!=["K8_B48","K48_B48"]
            or m["eight_founder_selection_salt"]!=4111092026
            or m["future_seed_salt"]!=4111092048
            or not m["same_eight_complete_diploid_founder_genotypes_per_source"]
            or not m["shared_initial_future_random_streams_across_K_and_gate"]
            or not m["no_plant_immigration"]):
        raise AssertionError("Demographic-only intervention changed")
    if (m["postshock_updates"]!=80 or m["future_visitor_environments"]!=["near","far"]
            or m["budgets"]!=[0.5,1,2,3,4,5,8]
            or [(x["name"],x["selfed_fraction"],x["outcross_fraction"])
                for x in m["postzygotic_gates"]]!=[
                    ("baseline",1,1),("self_half",0.5,1)]
            or {"K","gate","assigned_order"}.difference(m["future_seed_excludes"])):
        raise AssertionError("Postzygotic gate or pairing changed")
    if (g["n_histories"],g["n_t400_sources"],g["futures_per_source"],
            g["total_postshock_futures"],g["independent_inference_units"])!=(
            64,2048,56,114688,64):
        raise AssertionError("Incorrect full-cohort source/future counts")
    if (p["contrast"]!="tau(K8,B48)-tau(K48,B48)" or not p["two_sided"]
            or p["n_visitor_history_clusters"]!=64
            or p["bootstrap"]!={"draws":9999,"seed":2026100967,
                                "percentile95":True,
                                "paired_by":"same visitor history across all K and gates"}
            or p["meaningful_mean_difference_absolute"]!=0.005
            or not p["no_optional_stopping"] or not p["freeze_before_new_outcome_exposure"]):
        raise AssertionError("Registered primary test changed")
    return d

if __name__=="__main__":
    print(json.dumps({"status":frozen()["status"],"n_histories":64,
                      "n_t400_sources":2048,"n_futures":114688,
                      "outcomes_generated":False}))
