"""Pre-execution Q2 between-source vs within-source allocation accounting.

Pure variance identities for PRE-SPECIFIED bounded source-cluster contrasts.
No new populations, offspring, RNG seeds, histories, p-values, or permission
for the Model3 biological simulator. Illustrative variance components below
are deliberately hypothetical; the co-carriage Q2 future data do not exist.

For one visitor-context/one class, let X_{s,h} = m12 class indicator minus
m0 class indicator from paired source s and future history h. For genuinely
independent source pools and conditionally independent future histories:
    B = Var(E[X | source]), W = E[Var(X | source)]
    Var(mean paired contrast) = B/S + W/(S H).
The second term is shared across allocations at fixed S*H; the between-
source term improves strictly with S if B>0. Different visitor-context/class
contrasts may be correlated; this is NOT a 18-endpoint simultaneous CI or a
power analysis. 
"""
from __future__ import annotations

import json
from math import isfinite, sqrt

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    POSSIBLE_ALLOCATIONS,
    read_review_design,
)

STATUS="REVIEW_ONLY_Q2_SOURCE_VARIANCE_ALLOCATION_NOT_POWER"
HYPOTHETICAL_COMPONENTS={
    "zero_between_source_difference": {"between":0.0,"within":0.25},
    "small_between_source_difference": {"between":0.01,"within":0.25},
    "moderate_between_source_difference": {"between":0.04,"within":0.25},
}


def allocation_variance(
    independent_sources:int, paired_histories_per_source:int,
    variance_between_sources:float, variance_within_sources:float
)->dict:
    """Exact law-of-total-variance accounting, with stated assumptions."""
    s,h=independent_sources,paired_histories_per_source
    b,w=variance_between_sources,variance_within_sources
    if (type(s) is not int or type(h) is not int or
        s<1 or h<1 or
        type(b) not in (int,float) or type(w) not in (int,float) or
        not isfinite(b) or not isfinite(w) or
        min(b,w)<0 or b+w>1+1e-12):
        raise ValueError("Bounded class-difference variance components and genuine source/history counts required")
    between=b/s
    within=w/(s*h)
    return {
        "genuinely_independent_source_clusters":s,
        "paired_future_histories_nested_per_source":h,
        "total_source_history_pairs":s*h,
        "between_source_component_of_mean_variance":between,
        "within_source_component_of_mean_variance":within,
        "total_mean_variance":between+within,
        "illustrative_standard_error_not_a_CONFIRMED_SE":sqrt(between+within),
    }


def source_cluster_se_from_supplied_paired_differences(
    source_history_differences:list[list[float]],
)->dict:
    """Descriptive cluster-SE template for already validated [-1,1] contrasts.

    Do not feed this function raw model outputs directly. It assumes all six
    class labels and original source provenance were admitted by the upstream
    source-authenticated annual readout and paired-history validators.
    """
    rows=source_history_differences
    if not isinstance(rows,list) or len(rows)<2 or not all(
        isinstance(row,list) and row and len(row)==len(rows[0]) for row in rows
    ):
        raise ValueError("At least two independent source clusters with equal positive histories required")
    means=[]
    for row in rows:
        if any(type(x) not in (int,float) or not isfinite(x) or x < -1 or x > 1 for x in row):
            raise ValueError("Only finite already paired one-class differences in [-1,1] admitted")
        means.append(sum(row)/len(row))
    S=len(means)
    overall=sum(means)/S
    sample_between_mean_variance=sum((x-overall)**2 for x in means)/(S-1)
    return {
        "status":"SUPPLIED_CLUSTER_CONTRAST_DESCRIPTIVE_ONLY_NO_SOURCE_PROVENANCE_CHECK",
        "number_of_source_clusters_ASSUMED_inDEPENDENT":S,
        "paired_histories_per_source":len(rows[0]),
        "mean_paired_one_class_contrast":overall,
        "empirical_variance_of_source_mean_contrasts":sample_between_mean_variance,
        "descriptive_source_cluster_standard_error":sqrt(sample_between_mean_variance/S),
        "not_a_simultaneous_confidence_interval_or_power_result":True,
        "raw_genotypes_and_model_futures_generated":0,
    }



