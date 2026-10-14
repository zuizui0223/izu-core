"""Candidate independent-source-cluster precision and no-go audit for Q2.

This is an EXACT finite-sample Hoeffding + union bound for bounded paired
SOURCE-level contrasts. NOT statistical power, effect prediction, a justified
number of natural islands, a registered cohort, or authority to run Model3.
Only the old frozen class vocabulary & threshold definitions are consulted.
"""
from __future__ import annotations

import json
from math import ceil, log, sqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT / "data/design/chapter2_Q2_cocarriage_review_only_20261014.json"
OLD_CONTEXTS=(0,3,4)
ARMS=(0,12)
CLASSES=(
    "assurance_first","investment_first","near_simultaneous",
    "assurance_only","investment_only","neither",
)
POSSIBLE_ALLOCATIONS=((16,16),(32,8),(64,4),(128,2),(256,1))
ALPHA=0.05
NUM_SIX_CLASS_CONTRASTS=3*6
NUM_D_CONTRASTS=3
EPSILON_LEVELS=(0.1,0.15,0.2,0.25,0.3)
EXPECTED_SOURCE_HEAD="3d98f8330472c4101aef1ae29280f0bb334dca45"


def independent_source_hoeffding_required(
        eps:float, simultaneous_contrasts:int, bound_halfwidth:float)->int:
    """Union-bound 95% confidence radius, no Gaussian variance assumptions.

    The paired source-level contrast X_s lies in [-b,b], and S *genuinely*
    independent source clusters are required:
       Pr(any contrast misses by eps) <= 2*K exp(-S eps^2/(2*b^2))
    This is conservative and describes precision, NOT test power.
    """
    if (type(eps) not in (float,int) or eps<=0 or eps>2*bound_halfwidth
            or type(simultaneous_contrasts) is not int
            or simultaneous_contrasts<1
            or type(bound_halfwidth) not in (int,float)
            or bound_halfwidth<=0):
        raise ValueError("Valid positive epsilon, family size and bound required")
    return ceil((2*bound_halfwidth**2)*log(2*simultaneous_contrasts/ALPHA)/eps**2)


def independent_source_hoeffding_radius(
        independent_sources:int, simultaneous_contrasts:int, bound_halfwidth:float
)->float:
    if (type(independent_sources) is not int or independent_sources<=0
            or type(simultaneous_contrasts) is not int
            or simultaneous_contrasts<=0
            or bound_halfwidth<=0):
        raise ValueError("Invalid independent source budget")
    return sqrt((2*bound_halfwidth**2)*log(
        2*simultaneous_contrasts/ALPHA)/independent_sources)


