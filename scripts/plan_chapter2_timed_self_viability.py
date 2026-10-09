"""Validate the frozen prospective time-window self-viability study WITHOUT outcomes."""
from __future__ import annotations
import json
from pathlib import Path

SPEC=Path(__file__).resolve().parents[1]/"data/design/chapter2_timed_self_viability_20261009.json"
GATES=("baseline","self_half_early","self_half_late","self_half_full")
K_ARMS=("K8_B48","K48_B48")


def frozen(path=SPEC):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    h=d["genuinely_new_cohort"]
    bio=d["biological_scope"]
    g=d["complete_grid"]
    p=d["frozen_primary"]
    if d["status"]!="FROZEN_BEFORE_NEW_INDEPENDENT_OUTCOMES":
        raise AssertionError("New outcomes or changed protocol cannot be treated as preregistered")
    if (h["visitor_history_first"],h["visitor_history_last"],h["visitor_history_count"])!=(42110901,42110964,64):
        raise AssertionError("New independent visitor cohort changed")
    if (h["demographic_repeat_ids"]!=[42111901,42111902]
            or h["total_complete_diploid_t400_sources"]!=2048
            or not h["include_t400_extinctions_without_filter"]
            or not h["no_reuse_of_observed_histories"]):
        raise AssertionError("Independent prehistory source contract changed")
    for lo,hi in h["old_exposed_ranges"]:
        if not (h["visitor_history_last"]<lo or h["visitor_history_first"]>hi):
            raise AssertionError("New visitor cohort overlaps exposed histories")
    if (bio["fixed_background_B"]!=48 or bio["demographic_K_values"]!=[8,48]
            or bio["founder_sample_seed_salt"]!=4211092026
            or bio["future_stream_seed_salt"]!=4211092048
            or not bio["exact_same_full_diploid_F8_founder_genomes_across_K_and_all_gates"]
            or not bio["same_initial_future_random_streams_across_K_and_gates"]
            or not bio["no_plant_immigration"]):
        raise AssertionError("Fixed biological model and common randomization changed")
    if (tuple(x["name"] for x in bio["viability_gates"])!=GATES
            or [(x["selfed_viability_multiplier"],x["apply_updates"])
                 for x in bio["viability_gates"]]!=[
                    (1,[]),(0.5,[0,39]),(0.5,[40,79]),(0.5,[0,79])]
            or bio["postshock_horizon_updates"]!=80
            or bio["budget_support"]!=[0.5,1,2,3,4,5,8]):
        raise AssertionError("Timing intervention or future horizon changed")
    if (g["full_source_count"],g["future_conditions_per_source"],
            g["total_future_trajectories"],g["independent_statistical_clusters"])!=(
            2048,112,229376,64):
        raise AssertionError("Complete future campaign changed")
    if (p["primary_contrast"]!=
            "[tau_late(K8)-tau_late(K48)]-[tau_early(K8)-tau_early(K48)]"
            or p["bootstrap_draws"]!=9999 or p["bootstrap_seed"]!=2026100981
            or p["minimum_meaningful_absolute_probability"]!=0.005
            or p["bootstrap_unit"]!="paired visitor history"
            or not p["no_optional_stopping"]):
        raise AssertionError("Primary preregistered statistic changed")
    return d


if __name__=="__main__":
    print(json.dumps({"status":frozen()["status"],"histories":64,
                      "sources":2048,"future_trajectories":229376,
                      "new_outcomes_generated":False}))
