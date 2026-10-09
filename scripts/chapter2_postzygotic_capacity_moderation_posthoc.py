"""Post-outcome paired stress-regime moderation after full viability-factorial success.

Reauthenticate all 2048 original diploid states, 57344 original futures,
and 172032 perturbed futures BEFORE reading intervention outcomes.
Tests compare two co-varying stress REGIMES (founders AND carrying capacity);
they do not identify capacity alone or natural reproductive mediation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_postzygotic_factorial_readout import audit_all
from scripts.plan_chapter2_order_expression_identification import log_budget_weights

BOOTSTRAP_DRAWS=9999
BOOTSTRAP_SEED=2026100941
LABELS=("unbottlenecked_capacity48","eight_founders_capacity8")
GATES=("baseline","attenuate_self","attenuate_outcross","attenuate_both")


def history_level_order_effects(d:dict,occupancy:np.ndarray) -> np.ndarray:
    """Output [visitor history 64, two regimes, four viability gates]."""
    z=np.asarray(occupancy,dtype=float)
    if z.shape!=(64,4,2,2,2,7,2,2,4) or not np.isfinite(z).all():
        raise ValueError("Require all paired 64 histories and complete future grid")
    if np.any((z<0)|(z>1)):
        raise ValueError("Invalid occupancy outcome")
    w=log_budget_weights(d)
    weights=np.array([w[float(b)] for b in d["postshock"]["budgets"]])
    # Average nested demographic replicates and future visitor environments.
    means=z.mean(axis=(4,6))
    # [64 histories, four settings, two near/far, two orders, seven budgets, two regimes, four gates].
    if means.shape!=(64,4,2,2,7,2,4):
        raise AssertionError("Invalid axis pairing")
    pooled=np.tensordot(means,weights,axes=([4],[0]))
    # [64,4,2,2,2,4]: randomized schedule A-first minus I-first.
    assigned=pooled[:,:,:,0,:,:]-pooled[:,:,:,1,:,:]
    return assigned.mean(axis=(1,2))


def summarize_history_effects(v:np.ndarray,draws:int=BOOTSTRAP_DRAWS,
                              seed:int=BOOTSTRAP_SEED) -> dict:
    a=np.asarray(v,dtype=float)
    if a.shape!=(64,2,4) or not np.isfinite(a).all():
        raise ValueError("Cannot bootstrap branches or condition on survivor")
    indices=np.random.default_rng(seed).integers(0,64,size=(draws,64))
    def est(h):
        if h.shape!=(64,):
            raise ValueError("One outcome per visitor history required")
        low,high=np.percentile(h[indices].mean(axis=1),[2.5,97.5])
        return {
            "mean":float(h.mean()),
            "history_bootstrap95":[float(low),float(high)],
            "positive_histories":int(np.sum(h>1e-12)),
            "negative_histories":int(np.sum(h< -1e-12)),
            "zero_histories":int(np.sum(abs(h)<=1e-12)),
        }
    tau={}
    for i,regime in enumerate(LABELS):
        v0,vself,vout,vmix=(a[:,i,j] for j in range(4))
        tau[regime]={
            "baseline_assignment_effect":est(v0),
            "half_self_assignment_effect":est(vself),
            "self_viability_sensitivity":est(v0-vself),
            "outcross_viability_sensitivity":est(v0-vout),
            "factorial_nonadditivity":est(v0-vself-vout+vmix),
        }
    cap48=a[:,0,0]-a[:,0,1]
    cap8=a[:,1,0]-a[:,1,1]
    comparison=est(cap8-cap48)
    return {
        "status":"POST_OUTCOME_PAIRED_STRESS_REGIME_MODERATION_NOT_CONFIRMATORY",
        "source_run":37869990792,
        "source_sha":"9f69db754ede497b012f4e7dcba5d2aaae9c090a",
        "n_authenticated_t400_sources":2048,
        "n_authenticated_original_future_cells":57344,
        "n_authenticated_new_future_cells":172032,
        "n_history_clusters":64,
        "bootstrap":{"seed":seed,"draws":draws,"unit":"paired_visitor_history"},
        "by_regime":tau,
        "cap8_minus_cap48_self_viability_sensitivity":comparison,
        "interpretation_limits":[
            "Selected after observing main capacity8 positive result and capacity48 negative result; no prospective confirmation.",
            "The paired stress contrast compares EIGHT founding individuals plus capacity8 against unbottlenecked capacity48; founders and capacity co-vary.",
            "This is a causal contrast of deliberately assigned synthetic seed viability treatments within each frozen regime, not natural genetic mediation.",
            "A nonzero difference between two synthetic stress regimes does not identify a natural-island extinction threshold.",
            "Prior registered full-grid DID practical equivalence and failed 3/4-budget localization remain unchanged.",
            "All inferential units are 64 previously outcome-exposed visitor histories, not 229376 independent futures.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory",type=Path,required=True)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--perturbed",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    d,grid=audit_all(a.prehistory,a.baseline,a.perturbed)
    v=history_level_order_effects(d,grid["occupied"])
    result=summarize_history_effects(v)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "stress_regime_modulation":result["cap8_minus_cap48_self_viability_sensitivity"],
    },ensure_ascii=False))


if __name__=="__main__":
    main()