def verify_review_design(d:dict)->dict:
    if (d.get("status")!="UNREGISTERED_Q2_DESIGN_REVIEW_ONLY" or
        d.get("experimental_author_approval") is not False or
        d.get("biological_histories_generated") !=0 or
        d.get("may_launch_model3_histories") is not False or
        d.get("full_future_rng_registry_status") != "NOT_REGISTERED" or
        d.get("source_distribution_approved") is not False or
        d.get("observed_natural_islands") != 0 or
        d.get("source_pr512_head")!=EXPECTED_SOURCE_HEAD or
        d.get("original_model3_biology_sha")!="328548612e93469fcc8663f24548530a57399b9a" or
        d.get("original_model3_mutation_traits")!=[False,False,True] or
        d.get("independent_scientific_review_complete") is not False or
        d.get("source_pool_counts_are_options_not_approved") is not True or
        d.get("actual_launch_case_budget")!="NOT_REGISTERED" or
        d.get("original_archival_raw_genomes_and_independent_readback")!="REQUIRED_BEFORE_LAUNCH" or
        tuple(d.get("original_visitor_contexts",()))!=OLD_CONTEXTS or
        tuple(d.get("co_carriage_arms",()))!=ARMS or
        tuple(d.get("original_six_classes",()))!=CLASSES or
        d.get("response_A_founder_mean_delta")!=0.05 or
        d.get("response_I_founder_mean_delta")!=-0.05 or
        d.get("sustained_occupied_censuses") != 20 or
        d.get("near_simultaneous_window_updates")!=5 or
        d.get("original_model_updates")!=200 or
        d.get("t0_census")!=48 or
        d.get("carrying_capacity")!=48 or
        tuple(tuple(x) for x in d.get("illustrative_allocations",()))!=POSSIBLE_ALLOCATIONS or
        d.get("primary_outcome")!="full_six_class_probability_vector_by_visitor_context" or
        d.get("D_contrast_status")!="SECONDARY_UNDIRECTIONED" or
        d.get("suppress_future_seed_generation") is not True):
        raise ValueError("Not a frozen no-execution Q2 design-review candidate")
    rows=[]
    base_case_count=None
    for S,H in POSSIBLE_ALLOCATIONS:
        cases=S*H*len(OLD_CONTEXTS)*len(ARMS)
        if base_case_count is None:base_case_count=cases
        if cases!=base_case_count:
            raise ValueError("Candidate compute budgets not directly comparable")
        rows.append({
            "independent_artificial_source_genotype_inputs":S,
            "paired_stochastic_histories_per_source":H,
            "technical_only_cases_if_executed":cases,
            "conditional_future_update_calls_if_authorized":cases*200,
            "source_clusters_for_uncertainty":S,
            "source_level_maximum_95pct_familywise_halfwidth_for_one_class":
                independent_source_hoeffding_radius(S,NUM_SIX_CLASS_CONTRASTS,1),
            "source_level_maximum_95pct_familywise_halfwidth_for_D":
                independent_source_hoeffding_radius(S,NUM_D_CONTRASTS,2),
        })
    tables=[]
    for eps in EPSILON_LEVELS:
        tables.append({
            "target_halfwidth":eps,
            "n_independent_sources_for_all_18_six_class_probability_differences":
                independent_source_hoeffding_required(eps,NUM_SIX_CLASS_CONTRASTS,1),
            "n_independent_sources_for_three_secondary_D_differences":
                independent_source_hoeffding_required(eps,NUM_D_CONTRASTS,2),
        })
    return {
        "status":"REVIEW_ONLY_BOUNDED_SOURCE_CLUSTER_PRECISION_NOT_POWER",
        "biological_simulations_executed":0,
        "approved_stochastic_history_seeds":0,
        "distinct_independent_source_unit":"One independently drawn synthetic source-genotype realization",
        "paired_arm_unit":"Co-carriage m0 vs m12 within same source × history × visitor context",
        "source_cluster_estimands": {
            "class_contrast":"source-level within-ecology average over matched future-history differences of six-category onehot indicators, in [-1,+1]",
            "secondary_D_contrast":"source-level average over matched future-history differences of Afirst-minus-Ifirst score in [-2,+2]",
        },
        "independence_assumption":"Independent source-genotype realizations and between-source RNG; shared random numbers allowed ONLY within a matched source/history across arms/context",
        "not_a_power_analysis":"Hoeffding union bounds do not estimate a nonzero effect, variance, detection power or required real sample size",
        "familywise_confidence_level":0.95,
        "simultaneous_family_sizes":{"class_by_context":18,"D_by_context":3},
        "candidate_equal_compute_allocations":rows,
        "conservative_independent_source_precision_targets":tables,
        "preserved_scientific_no_go":[
            "No new source population distribution selected on biological/ecological evidence",
            "The 16 old synthetic source fixtures are technical pilots, not 16 independent observed islands",
            "Total scenarios 1536 per candidate are not registered production trajectories",
            "No empirical co-carriage long-run order effect size exists for source-cluster power",
            "Existing 1536 historical A-width genotype-access pilot is a DIFFERENT intervention",
            "Original Model3 mutation mask, population fitness/survival and raw-genome source remain unchanged",
            "New source seeds, future histories, raw genome archive and author execution approval remain unavailable",
        ],
    }



