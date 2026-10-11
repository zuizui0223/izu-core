"""Audit uncertainty in K32 eight-generation three-arm OLD-history receipts.

The sample count is nested demographic replicates from ONE archived visitor
history, never independent ecological histories. Normal intervals quantify
Monte Carlo precision of means, not biological confidence or model adequacy.
For extinction use Wilson bounds and a conservative two-sample difference
interval rather than falsely reporting [0,0] when no extinctions are drawn.
"""
from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path

Z95 = 1.959963984540054
EXPECTED_HISTORY = 26110601


def _finite(x):
    import math
    return isinstance(x, (int, float)) and math.isfinite(x)


def wilson_interval(k: int, n: int, z: float = Z95):
    """Two-sided Wilson score interval for a binomial success probability."""
    if type(n) is not int or n <= 0 or type(k) is not int or not 0 <= k <= n:
        raise ValueError("invalid binomial count")
    p = k / n
    den = 1. + z*z/n
    middle = (p + z*z/(2*n))/den
    delta = z * sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return [max(0., middle-delta), min(1., middle+delta)]


def _mean_contrast(a, b, key, sekey):
    x, y = float(a[key]), float(b[key])
    sx, sy = float(a[sekey]), float(b[sekey])
    if not all(_finite(k) for k in (x,y,sx,sy)) or min(sx,sy) < 0:
        raise ValueError("invalid Monte Carlo means / standard errors")
    d = y-x
    se = sqrt(sx*sx + sy*sy)
    return {
        "gaussian_minus_exact": d,
        "independent_ensemble_mc_se": se,
        "approximate_mc_95_interval": [d-Z95*se, d+Z95*se],
        "scope": "MC sampling precision conditional on one archived visitor history",
    }


def _binary_contrast(a, b, field):
    n = int(a["draws"])
    if n != int(b["draws"]):
        raise ValueError("unequal binary sampling denominators")
    ka = int(round(float(a[field])*n))
    kb = int(round(float(b[field])*n))
    if (abs(ka/n-float(a[field])) > 1e-12 or
        abs(kb/n-float(b[field])) > 1e-12):
        raise ValueError("reported frequency inconsistent with integer draws")
    aa, bb = wilson_interval(ka,n), wilson_interval(kb,n)
    # Conservative Wilson-component envelope; intentionally can be wider
    # than exact unconditional inference and must not be called a formal
    # exact 95% interval on the difference.
    return {
        "exact_events": ka, "gaussian_events": kb,
        "draws_per_arm": n,
        "exact_wilson_95": aa, "gaussian_wilson_95": bb,
        "gaussian_minus_exact": (kb-ka)/n,
        "conservative_wilson_difference_envelope": [bb[0]-aa[1],bb[1]-aa[0]],
        "scope": "conditional demographic MC only; conservative component envelope",
    }


def audit_one(data):
    c = data["conditions"]
    for key, expected in (
        ("capacity",32), ("mutation_rate",0),
        ("generations",8),("old_visitor_history",EXPECTED_HISTORY),
        ("independent_visitor_histories",1),
        ("new_visitor_histories_sampled",0),
        ("confirmatory_cohorts_accessed",False),
        ("reproductive_setting","prior_selfing"),
    ):
        if c[key] != expected:
            raise ValueError(f"unexpected source configuration: {key}")
    if data["canonical_biology_modified"] or "not_natural_island_observation" not in data["evidence_type"]:
        raise ValueError("unsafe biological or evidence provenance")
    arms=data["arms"]
    a=arms["exact_finite_Markov"]
    g=arms["projected_Gaussian"]
    if a["draws"]!=g["draws"] or a["draws"] < 16:
        raise ValueError("need at least 16 independent demographic repeats per arm")
    if a["max_conservation_error"] or g["max_conservation_error"]:
        raise ValueError("invalid exact integer mass audit")
    richness=_mean_contrast(a,g,"mean_genotype_classes","richness_monte_carlo_se")
    allele=_mean_contrast(a,g,"mean_allele_types_lost","allele_loss_monte_carlo_se")
    traits=[
        {
            "trait_index":i,
            "gaussian_minus_exact":g["trait_mean_given_occupied"][i]-a["trait_mean_given_occupied"][i],
            "independent_ensemble_mc_se":sqrt(
                g["trait_mean_se_given_occupied"][i]**2+
                a["trait_mean_se_given_occupied"][i]**2
            ),
        } for i in range(3)
    ] if min(a["n_occupied"],g["n_occupied"])>1 else None
    if traits is not None:
        for t in traits:
            x=t["gaussian_minus_exact"]
            se=t["independent_ensemble_mc_se"]
            t["approximate_mc_95_interval"]=[x-Z95*se,x+Z95*se]
    det=arms["deterministic_conditional_expectation"]
    return {
        "ovule_budget":c["ovule_budget"],
        "draws_per_stochastic_arm":a["draws"],
        "n_independent_visitor_histories":1,
        "genotype_richness_difference":richness,
        "allele_types_lost_difference":allele,
        "any_allele_loss":_binary_contrast(a,g,"probability_any_allele_lost"),
        "population_extinction":_binary_contrast(a,g,"probability_extinct"),
        "three_survivor_trait_means":traits,
        "deterministic_proxy": {
            "maximum_fractional_parent_projection_l1":det["max_projected_parent_l1"],
            "exact_markov_expectation_claimed":False,
            "probability_comparison_is_not_from_demographic_replicates":True,
        },
    }


def audit_both(normal, stressed):
    first=audit_one(normal)
    second=audit_one(stressed)
    if first["ovule_budget"]!=8 or second["ovule_budget"]!=3:
        raise ValueError("expected primary 8 and resource-stress 3 regimes")
    return {
        "status":"K32_MC_PRECISION_AUDIT_EXPLORATORY",
        "evidence_type":"simulation_MC_precision_not_field_inference",
        "n_independent_visitor_histories":1,
        "cases":[first,second],
        "interpretation":[
            "A zero-event 512-draw sample does NOT prove zero extinction probability.",
            "Approximate Gaussian-vs-exact intervals quantify independent nested demographic simulation error, not transfer between islands.",
            "Rare extinction comparisons are exploratory; use conservative Wilson component envelopes.",
            "No deterministic stochastic-process equivalence or continuous-time SDE/SPDE is established.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--standard",required=True,type=Path)
    p.add_argument("--stress",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    report=audit_both(json.loads(args.standard.read_text()),json.loads(args.stress.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":report["status"],
        "main_richness_interval":report["cases"][0]["genotype_richness_difference"]["approximate_mc_95_interval"],
        "stress_extinction_interval_envelope":report["cases"][1]["population_extinction"]["conservative_wilson_difference_envelope"],
    }))


if __name__=="__main__":
    main()
