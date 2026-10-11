"""Q3→Q4: exact genotype-census factorial using the NATIVE Model 3 reproductive ledger.

Disentangle the genotype-dependent total viable-seed intensity (mu) and
offspring-genotype parental lottery (q) as a 2x2 source-operator experiment.
No new stochastic population histories, mutations or model retuning. These
artificially recombined channels are NOT natural causal mediation effects.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json

import numpy as np
from scipy.stats import poisson, multinomial

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.audit_chapter2_exact_clonal_demographic_null import (
    fixed_config, static_visitors,
)
from scripts.model3_island.types import PlantState

K = 8
B = 48
N0 = 8
BUDGETS = (4.5, 6.0, 8.0)
GENOTYPES = ((.2, .2), (.2, .5), (.5, .5))
MODES = ("native", "fixed_expression")
STATUS = "POSTDISCOVERY_EXACT_Q3Q4_OPERATOR_FACTORIAL_NOT_CAUSAL_MEDIATION"


@lru_cache(maxsize=1)
def states():
    items = tuple(
        (low, het, n-low-het)
        for n in range(K+1)
        for low in range(n+1)
        for het in range(n-low+1)
    )
    if len(items) != comb(K+3, 3):
        raise AssertionError("unexpected number of genotype/census states")
    return items


def source(counts):
    if len(counts) != 3 or any(type(x) is not int or x < 0 for x in counts):
        raise ValueError("three nonnegative genotype counts required")
    n = sum(counts)
    if not 1 <= n <= K:
        raise ValueError("only living source populations N1..8 are supported")
    alleles = np.zeros((n,3,2), dtype=float)
    alleles[:,0,:] = .2
    alleles[:,2,:] = .35
    alleles[:,1,:] = np.repeat(np.asarray(GENOTYPES), counts, axis=0)
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def source_ledgers(counts, budget):
    if budget not in BUDGETS:
        raise ValueError("outside previously exposed source budgets")
    original = source(counts)
    expressed = original.alleles.copy()
    expressed[:,1,:] = .35
    fixed = replace(original, alleles=expressed)
    cfg = fixed_config(K, budget)
    native = reproduce_kb(
        original, static_visitors(), cfg, background_denominator_capacity=B
    )
    clamped = reproduce_kb(
        fixed, static_visitors(), cfg, background_denominator_capacity=B
    )
    return original, native, clamped


def intensity_and_genotype_probabilities(counts, budget, mode):
    if mode not in MODES:
        raise ValueError("unknown expression policy")
    original, native, fixed = source_ledgers(counts, budget)
    ledger = native if mode == "native" else fixed
    pair = ledger.outcross.copy()
    pair[np.diag_indices(len(original.ids))] += ledger.self_viable
    mu = float(pair.sum())
    if mu <= 0:
        raise ArithmeticError("zero source viable seeds")
    weights = pair / mu  # father i, mother j, same indexing as population.advance
    p_high = (original.alleles[:,1,:] == .5).sum(axis=1) / 2.
    father = p_high[:,None]
    mother = p_high[None,:]
    genotype_probs = np.array([
        np.sum(weights*(1-father)*(1-mother)),
        np.sum(weights*(father*(1-mother)+(1-father)*mother)),
        np.sum(weights*father*mother),
    ],dtype=float)
    if abs(float(genotype_probs.sum())-1.) > 1e-12:
        raise ArithmeticError("Mendelian/parentage mass was lost")
    genotype_probs = np.clip(genotype_probs, 0., 1.)
    genotype_probs /= genotype_probs.sum()
    # Eliminate roundoff at fully monomorphic source states.
    genotype_probs[-1] = max(0., 1.-float(genotype_probs[:2].sum()))
    return mu, genotype_probs


def transition(budget, intensity_mode, parentage_mode):
    if intensity_mode not in MODES or parentage_mode not in MODES:
        raise ValueError("unknown factorial channel")
    all_s = states()
    by_n = {
        n: (
            np.array([i for i,s in enumerate(all_s) if sum(s)==n],dtype=int),
            np.array([s for s in all_s if sum(s)==n],dtype=int),
        ) for n in range(K+1)
    }
    matrix = np.zeros((len(all_s),len(all_s)),dtype=float)
    matrix[0,0] = 1.
    for i, s in enumerate(all_s[1:], start=1):
        mu_native, q_native = intensity_and_genotype_probabilities(s,budget,"native")
        mu_fixed, q_fixed = intensity_and_genotype_probabilities(s,budget,"fixed_expression")
        mu = mu_native if intensity_mode=="native" else mu_fixed
        q = q_native if parentage_mode=="native" else q_fixed
        recruits = np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            indices, compositions = by_n[n]
            matrix[i,indices] = recruits[n]*multinomial.pmf(compositions,n=n,p=q)
    if np.any(matrix < 0) or not np.allclose(matrix.sum(axis=1),1.,atol=1e-12,rtol=0):
        raise AssertionError("exact demographic/genetic Markov kernel invalid")
    return matrix


def propagate(matrix, horizons=(1,2,5,10,20,40,80)):
    all_s = states()
    p = np.zeros(len(all_s))
    p[all_s.index((0,N0,0))] = 1.
    N = np.array([sum(s) for s in all_s],dtype=int)
    low = np.array([s[0]>0 and s[1]==s[2]==0 for s in all_s])
    high = np.array([s[2]>0 and s[1]==s[0]==0 for s in all_s])
    mean = np.array([
        .2+.3*(s[1]+2*s[2])/(2*sum(s)) if sum(s) else 0.
        for s in all_s
    ])
    results = {}
    for t in range(max(horizons)+1):
        if t in horizons:
            occ = float(p[N>0].sum())
            plow = float(p[low].sum())
            phigh = float(p[high].sum())
            results[str(t)] = {
                "P_occupied": occ,
                "expected_census_unconditional": float(p@N),
                "expected_genetic_mean_if_occupied": float(p@mean/occ) if occ else None,
                "P_fixed_low_unconditional": plow,
                "P_fixed_high_unconditional": phigh,
                "P_fixed_low_given_occupied": plow/occ if occ else None,
                "P_fixed_high_given_occupied": phigh/occ if occ else None,
                "P_segregating_given_occupied": (occ-plow-phigh)/occ if occ else None,
                "total_probability_mass": float(p.sum()),
            }
        if t < max(horizons):
            p = p @ matrix
    return results


def audit():
    rows = []
    for budget in BUDGETS:
        arms = {
            intensity+"|"+parentage: propagate(transition(budget,intensity,parentage))
            for intensity,parentage in product(MODES, repeat=2)
        }
        first = [x["1"]["P_occupied"] for x in arms.values()]
        if max(first)-min(first) > 1e-12:
            raise AssertionError("unmatched original heterozygous founders")
        v = {k:x["80"]["P_occupied"] for k,x in arms.items()}
        full = v["native|native"]-v["fixed_expression|fixed_expression"]
        seed_only = v["native|fixed_expression"]-v["fixed_expression|fixed_expression"]
        parentage_only = v["fixed_expression|native"]-v["fixed_expression|fixed_expression"]
        interaction = full-seed_only-parentage_only
        if abs(full-seed_only-parentage_only-interaction)>1e-14:
            raise AssertionError("factorial accounting identity failed")
        rows.append({
            "ovule_budget":budget,
            "P80":v,
            "native_minus_fixed":full,
            "source_mu_channel_at_fixed_parentage":seed_only,
            "source_parentage_channel_at_fixed_mu":parentage_only,
            "remaining_channel_interaction":interaction,
            "arms":arms,
        })
    return {
        "schema":"chapter2_q3q4_exact_native_operator_factorial_v1",
        "status":STATUS,
        "source":"native scripts/chapter2_kb_reproduction.py + Model3 parent-pair and Poisson rules",
        "source_genotype":"eight 0.20/0.50 heterozygous founders; native vs fixed I=.35",
        "K":K,"B":B,"states":len(states()),
        "new_stochastic_histories":0,"new_genetic_trajectories":0,
        "independent_confirmation":False,
        "results":rows,
        "scientific_limit":"Artificial surgery splits mu (Poisson intensity) from q (offspring-parentage distribution). Contrasts are algebraic 2x2 source-operator effects, NOT natural biological mediation fractions, preregistered evidence, island extinction or a new model family."
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    out=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{
        "budget":r["ovule_budget"],"P80":r["P80"],
        "seed_channel":r["source_mu_channel_at_fixed_parentage"],
        "parentage_channel":r["source_parentage_channel_at_fixed_mu"],
        "interaction":r["remaining_channel_interaction"],
    } for r in out["results"]],sort_keys=True))


if __name__ == "__main__":
    main()
