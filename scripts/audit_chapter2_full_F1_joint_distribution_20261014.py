"""Original Model3 conditional one-child A/I JOINT distribution; no biological births.

The source is synthetic and phenotype-stratified. The parental lottery is the
original reproduction Ledger with selfing contributions on the diagonal.
Given father/mother, independent diploid A and I copy choices yield 16
equally weighted allele combinations. This integrates that law analytically,
never calling population.inherit, population.advance, or model history.
"""
from __future__ import annotations

import json
import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, original_fixture, original_context, ledger_parity,
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    POOL_COUNT, OVERLAPS, balanced_source, balanced_cocarriage,
)

DENOMINATOR = 32
LEVELS = DENOMINATOR + 1
TOL = 1e-12


def one_offspring_joint_distribution(state:types.PlantState, ledger:types.Ledger)->np.ndarray:
    """Probability mass over (A=bin/32, I=bin/32) for one resident child.

    The original synthetic t0 parent alleles are exact multiples of 1/16.
    Therefore each offspring mean of two alleles lies on a 1/32 grid.
    """
    if (not isinstance(state,types.PlantState) or
        not isinstance(ledger,types.Ledger) or len(state.ids)!=48 or
        ledger.outcross.shape!=(48,48)):
        raise ValueError("Original full-N48 Model3 parent genotype and Ledger are required")
    a=state.alleles
    if (not np.isfinite(a).all() or
        not np.array_equal(16*a[:,:, :],np.rint(16*a))):
        raise ValueError("Only exact original synthetic sixteenth-grid source alleles admitted")
    parent=ledger.outcross.copy()
    parent[np.diag_indices(48)] += ledger.self_viable
    if not np.isfinite(parent).all() or np.min(parent)<0:
        raise ValueError("Invalid source native parent returns")
    total=float(parent.sum())
    if total<=0:raise ValueError("No resident offspring parental contribution")
    parent/=total
    output=np.zeros((LEVELS,LEVELS),dtype=np.float64)
    p16=(parent/16).ravel()
    for af in (0,1):
        for am in (0,1):
            Abin=np.rint(16*(a[:,2,af,None]+a[None,:,2,am])).astype(np.int64)
            for inf in (0,1):
                for inm in (0,1):
                    Ibin=np.rint(16*(a[:,1,inf,None]+a[None,:,1,inm])).astype(np.int64)
                    if (Abin.min()<0 or Abin.max()>DENOMINATOR
                        or Ibin.min()<0 or Ibin.max()>DENOMINATOR):
                        raise ValueError("Synthetic first-offspring allele violates unit interval")
                    np.add.at(output,(Abin.ravel(),Ibin.ravel()),p16)
    if (not np.isfinite(output).all() or np.min(output)<0
        or abs(float(output.sum())-1)>TOL):
        raise ValueError("Original-parent pair 16-copy offspring probability mass does not close")
    return output


def total_variation(p:np.ndarray,q:np.ndarray)->float:
    if (p.shape!=(LEVELS,LEVELS) or q.shape!=p.shape
        or not np.isfinite(p).all() or not np.isfinite(q).all()
        or np.min(p)<0 or np.min(q)<0
        or abs(float(p.sum())-1)>TOL or abs(float(q.sum())-1)>TOL):
        raise ValueError("Inadmissible pair of 1/32 offspring distributions")
    return float(np.abs(p-q).sum()/2)


