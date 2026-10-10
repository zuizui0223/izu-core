"""Exactly compute source Model3 one-generation K=48 Poisson demographic ceiling.

Input is the previously SHA-verified ORIGINAL evolved-genome source JSON.
This is a post-discovery algebraic consequence of the existing demographic
operator, not new stochastic evolution or a future population viability trial.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import poisson

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA="34846d5ea2b758c7123af42130cceec7b3581c4c9a95dcbd0de52c651a599b57"
K=48


def poisson_capped_moments(total_viable:float, capacity:int=48):
    if not np.isfinite(total_viable) or total_viable<0 or capacity<1:
        raise ValueError("invalid source reproduction/capacity")
    x=float(total_viable)
    # E[min(Poisson(x),K)] = x P(Z<=K-2) + K P(Z>=K).
    expected=x*poisson.cdf(capacity-2,x)+capacity*poisson.sf(capacity-1,x)
    return dict(expected_next_census=float(expected),
                probability_below_capacity=float(poisson.cdf(capacity-1,x)),
                probability_occupied=float(-np.expm1(-x)))


def audit(original:Path):
    if hashlib.sha256(original.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise ValueError("input does not match original SHA-verified native genome audit")
    data=json.loads(original.read_text(encoding="utf-8"))
    if data["n_reproduced_state_ledgers"]!=1024 or data["n_independent_histories"]!=64:
        raise ValueError("source historical accounting incomplete")
    out=[]
    for setting in ("delayed_control","prior_selfing","pollen_discount","assurance_cost"):
        for arm in ("near","far"):
            rows=[r for r in data["history_rows"] if r["setting"]==setting and
                  r["arm"]==arm and r["period"]==400 and r["admissible"]]
            if len(rows)!=64:raise ValueError("expected original 64 history blocks")
            values=[]
            for row in rows:
                muE=row["evolving"]["total_viable_maternal"]
                muI=row["evolving_with_investment_clamped_to_fixed_arm_mean"]["total_viable_maternal"]
                e=poisson_capped_moments(muE,K)
                i=poisson_capped_moments(muI,K)
                values.append(dict(history=row["seed"],evolved_viable_mu=muE,
                    investment_clamped_viable_mu=muI,
                    expected_census_delta=e["expected_next_census"]-i["expected_next_census"],
                    evolved_probability_below_K=e["probability_below_capacity"],
                    clamp_probability_below_K=i["probability_below_capacity"]))
            dif=np.asarray([v["expected_census_delta"] for v in values])
            out.append(dict(setting=setting,arm=arm,K=K,n_histories=64,
                min_viable_seed_mu=float(min(min(v["evolved_viable_mu"],
                            v["investment_clamped_viable_mu"]) for v in values)),
                mean_evolved_viable_seed_mu=float(np.mean([v["evolved_viable_mu"] for v in values])),
                mean_expected_census_delta=float(dif.mean()),
                max_abs_expected_census_delta=float(np.max(np.abs(dif))),
                max_probability_next_census_below_K=float(max(
                    max(v["evolved_probability_below_K"],v["clamp_probability_below_K"])
                    for v in values)),history_rows=values))
    return dict(
        status="EXACT_POSTDISCOVERY_SOURCE_ONE_STEP_RECRUITMENT_CEILING",
        parent_source_sha256=SOURCE_SHA,
        demographic_contract={"survival":0,"immigration":0,
            "resident_birth_attempts":"Poisson(total expected viable maternal seed)",
            "next_N":"min(K,resident_birth_attempts)","K":K},
        summary=out,
        interpretation="Near original t400 viability far exceeds K; source immediate mean recruit/census response is capacity-capped. Not long-term occupancy, extirpation, heritable evolutionary group selection or causal mediation.",
        n_new_ecological_histories=0,
    )


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-json",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.source_json)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([x for x in result["summary"] if x["arm"]=="near"],indent=2))


if __name__=="__main__":
    main()
