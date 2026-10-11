"""Conservative post-outcome paired-history CI sensitivity for source Gamma_persist.

Original source-lock and raw outcomes remain unchanged. This is explicitly a
SEPARATE methodological sensitivity: naive paired percentile bootstrap
becomes degenerate when all observed pairs have equal endpoints.
Exact Clopper-Pearson binomial bounds for each exclusive discordance
probability, combined by Bonferroni, give >=95% simultaneous coverage for
the difference p(plus_only) - p(minus_only) under independent visitor histories.
No field-ecology or finite-genetic-evolution inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scipy.stats import beta

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"data/results/chapter2_gamma_persist_64_history_holdout_receipt_20261010.json"
STATUS="POST_OUTCOME_EXACT_PAIRED_DISCORDANCE_INTERVAL_SENSITIVITY"


def cp_bernoulli(k,n,alpha):
    if (type(k) is not int or type(n) is not int or type(alpha) not in (int,float)
            or n<1 or not 0<=k<=n or not 0<alpha<1):
        raise ValueError("invalid exact binomial interval inputs")
    lo=0.0 if k==0 else float(beta.ppf(alpha/2,k,n-k+1))
    hi=1.0 if k==n else float(beta.ppf(1-alpha/2,k+1,n-k))
    if not 0<=lo<=hi<=1:
        raise AssertionError("exact binomial CI not normalized")
    return [lo,hi]


def paired_exact_interval(plus_only,minus_only,n):
    if (type(plus_only) is not int or type(minus_only) is not int
            or plus_only+minus_only>n):
        raise ValueError("paired path discordance counts out of range")
    # Each Bernoulli event refers to the same history but a different
    # exclusive discordance category. The individual marginal CP intervals
    # remain exact; a Bonferroni union bound does not assume their independence.
    positive=cp_bernoulli(plus_only,n,.025)
    negative=cp_bernoulli(minus_only,n,.025)
    lo=positive[0]-negative[1]
    hi=positive[1]-negative[0]
    return [float(lo),float(hi)]


def classify(ci,rope=.05):
    lo,hi=ci
    if lo>rope:return "resolved_positive"
    if hi< -rope:return "resolved_negative"
    if lo>=-rope and hi<=rope:return "practically_equivalent"
    return "inconclusive"


def audit():
    raw=RECEIPT.read_bytes()
    d=json.loads(raw)
    if (d["status"]!="EXECUTED_MODEL_INTERNAL_NEW_64_VISITOR_HISTORIES_NO_EVOLUTION"
            or d["outcome_units"]["visitor_histories"]!=64
            or d["outcome_units"]["n_futures"]!=1024
            or d["raw_json_sha256"]!="a96540fa9c6e96ba3f1e9c15d9dcc0690707742316911f730a425ec76c5275c7"
            or len(d["results"])!=8):
        raise ValueError("invalid source-locked original outcome receipt")
    result=[]
    for r in d["results"]:
        for horizon in ("20","80"):
            v=r["horizons"][horizon]
            plus=v["n_shift_plus_occupied"]
            minus=v["n_shift_minus_occupied"]
            plus_only=v["n_plus_only"];minus_only=v["n_minus_only"]
            n=64
            if (not all(type(x) is int for x in (plus,minus,plus_only,minus_only))
                    or not all(0<=x<=n for x in (plus,minus,plus_only,minus_only))
                    or plus-minus!=plus_only-minus_only):
                raise AssertionError("disagreement with original paired histories")
            both=plus-plus_only
            neither=n-(both+plus_only+minus_only)
            if not 0<=both<=n or not 0<=neither<=n:
                raise AssertionError("inconsistent paired data")
            interval=paired_exact_interval(plus_only,minus_only,n)
            result.append({
                "K":r["K"],"assurance":r["assurance"],"gate":r["gate"],
                "horizon":int(horizon),
                "n_plus_occupied":plus,"n_minus_occupied":minus,
                "plus_only":plus_only,"minus_only":minus_only,
                "both_survived":both,"both_extinct":neither,
                "delta_plus_minus":(plus-minus)/n,
                "bonferroni_cp_simultaneous_95":interval,
                "conservative_classification":classify(interval),
                "original_bootstrap_practical_equivalence_may_undercover":True,
            })
    if len(result)!=16:
        raise AssertionError("missing any original source cell")
    return {
        "status":STATUS,
        "source_receipt_sha256":hashlib.sha256(raw).hexdigest(),
        "source_raw_artifact_sha256":d["raw_json_sha256"],
        "original_source_commit":d["executed_source_commit"],
        "independent_model_visitor_histories":64,
        "ecologically_independent_natural_island_systems":0,
        "method":"95% Bonferroni-combined marginal exact Clopper-Pearson CIs of paired plus-only and minus-only visitor-history Bernoulli proportions; interval arithmetic gives conservative CI for their difference.",
        "classification_uses_probability_points_ROPE":0.05,
        "claim_boundary":"POST-OUTCOME uncertainty sensitivity, original precommitted paired percentile bootstrap retained but not reliable for declaring zero-effect equivalence at structural occupancy floors and ceilings.",
        "results":result,
        "by_horizon":{
            str(h):{
                v:sum(r["conservative_classification"]==v and r["horizon"]==h for r in result)
                for v in ("resolved_positive","resolved_negative",
                          "practically_equivalent","inconclusive")
            } for h in (20,80)
        },
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],
        "by_horizon":result["by_horizon"],
        "all_results":[{
            "K":r["K"],"assurance":r["assurance"],"gate":r["gate"],
            "horizon":r["horizon"],"delta":r["delta_plus_minus"],
            "ci":r["bonferroni_cp_simultaneous_95"],
            "verdict":r["conservative_classification"]
        } for r in result["results"]]
    },sort_keys=True))


if __name__=="__main__":
    main()
