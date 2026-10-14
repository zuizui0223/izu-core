"""Source-backed scientific claim gate for PR #512: no biology or future updates.

This ledger triangulates three already constructed t0 analytic estimands.
It does not generate offspring, estimate long-run order or Q4 persistence.
"""
from __future__ import annotations

import json

from scripts.audit_chapter2_balanced_cocarriage_20261014 import source_only_audit
from scripts.audit_chapter2_directional_cosegregation_20261014 import (
    technical_report as signed_t0,
)
from scripts.audit_chapter2_F1_founder_relative_tails_20261014 import (
    technical_report as founder_relative_t0,
)


def claim_gate() -> dict:
    variance = source_only_audit()
    signed = signed_t0()
    founder = founder_relative_t0()
    if (len(variance["rows"]), len(signed["rows"]), len(founder["rows"])) != (
        192,192,192
    ):
        raise ValueError("Incomplete exact t0 source claim inventory")
    if (variance["new_biological_genotype_transmission_or_population_histories"] != 0 or
        signed["new_biological_offspring_or_population_futures"] != 0 or
        founder["new_biological_futures_or_sustained_events"] != 0):
        raise ValueError("Retrospective source only; actual biological futures not admitted")

    idx0={(x["artificial_source_pool"],x["visitor_context"],x["co_carriers_m"]):x
          for x in variance["rows"]}
    idx1={(x["synthetic_source_pool"],x["visitor_context"],x["co_carriers_m"]):x
          for x in signed["rows"]}
    idx2={(x["synthetic_source_pool"],x["visitor_context"],x["co_carriers_m"]):x
          for x in founder["rows"]}
    if (len(idx0),len(idx1),len(idx2))!=(192,192,192) or set(idx0)!=set(idx1) or set(idx1)!=set(idx2):
        raise ValueError("Paired source/context/m key domain failed")
    summary=[]
    for context in (0,3,4):
        sign_delta=[]
        founder_delta=[]
        founder_m0_positive=0
        founder_up=founder_down=founder_ties=0
        signed_m0_outcross_pos=0
        for pool in range(16):
            key=lambda m:(pool,context,m)
            a0,a12=idx0[key(0)],idx0[key(12)]
            s0,s12=idx1[key(0)],idx1[key(12)]
            f0,f12=idx2[key(0)],idx2[key(12)]
            for value in (
                "expected_first_offspring_variance_A",
                "expected_first_offspring_variance_I",
            ):
                if abs(a0[value]-a12[value])>2e-14:
                    raise ValueError("Single-trait F1 variance no longer matched")
            for value in (
                "p_A_above_selected_parent_midpoint",
                "p_I_below_selected_parent_midpoint",
            ):
                if abs(s0[value]-s12[value])>2e-14:
                    raise ValueError("Signed single-trait F1 deviation no longer matched")
            for value in (
                "p_one_offspring_A_at_least_plus_0p05",
                "p_one_offspring_I_at_most_minus_0p05",
            ):
                if abs(f0[value]-f12[value])>2e-14:
                    raise ValueError("Founder-referenced one-child marginal tails no longer matched")
            ds=s12["p_A_up_and_I_down"]-s0["p_A_up_and_I_down"]
            df=f12["p_one_offspring_both_0p05_thresholds"]-f0["p_one_offspring_both_0p05_thresholds"]
            sign_delta.append(ds)
            founder_delta.append(df)
            founder_m0_positive+=f0["p_one_offspring_both_0p05_thresholds"]>0
            founder_up+=df>1e-14
            founder_down+=df< -1e-14
            founder_ties+=abs(df)<=1e-14
            signed_m0_outcross_pos+=s0["p_A_up_and_I_down_from_outcross_parent_pair"]>0
            if ds <= 0:
                raise ValueError("m12 co-carriage did not raise signed midpoint deviations under stated context")
            for m in (0,12):
                s=idx1[key(m)]
                if s["p_A_up_and_I_down"]!=s["p_A_up_and_I_up"]:
                    raise ValueError("Joint sign quadrants show unexpected directional bias")
                if abs(s["p_A_up_and_I_down"] - s["p_A_up_and_I_down_from_selfed_parent_pair"]
                       -s["p_A_up_and_I_down_from_outcross_parent_pair"])>2e-14:
                    raise ValueError("Self/outcross parental source partition failed")
        summary.append({
            "visitor_context":context,
            "artificial_source_profiles":16,
            "m12_minus_m0_signed_parent_midpoint_A_up_I_down_min":min(sign_delta),
            "m12_minus_m0_signed_parent_midpoint_A_up_I_down_max":max(sign_delta),
            "m12_minus_m0_founder_mean_single_child_Aplus_Iminus_min":min(founder_delta),
            "m12_minus_m0_founder_mean_single_child_Aplus_Iminus_max":max(founder_delta),
            "founder_mean_one_child_positive_contrast_count":founder_up,
            "founder_mean_one_child_negative_contrast_count":founder_down,
            "founder_mean_one_child_tie_count":founder_ties,
            "founder_mean_m0_one_child_both_thresholds_positive_count":founder_m0_positive,
            "signed_m0_from_outcross_positive_source_count":signed_m0_outcross_pos,
            "signed_joint_directional_contrast_positive_source_count":sum(d>0 for d in sign_delta),
        })
    if (summary[0]["founder_mean_one_child_positive_contrast_count"]!=5 or
        summary[0]["founder_mean_one_child_negative_contrast_count"]!=11 or
        summary[0]["founder_mean_m0_one_child_both_thresholds_positive_count"]!=15 or
        summary[0]["signed_m0_from_outcross_positive_source_count"]!=0 or
        any(row["signed_joint_directional_contrast_positive_source_count"]!=16 for row in summary) or
        any(row["signed_m0_from_outcross_positive_source_count"]!=16 for row in summary[1:])):
        raise ValueError("Previously checked structural sign/source constraints no longer reproduce")

    return {
        "schema":"chapter2_pr512_source_bound_claim_gate_v1",
        "source_status":"ORIGINAL_MODEL3_OPERATOR_ON_EXPLICIT_SYNTHETIC_T0_ONLY",
        "new_biological_histories":0,
        "observed_natural_islands":0,
        "t0_source_profiles":16,
        "source_context_m_combinations":192,
        "admitted_claims":[
            "With artificial quartet-balanced source phenotypes, both traits' t0 marginal expected F1 variation is unchanged across m",
            "m=12 versus m=0 raises signed two-locus first-offspring departures from selected parent midpoints across all 16 artificial source profiles in each original ecological context",
            "Context0 founder-relative single-offspring A+0.05/I-0.05 occurrence contrasts have 5 positive and 11 negative source-profile differences",
            "An individual first-offspring founder-relative threshold and any parental-midpoint signed genotype deviation do not identify a sustained evolving population-mean order",
        ],
        "excluded_claims":[
            "A/I co-carriage promotes adaptation or produces a directional selection advantage",
            "An island founder bottleneck is sufficient to reverse the long-run evolutionary order",
            "Original 1,536 genetic-access pilot tests this co-carriage intervention",
            "A-first causes improved island population survival",
            "These 16 artificial source inputs are empirically independent natural island lineages",
        ],
        "order_score_D":"NOT_MEASURED_NO_BIOLOGICAL_FUTURES",
        "sustained_twenty_occupied_census_response":"NOT_MEASURED",
        "population_persistence_Q4":"NOT_MEASURED",
        "context_summary":summary,
    }


if __name__=="__main__":
    print(json.dumps(claim_gate(),ensure_ascii=False,indent=2,sort_keys=True))
