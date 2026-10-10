"""Exact one-generation inherited trait moments under original Model 3 recruitment.

A closed-form Q1→Q3 bridge for frozen diploid parents and original F/P/S ledger,
with the original Poisson founder lottery and demographic K truncation integrated
rather than conditioning on a convenient fixed number of offspring.

This is a post-discovery, deterministic source-operator check, NOT a new visitor
history, trial, long-horizon fitness/selection estimate, or genetic mediation.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import poisson

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_TRAITS = (.2, .35, .35)
VISITOR_OPTIMA = (.15, .35, .55, .75)
CAPACITIES = (8, 48)
B = 48
BUDGET = 6.
STATUS = "EXACT_ONE_STEP_Q3_GENETIC_LOTTERY_POST_DISCOVERY_NOT_MEDIATION"


def plants(investment_alleles) -> PlantState:
    g = np.asarray(investment_alleles, dtype=float)
    if g.ndim != 2 or g.shape != (8, 2) or not np.isfinite(g).all() or (g < 0).any() or (g > 1).any():
        raise ValueError("exactly eight bounded diploid investment genotypes required")
    alleles = np.empty((8, 3, 2), dtype=float)
    alleles[:, 0, :] = SOURCE_TRAITS[0]
    alleles[:, 1, :] = g
    alleles[:, 2, :] = SOURCE_TRAITS[2]
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(8 * 3 * 2, dtype=np.int64).reshape(8, 3, 2),
        mutation_flags=np.zeros((8, 3, 2), dtype=bool),
        ids=np.arange(8, dtype=np.int64),
        birth_years=np.zeros(8, dtype=np.int64)
    )


def visitors() -> VisitorState:
    return VisitorState(
        ids=np.arange(4, dtype=np.int64),
        optima=np.array(VISITOR_OPTIMA),
        breadths=np.full(4, .18),
        effectiveness=np.ones(4)
    )


def config(k: int):
    if k not in CAPACITIES:
        raise ValueError("K outside the previously exposed 8/48 capacity grid")
    base = source_config(load_design(DEFAULT_DESIGN), "delayed_control", 0.0, "evolving")
    return replace(
        base, capacity=k, ovule_budget=BUDGET,
        mutation_rate=0., mutation_sd=0., survival=0.,
        seed_arrival=replace(base.seed_arrival, supply=0.)
    )


def offspring_count_probabilities(mu: float, k: int):
    """Exact probabilities of R=min(Poisson(mu),K) for r=0..K."""
    if k not in CAPACITIES or not np.isfinite(mu) or mu < 0:
        raise ValueError("invalid original source recruitment intensity or cap")
    result = np.zeros(k + 1)
    result[:k] = poisson.pmf(np.arange(k), mu)
    result[k] = poisson.sf(k - 1, mu)
    if not np.isclose(result.sum(), 1., rtol=0, atol=1e-12):
        raise ArithmeticError("offspring count mass incomplete")
    return result


def one_generation_moments(state: PlantState, k: int) -> dict:
    """Integrate original donor×recipient parent-pair and Mendelian lotteries.

    Population.advance samples an independent parental pair for each retained
    recruit proportional to the original F/P/S matrix; parent-pair weights do
    not depend on the Poisson potential count nor on the retained cap R.
    Given R=r>0 each offspring has the same conditional first two trait moments,
    so Var(mean inherited trait | R=r) = Var(single inherited offspring)/r.

    At R=0 mean trait is MISSING, not zero. The survival-conditioned mean and
    variance marginalize R=1..K under the real source Poisson recruitment law.
    """
    if len(state.ids) != 8 or k < len(state.ids) or k not in CAPACITIES:
        raise ValueError("wrong eight-founder source or K")
    if not np.all(state.mutation_flags == 0):
        raise ValueError("post-mutational source not supported")
    cfg = config(k)
    ledger = reproduce_kb(state, visitors(), cfg, background_denominator_capacity=B)
    pairs = ledger.outcross.copy()
    pairs[np.diag_indices(len(state.ids))] += ledger.self_viable
    total = float(pairs.sum())
    if not total > 0 or not np.isfinite(total):
        raise ValueError("invalid parental return distribution")
    w = pairs / total
    if not np.isclose(w.sum(), 1, atol=1e-12, rtol=0):
        raise ArithmeticError("parent-pair mass incomplete")
    rdist = offspring_count_probabilities(total, k)
    p_survive = float(1-rdist[0])
    if not p_survive > 0:
        raise ValueError("no recruited offspring")
    expected_R = float(np.dot(np.arange(k+1), rdist))
    E_inverse_R_given_alive = float(
        np.dot(1/np.arange(1, k+1), rdist[1:]) / p_survive
    )
    traits = {}
    for trait, name in enumerate(("matching", "investment", "assurance")):
        # Rows are FATHERS, columns are MOTHERS in Model 3.
        dip = state.alleles[:, trait, :]
        adult_means = dip.mean(axis=1)
        pair_E = (adult_means[:, None] + adult_means[None, :]) / 2
        newborn_E = float(np.sum(w * pair_E))
        parent_lottery = float(np.sum(w * (pair_E-newborn_E)**2))
        diffs = dip[:, 0]-dip[:, 1]
        # Original inherit randomly chooses one of two homologs from each
        # parent; newborn phenotype is mean of two transmitted homologs.
        pair_segregation = (diffs[:, None]**2 + diffs[None, :]**2)/16
        mendelian = float(np.sum(w * pair_segregation))
        one_child_var = parent_lottery+mendelian
        inherited_mean_var_given_alive = one_child_var * E_inverse_R_given_alive
        traits[name] = {
            "founder_mean": float(dip.mean()),
            "expected_child_mean_conditional_on_occupancy": newborn_E,
            "expected_child_mean_shift_conditional_on_occupancy": newborn_E-float(dip.mean()),
            "parent_pair_lottery_single_child_variance": parent_lottery,
            "mendelian_single_child_variance": mendelian,
            "single_child_variance": one_child_var,
            "mean_trait_variance_conditional_on_occupancy": inherited_mean_var_given_alive,
            "mean_trait_sd_conditional_on_occupancy": float(np.sqrt(inherited_mean_var_given_alive)),
            "unconditional_next_allele_copy_trait_sum": 2*expected_R*newborn_E
        }
    return {
        "K": k, "pollen_background_B": B, "ovule_budget": BUDGET,
        "original_source_viable_seed_mean": total,
        "P_next_occupied": p_survive,
        "E_next_census": expected_R,
        "E_inverse_recruits_given_occupied": E_inverse_R_given_alive,
        "original_parent_selfing_share_by_expected_viable_seeds": (
            float(ledger.self_viable.sum()/total)
        ),
        "results_by_trait": traits,
        "independent_genetic_histories": 0
    }


def run_all() -> dict:
    homo = plants(np.full((8,2), .35))
    hetero = plants(np.tile(np.array([.2,.5]), (8,1)))
    # Balanced source-selected gradient fixture; these are transparent,
    # deterministic previously discussed artificial value ranges, NOT real
    # evolving genomes from #411.
    variable_means = np.array([.20,.25,.30,.35,.40,.45,.50,.55])
    diverse = plants(np.stack((variable_means-.02, variable_means+.02), axis=1))
    scenarios = {
        "homozygous_same_phenotype": homo,
        "heterozygous_same_phenotype": hetero,
        "segregating_investment_gradient": diverse,
    }
    results = []
    for label, state in scenarios.items():
        records = [one_generation_moments(state,k) for k in CAPACITIES]
        a,b=records
        # Same eight parental phenotypes and same B=48 => identical reproduction
        # and first-year occupancy, different retained recruit K distributions.
        if not np.isclose(a["original_source_viable_seed_mean"],
                          b["original_source_viable_seed_mean"], atol=1e-11, rtol=0):
            raise AssertionError("K changed the fixed B=48 source reproduction")
        if not np.isclose(a["P_next_occupied"],b["P_next_occupied"], atol=1e-11, rtol=0):
            raise AssertionError("K directly changed one-step occupancy at fixed mu")
        if not (a["E_next_census"] < b["E_next_census"] and
                a["E_inverse_recruits_given_occupied"] >= b["E_inverse_recruits_given_occupied"]):
            raise AssertionError("capacity did not alter the full recruitment lottery")
        results.append({"fixture": label, "by_capacity": records})
    for trait in ("matching","investment","assurance"):
        for z in results[0]["by_capacity"]:
            if z["results_by_trait"][trait]["single_child_variance"] > 1e-15:
                raise AssertionError("homozygote clonal genotype variance nonzero")
    for z in results[1]["by_capacity"]:
        q=z["results_by_trait"]["investment"]
        if not (q["parent_pair_lottery_single_child_variance"] < 1e-15
                and q["mendelian_single_child_variance"] > 0):
            raise AssertionError("hidden heterozygosity is not separated from parent lottery")
    for z in results[2]["by_capacity"]:
        q=z["results_by_trait"]["investment"]
        if not (q["parent_pair_lottery_single_child_variance"] > 0
                and q["mendelian_single_child_variance"] > 0):
            raise AssertionError("genotypic source variation terms not identified")
    return {
        "schema": "chapter2_q3_unconditional_recruitment_genetic_moments_v1",
        "status": STATUS,
        "experimental_status": "POST_DISCOVERY_DETERMINISTIC_SOURCE_FIXTURE_ONLY",
        "original_biology": "original Model3 reproduce_kb and population.advance parent-pair/Mendelian rules",
        "assumptions": {
            "source_population_N":8, "adult_survival":0, "seed_immigration":0,
            "mutation":0,"visitor_functional_types_fixed":4,
            "background_pollen_B":B,"resource_budget":BUDGET,
            "next_census":"min(Poisson(total viable maternal seeds),K)",
            "trait_mean_if_extinct":"MISSING",
            "offspring_pair_lottery":"independent conditional on positive retained R"
        },
        "n_new_visitor_histories":0,
        "n_new_evolutionary_trajectories":0,
        "n_new_stochastic_demographic_paths":0,
        "results":results,
        "scientific_boundary": (
            "Exact first-generation moments for static synthetic sources; mean "
            "inherited shift and variance do not identify realized long-run adaptation, "
            "change in population occupancy from selection, or natural island extinction."
        )
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([
        {"fixture":x["fixture"],
         "K":y["K"],
         "P_next_occupied":y["P_next_occupied"],
         "investment":y["results_by_trait"]["investment"]}
        for x in result["results"] for y in x["by_capacity"]
    ],sort_keys=True))


if __name__=="__main__":
    main()
