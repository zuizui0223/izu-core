"""Exact original Model3 one-generation Price identity: Q1 genetic returns → Q3 mean.

A deterministic conservation/identifiability audit, not a demonstration that
Q1 sign predicts 80-year evolutionary trajectories or survival. Source F/P/S
and original Mendelian paternal/maternal lottery are unmodified. Adult survival,
mutation and seed immigration are zero; the offspring mean is defined only if
at least one recruit exists.

The density/visitor/trait grid is previously exposed synthetic Model3 biology,
NOT a new independent ecological experiment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import poisson

from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import source
from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import (
    config, visitors
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.audit_chapter2_q3_recruitment_genetic_moments import (
    plants, one_generation_moments
)

STATUS = "EXACT_ORIGINAL_SOURCE_Q1_TO_Q3_PRICE_IDENTITY_NOT_LONGRUN_SELECTION"
# Both genetically monomorphic and polymorphic source census conditions;
# no outcome-conditioned selection of favorable source states.
SOURCE_COUNTS = (
    (0,8,0), (8,0,0), (0,0,8), (2,4,2),
    (5,2,1), (1,2,5), (1,2,1), (2,3,2)
)
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
BUDGETS = (6.,8.)
VISITOR_FRACTIONS = (0., .5, 1.)
B = 48


def genetic_price_audit(genome, setting: str, budget: float, fraction: float):
    n = len(genome.ids)
    if n < 1 or n > 8 or genome.mutation_flags.any():
        raise ValueError("nonempty source no-mutation diploid census N1..8 required")
    if setting not in SETTINGS or budget not in BUDGETS or fraction not in VISITOR_FRACTIONS:
        raise ValueError("source ecological condition is not in the disclosed grid")
    ledger = reproduce_kb(
        genome, visitors(fraction), config(setting,budget),
        background_denominator_capacity=B,
    )
    maternal = ledger.outcross.sum(axis=0)  # column j: viable maternal outcross
    paternal = ledger.outcross.sum(axis=1)  # row i: viable paternal outcross
    selfed = ledger.self_viable
    W = .5*(maternal+paternal)+selfed
    total_seed_mu=float(ledger.outcross.sum()+selfed.sum())
    if not np.isclose(W.sum(),total_seed_mu,atol=1e-11,rtol=0) or total_seed_mu <= 0:
        raise AssertionError("F/P/S full genetic parental return not conserved")
    p=ledger.outcross.copy()
    np.fill_diagonal(p,np.diag(p)+selfed)
    p/=total_seed_mu
    if not np.isclose(p.sum(),1,atol=1e-12,rtol=0):
        raise ArithmeticError("source independent parent-pair lottery not normalized")
    g=genome.alleles[:,1,:].mean(axis=1)
    adult_mean=float(g.mean())
    from_parent_pairs=float(
        (p*((g[:,None]+g[None,:])*.5)).sum()
    )
    from_full_genetic_W=float(np.dot(W,g)/total_seed_mu)
    cov=float(np.mean((g-adult_mean)*(W-W.mean())))
    covariance_shift=float(cov/W.mean())
    direct_shift=from_parent_pairs-adult_mean
    if not np.isclose(
        from_parent_pairs,from_full_genetic_W,atol=1e-12,rtol=0
    ) or not np.isclose(
        direct_shift,covariance_shift,atol=1e-12,rtol=0
    ):
        raise AssertionError("full-parent genetic Price identity failed")
    if not np.isclose(maternal.sum(),paternal.sum(),atol=1e-12,rtol=0):
        raise ArithmeticError("paternal and maternal outcross counts disagree")
    # Exact only in the source zero-adult-survival, no-immigrant recruitment
    # operator: the event of at least one offspring ignores demographic K>=1.
    occupied_next=float(-np.expm1(-total_seed_mu))
    if not 0 < occupied_next <= 1:
        raise AssertionError("conditional genetic mean has no valid source occupancy")
    p_recruits=np.r_[poisson.pmf(np.arange(8),total_seed_mu),
                      poisson.sf(7,total_seed_mu)]
    expected_recruits=float(np.dot(np.arange(9),p_recruits))
    variance=float(np.var(g))
    return {
        "current_N":n,
        "source_viable_seed_mu":total_seed_mu,
        "P_next_occupied":occupied_next,
        "founder_mean_investment":adult_mean,
        "founder_genotypic_variance":variance,
        "expected_next_genetic_mean_if_occupied":from_parent_pairs,
        "expected_investment_shift_if_occupied":direct_shift,
        "price_cov_genotype_full_W":cov,
        "price_shift_cov_over_mean_W":covariance_shift,
        "full_genetic_parental_return_W":W.tolist(),
        "maternal_outcross_F":maternal.tolist(),
        "paternal_outcross_P":paternal.tolist(),
        "viable_selfed_S":selfed.tolist(),
        "genotypic_parent_means":g.tolist(),
        "expected_unconditional_allele_copy_sum_if_K8":float(2*expected_recruits*from_parent_pairs),
    }


def audit():
    records=[]
    for counts in SOURCE_COUNTS:
        genome=source(counts)
        for setting in SETTINGS:
            for budget in BUDGETS:
                for fraction in VISITOR_FRACTIONS:
                    a=genetic_price_audit(genome,setting,budget,fraction)
                    records.append({
                        "source_genotype_counts":list(counts),
                        "mating_rule":setting,"resource_budget":budget,
                        "four_visitor_functional_replacement":fraction,
                        "result":a,
                    })
    # Cross-check against independently merged exact recruit-count/Mendelian
    # one-generation Q3 contract for the transparently variable eight-adult fixture.
    gradient=np.array([.20,.25,.30,.35,.40,.45,.50,.55])
    diverse=plants(np.stack((gradient-.02,gradient+.02),axis=1))
    direct=genetic_price_audit(diverse,"delayed_control",6.,0.)
    established=one_generation_moments(diverse,8)["results_by_trait"]["investment"]
    if not np.isclose(direct["expected_investment_shift_if_occupied"],
                      established["expected_child_mean_shift_conditional_on_occupancy"],
                      atol=1e-12,rtol=0):
        raise AssertionError("separate Q3 original source moment no longer agrees")
    sign_counts={
        key:sum(
            (row["result"]["expected_investment_shift_if_occupied"]>1e-12 if key=="positive"
             else row["result"]["expected_investment_shift_if_occupied"]< -1e-12 if key=="negative"
             else abs(row["result"]["expected_investment_shift_if_occupied"])<=1e-12)
            for row in records)
        for key in ("positive","negative","numerically_zero")
    }
    return {
        "schema":"chapter2_q1q3_full_W_price_identity_source_v1",
        "status":STATUS,
        "formula":"E[child investment mean | next N>0]-parent mean = Cov(parent investment mean_i, S_i+0.5*F_i+0.5*P_i) / mean(S+0.5F+0.5P)",
        "n_genotype_source_compositions":len(SOURCE_COUNTS),
        "n_original_mating_rules":len(SETTINGS),
        "n_resource_budgets":len(BUDGETS),
        "n_fixed_richness_functional_assemblages":len(VISITOR_FRACTIONS),
        "n_source_evaluations":len(records),
        "sign_count_is_model_state_count_not_ecological_replication":sign_counts,
        "independent_visitor_histories":0,
        "independent_natural_islands":0,
        "new_evolutionary_trajectories":0,
        "diverse_original_q3_contract_investment":direct,
        "limitations":[
            "This Price identity is standard algebra, NOT a newly discovered adaptive biological effect.",
            "It does not equate a finite one-focal mutant marginal beta gradient with a standing-genetic-covariance response.",
            "The expected genetic mean is conditional on next N>0, and extinct populations' mean allele trait is undefined rather than zero.",
            "Exact one-generation expectation does not identify realized 80-update allele trajectories or a Q3-to-Q4 natural survival mediator.",
            "Genetic sources, visitor optima, and budgets are fixed exploratory synthetic model states; evaluated states are NOT independently sampled islands.",
        ],
        "results":records,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    results=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(results,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":results["status"],
        "source_states":results["n_source_evaluations"],
        "sign_counts":results["sign_count_is_model_state_count_not_ecological_replication"],
        "reference_Q3_expected_shift":results["diverse_original_q3_contract_investment"]["expected_investment_shift_if_occupied"]
    },sort_keys=True))


if __name__=="__main__":
    main()
