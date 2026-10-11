"""Statewise delivered-pollen equality under fixed-richness functional replacement.

For EVERY finite census/genotype and expression-policy state, rescale
effectiveness of the original four-visitor assemblage until the aggregate
pollen DELIVERED matches that under shifted four-visitor optima.
This is an artificial source-operator negative control, NOT a feasible
ecological intervention and NOT natural causal mediation.

All operators use original Model3 reproduce_kb, native Poisson capped K8
recruitment, and Mendelian parentage, with zero adult survival/mutation/
immigration. The 165-state model is mathematically exact only for this
restricted fixed-visitor/three-genotype model family.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from pathlib import Path
import argparse
import json

import numpy as np
from scipy.stats import poisson, multinomial

from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import (
    visitors, config, source, states, by_n, K, B, N0, MODES
)
from scripts.model3_island.types import VisitorState
from scripts.chapter2_kb_reproduction import reproduce_kb

FRACTIONS = (.25, .5, 1.)
SETTINGS = ("delayed_control","prior_selfing","pollen_discount","assurance_cost")
BUDGETS = (6.,8.)
POLICIES = ("native","fixed_expression")
VISITOR_ARMS = ("shifted4","original4_statewise_equal_delivery")
YEARS = 80
STATUS = "EXPLORATORY_STATEWISE_EQUAL_TOTAL_POLLEN_NEGATIVE_CONTROL_NO_CAUSAL_MEDIATION"


def original_genome_and_expression(counts, policy):
    if policy not in POLICIES: raise ValueError("unrecognized source genetic expression")
    genome=source(counts)
    expressed=genome
    if policy=="fixed_expression":
        aa=genome.alleles.copy()
        aa[:,1,:]=.35
        expressed=replace(genome,alleles=aa)
    return genome,expressed


def parentage_and_mu(counts, ledger):
    parents=ledger.outcross.copy()
    np.fill_diagonal(parents,np.diag(parents)+ledger.self_viable)
    mu=float(parents.sum())
    if mu<=0 or not np.isfinite(mu):
        raise ArithmeticError("missing source viable seed recruitment")
    w=parents/mu
    # Genotype CLASS, not numerical allele value (PR #466 regression).
    # Offspring inherit genomic homologs even when investment expression is
    # clamped in the reproductive source.
    h=np.repeat(np.array([0.,.5,1.]),np.asarray(counts,dtype=int))
    f=h[:,None]; m=h[None,:]
    q=np.array([np.sum(w*(1-f)*(1-m)),
                np.sum(w*(f*(1-m)+(1-f)*m)),np.sum(w*f*m)],dtype=float)
    if not np.isclose(q.sum(),1.,atol=1e-12,rtol=0):
        raise AssertionError("Mendelian probability mass lost")
    q=np.clip(q,0.,1.);q/=q.sum()
    q[-1]=max(0.,1.-float(q[:2].sum()))
    return mu,q


def source_equalized(counts,setting,budget,fraction,policy):
    if fraction not in FRACTIONS or setting not in SETTINGS or budget not in BUDGETS:
        raise ValueError("unsupported prespecified source functional context")
    dna, expressed=original_genome_and_expression(counts,policy)
    vshift=visitors(fraction)
    vref=visitors(0.)
    cfg=config(setting,budget)
    shifted=reproduce_kb(expressed,vshift,cfg,background_denominator_capacity=B)
    plain=reproduce_kb(expressed,vref,cfg,background_denominator_capacity=B)
    ds=float(shifted.delivered.sum())
    dr=float(plain.delivered.sum())
    if len(vshift.ids)!=4 or len(vref.ids)!=4:
        raise AssertionError("four types not retained")
    if not (0<=ds<=dr+1e-10):
        raise AssertionError("reference source cannot equalize shifted delivery")
    # In a census N=1, transfer excludes the self donor, so both total
    # delivered values are exactly zero. No scale is identifiable or needed.
    if dr == 0:
        if ds!=0 or len(dna.ids)!=1:
            raise AssertionError("unanticipated zero pollen source")
        scale=1.
    else:
        scale=ds/dr
        if not 0<scale<=1+1e-12:
            raise ArithmeticError("unphysical delivery matching scale")
    v_equal=VisitorState(
        ids=vref.ids,optima=vref.optima,breadths=vref.breadths,
        effectiveness=np.full(4,scale,dtype=float))
    equal=reproduce_kb(expressed,v_equal,cfg,
                       background_denominator_capacity=B)
    de=float(equal.delivered.sum())
    if not np.isclose(ds,de,atol=1e-12,rtol=0):
        raise AssertionError("total pollen did not equalize in this genetic state")
    mu_shifted,q_shifted=parentage_and_mu(counts,shifted)
    mu_equal,q_equal=parentage_and_mu(counts,equal)
    return {
        "shifted4":(mu_shifted,q_shifted),
        "original4_statewise_equal_delivery":(mu_equal,q_equal),
        "matched_pollen":ds,
        "effectiveness_multiplier":float(scale),
        "viable_seed_difference":mu_shifted-mu_equal,
        "paternal_q_L1":float(np.abs(q_shifted-q_equal).sum()),
        "source_census":len(dna.ids),
    }


@lru_cache(maxsize=None)
def transition(setting,budget,fraction,policy,visitor_arm):
    if visitor_arm not in VISITOR_ARMS or policy not in POLICIES:
        raise ValueError("unknown operator arm or genetic expression")
    original=states()
    T=np.zeros((len(original),len(original)),dtype=float)
    T[0,0]=1.
    for i,s in enumerate(original[1:],start=1):
        x=source_equalized(s,setting,budget,fraction,policy)
        mu,q=x[visitor_arm]
        recruits=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            cols,genotypes=by_n()[n]
            T[i,cols]=recruits[n]*multinomial.pmf(genotypes,n=n,p=q)
    if np.any(T<0) or not np.isfinite(T).all() or not np.allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0):
        raise AssertionError("nonstochastic census-genotype kernel")
    return T


def longrun(T):
    s=states();p=np.zeros(len(s))
    p[s.index((0,N0,0))]=1.
    occupied=np.asarray([sum(x)>0 for x in s])
    low=np.asarray([x[0]>0 and x[1]==x[2]==0 for x in s])
    for _ in range(YEARS):p=p@T
    alive=float(p[occupied].sum())
    low_joint=float(p[low].sum())
    return {
        "P80_occupied":alive,
        "P80_low_allele_fixed_and_occupied":low_joint,
        "P80_low_allele_fixed_given_occupied":low_joint/alive if alive else None,
    }


def audit():
    rows=[]
    for frac in FRACTIONS:
        for setting in SETTINGS:
            for budget in BUDGETS:
                founder=source_equalized((0,N0,0),setting,budget,frac,"native")
                armp={}
                for policy in POLICIES:
                    for arm in VISITOR_ARMS:
                        armp[policy+"|"+arm]=longrun(
                            transition(setting,budget,frac,policy,arm))
                native=armp["native|shifted4"]
                equal=armp["native|original4_statewise_equal_delivery"]
                fixed_shift=armp["fixed_expression|shifted4"]
                fixed_equal=armp["fixed_expression|original4_statewise_equal_delivery"]
                rows.append({
                    "mismatch_fraction":frac,"setting":setting,"budget":budget,
                    "founder_effectiveness_multiplier":founder["effectiveness_multiplier"],
                    "founder_total_pollen_equalized":founder["matched_pollen"],
                    "founder_seed_difference":founder["viable_seed_difference"],
                    "founder_parentage_L1":founder["paternal_q_L1"],
                    "P80_native_shift_minus_equalized":(
                        native["P80_occupied"]-equal["P80_occupied"]),
                    "P80_fixed_shift_minus_equalized":(
                        fixed_shift["P80_occupied"]-fixed_equal["P80_occupied"]),
                    "P80_genetic_expression_delta_shift":(
                        native["P80_occupied"]-fixed_shift["P80_occupied"]),
                    "P80_genetic_expression_delta_equalized":(
                        equal["P80_occupied"]-fixed_equal["P80_occupied"]),
                    "P80_low_allele_fixed_joint_shift_minus_equalized":(
                        native["P80_low_allele_fixed_and_occupied"] -
                        equal["P80_low_allele_fixed_and_occupied"]),
                    "full_arms":armp,
                })
    return {
        "schema":"chapter2_q3q4_statewise_total_pollen_equalized_v1",
        "status":STATUS,
        "n_independent_biological_histories":0,
        "n_visitor_types_each_arm":4,
        "n_original_mating_systems":len(SETTINGS),
        "n_resource_budgets":len(BUDGETS),
        "n_functional_shifts":len(FRACTIONS),
        "n_source_settings":len(rows),
        "states_per_operator":len(states()),
        "limitations":[
            "Pollen is equalized to the same AGGREGATE total in EACH census-genotype-policy state, not per maternal recipient or paternal donor.",
            "Statewise reference effectiveness depends on plant genotype, census and genetic expression policy, and is a mathematical operator surgery, not a biologically realizable static visitor population.",
            "A remaining 80-generation difference can reflect redistribution of pollen receipt, seed production, genotype/parentage and nonlinear demographic feedback; it cannot be allocated to one path.",
            "Results are source-selected synthetic Model3 conditional probabilities, not new natural islands, independent ecological history samples, phylogenetic confirmation or proof of evolutionary suicide.",
        ],
        "results":rows,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    x=p.parse_args()
    d=audit();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([
        {k:row[k] for k in (
            "mismatch_fraction","setting","budget","founder_seed_difference",
            "P80_native_shift_minus_equalized","P80_genetic_expression_delta_shift",
            "P80_genetic_expression_delta_equalized")}
        for row in d["results"]
    ],sort_keys=True))


if __name__=="__main__":main()
