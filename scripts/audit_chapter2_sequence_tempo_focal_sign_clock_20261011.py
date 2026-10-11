"""Pre-evolution ORIGINAL source β_A/β_I sign-clock under dose-matched loss.

Uses a FIXED CLONAL n48 X=I=A=.50 reference state, unchanged native
Model3 reproduce, and the actual frozen abrupt vs gradual visitor schedule.
This is a mechanistic timing *prediction* before actual inherited evolution,
not an estimate of historical allele change or evolutionary benefit.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import numpy as np

from scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import (
    ROOT, contract, original_model_config, source_reference_state, visitor_profile,
    functional_visitors, calibration, one_focal_gradient
)

TRAITS=("assurance","investment")
TIMINGS=("delayed","prior")
COSTS=(0.,.5)
PROFILE_SEEDS=range(48271001,48271017)
SCHEDULES=("abrupt","gradual")
DEADBAND=.02
STATUS="ORIGINAL_SOURCE_FIXED_GENOTYPE_SELECTIVE_SIGN_CLOCK_NOT_REALIZED_EVOLUTION"


def local_beta(profile_seed,timing,cost,lam,trait):
    d,_=contract()
    state=source_reference_state(d)
    start,end=visitor_profile(profile_seed,d)
    visitor=functional_visitors(start,end,lam)
    cfg=original_model_config(timing,cost,0.,d)
    j={"investment":1,"assurance":2}[trait]
    return one_focal_gradient(state,visitor,cfg,0,j,h=.005)


def sign_clock(profile_seed,timing,cost):
    if profile_seed not in PROFILE_SEEDS or timing not in TIMINGS or cost not in COSTS:
        raise ValueError("outside source fitness timing contrast")
    plan=calibration(profile_seed,contract()[0])
    betaA=[]
    for l in np.linspace(0,1,21):
        value=local_beta(profile_seed,timing,cost,float(l),"assurance")
        betaA.append(value)
    if not all(np.isfinite(x) and x>.02 for x in betaA):
        raise AssertionError("assurance selection was not initially and continuously positive")

    # Investment fitness sign endpoint check prevents accidentally selecting
    # a source profile in which investment never loses its focal advantage.
    at_start=local_beta(profile_seed,timing,cost,0.,"investment")
    at_end=local_beta(profile_seed,timing,cost,1.,"investment")
    if not at_start>.02 or not at_end<-.02:
        raise AssertionError("no full W investment sign reversal in frozen source")
    # Determine the earliest *negative* local beta, not the first mean trait
    # shift, using the original source fitness operator.
    lo,hi=0.,1.
    for _ in range(30):
        m=(lo+hi)/2
        if local_beta(profile_seed,timing,cost,m,"investment")<-.02:
            hi=m
        else:
            lo=m
    critical=(lo+hi)/2
    out={}
    for schedule in SCHEDULES:
        seq=plan["abrupt_lambdas"] if schedule=="abrupt" else plan["ramp_lambdas"]
        observed=next((t for t,lam in enumerate(seq) if lam>critical),None)
        if observed is None:raise AssertionError("the controlled treatment never enters negative selection")
        # Check numerical derivative before/after, including the transition
        # year (not arbitrary integer threshold rounding).
        b=local_beta(profile_seed,timing,cost,float(seq[observed]),"investment")
        if not b < -.02:
            raise AssertionError("numerical negative-investment source onset misidentified")
        if observed:
            preceding=local_beta(profile_seed,timing,cost,float(seq[observed-1]),"investment")
            if preceding<-.02:
                raise AssertionError("beta_I was negative earlier")
        out[schedule]={
            "first_update_with_negative_focal_beta_I":int(observed),
            "lambda_at_first_negative":float(seq[observed]),
            "beta_I_at_first_negative":float(b),
        }
    return {
        "source_profile_seed":profile_seed,
        "assurance_timing":timing,
        "direct_assurance_cost":cost,
        "reference_allele_means":[.5,.5,.5],
        "source_census_N":48,
        "focal_beta_I_matched":float(at_start),
        "focal_beta_I_shifted":float(at_end),
        "positive_assurance_beta_range":[float(min(betaA)),float(max(betaA))],
        "lambda_for_beta_I_below_negative_deadband":float(critical),
        "dose_matched_break_index":plan["break_index"],
        "by_schedule":out,
        "sudden_minus_gradual_negative_selection_onset":(
            out["abrupt"]["first_update_with_negative_focal_beta_I"]-
            out["gradual"]["first_update_with_negative_focal_beta_I"]
        ),
    }


def audit():
    rows=[sign_clock(seed,timing,cost) for seed in PROFILE_SEEDS
          for timing in TIMINGS for cost in COSTS]
    if len(rows)!=64:
        raise AssertionError("source sign clock incomplete")
    return {
        "schema":"chapter2_functional_loss_selection_source_sign_clock_v1",
        "status":STATUS,
        "n_synthetic_visitor_profiles":16,
        "n_cost_timing_source_conditions":4,
        "n_source_cells":len(rows),
        "n_new_evolutionary_outcomes":0,
        "n_natural_ecological_systems":0,
        "biological_operator":"original scripts/model3_island/reproduction.py::reproduce and full W=(F+P)/2+S",
        "genetic_allele_source":"fixed homozygous reference mean X=I=A=.5; no offspring observed in this audit",
        "interpretation_ceiling":"Clock for instantaneous local source selection sign only, not the date genomic I changes. Assured A beta positive at the reference plant state and investment beta flips as pollinator matching deteriorates; the actual stochastic genetic response may show different order because standing variation, drift, differential selection among adults, mutation and density feedback.",
        "results":rows,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{
        "seed":r["source_profile_seed"],
        "timing":r["assurance_timing"],
        "cost":r["direct_assurance_cost"],
        "A_beta_range":r["positive_assurance_beta_range"],
        "I_initial":r["focal_beta_I_matched"],
        "I_final":r["focal_beta_I_shifted"],
        "source_onset_sudden_minus_gradual":r["sudden_minus_gradual_negative_selection_onset"]
    } for r in d["results"]],sort_keys=True))


if __name__=="__main__":main()
