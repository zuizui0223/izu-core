"""Post-outcome exploratory ablation of Gaussian genotype projection.

This decomposes the already-discovered genotype richness overestimate into:
(A) Gaussian shock + clip/renormalize (before integerization), and
(B) deterministic largest-remainder rounding versus a *conditional
multinomial readout* of the projected real-valued probabilities.

The alternative readout is NOT a proposed replacement for Model 3, does
not fix the stochastic process, and is not an independent confirmation.
Original source biology and prior results are unchanged.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scripts.audit_model3_gaussian_presence_bias import (
    exact_child_genotype_law,exact_expected_richness,
)

def dissect_projection(*,capacity:int=8,draws:int=8192,seed:int=20261009)->dict:
    if capacity not in (8,32,128) or type(draws) is not int or not 2048<=draws<=65536:
        raise ValueError("restricted exploratory diagnostic")
    q=exact_child_genotype_law(capacity=capacity,ovule_budget=8.)
    expected=exact_expected_richness(q,capacity)["expected_n_genotype_classes"]
    rng=np.random.default_rng(seed+capacity+25000)
    deterministic_richness=[]
    conditional_multinomial_richness=[]
    clipped_mass=[]
    n_negative=[]
    normalized_weight_rms=[]
    for _ in range(draws):
        raw=np.sqrt(capacity*q)*rng.standard_normal(len(q))
        shock=raw-q*raw.sum()
        counts=capacity*q+shock
        negative=np.minimum(counts,0.)
        n_negative.append(int((counts<0).sum()))
        clipped_mass.append(float(-negative.sum()))
        positive=np.maximum(counts,0.)
        if not positive.sum()>0:
            raise ArithmeticError("Gaussian draw projects to empty simplex")
        p=positive/positive.sum()
        normalized_weight_rms.append(
            float(np.sqrt(np.mean((p-q)**2)))
        )
        target=capacity*p
        floored=np.floor(target).astype(int)
        residual=capacity-int(floored.sum())
        if not 0<=residual<len(q):
            raise ArithmeticError("invalid integer rounding")
        if residual:
            order=np.argsort(-(target-floored),kind="stable")
            floored[order[:residual]]+=1
        if int(floored.sum())!=capacity:
            raise ArithmeticError("projected census not conserved")
        deterministic_richness.append(int(np.count_nonzero(floored)))
        # Given the SAME clipped/renormalized real probabilities,
        # calculate class richness under multinomial integerization
        # exactly, without another Monte Carlo layer.
        expected_class_presence=-np.expm1(capacity*np.log1p(-p))
        conditional_multinomial_richness.append(
            float(expected_class_presence.sum())
        )
    integer_richness=np.asarray(deterministic_richness,dtype=float)
    stochastic_readout=np.asarray(conditional_multinomial_richness,dtype=float)
    delta=integer_richness-stochastic_readout
    return {
        "status":"POST_OUTCOME_EXPLORATORY_GAUSSIAN_PROJECTION_MECHANISM",
        "K":capacity,
        "draws":draws,
        "exact_multinomial_expected_richness":expected,
        "gaussian_clip_normalize_then_multinomial_expected_richness":
            float(stochastic_readout.mean()),
        "gaussian_clip_normalize_then_largest_remainder_richness":
            float(integer_richness.mean()),
        "bias_from_gaussian_clip_normalize_before_rounding":
            float(stochastic_readout.mean()-expected),
        "additional_richness_shift_due_to_deterministic_integer_rounding":
            float(delta.mean()),
        "total_largest_remainder_minus_exact":
            float(integer_richness.mean()-expected),
        "se_total_largest_remainder":
            float(integer_richness.std(ddof=1)/np.sqrt(draws)),
        "se_paired_rounding_effect":
            float(delta.std(ddof=1)/np.sqrt(draws)),
        "fraction_gaussian_draws_with_any_negative_genotype_count":
            float(np.mean(np.asarray(n_negative)>0)),
        "mean_number_negative_preprojection_genotype_counts":
            float(np.mean(n_negative)),
        "mean_clipped_negative_mass":
            float(np.mean(clipped_mass)),
        "mean_normalized_weight_rmse_against_canonical_q":
            float(np.mean(normalized_weight_rms)),
        "biology_unmodified":True,
        "full_SDE_SPDE_validated":False,
        "post_outcome_exploratory":True,
        "no_INLA_geographic":True,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--draws",type=int,default=8192)
    args=p.parse_args()
    cases=[dissect_projection(capacity=k,draws=args.draws) for k in (8,32,128)]
    doc={"schema":"model3_gaussian_projection_mechanism_20261009_v1",
         "status":"post_outcome_exploratory_numerical_diagnostic",
         "cases":cases}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(doc,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":doc["status"],
        "cases":[{"K":r["K"],
                  "exact":r["exact_multinomial_expected_richness"],
                  "pre_rounding_richness":r["gaussian_clip_normalize_then_multinomial_expected_richness"],
                  "post_rounding_richness":r["gaussian_clip_normalize_then_largest_remainder_richness"],
                  "noise_clip_shift":r["bias_from_gaussian_clip_normalize_before_rounding"],
                  "rounding_shift":r["additional_richness_shift_due_to_deterministic_integer_rounding"],
                  "negative_draw_fraction":r["fraction_gaussian_draws_with_any_negative_genotype_count"]}
                 for r in cases],
    }))

if __name__=="__main__":
    main()
