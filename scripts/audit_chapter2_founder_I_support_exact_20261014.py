#!/usr/bin/env python3
"""Exact original-founder I allele-support combinations; no Model3 futures.

The old t0 original genotype file and native types are source authenticated.
For the counterfactual I-homolog-collapse state, I alleles are each adult's
original expressed I value, not a new observed genotype or run outcome.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
import json

import numpy as np

from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    ORIGINAL_BLOB, original_fixture, source_state
)

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT / "data/results/chapter2_founder_I_support_exact_20261014.json"
EXPECTED={
    "main": {6:12,7:6,8:6,9:12,10:12},
    "confirmation": {7:6,8:30,9:6,10:6},
}
FOUNDERS=(2,8,24,48)
DELTA=Fraction(1,20)


def i_mean_profile(block: str, fixture=None) -> tuple[tuple[int,int],...]:
    if block not in EXPECTED:
        raise ValueError("Only historical main/confirmation t0 sources admitted")
    d=original_fixture() if fixture is None else fixture
    old=source_state(d,block)
    # Original I adult phenotype = mean of two homologs, in exact sixteenths.
    means=old.alleles[:,1,:].mean(axis=1)
    units=means*16
    if (len(means)!=48 or not np.isfinite(units).all() or
            not np.array_equal(units,np.rint(units))):
        raise ValueError("Original I means are not exact sixteenth units")
    profile=dict(Counter(int(z) for z in units))
    if profile != EXPECTED[block]:
        raise ValueError("Original I founder-class frequencies changed")
    return tuple(sorted(profile.items()))


def exact_mutation_free_I_support(profile:tuple[tuple[int,int],...],
                                  sample_n:int) -> dict:
    if (type(sample_n) is not int or sample_n<1 or
            type(profile) is not tuple or not profile or
            any(type(v) is not int or type(c) is not int or
                    c<=0 or v<0 or v>16 for v,c in profile) or
            len({v for v,_ in profile})!=len(profile)):
        raise ValueError("Invalid finite source profile or sample size")
    total=sum(k for _,k in profile)
    if sample_n>total:
        raise ValueError("Impossible founder count")
    den=comb(total,sample_n)
    num=0
    covered=0
    valid_classes=0
    def walk(j,remaining,abundance,sum_units,minimum):
        nonlocal num,covered,valid_classes
        if j==len(profile):
            if remaining: return
            covered+=abundance
            valid_classes+=1
            # This is an ALLELE-SUPPORT necessary condition only.
            # mean I = sum_units/(16*n), min I = minimum/16.
            # mean I - min I >= 0.05 iff 5*(sum_units-n*minimum)>=4*n.
            if 5*(sum_units-sample_n*minimum)>=4*sample_n:
                num+=abundance
            return
        value,count=profile[j]
        rest=sum(k for _,k in profile[j+1:])
        for take in range(max(0,remaining-rest),min(count,remaining)+1):
            walk(j+1,remaining-take,abundance*comb(count,take),
                 sum_units+value*take, minimum if take==0 else min(minimum,value))
    walk(0,sample_n,1,0,17)
    if covered!=den or not (0<=num<=den):
        raise AssertionError("All without-replacement original t0 founder draws not covered")
    f=Fraction(num,den)
    return {"n_founders":sample_n,"total_combinations":den,
            "mutation_free_necessary_support_count":num,
            "exact_support_probability":str(f),
            "decimal_support_probability":float(f),
            "enumerated_phenotype_count_combinations":valid_classes}


def audit() -> dict:
    fixture=original_fixture()
    rows=[]
    for block in EXPECTED:
        profile=i_mean_profile(block,fixture)
        for n in FOUNDERS:
            row=exact_mutation_free_I_support(profile,n)
            row["original_founder_block"]=block
            rows.append(row)
    return {
        "schema":"chapter2_founder_original_I_h0_necessary_support_exact_v1",
        "status":"ORIGINAL_SOURCE_COMBINATORIAL_DIAGNOSTIC_NO_BIOLOGY",
        "original_t0_fixture_git_blob":ORIGINAL_BLOB,
        "original_sources_per_block":48,
        "counterfactual":"Collapse both I homologs to each source adult's original expressed I mean; preserve between-adult differences",
        "A_behavior":"Not measured here; assurance A mutation exists in original Model3",
        "target":"I mean decline by 0.05 relative to each sampled founder population's own mean",
        "outcome_definition":"Min founding I allele <= founding I mean - 0.05: necessary for mutation-free population-mean reachability, NOT sustained 20-census event",
        "founder_blocks":2,
        "genetic_futures_or_simulation_histories_run":0,
        "rows":rows,
        "limits":[
            "Zero I within-individual heterozygosity does not remove standing among-adult I differences",
            "Necessary allele lower-bound support does not prove evolution, selection, or persistence",
            "These are all combinatorial draws from two fixed old source phenotypes, not independent natural islands",
            "The event remains subject to mutation modes, parental selection, stochastic sampling, fixation and extinction",
            "Do not interpret hypothetical I carrier retention as complete I-target access",
        ],
    }


def check_committed_result()->dict:
    actual=audit()
    saved=json.loads(RESULT.read_text(encoding="utf-8"))
    if saved!=actual:
        raise ValueError("Committed exact I support receipt differs from rederived original t0 genotype means")
    return actual


if __name__=="__main__":
    print(json.dumps(check_committed_result(),ensure_ascii=False,indent=2))
