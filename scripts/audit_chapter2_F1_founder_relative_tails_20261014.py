"""Analytic single-F1 founder-relative +/-0.05 genotype tails, NO births.

Unlike signed departures from the selected parental midpoint, this conditions
on the original full-48 artificial source founder mean. The object is one
theoretical resident offspring and is NOT the sustained 20-census evolution
of the population mean under Model3.
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


def source_mean_threshold_tails(
    state:types.PlantState, ledger:types.Ledger, *,
    threshold:float=0.05
)->dict:
    """Parent-lottery × two-copy meiosis probability for one prospective child.

    All old source conditional diploid genotypes are exact dyadic rationals;
    threshold uses original 0.05 decimal as in model event observer.
    No source-wide offspring population, first reproduction or outcome is run.
    """
    n=len(state.ids)
    if (n!=48 or state.alleles.shape!=(48,3,2)
        or not isinstance(ledger,types.Ledger)
        or ledger.outcross.shape!=(48,48)
        or threshold!=0.05
        or not np.all(state.alleles[:,2,:].mean(axis=1)==0.5)):
        raise ValueError("Only the unchanged A=.5 native original 48-founder t0 scope admitted")
    parent=ledger.outcross.copy()
    parent[np.diag_indices(n)]+=ledger.self_viable
    norm=float(parent.sum())
    if norm<=0 or not np.isfinite(norm):
        raise ValueError("No valid resident parental lottery")
    p=parent/norm
    allmeans=state.alleles.mean(axis=2)
    baseline=allmeans.mean(axis=0)
    A_target=float(baseline[2]+threshold)
    I_target=float(baseline[1]-threshold)
    A=state.alleles[:,2,:]
    I=state.alleles[:,1,:]
    pA=np.zeros((n,n),dtype=float)
    pI=np.zeros((n,n),dtype=float)
    for fc in (0,1):
        for mc in (0,1):
            pA+=((A[:,fc,None]+A[None,:,mc])/2>=A_target)/4
            pI+=((I[:,fc,None]+I[None,:,mc])/2<=I_target)/4
    # Conditional independence is in original Model3 segregational-copy RNG:
    # draw gametes separately at A and I given father/mother identities.
    joint=pA*pI
    diag=np.eye(n,dtype=bool)
    self_J=float(np.sum(p[diag]*joint[diag]))
    cross_J=float(np.sum(p[~diag]*joint[~diag]))
    total_J=self_J+cross_J
    marginal_A=float(np.sum(p*pA))
    marginal_I=float(np.sum(p*pI))
    parental_I=(allmeans[:,1,None]+allmeans[None,:,1])/2
    with_I_pair_mean_already_low=float(np.sum(
        p*joint*(parental_I<=I_target)))
    with_I_pair_mean_above=float(np.sum(
        p*joint*(parental_I>I_target)))
    if (abs(total_J-float(np.sum(p*joint)))>1e-13
        or abs(with_I_pair_mean_already_low+with_I_pair_mean_above-total_J)>1e-13
        or not 0<=total_J<=min(marginal_A,marginal_I)+1e-13
        or abs(float(p.sum())-1)>1e-12):
        raise ValueError("Founder-relative single-offspring threshold probability closure failed")
    return {
        "founder_mean_A":float(baseline[2]),
        "founder_mean_I":float(baseline[1]),
        "one_offspring_A_target":A_target,
        "one_offspring_I_target":I_target,
        "p_one_offspring_A_at_least_plus_0p05":marginal_A,
        "p_one_offspring_I_at_most_minus_0p05":marginal_I,
        "p_one_offspring_both_0p05_thresholds":total_J,
        "p_both_via_selfed_parent_pair":self_J,
        "p_both_via_outcross_parent_pair":cross_J,
        "p_both_where_selected_parent_I_midpoint_already_below_threshold":
            with_I_pair_mean_already_low,
        "p_both_where_selected_parent_I_midpoint_above_threshold":
            with_I_pair_mean_above,
        "n_actual_births_or_future_population_updates":0,
        "estimand":"single resident offspring from original t0 parental lottery, founder-relative +/-0.05; NOT a population-mean 20-census event",
    }


def technical_report()->dict:
    d=original_fixture()
    contexts={k:original_context(d,"main",k) for k in CONTEXTS}
    rows=[]
    for pool in range(POOL_COUNT):
        base=balanced_source(pool)
        for context,(cfg,vis) in contexts.items():
            ref_A=ref_I=None
            for m in OVERLAPS:
                edited=balanced_cocarriage(base,pool,m)
                ledger_parity(base,edited,cfg,vis)
                ledger=reproduction.reproduce(edited,vis,cfg)
                tails=source_mean_threshold_tails(edited,ledger)
                if ref_A is None:
                    ref_A=tails["p_one_offspring_A_at_least_plus_0p05"]
                    ref_I=tails["p_one_offspring_I_at_most_minus_0p05"]
                elif (abs(ref_A-tails["p_one_offspring_A_at_least_plus_0p05"])>2e-14
                    or abs(ref_I-tails["p_one_offspring_I_at_most_minus_0p05"])>2e-14):
                    raise ValueError("Individual founder-relative marginal threshold probabilities changed by co-carriage")
                rows.append({"synthetic_source_pool":pool,
                             "visitor_context":context,
                             "co_carriers_m":m, **tails})
    if len(rows)!=POOL_COUNT*len(CONTEXTS)*len(OVERLAPS):
        raise AssertionError("Founder-relative t0 conditional allele tail grid incomplete")
    aggregates=[]
    for context in CONTEXTS:
        for m in OVERLAPS:
            vals=[r for r in rows if r["visitor_context"]==context
                  and r["co_carriers_m"]==m]
            aggregates.append({
                "context":context,"co_carriers_m":m,"source_profiles":len(vals),
                "p_single_child_joint_min":min(v["p_one_offspring_both_0p05_thresholds"] for v in vals),
                "p_single_child_joint_max":max(v["p_one_offspring_both_0p05_thresholds"] for v in vals),
                "p_single_child_joint_self_min":min(v["p_both_via_selfed_parent_pair"] for v in vals),
                "p_single_child_joint_self_max":max(v["p_both_via_selfed_parent_pair"] for v in vals),
                "p_single_child_joint_outcross_min":min(v["p_both_via_outcross_parent_pair"] for v in vals),
                "p_single_child_joint_outcross_max":max(v["p_both_via_outcross_parent_pair"] for v in vals),
            })
    return {
        "schema":"chapter2_balanced_AI_founder_mean_single_F1_threshold_tails_v1",
        "status":"NO_BIOLOGY_ORIGINAL_MODEL3_CONDITIONAL_F1_THRESHOLD_ANALYTIC",
        "artificial_source_profiles":POOL_COUNT,
        "source_contexts":list(CONTEXTS),
        "matched_F1_single_offspring_contrasts":len(rows),
        "new_biological_futures_or_sustained_events":0,
        "permanently_distinct_from":["selected_parent_pair_midpoint_signed_deviation",
                                    "realized_F1_population_mean",
                                    "original_20_occupied_census_sustained_phenotype_event"],
        "warnings":[
            "One favorable-threshold *offspring* is not population-mean evolution or an order result",
            "Original initial I phenotypic differences across adults can pass the I target even with no hidden I carrier",
            "Parental-pair I mean below target is a descriptive stratum, not an isolated causal channel",
            "No mutation, selection over time, new ecological histories or survival simulated",
            "No true mainland source alleles or population-level persistence inferred",
        ],
        "summary_by_ecology_and_overlap":aggregates,
        "rows":rows,
    }


if __name__=="__main__":
    print(json.dumps(technical_report(),indent=2,sort_keys=True))
