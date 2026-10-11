"""One-generation Gaussian genotype projection bias relative to exact Mendelian sampling.

Instead of comparing two noisy finite ensembles, this audit computes the exact
expected genotype-class richness and per-class presence probabilities for
n fixed Mendelian offspring analytically, and Monte Carlo estimates ONLY
the projected Gaussian surrogate probabilities. This isolates systematic
projection+integer-rounding bias from between-arm demographic noise.

Each q is obtained from the unmodified canonical Model 3 reproduce()
and three-locus Mendelian gamete kernel at a fixed engineered parental
state. No new ecological visitor histories, mutation, or geographic INLA.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import (
    fixed_support_problem, gaussian_integer_offspring,
)
from scripts.audit_model3_stochastic_bridge import offspring_genotype_distribution, parent_pair_probabilities
from scripts.model3_island.reproduction import reproduce

CAPACITIES=(8,32,128)


def exact_child_genotype_law(*, capacity:int=8, ovule_budget:float=8.):
    counts,grid,visitors,config=fixed_support_problem(
        capacity=capacity,ovule_budget=ovule_budget
    )
    from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
    state=genotype_counts_to_canonical_state(counts,grid,year=0,
                                             capacity=config.capacity)
    ledger=reproduce(state,visitors,config)
    weights,_=parent_pair_probabilities(state,ledger,config)
    q=offspring_genotype_distribution(state,weights,grid)
    return q


def exact_expected_richness(q:np.ndarray,n:int)->dict:
    """Finite categorical sampling: genotype present with P=1-(1-q_g)^n."""
    q=np.asarray(q,dtype=float)
    if n<1 or (q<0).any() or not np.isclose(q.sum(),1,atol=1e-12):
        raise ValueError("invalid exact offspring law")
    probability_present=-np.expm1(n*np.log1p(-q))
    probability_absent=np.exp(n*np.log1p(-q))
    return {
        "expected_n_genotype_classes":float(probability_present.sum()),
        "probability_present":probability_present,
        "probability_absent":probability_absent,
    }


def projected_gaussian_presence_audit(
    *,capacity:int=8,ovule_budget:float=8.,draws:int=8192,seed:int=20261009
)->dict:
    if (capacity not in CAPACITIES or ovule_budget not in (3.,8.)
            or type(draws) is not int or not 2048<=draws<=65536
            or type(seed) is not int or seed<0):
        raise ValueError("unapproved numerical diagnostic")
    q=exact_child_genotype_law(capacity=capacity,ovule_budget=ovule_budget)
    exact=exact_expected_richness(q,capacity)
    rng=np.random.default_rng(seed+capacity)
    count_presence=np.zeros(len(q),dtype=np.int64)
    counts_sum=np.zeros(len(q),dtype=float)
    class_counts=np.empty(draws,dtype=np.int64)
    for i in range(draws):
        sample=gaussian_integer_offspring(q,capacity,rng)
        present=sample>0
        count_presence+=present
        counts_sum+=sample
        class_counts[i]=present.sum()

    projected_presence=count_presence/draws
    projected_richness=float(class_counts.mean())
    expected_exact=exact["expected_n_genotype_classes"]
    # The two stochastic draws are NOT compared: exact baseline has zero MC
    # error. This uncertainty is ONLY projected-Gaussian sampling error.
    se_richness=float(class_counts.std(ddof=1)/np.sqrt(draws))
    presence_se=np.sqrt(
        projected_presence*(1-projected_presence)/draws
    )
    systematic_presence_gap=projected_presence-exact["probability_present"]
    zscore=abs(projected_richness-expected_exact)/se_richness if se_richness>0 else None
    rare_positive=np.flatnonzero((q>0)&(capacity*q<1))
    positives_ignored=[
        {"class_index":int(k),
         "true_probability":float(q[k]),
         "exact_present_probability":float(exact["probability_present"][k]),
         "projected_present_probability":float(projected_presence[k])}
        for k in rare_positive if projected_presence[k]==0
    ]
    return {
        "status":"PROJECTED_GAUSSIAN_GENOTYPE_PRESENCE_FIDELITY_AUDIT",
        "capacity_and_conditioned_recruitment_n":capacity,
        "ovule_budget":ovule_budget,
        "genotype_classes":len(q),
        "positive_offspring_classes":int((q>0).sum()),
        "simulation_repeats_projected_only":draws,
        "original_biology_mutated":False,
        "full_spde_validated":False,
        "source":"canonical_Model3_reproduce_and_full_joint_Mendelian_inheritance",
        "exact_multinomial_expected_richness":expected_exact,
        "projected_gaussian_mean_richness":projected_richness,
        "projected_gaussian_mean_richness_mc_se":se_richness,
        "richness_difference_projected_minus_exact":
            float(projected_richness-expected_exact),
        "absolute_richness_difference_in_MC_standard_errors":(
            float(zscore) if zscore is not None else None
        ),
        "max_abs_genotype_presence_probability_difference":
            float(np.max(np.abs(systematic_presence_gap))),
        "max_presence_mc_se":float(np.max(presence_se)),
        "max_abs_expected_genotype_count_difference":
            float(np.max(np.abs(counts_sum/draws-capacity*q))),
        "n_exact_positive_genotype_classes_never_seen_under_projection":
            len(positives_ignored),
        "examples_exact_positive_but_projection_missing":positives_ignored[:8],
        "full_q":q.tolist(),
        "exact_class_presence_probabilities":exact["probability_present"].tolist(),
        "projected_class_presence_probabilities":projected_presence.tolist(),
        "interpretation_limits":[
            "Expected exact richness is analytical, not a second Monte Carlo estimate.",
            "Projected-Gaussian expectation is a finite seeded Monte Carlo estimate.",
            "Bias estimates describe clipping and integer rounding as well as Gaussian approximation.",
            "The observed finite N comparison is not a long-run mutation-enabled SPDE.",
            "Changing plant capacity changes the Model 3 pollen and fitness denominator.",
            "No natural island data or INLA analysis used.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--draws",type=int,default=8192)
    args=p.parse_args()
    rows=[projected_gaussian_presence_audit(
        capacity=k,ovule_budget=8.,draws=args.draws
    ) for k in CAPACITIES]
    report={
        "schema":"model3_projected_gaussian_one_step_richness_20261009_v1",
        "status":"numeric_boundary_audit_not_SPDE_admission",
        "cases":rows,
        "geographic_INLA_performed":False,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True,
                                   allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":report["status"],
        "richness":[{
            "K":r["capacity_and_conditioned_recruitment_n"],
            "exact":r["exact_multinomial_expected_richness"],
            "projected":r["projected_gaussian_mean_richness"],
            "bias":r["richness_difference_projected_minus_exact"],
            "mc_se":r["projected_gaussian_mean_richness_mc_se"],
            "largest_presence_gap":r["max_abs_genotype_presence_probability_difference"],
        } for r in rows],
    }))


if __name__=="__main__":
    main()
