"""Source-only A–I background diagnostic; NO new evolutionary histories.

Part 1 reconstitutes the eight Q1 fresh founders from their ORIGINAL frozen
design; their assurance alleles are all 0.5, so founding Cov(A,I) is exactly
zero. Part 2 constructs three deliberately artificial 12-plant populations
with identical A/I locus marginals but positive/negative/zero individual
cross-locus genotype alignment. In a no-visitor source-native Model 3
reproductive ledger, I is expression-neutralized ONLY in the payoff ledger:
the true I allele genotypes are the inherited target of the assay.

One-step expected I response is the ordinary selection covariance / Price
identity, not a new hitchhiking theorem, dynamic sweep, or experimental proof
that historical Q1 founder effects were caused by A-I associations.
The original Model 3 reproduction and diploid inheritance code is untouched.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

from scripts.chapter2_two_origins_technical_20261019 import (
    Island, _config, _expressed_state, _visitors,
)
from scripts.model3_island.types import PlantState
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    load_frozen as load_q1_frozen, founder as q1_founder,
)

STATUS = "SOURCE_ONLY_AI_BACKGROUND_DIAGNOSTIC_NOT_CAUSAL"
N = 12
LOCUS_I = 1
LOCUS_A = 2
FROZEN_Q1_SEEDS = tuple(range(560201, 560209))
PAIRINGS = ("positive", "negative", "balanced")


def q1_original_founder_screen():
    design, _ = load_q1_frozen()
    spec = design["founder_genomes"]
    if (tuple(spec["A_initial_alleles"]) != (.5, .5) or
            list(FROZEN_Q1_SEEDS) != list(range(spec["first_seed"], spec["last_seed"] + 1))):
        raise ValueError("Q1 frozen source-founder protocol changed")
    rows = []
    for seed in FROZEN_Q1_SEEDS:
        pop = q1_founder(design, seed)
        if len(pop.ids) != 48 or not np.array_equal(
                pop.alleles[:, LOCUS_A, :],
                np.full((48,2),.5)):
            raise ValueError("source Q1 assurance locus was not initially fixed")
        A = pop.alleles[:, LOCUS_A, :].mean(axis=1)
        I = pop.alleles[:, LOCUS_I, :].mean(axis=1)
        M = pop.alleles[:, 0, :].mean(axis=1)
        cov = float(np.mean((A - A.mean()) * (I - I.mean())))
        if cov != 0.:
            raise ArithmeticError("Q1 founding A/I covariance nonzero despite invariant A")
        rows.append(dict(founder_seed=seed, initial_A=float(A.mean()),
                         initial_A_variance=float(np.var(A)),
                         initial_I_mean=float(I.mean()),
                         initial_I_variance=float(np.var(I)),
                         initial_M_variance=float(np.var(M)),
                         founding_unphased_individual_A_I_covariance=cov))
    return rows


def synthetic_parent_state(pairing: str):
    """12 homozygous plants; identical per-locus copy and diplotype counts."""
    if pairing not in PAIRINGS:
        raise ValueError("unregistered synthetic parent alignment")
    A = np.array([.75] * 6 + [.25] * 6, dtype=float)
    if pairing == "positive":
        I = np.array([.65] * 6 + [.35] * 6)
    elif pairing == "negative":
        I = np.array([.35] * 6 + [.65] * 6)
    else:
        I = np.array([.65]*3 + [.35]*3 + [.65]*3 + [.35]*3)
    genes = np.zeros((N,3,2),dtype=float)
    genes[:,0,:] = .5
    genes[:,1,:] = I[:,None]
    genes[:,2,:] = A[:,None]
    origin = np.arange(N*6,dtype=np.int64).reshape(N,3,2)
    state = PlantState(
        genes,origin,np.zeros((N,3,2),dtype=bool),
        np.arange(N,dtype=np.int64),np.zeros(N,dtype=np.int64))
    return state


def neutral_investment_ledger(state, *, budget=4.5):
    if budget not in (4.5,8.):
        raise ValueError("technical budgets only")
    island = Island("technical_no_visitors_ai_alignment",float(budget),0)
    cfg = _config(island,assurance_mode="evolving",initial_a=.5)
    # I is phenotypically 0.5 in this PAYOFF only; true I alleles in state
    # remain unchanged and would transmit through canonical inheritance.
    ledger=reproduce(_expressed_state(state,.5,True),_visitors(island),cfg)
    if np.any(ledger.outcross) or len(state.ids)!=N:
        raise AssertionError("zero-visitor source parental weights not pure viable selfing")
    return ledger


def expected_shift(state,ledger):
    """Exact expected inherited I change conditional on an offspring draw."""
    if len(state.ids)!=N:
        raise ValueError("artificial parent census changed")
    I = state.alleles[:,LOCUS_I,:].mean(axis=1)
    parent_weights = (.5*ledger.outcross.sum(axis=0) +
                      .5*ledger.outcross.sum(axis=1) +
                      ledger.self_viable)
    total = float(parent_weights.sum())
    if not (total>0 and np.isfinite(total)):
        raise ValueError("no expected reproduction")
    initial = float(I.mean())
    next_mean = float(np.dot(parent_weights,I)/total)
    cov = float(np.mean((parent_weights-parent_weights.mean()) * (I-initial)))
    price = cov/float(parent_weights.mean())
    if abs(next_mean-initial-price)>1e-13:
        raise ArithmeticError("conditional Price identity fails")
    A = state.alleles[:,LOCUS_A,:].mean(axis=1)
    return dict(initial_I=initial, expected_next_I=next_mean,
                expected_one_generation_delta_I=next_mean-initial,
                price_covariance_term=price,
                unphased_A_I_individual_covariance=float(np.mean(
                    (A-A.mean())*(I-initial))),
                mean_parent_weight=float(parent_weights.mean()))


def synthetic_phase_audit(budget=4.5):
    trial=[]
    marginal_reference=None
    state0=None
    for phase in PAIRINGS:
        state=synthetic_parent_state(phase)
        if state0 is None:
            state0=state
        marginal=[tuple(np.sort(state.alleles[:,l,:].reshape(-1)))
                  for l in range(3)]
        if marginal_reference is None:
            marginal_reference=marginal
        elif marginal!=marginal_reference:
            raise AssertionError("source A/I per-locus allele marginals mismatch")
        trial.append(dict(pairing=phase,**expected_shift(
            state,neutral_investment_ledger(state,budget=budget))))

    # The random-exchange null means uniform reassignment of exactly six
    # HIGH-I homozygous diplotypes across twelve unchanged A backgrounds.
    # Enumerate ALL 12-choose-6 = 924 assignments, not Monte Carlo.
    baseline=state0.alleles
    means=[]
    for high_positions in itertools.combinations(range(N),6):
        trial_alleles=baseline.copy()
        trial_alleles[:,LOCUS_I,:]=.35
        trial_alleles[list(high_positions),LOCUS_I,:]=.65
        st=PlantState(
            trial_alleles,state0.allele_origin,state0.mutation_flags,
            state0.ids,state0.birth_years)
        weighted=expected_shift(st,neutral_investment_ledger(st,budget=budget))
        means.append(weighted["expected_one_generation_delta_I"])
    avg=float(math.fsum(means)/len(means))
    if len(means)!=924 or abs(avg)>1e-14:
        raise ArithmeticError("all-reassignments I-response null not zero")
    if not(trial[0]["expected_one_generation_delta_I"]>0 and
           trial[1]["expected_one_generation_delta_I"]<0 and
           abs(trial[2]["expected_one_generation_delta_I"])<1e-13):
        raise ArithmeticError("source controlled I background sign test failed")
    return dict(budget=budget,per_locus_marginals_identical=True,
                I_direct_effect_in_payoff_disabled=True,
                M_alleles_constant=.5,
                source_unchanged_model3_reproduction=True,
                phase_results=trial,
                exact_924_permutation_null_mean_I_shift=avg,
                permutation_assignments=924)


def audit():
    founders=q1_original_founder_screen()
    synthetic=[synthetic_phase_audit(4.5),synthetic_phase_audit(8.)]
    return dict(status=STATUS,
                original_q1_fresh_founders=founders,
                all_original_eight_q1_A_loci_start_monomorphic=True,
                all_original_eight_q1_founder_A_I_covariances_zero=True,
                original_q1_positive_mutation_allowed=True,
                synthetic_source_only_one_step=synthetic,
                no_new_population_trajectory_advanced=True,
                no_posthoc_new_field_inference=True,
                scope=[
                    "Q1 fresh founder origin A alleles were uniformly 0.5; a PRE-EXISTING high-A/high-I founder association cannot explain PR569 founder sign heterogeneity.",
                    "A mutants can arise later in the original Q1 positive-mutation experiment; future I-background associations may arise dynamically.",
                    "The 12-individual synthetic positive/negative phase experiment simply demonstrates an established genetic selection covariance identity.",
                    "I expression is artificially neutralized only for reproductive returns; I inherited alleles remain distinct.",
                    "The exact 924-state diplotype reallocation null is a mathematical permutation average, NOT 924 independently simulated island populations.",
                    "A and I are independently segregating loci in the native Model3; these covariance readouts are NOT phased linkage disequilibrium.",
                    "No long-term evolutionary hitchhiking was proved, and no source Q1 I response was attributed to A mutations.",
                ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-only",action="store_true")
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    if not args.source_only:
        p.error("only read-only model/source audit is permitted")
    body=json.dumps(audit(),indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        if args.out.exists():
            raise FileExistsError("no overwriting original source audit")
        args.out.write_text(body,encoding="utf8")
    else:
        print(body,end="")


if __name__=="__main__":
    main()
