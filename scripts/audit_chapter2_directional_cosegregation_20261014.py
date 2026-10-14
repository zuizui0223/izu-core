"""Directional A-up/I-down first-offspring meiosis under fixed original Model3 returns.

No biological birth, offspring census, population.advance/inherit, mutation,
long-run trajectory, response-order event, or survival simulation. All expected
probabilities condition on one resident offspring and its drawn parental pair.
"""
from __future__ import annotations

import json
import numpy as np

from scripts.model3_island import types, reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, original_fixture, original_context, ledger_parity,
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    POOL_COUNT, OVERLAPS, balanced_source, balanced_cocarriage,
    joint_pre_mutation_segregational_deviations,
)
from scripts.audit_chapter2_founder_F1_conditional_moments_20261014 import (
    conditional_f1_moments,
)


def directional_f1(state: types.PlantState, ledger: types.Ledger) -> dict:
    """Integrate sign of allele-segregation departure from parental midpoint.

    Given 0/1/2 symmetric heterozygous parents at one locus, each sign is
    obtained with probability 0 / 1/2 / 1/4. A/I segregation is independent
    *conditional on parent IDs*. Mixture over parent pairs is not independent.
    """
    n = len(state.ids)
    if n != 48 or not isinstance(ledger, types.Ledger):
        raise ValueError("Original native populated 48-adult source/Ledger required")
    old = joint_pre_mutation_segregational_deviations(state, ledger)
    het_A = (state.alleles[:,2,0] != state.alleles[:,2,1]).astype(np.int8)
    het_I = (state.alleles[:,1,0] != state.alleles[:,1,1]).astype(np.int8)
    count_A = het_A[:,None] + het_A[None,:]
    count_I = het_I[:,None] + het_I[None,:]

    pplus_A = np.where(count_A == 2, 0.25, (count_A == 1)*0.5)
    pminus_I = np.where(count_I == 2, 0.25, (count_I == 1)*0.5)
    parent = ledger.outcross.copy()
    parent[np.diag_indices(n)] += ledger.self_viable
    total = float(parent.sum())
    if not np.isfinite(total) or total <= 0:
        raise ValueError("No valid expected resident offspring lottery")
    p = parent / total
    sign_pair = pplus_A*pminus_I
    self_mask = np.eye(n, dtype=bool)
    signed_total = float(np.sum(p*sign_pair))
    signed_self = float(np.sum(p[self_mask]*sign_pair[self_mask]))
    signed_outcross = float(np.sum(p[~self_mask]*sign_pair[~self_mask]))
    P_A_up = float(np.sum(p*pplus_A))
    P_I_down = float(np.sum(p*pminus_I))
    self_probability = float(np.trace(p))
    baseline_independent = P_A_up*P_I_down
    if (abs(signed_total - old["p_joint_nonzero_A_and_I_segregation"]/4) > 1e-14
        or abs(P_A_up - old["p_nonzero_A_segregation_relative_to_parent_midpoint"]/2) > 1e-14
        or abs(P_I_down - old["p_nonzero_I_segregation_relative_to_parent_midpoint"]/2) > 1e-14
        or abs(signed_total-signed_self-signed_outcross)>1e-14
        or not 0<=signed_total<=min(P_A_up,P_I_down)+1e-14):
        raise ValueError("Signed same-offspring Mendelian probability identity failed")
    return {
        "condition":"randomly selected resident offspring prior to mutation",
        "sign_reference":"each of the selected two parents' mean phenotype at each locus",
        "p_A_above_selected_parent_midpoint":P_A_up,
        "p_I_below_selected_parent_midpoint":P_I_down,
        "p_A_up_and_I_down":signed_total,
        "p_A_up_and_I_up":signed_total,
        "p_A_down_and_I_down":signed_total,
        "p_A_down_and_I_up":signed_total,
        "p_A_up_and_I_down_from_selfed_parent_pair":signed_self,
        "p_A_up_and_I_down_from_outcross_parent_pair":signed_outcross,
        "p_selfed_parent_pair":self_probability,
        "excess_joint_direction_over_independent_marginals":
            signed_total-baseline_independent,
        "covariance_of_signed_Mendelian_A_and_I_deviations":0.0,
        "p_original_joint_nonzero_deviation":old[
            "p_joint_nonzero_A_and_I_segregation"],
    }