def paired_source_level_class_contrasts(rows:list[dict])->dict:
    """Validate a possible future *data schema* with six-class labels.

    This does not load/run or synthesize biology: only supplied categorical
    labels are checked. Caller is responsible for authenticated full-genome
    replays and original sustained-event classification BEFORE this step.
    """
    if not isinstance(rows,list) or not rows:
        raise ValueError("No paired categorized future rows supplied")
    expected_fields={"source_id","history_id","future_master_identity",
                     "context","m","category","extinct_by_horizon"}
    by_key={}
    future_identity_by_cluster={}
    histories={}
    for row in rows:
        if (not isinstance(row,dict) or set(row)!=expected_fields
            or type(row["source_id"]) is not str or not row["source_id"]
            or type(row["history_id"]) is not str or not row["history_id"]
            or type(row["future_master_identity"]) is not str
            or not row["future_master_identity"]
            or type(row["context"]) is not int or row["context"] not in OLD_CONTEXTS
            or type(row["m"]) is not int or row["m"] not in ARMS
            or row["category"] not in CLASSES
            or type(row["extinct_by_horizon"]) is not bool):
            raise ValueError("Incomplete original six-class paired source data contract")
        cluster=(row["source_id"],row["history_id"])
        key=cluster+(row["context"],row["m"])
        if key in by_key:
            raise ValueError("Duplicated source/history/context/arm future")
        by_key[key]=row
        histories.setdefault(row["source_id"],set()).add(row["history_id"])
        prior=future_identity_by_cluster.setdefault(
            cluster,row["future_master_identity"]
        )
        if prior!=row["future_master_identity"]:
            raise ValueError("Arms/visitor contexts do not use same paired future master")
    # A master seed belongs to exactly one independent source × history;
    # identical random streams are used ONLY within its paired treatment cells.
    if len(set(future_identity_by_cluster.values()))!=len(future_identity_by_cluster):
        raise ValueError("Future random master reused across independent source histories")
    required={(ctx,arm) for ctx in OLD_CONTEXTS for arm in ARMS}
    for source in histories:
        for history in histories[source]:
            seen={(ctx,m) for (s,h,ctx,m) in by_key if (s,h)==(source,history)}
            if seen!=required:
                raise ValueError("Missing ecology/arm in paired independent source/history unit")
    sizes=set(map(len,histories.values()))
    if len(sizes)!=1:
        raise ValueError("Different future history counts per source require preregistered weights")
    n_histories=sizes.pop()
    source_records=[]
    for source in sorted(histories):
        for context in OLD_CONTEXTS:
            differences={}
            for klass in CLASSES:
                lo=sum(by_key[(source,h,context,ARMS[0])]["category"]==klass
                       for h in histories[source])/n_histories
                hi=sum(by_key[(source,h,context,ARMS[1])]["category"]==klass
                       for h in histories[source])/n_histories
                differences[klass]=hi-lo
            if abs(sum(differences.values()))>1e-12:
                raise AssertionError("All six-class frequencies do not sum to one per arm")
            source_records.append({
                "source_id":source,"context":context,
                "paired_histories":n_histories,
                "six_class_probability_differences_m12_minus_m0":differences,
                "secondary_order_score_D_difference":
                    differences["assurance_first"]-differences["investment_first"],
            })
    return {
        "status":"CATEGORICAL_PAIRED_SOURCE_CLUSTER_SCHEMA_ONLY",
        "already_given_rows":len(rows),
        "independent_source_clusters":len(histories),
        "paired_histories_per_source":n_histories,
        "source_by_context_contrasts":len(source_records),
        "not_an_event_reader":"Original raw-genome event classification must be verified separately",
        "no_source_genotypes_or_futures_generated":True,
        "source_records":source_records,
    }

def read_review_design()->dict:
    return verify_review_design(json.loads(DESIGN.read_text(encoding="utf-8")))


if __name__=="__main__":
    print(json.dumps(read_review_design(),sort_keys=True,indent=2))
