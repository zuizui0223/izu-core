"""Fail-closed prospective 2×2 demographic K / pollen-background B protocol.

This only validates design; no prospective biological outcomes are generated.
"""
import json
from pathlib import Path

PROTOCOL = Path(__file__).resolve().parents[1]/"data/design/chapter2_kb_decoupled_20261009.json"


def validate_protocol(path=PROTOCOL):
    p=json.loads(Path(path).read_text(encoding="utf-8"))
    h=p["independent_cohort"]
    r=p["intervention"]
    g=p["full_grid"]
    e=p["primary_estimand"]
    if p["status"]!="FROZEN_PROSPECTIVE_DESIGN_NO_NEW_OUTCOMES":
        raise AssertionError("Cannot overwrite prospective study with a results document")
    if (h["visitor_history_first"],h["visitor_history_last"],
            h["n_independent_history_clusters"])!=(40110901,40110964,64):
        raise AssertionError("New unused 64-history cohort changed")
    if (h["demographic_repeat_ids"]!=[40111901,40111902]
            or h["full_diploid_t400_source_count"]!=2048
            or not h["include_extinct_t400_without_selection"]):
        raise AssertionError("Fresh complete t400 source contract changed")
    for a,b in h["banned_earlier_ranges"]:
        if not (h["visitor_history_last"]<a or h["visitor_history_first"]>b):
            raise AssertionError("Already exposed history IDs reused")
    if (r["true_demographic_capacity_K"]!=[8,48]
            or r["background_normalizer_B"]!=[8,48]
            or r["four_cells_ordered"]!=["K8_B8","K8_B48","K48_B8","K48_B48"]
            or not r["exact_same_source_diploid_ids_and_alleles_four_cells"]
            or r["sampled_founders_max_n"]!=8
            or r["founder_subsample_seed_tag"]!=4011092026):
        raise AssertionError("Orthogonal factorial changed")
    if ([(x["name"],x["selfed_fraction"],x["outcross_fraction"])
            for x in r["viability_gates"]]!=[
                ("baseline",1,1),("self_half",0.5,1)]
            or r["budgets"]!=[0.5,1,2,3,4,5,8]
            or r["future_visitors"]!=["near","far"]
            or r["postshock_updates"]!=80):
        raise AssertionError("Postzygotic intervention/outcome horizon changed")
    if (g["n_t400_sources"],g["n_futures_per_source"],
            g["n_raw_future_trajectories"])!=(2048,112,229376):
        raise AssertionError("Full raw future count changed")
    if (e["focal_contrast"]!="tau(K8,B8)-tau(K8,B48)"
            or e["cluster_bootstrap_draws"]!=9999
            or e["cluster_bootstrap_seed"]!=2026100957
            or e["decision_minimum_meaningful_absolute"]!=0.005
            or not e["history_count_fixed_before_new_outcomes"]
            or not e["no_optional_stopping"]):
        raise AssertionError("Primary estimand/inference altered")
    return p


if __name__=="__main__":
    p=validate_protocol()
    print(json.dumps({"status":p["status"],"n_histories":64,
                      "n_sources":2048,"planned_futures":229376,
                      "new_outcomes_generated":False}))