def source_overhead_cost_tradeoff(
    variance_between_sources:float,
    variance_within_sources:float,
    cost_per_verified_source:float,
    cost_per_paired_history_bundle:float,
)->dict:
    """Continuous S,H review with source-validation overhead, NOT an approved optimum.

    Suppose C = S*(c_source + H*c_history), with c_history priced as
    ONE matched m0/m12 history bundle across the same three ecologies.
    Substituting S=C/(c_source+H*c_history) in Var(mean):
      C*Var(mean) = B*c_source + W*c_history
                    + B*c_history*H + W*c_source/H.
    For B>0, W>0, c_source>0, interior Hstar =
        sqrt(W*c_source/(B*c_history)).
    But biological replication requires INTEGER S and H>=1 and at least
    two source clusters for empirical cluster uncertainty. The source/visitor
    input, archive cost, true B,W and external validation are all unavailable.
    """
    b,w,c_source,c_hist=(variance_between_sources,variance_within_sources,
                         cost_per_verified_source,cost_per_paired_history_bundle)
    if any(type(x) not in (float,int) or not isfinite(x) for x in (
            b,w,c_source,c_hist)) or min(b,w,c_source)<0 or c_hist<=0 or b+w>1+1e-12:
        raise ValueError("Finite nonnegative hypothetical variance and source cost, positive future-bundle cost required")
    if b==0:
        optimal_h=None
        interpretation=(
            "If between-source variance B=0 and source overhead is positive, "
            "greater H improves fixed-cost precision; without overhead all "
            "allocations have same variance at equal bundled-history cost"
        )
    elif w==0 or c_source==0:
        optimal_h=1.0
        interpretation=(
            "One conditional history per source minimizes the continuous "
            "fixed-cost objective under zero W or zero source overhead"
        )
    else:
        optimal_h=max(1.0,sqrt(w*c_source/(b*c_hist)))
        interpretation=(
            "Continuous interior optimum, NOT an integer executable design; "
            "requires measured B, W and actual per-source/time-history cost"
        )
    return {
        "status":"HYPOTHETICAL_COST_ADJUSTED_SOURCE_ALLOCATION_NOT_APPROVED",
        "hypothetical_B_between":b,
        "hypothetical_W_within":w,
        "hypothetical_verified_source_overhead":c_source,
        "hypothetical_paired_six_path_bundle_cost":c_hist,
        "continuous_history_count_per_source":optimal_h,
        "interpretation":interpretation,
        "cost_definition":"C=S*(c_source+H*c_history), c_history includes both co-carriage arms and all three visitor contexts",
        "fixed_cost_times_variance_identity":
            "C Var(mean)=(B+W/H)*(c_source+H*c_history)",
        "not_a_source_distribution_effect_estimate":True,
        "biological_futures_or_source_production":0,
    }


def technical_report()->dict:
    source_contract=read_review_design()
    if (source_contract["status"]!="REVIEW_ONLY_BOUNDED_SOURCE_CLUSTER_PRECISION_NOT_POWER"
        or source_contract["biological_simulations_executed"]!=0
        or tuple((a["independent_artificial_source_genotype_inputs"],
                  a["paired_stochastic_histories_per_source"])
                 for a in source_contract["candidate_equal_compute_allocations"])!=POSSIBLE_ALLOCATIONS):
        raise ValueError("Existing unapproved source-cluster allocations changed")
    rows=[]
    for name,components in HYPOTHETICAL_COMPONENTS.items():
        for s,h in POSSIBLE_ALLOCATIONS:
            out=allocation_variance(s,h,components["between"],components["within"])
            rows.append({
                "variance_assumption_name":name,
                "hypothetical_between_source_variance":components["between"],
                "hypothetical_within_source_variance":components["within"],
                "hypothetical_model_NOT_empirical":True,
                "future_model3_paths_IF_AUTHORIZED":s*h*2*3,
                **out,
            })
    # At fixed independent source/history *product*, B/S shrinks if B>0.
    for name,components in HYPOTHETICAL_COMPONENTS.items():
        group=[x for x in rows if x["variance_assumption_name"]==name]
        if len({x["total_source_history_pairs"] for x in group})!=1:
            raise AssertionError("Unequal hypothetical source-history budgets")
        within=[x["within_source_component_of_mean_variance"] for x in group]
        if max(within)-min(within)>1e-15:
            raise AssertionError("Within-history mean variance must be fixed at equal S*H")
        variance=[x["total_mean_variance"] for x in group]
        if components["between"]==0:
            if max(variance)-min(variance)>1e-15:
                raise AssertionError("All allocations should tie if between-source variance zero")
        elif any(variance[i+1]>=variance[i] for i in range(len(variance)-1)):
            raise AssertionError("Independent source count failed to reduce nonzero between-source component")
    return {
        "schema":"chapter2_Q2_source_allocation_between_within_variance_review_v0",
        "status":STATUS,
        "source": "Original unapproved Q2 source-cluster design manifest",
        "conditional_independence_assumption": (
            "Independent source-genotype realizations; conditionally iid paired stochastic "
            "history contrasts nested within each source, ecological setting and class"
        ),
        "pairing":"m0/m12 share a history within source. Different source clusters do not share future master seeds",
        "all_illustrative_future_histories_are_unrun":True,
        "new_model3_biological_histories":0,
        "approved_source_genotype_distribution":False,
        "empirical_between_source_variance_available":False,
        "empirical_within_source_variance_available":False,
        "allocation_approval":False,
        "mathematical_identity":"Var(grand_mean) = B/S + W/(S*H); B = Var(E[X|source]), W = E Var(X|source)",
        "estimand":"one original six-class category's m12-minus-m0 paired probability difference in one pollinator context",
        "multiple_contexts_and_classes":"Must be analyzed jointly by separate preregistered familywise uncertainty; not done here",
        "hypothetical_cost_overhead_sensitivity":[
            source_overhead_cost_tradeoff(b,.25,c,1.)
            for b,c in ((.04,1.),(.04,4.),(.04,16.),(.01,4.),(0.,4.))
        ],
        "illustrative_rows":rows,
        "limitations":[
            "B and W are hypothetical source/history variance components, not estimated co-carriage effects",
            "Fixed total simulated trajectories at equal S*H omit source-generation cost and within-source covariation across ecological contexts",
            "S=256,H=1 does not separately identify within-source variance from one history per pool, even though source-level total contrast variance can be estimated",
            "Strict variance improvement with larger S is only under the declared nested conditional independence model and B>0",
            "This does not supply power, an approved minimum ecological difference, preregistered source seeds or raw-genome custody",
            "The original 16 synthetic phenotype-strata inputs are not natural independent island populations",
        ],
    }


if __name__=="__main__":
    print(json.dumps(technical_report(),indent=2,sort_keys=True))
