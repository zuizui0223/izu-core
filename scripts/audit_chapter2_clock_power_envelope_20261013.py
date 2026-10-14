"""Pre-outcome assumed-effect power envelope, no Model 3 biological simulation.

P(one-sided directional success under a two-sided-normal 95% lower bound > 0)
with an explicitly ASSUMED independent paired-history standard deviation.
This is not empirical power or a basis for declaring clock superiority.
"""
from __future__ import annotations
import argparse
from math import ceil,erf,sqrt
from pathlib import Path
import json

Z_975=1.959963984540054
Z_80=0.8416212335729143
EFFECT_GRID=(0.01,0.02,0.03)
SIGMA_GRID=(0.05,0.1,0.15,0.2,0.25)
HISTORY_GRID=(128,256,512,768,896,1024)
MIN_WORTHWHILE_LOGLOSS_REDUCTION=.02
PLANNING_SIGMA_FLOOR=.15
MIN_CONFIRM_CLUSTERS=512
MAX_CONFIRM_CLUSTERS=1024
ROUND_CONFIRM_CLUSTERS=128 # balanced two founder blocks, 64 new seeds each
PILOT_CLUSTERS=128


def normal_cdf(x: float)->float:
    return .5*(1+erf(x/sqrt(2)))


def probability_success(effect:float,sigma:float,n:int)->float:
    if not (effect>0 and sigma>0 and n>0):raise ValueError("positive effect/sigma/independent histories required")
    return normal_cdf(effect*sqrt(n)/sigma - Z_975)


def required_clusters(sigma:float,effect:float=MIN_WORTHWHILE_LOGLOSS_REDUCTION)->int:
    if not (sigma>0 and effect>0):raise ValueError("positive hypothetical sigma/effect required")
    exact=ceil(((Z_975+Z_80)*sigma/effect)**2)
    rounded=int(ceil(exact/ROUND_CONFIRM_CLUSTERS)*ROUND_CONFIRM_CLUSTERS)
    return max(MIN_CONFIRM_CLUSTERS,rounded)


def plan_confirmation(sigma_hat:float)->dict:
    """Rule declared BEFORE pilot. Pilot effect estimate never enters."""
    if not (sigma_hat>0):raise ValueError("positive paired-history SD required")
    effective_sigma=max(sigma_hat,PLANNING_SIGMA_FLOOR)
    n=required_clusters(effective_sigma)
    return {"assumed_or_pilot_sd":sigma_hat,"planning_sigma":effective_sigma,
            "independent_clusters":n if n<=MAX_CONFIRM_CLUSTERS else None,
            "clusters_per_founder":n//2 if n<=MAX_CONFIRM_CLUSTERS else None,
            "confirm_trajectories":12*n if n<=MAX_CONFIRM_CLUSTERS else None,
            "decision":"RUN_ONLY_AFTER_PROTOCOL_REVIEW" if n<=MAX_CONFIRM_CLUSTERS else "NO_GO_PRECISION_EXCEEDS_CAP",
            "pilot_effect_point_estimate_used":False}


def audit()->dict:
    grid=[{"assumed_delta_log_loss":d,"assumed_paired_history_sd":s,"clusters":n,
           "asymptotic_normal_power":probability_success(d,s,n)}
          for d in EFFECT_GRID for s in SIGMA_GRID for n in HISTORY_GRID]
    examples=[plan_confirmation(s) for s in SIGMA_GRID]
    return {"schema":"chapter2_clock_power_envelope_assumption_sensitivity_v1",
            "status":"DESIGN_ONLY_HYPOTHETICAL_NORMAL_POWER_NOT_EMPIRICAL",
            "test":"paired history mean proper-score reduction; require lower 95% interval > 0",
            "primary_score":"six-category held-out log loss",
            "hypothetical_min_important_gain":MIN_WORTHWHILE_LOGLOSS_REDUCTION,
            "independent_unit":"founder + stochastic visitor-history stream, paired across 12 treatment/context cells",
            "pilot":{"per_founder_clusters":PILOT_CLUSTERS//2,"clusters":PILOT_CLUSTERS,"treatments_per_cluster":12,"trajectories":PILOT_CLUSTERS*12,"used_in_confirmation":False},
            "confirmation_selection_rule":{"alpha_two_sided":.05,"power_target":.80,"sigma_floor":PLANNING_SIGMA_FLOOR,
              "min_clusters":MIN_CONFIRM_CLUSTERS,"max_clusters":MAX_CONFIRM_CLUSTERS,"round_to":ROUND_CONFIRM_CLUSTERS,
              "effect_used":MIN_WORTHWHILE_LOGLOSS_REDUCTION,"if_over_cap":"NO_GO; do not inflate effect or weaken rule"},
            "design_grid":grid,"example_confirmation_allocations":examples,
            "limitations":["sigma values are scenarios, not sample SD estimates of an independent new factorial experiment",
                           "normal paired-history formula assumes independent streams and ignores fitted-model uncertainty",
                           "single model-family/three fixed ecological contexts are not independent biological systems",
                           "predictor class, competing flexible null, calibration and error grouping must be fixed before confirmation",
                           "no original or new biological Model3 simulations performed"]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(audit(),f,indent=2,allow_nan=False);f.write("\n")
    print(json.dumps({"status":"DESIGN_ONLY", "scenario_rows":len(audit()["design_grid"]), "assumed_sd_015":plan_confirmation(.15),"assumed_sd_020":plan_confirmation(.2)}))

if __name__=="__main__":main()