def technical_report()->dict:
    """Exactly 16 x 3 x 4 (old biologic operator; synthetic source genotypes)."""
    fixture=original_fixture()
    contexts={c:original_context(fixture,"main",c) for c in CONTEXTS}
    rows=[]
    for pool in range(POOL_COUNT):
        original=balanced_source(pool)
        for context,(config,vis) in contexts.items():
            baseline=None
            signed_baseline=None
            for m in OVERLAPS:
                changed=balanced_cocarriage(original,pool,m)
                ledger_parity(original,changed,config,vis)
                source_ledger=reproduction.reproduce(changed,vis,config)
                child=conditional_f1_moments(changed,source_ledger)
                signed=directional_f1(changed,source_ledger)
                fixed={
                    "expected_offspring_M_I_A":child["expected_single_offspring_mean_M_I_A"],
                    "F1_variance_M_I_A":child["first_offspring_variance_M_I_A"],
                    "A_signed_marginal":signed["p_A_above_selected_parent_midpoint"],
                    "I_signed_marginal":signed["p_I_below_selected_parent_midpoint"],
                }
                if baseline is None:
                    baseline=fixed
                else:
                    for key in fixed:
                        if not np.allclose(fixed[key],baseline[key],atol=2e-14,rtol=0):
                            raise ValueError("Marginal F1 state changed across co-carriage conditions")
                if context==0:
                    if (abs(fixed["A_signed_marginal"]-.0625)>1e-14 or
                        abs(fixed["I_signed_marginal"]-.0625)>1e-14):
                        raise ValueError("Selfed-only direction marginal no longer at exactly 1/16")
                    if abs(signed["p_A_up_and_I_down"] - m/768)>1e-14:
                        raise ValueError("Selfing-only directional co-carriage formula changed")
                    if signed["p_A_up_and_I_down_from_outcross_parent_pair"]!=0:
                        raise ValueError("Unvisited context cannot provide outcross direction")
                rows.append({
                    "synthetic_source_pool":pool,
                    "visitor_context":context,
                    "co_carriers_m":m,
                    "marginals_are_matched":True,
                    "source_N":48,
                    **signed,
                })
    if len(rows)!=POOL_COUNT*len(CONTEXTS)*len(OVERLAPS):
        raise AssertionError("Incomplete signed meiosis source×ecology×overlap grid")
    results=[]
    for context in CONTEXTS:
        for m in OVERLAPS:
            group=[x for x in rows if x["visitor_context"]==context and
                   x["co_carriers_m"]==m]
            vals=[x["p_A_up_and_I_down"] for x in group]
            ss=[x["p_A_up_and_I_down_from_selfed_parent_pair"] for x in group]
            oo=[x["p_A_up_and_I_down_from_outcross_parent_pair"] for x in group]
            results.append({
                "visitor_context":context,"co_carriers_m":m,
                "n_synthetic_sources":len(group),
                "p_joint_signed_min":min(vals),
                "p_joint_signed_max":max(vals),
                "p_selfed_joint_signed_min":min(ss),
                "p_selfed_joint_signed_max":max(ss),
                "p_outcross_joint_signed_min":min(oo),
                "p_outcross_joint_signed_max":max(oo),
            })
    return {
        "schema":"chapter2_balanced_AI_directional_conditional_meiosis_v1",
        "status":"NO_BIOLOGY_NATIVE_REPRODUCTION_PREMUTATION_SIGNED_MEIOSIS",
        "synthetic_phenotype_balanced_source_inputs":POOL_COUNT,
        "original_model3_visitor_contexts":list(CONTEXTS),
        "conditional_signed_first_offspring_cases":len(rows),
        "new_biological_offspring_or_population_futures":0,
        "sustained_A_or_I_response_events_computed":False,
        "Q4_survival_or_persistence_computed":False,
        "natural_genetic_linkage_or_selection_covariance_identified":False,
        "direction_is_relative_to_selected_parent_midpoint_not_founder_mean":True,
        "independent_natural_island_sources_observed":0,
        "long_run_response_order_unidentified":True,
        "summary_by_visitor_context_and_m":results,
        "rows":rows,
        "interpretation":[
            "A_up and I_down is one of four equally likely SIGN configurations given two nonzero Mendelian departures",
            "Conditional on parent IDs A and I segregation signs are independent; unconditional joint tails depend on parent mixture",
            "Zero signed gametic-deviation covariance is compatible with changed frequency of same-offspring co-occurrence",
            "Nonzero favorable co-segregation also has identically likely unfavorable A_up/I_up; direction is not selected at t0",
            "Selfed and outcrossed parent pairs are separated without simulating offspring births",
            "This is not a founder mean +0.05 / -0.05 sustained response event or order reversal",
            "No mutation, population updates, density feedback or long-run viability simulated",
        ],
    }


def main()->None:
    print(json.dumps(technical_report(),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
