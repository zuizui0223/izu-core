"""Family-wise 12-contrast interval audit for source-replayed t20 transplants.

These exact Clopper-Pearson/Bonnferroni intervals are a POST-OUTCOME
multiplicity sensitivity, not a prospective new hypothesis test. The 12
paired comparisons share the same 50 eligible ecological model histories,
so an additional family-wise union bound controls simultaneous coverage
without treating correlated arm labels as independent samples.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import (
    cp_bernoulli,classify,
)

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"data/results/chapter2_t20_joint_genome_transplant_receipt_20261010.json"
STATUS="POST_OUTCOME_TRANSPLANT_12_CONTRAST_FAMILYWISE_SENSITIVITY"


def familywise_interval(positive_only,negative_only,n,family_size):
    if (type(family_size) is not int or family_size<1
            or type(n) is not int or n<1
            or type(positive_only) is not int or type(negative_only) is not int
            or min(positive_only,negative_only)<0
            or positive_only+negative_only>n):
        raise ValueError("invalid paired family inputs")
    # Per marginal binomial probability interval alpha = 0.05/(2*M).
    # Union of 2*M errors <= .05, even when contrasts share histories.
    adjusted=.05/(2*family_size)
    pos=cp_bernoulli(positive_only,n,adjusted)
    neg=cp_bernoulli(negative_only,n,adjusted)
    return [float(pos[0]-neg[1]),float(pos[1]-neg[0])]


def audit():
    b=RECEIPT.read_bytes()
    d=json.loads(b)
    if (d["status"]!="POST_OUTCOME_REPLAY_EXPOSED_HISTORIES_COMPLETE_50_ELIGIBLE_NO_INDEPENDENT_CONFIRMATION"
            or d["raw_json_sha256"]!="1c15f1921817f573662615343623e3890c5dce99413484fdd41bb4c07ab52eaf"
            or d["common_t20_alive"]!=50
            or len(d["paired_contrasts"])!=12):
        raise ValueError("source-locked transplant receipt changed")
    out=[]
    for contrast in d["paired_contrasts"]:
        n=50
        if (contrast["s"]-contrast["n"]!=contrast["sp"]-contrast["np"]
                or abs((contrast["s"]-contrast["n"])/n-contrast["d"])>1e-12):
            raise AssertionError("stored source-matched paired discordance inconsistent")
        ci=familywise_interval(contrast["sp"],contrast["np"],n,12)
        exact_single=contrast["ci"]
        if ci[0]>exact_single[0]+1e-12 or ci[1]<exact_single[1]-1e-12:
            raise AssertionError("familywise CI cannot be narrower than original")
        out.append({
            "effect":contrast["kind"],
            "K":contrast.get("K"),
            "donor":contrast.get("G"),
            "future":contrast.get("future"),
            "n_joint_t20_survivor_histories":n,
            "paired_selected_vs_alternative_count":[contrast["s"],contrast["n"]],
            "difference":contrast["d"],
            "single_comparison_conservative95":exact_single,
            "familywise_12_contrast_conservative95":ci,
            "familywise_direction_relative_to_zero":(
                "positive" if ci[0]>0 else "negative" if ci[1]<0 else "uncertain"
            ),
            "familywise_ROPE_5pp_verdict":classify(ci),
            "none_are_independently_preregistered_new_ecological_results":True,
        })
    primary=next(x for x in out if x["effect"]=="genome_origin"
                 and x["K"]==48 and x["future"]=="selected")
    secondary=next(x for x in out if x["effect"]=="genome_origin"
                   and x["K"]==8 and x["future"]=="selected")
    return {
        "status":STATUS,
        "source_receipt_sha256":hashlib.sha256(b).hexdigest(),
        "source_raw_json_sha256":d["raw_json_sha256"],
        "n_comparisons":12,
        "n_common_eligible_exposed_model_visitor_histories":50,
        "primary_K48_genome_effect_verdict":primary["familywise_ROPE_5pp_verdict"],
        "posthoc_K8_genome_effect_verdict":secondary["familywise_ROPE_5pp_verdict"],
        "n_resolved_positive_effects_above_5pp_familywise":sum(
            x["familywise_ROPE_5pp_verdict"]=="resolved_positive" for x in out
        ),
        "n_inconclusive_effects_familywise":sum(
            x["familywise_ROPE_5pp_verdict"]=="inconclusive" for x in out
        ),
        "contrasts":out,
        "inference_limit":"All outcomes reused a previously exposed stochastic Model3 ecology cohort and exclude t20 sources where either donor arm was extinct. This is conditional genomic-distribution intervention, not independent confirmation or a unique fitness/selection/drift decomposition."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    data=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":data["status"],"n":data["n_comparisons"],
        "primary_K48":data["primary_K48_genome_effect_verdict"],
        "secondary_K8":data["posthoc_K8_genome_effect_verdict"],
        "familywise_positive_above_5pp":data["n_resolved_positive_effects_above_5pp_familywise"],
        "familywise_inconclusive":data["n_inconclusive_effects_familywise"],
        "contrasts":data["contrasts"],
    },sort_keys=True))


if __name__=="__main__":
    main()
