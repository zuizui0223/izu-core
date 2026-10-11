"""Does density's selection effect differ among individuals in SAME population?

Source-native full genetic fitness gradients, not a monomorphic-clone result.
Keeps the distribution of EIGHT distinct flower phenotypes exactly constant
across census N8/N24/N48 by repeating each genotype 1/3/6 times.
Capacity K48 and pollen background B48 stay fixed, so the variable here is
CURRENT census and focal conspecific composition, not population carrying
capacity K or number of pollinator types.

All 192 source cells are post-outcome synthetic mechanism tests, NOT 192
independent islands, natural fitness coefficients or historical allele changes.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_order_selection_mismatch_census_20261011 import (
    plants, visitor_state, source_config, genetic_return, perturb,
    N_VALUES, TIMINGS, ASSURANCE_COSTS,
)

# No genetic mutation is simulated: eight diploid HOMOZYGOUS phenotypes
# are repeated to the same relative mixture at three total censuses.
FIXTURES=("clonal","investment_heterogeneity","matching_heterogeneity",
          "matching_and_investment_heterogeneity")
MISMATCH=(0.,.25,.5,1.)
STEPS=(.005,.0025)
STATUS="POSTDISCOVERY_INDIVIDUAL_LEVEL_DENSITY_FUNCTIONAL_MATCHING_SOURCE_ONLY"


def genotype_fixture(n,fixture):
    if n not in N_VALUES or fixture not in FIXTURES:
        raise ValueError("unsupported census or source heterogeneous fixture")
    base=plants(n)
    alleles=base.alleles.copy()
    # Eight types whose relative abundances remain exactly 1/8 at each N.
    type_id=np.arange(n,dtype=int)%8
    variable_I=np.linspace(.2,.5,8)[type_id]
    variable_X=np.linspace(.05,.55,8)[type_id]
    if fixture in ("investment_heterogeneity","matching_and_investment_heterogeneity"):
        alleles[:,1,:]=variable_I[:,None]
    if fixture in ("matching_heterogeneity","matching_and_investment_heterogeneity"):
        alleles[:,0,:]=variable_X[:,None]
    state=replace(base,alleles=alleles)
    if not np.allclose(state.alleles.mean(axis=2)[:,2],.35):
        raise AssertionError("assurance was not held fixed")
    return state


def gradient_for_adult(state,idx,visitor,cfg,h):
    if idx<0 or idx>=len(state.ids) or h not in STEPS:
        raise ValueError("focal outside source or finite step")
    a=state.alleles.copy()
    a[idx,1,:]+=h
    hi=genetic_return(replace(state,alleles=a),visitor,cfg,where=idx)["W"]
    a[idx,1,:]-=2*h
    lo=genetic_return(replace(state,alleles=a),visitor,cfg,where=idx)["W"]
    if not 0<hi or not 0<lo:
        raise ArithmeticError("genetic payoff must remain positive")
    return float((np.log(hi)-np.log(lo))/(2*h))


def source_selection(n,fixture,mismatch,timing,cost):
    state=genotype_fixture(n,fixture)
    v=visitor_state(mismatch)
    cfg=source_config(timing,cost)
    betas=np.array([
        gradient_for_adult(state,i,v,cfg,.0025)
        for i in range(n)
    ],dtype=float)
    # Verify both derivative widths at each unique phenotype, not only the
    # clone median. Near-zero derivatives must remain explicitly classified.
    refinement=np.array([gradient_for_adult(state,i,v,cfg,.005) for i in range(8)])
    if np.any(np.abs(refinement-betas[:8]) > .02+.05*np.maximum(
        np.abs(refinement),np.abs(betas[:8])
    )):
        raise AssertionError("focal finite-gradient step unstable")
    # The repeated types must all have the same fitness gradient within
    # their own genotype category, irrespective of their arbitrary IDs.
    shaped=betas.reshape(n//8,8)
    if not np.allclose(shaped,shaped[0],rtol=0,atol=1e-11):
        raise AssertionError("identical source genotypes show different beta")
    types=betas[:8]
    with np.errstate(invalid="raise"):
        signed=np.where(types>.02,1,np.where(types<-.02,-1,0))
    source_total=genetic_return(state,v,cfg)
    return {
        "census_N":n,"fixture":fixture,
        "functional_mismatch_fraction":mismatch,
        "assurance_timing":timing,"assurance_cost":cost,
        "individual_genotype_types":8,
        "adult_focal_log_W_investment_beta_by_type":types.tolist(),
        "focal_beta_median":float(np.median(betas)),
        "focal_beta_min":float(types.min()),
        "focal_beta_max":float(types.max()),
        "n_focal_types_positive":int((signed==1).sum()),
        "n_focal_types_negative":int((signed==-1).sum()),
        "n_focal_types_near_zero":int((signed==0).sum()),
        "mixed_opposite_fitness_signs_within_one_population":bool(
            np.any(signed==1) and np.any(signed==-1)
        ),
        "reference_total_viable_seed_mu":source_total["group_seed"],
        "reference_total_delivered_pollen":source_total["pollen_delivery"],
        "source_capacity_K":cfg.capacity,
        "pollen_background_B":48,
    }


def audit():
    rows=[]
    for fixture in FIXTURES:
        for timing in TIMINGS:
            for cost in ASSURANCE_COSTS:
                for mismatch in MISMATCH:
                    for n in N_VALUES:
                        rows.append(source_selection(n,fixture,mismatch,timing,cost))
    controls={(x["fixture"],x["assurance_timing"],x["assurance_cost"],
               x["functional_mismatch_fraction"],x["census_N"]):x for x in rows}
    if len(controls)!=len(rows):
        raise AssertionError("source context duplicates")
    return {
        "schema":"chapter2_source_individual_trait_by_census_gradient_v1",
        "status":STATUS,"n_source_cells":len(rows),
        "n_flower_genotype_composition_fixtures":len(FIXTURES),
        "n_mating_timing_cost_factorial":len(TIMINGS)*len(ASSURANCE_COSTS),
        "n_functional_mismatch_fractions":len(MISMATCH),
        "n_census_conditions":len(N_VALUES),
        "n_independent_island_systems":0,
        "n_new_stochastic_plant_histories":0,
        "source":"original Model3 reproduce_kb, full W=.5F+.5P+S at each focal adult",
        "scientific_warning":[
            "N is a community-wide current census, not a different N for each individual in that population.",
            "At SAME N, selection gradients differ among individuals because investment and/or matching genotypes differ.",
            "The same eight diploid HOMOZYGOUS phenotypes are present at frequency 1/8 for N8/24/48; repeated identical clones isolate current census from composition frequencies, not future evolution.",
            "Positive and negative focal investment gradients at the same N do not establish a realized allele response without genotype-by-W covariance, segregation and demographic histories.",
            "All values are post-discovery Model3 mathematical fixtures, not measured natural individual fitness or 192 island populations."
        ],
        "rows":rows
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    d=audit();a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([
        {k:x[k] for k in (
            "fixture","assurance_timing","assurance_cost","functional_mismatch_fraction",
            "census_N","focal_beta_min","focal_beta_max",
            "n_focal_types_positive","n_focal_types_negative")}
        for x in d["rows"] if x["assurance_timing"]=="delayed" and x["assurance_cost"]==0.
    ],sort_keys=True))


if __name__=="__main__":main()