def technical_report()->dict:
    d=original_fixture()
    contexts={k:original_context(d,"main",k) for k in CONTEXTS}
    rows=[]
    for pool in range(POOL_COUNT):
        base=balanced_source(pool)
        for context,(cfg,vis) in contexts.items():
            baseline=None
            for m in OVERLAPS:
                edited=balanced_cocarriage(base,pool,m)
                ledger_parity(base,edited,cfg,vis)
                led=reproduction.reproduce(edited,vis,cfg)
                joint=one_offspring_joint_distribution(edited,led)
                pA=joint.sum(axis=1)
                pI=joint.sum(axis=0)
                if baseline is None:
                    baseline=joint
                dA=float(np.abs(pA-baseline.sum(axis=1)).max())
                dI=float(np.abs(pI-baseline.sum(axis=0)).max())
                if max(dA,dI)>TOL:
                    raise ValueError("Full one-trait F1 offspring distributions differ across co-carrier m")
                tv=total_variation(joint,baseline)
                if m==0 and tv!=0:
                    raise ValueError("Reference F1 joint distribution not identical to itself")
                if m>0 and tv<=1e-8:
                    raise ValueError("A/I co-carriage does not change synthetic two-trait F1 law")
                rows.append({
                    "source_pool":pool,"visitor_context":context,"co_carriers_m":m,
                    "all_marginal_F1_distributions_matched":True,
                    "A_marginal_max_absolute_bin_difference_from_m0":dA,
                    "I_marginal_max_absolute_bin_difference_from_m0":dI,
                    "joint_A_I_total_variation_from_m0":tv,
                    "joint_nonzero_bins":int(np.count_nonzero(joint)),
                })
    if len(rows)!=POOL_COUNT*len(CONTEXTS)*len(OVERLAPS):
        raise AssertionError("Full synthetic source/context/overlap joint genotype distribution grid incomplete")
    summary=[]
    for context in CONTEXTS:
        vals=[x for x in rows if x["visitor_context"]==context and x["co_carriers_m"]==12]
        allctx=[x for x in rows if x["visitor_context"]==context]
        nonmonotonic=0
        for pool in range(POOL_COUNT):
            dist={x["co_carriers_m"]:x["joint_A_I_total_variation_from_m0"]
                  for x in allctx if x["source_pool"]==pool}
            nonmonotonic+=not(dist[3]<dist[6]<dist[12])
        summary.append({
            "visitor_context":context,"synthetic_sources":len(vals),
            "min_m12_vs_m0_joint_total_variation":min(x["joint_A_I_total_variation_from_m0"] for x in vals),
            "max_m12_vs_m0_joint_total_variation":max(x["joint_A_I_total_variation_from_m0"] for x in vals),
            "sources_with_nonzero_m12_vs_m0_joint_change":sum(x["joint_A_I_total_variation_from_m0"]>1e-8 for x in vals),
            "n_sources_with_nonmonotone_TV_across_m3_m6_m12":nonmonotonic,
            "max_single_trait_distribution_bin_error_across_m":max(max(x["A_marginal_max_absolute_bin_difference_from_m0"],
                x["I_marginal_max_absolute_bin_difference_from_m0"]) for x in allctx),
        })
    return {
        "schema":"chapter2_synthetic_founder_AI_full_single_child_joint_distribution_v1",
        "status":"EXACT_NATIVE_MODEL3_T0_JOINT_GENOTYPE_PROBABILITY_ONLY",
        "source_profiles":POOL_COUNT,"original_ecology_contexts":list(CONTEXTS),
        "conditional_first_offspring_distributions":len(rows),
        "trait_grid_bins":"0/32 through 32/32, genotype-expressed trait values",
        "future_biological_histories":0,"actual_offspring_births":0,
        "real_natural_island_populations_sampled":0,
        "long_run_evolution_order": "NOT_MEASURED",
        "Q4_population_persistence": "NOT_MEASURED",
        "claims":[
            "For each synthetic source and ecology, changing within-quartet A/I co-carriage leaves the entire separate A and I offspring phenotype probability distributions unchanged",
            "Yet the exact paired A/I offspring joint distribution changes as co-carriage alters which loci are carried by the same potentially transmitting parent",
            "A/I copy inheritance is independent conditional on selected parents; unconditional within-offspring two-locus dependence can change",
            "Total-variation distances are descriptive for 16 artificial genotype source profiles, not field-derived island estimates",
            "Changes in joint genotype distribution do not establish preferential adaptive sign, long-run evolutionary-order reversal or survival benefit",
        ],
        "context_summary":summary,
        "rows":rows,
    }


if __name__=="__main__":
    print(json.dumps(technical_report(),sort_keys=True,indent=2))
