"""Q2 six-class source aggregation: average paired class vectors BEFORE distance.

READ ONLY, source-authenticated *upstream* data-contract validation only.
Neither these functions nor their tests produce biological histories, claim
authenticated raw-genome archives, or perform an evolutionary simulation.

Averages over genuinely independent source-genotype clusters are the
appropriate estimand; the number of histories nested within source is NOT
the number of independent sources. This file is deliberately downstream of
paired_source_level_class_contrasts, which checks source fingerprints,
paired m=0/12 categories, history counts and six-class completeness.

TV(average difference vector) is NOT average(TV(source differences)).
The first is population-averaged arm separation; the latter describes the
conditional within-source separation even if source effects cancel.
"""
from __future__ import annotations

from math import fsum, isfinite

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    CLASSES, OLD_CONTEXTS, paired_source_level_class_contrasts,
)

TOL = 1e-12


def aggregate_validated_source_vectors(validated:dict)->dict:
    """Aggregate an existing validated source-record contract, no raw data.

    This call alone does not verify the original annual genotypes, source
    provenance, true independence or ecological meaning. Refuse a naked
    hand-assembled pseudo-contract; use the public raw-category entrypoint
    to validate paired row structure immediately before aggregation.
    """
    if (not isinstance(validated,dict)
        or validated.get("status")!="CATEGORICAL_PAIRED_SOURCE_CLUSTER_SCHEMA_ONLY"
        or validated.get("no_source_genotypes_or_futures_generated") is not True
        or validated.get("hash_validation_is_not_independence_proof") is not True):
        raise ValueError("Not an admitted source-level six-class category contract")
    n=validated.get("independent_source_clusters")
    source_rows=validated.get("source_records")
    if type(n) is not int or n<2 or not isinstance(source_rows,list):
        raise ValueError("At least two distinctly identified source clusters required")
    expected_records=n*len(OLD_CONTEXTS)
    if len(source_rows)!=expected_records:
        raise ValueError("Incomplete source by ecological context grid")
    by_context={ctx:{} for ctx in OLD_CONTEXTS}
    for record in source_rows:
        if (not isinstance(record,dict)
            or set(record)!={
                "source_id","context","paired_histories",
                "six_class_probability_differences_m12_minus_m0",
                "secondary_order_score_D_difference",
            } or type(record["source_id"]) is not str
            or not record["source_id"]
            or type(record["context"]) is not int
            or record["context"] not in OLD_CONTEXTS):
            raise ValueError("Malformed source-level category difference vector")
        contrast=record["six_class_probability_differences_m12_minus_m0"]
        if (not isinstance(contrast,dict)
            or set(contrast)!=set(CLASSES)
            or any(type(v) not in (int,float) or not isfinite(v)
                   or abs(v)>1+TOL for v in contrast.values())
            or abs(fsum(contrast.values()))>TOL
            or .5*fsum(abs(contrast[c]) for c in CLASSES)>1+TOL
            or type(record["paired_histories"]) is not int
            or record["paired_histories"]!=validated.get("paired_histories_per_source")):
            raise ValueError("Source-specific six-class difference violates probability closure")
        d=contrast["assurance_first"]-contrast["investment_first"]
        if (type(record["secondary_order_score_D_difference"]) not in (int,float)
            or not isfinite(record["secondary_order_score_D_difference"])
            or abs(record["secondary_order_score_D_difference"]-d)>TOL):
            raise ValueError("Source-specific order score not induced by six categories")
        ctx=record["context"]
        source=record["source_id"]
        if source in by_context[ctx]:
            raise ValueError("Source duplicated within visitor-context arm comparison")
        by_context[ctx][source]=record

    source_roster=set(by_context[OLD_CONTEXTS[0]])
    if (len(source_roster)!=n
        or any(set(by_context[ctx])!=source_roster for ctx in OLD_CONTEXTS)):
        raise ValueError("Different source roster across visitor ecology contexts")

    summaries=[]
    for ctx in OLD_CONTEXTS:
        records=[by_context[ctx][source] for source in sorted(source_roster)]
        pooled={k:fsum(r["six_class_probability_differences_m12_minus_m0"][k]
                        for r in records)/n for k in CLASSES}
        source_distances=[
            .5*fsum(abs(r["six_class_probability_differences_m12_minus_m0"][k])
                    for k in CLASSES) for r in records
        ]
        pooled_tv=.5*fsum(abs(pooled[k]) for k in CLASSES)
        conditional_tv=fsum(source_distances)/n
        gap=conditional_tv-pooled_tv
        mean_d=fsum(r["secondary_order_score_D_difference"]
                    for r in records)/n
        if (abs(fsum(pooled.values()))>TOL
            or pooled_tv>1+TOL
            or conditional_tv>1+TOL
            or gap < -TOL
            or abs(mean_d-(pooled["assurance_first"]-
                            pooled["investment_first"]))>TOL):
            raise AssertionError("TV convexity or source-mean order-score identity violated")
        summaries.append({
            "original_visitor_context":ctx,
            "source_clusters":n,
            "primary_source_averaged_six_class_probability_difference_m12_minus_m0":pooled,
            "primary_vector_sums_to_zero":abs(fsum(pooled.values()))<=TOL,
            "secondary_D_from_aggregated_vector":mean_d,
            "population_averaged_arm_total_variation_after_source_aggregation":pooled_tv,
            "mean_source_conditional_total_variation_BEFORE_source_aggregation":conditional_tv,
            "source_effect_cancellation_gap":max(0.,gap),
            "source_conditional_total_variation_min":min(source_distances),
            "source_conditional_total_variation_max":max(source_distances),
            "source_D_positive_count":sum(
                r["secondary_order_score_D_difference"]>TOL for r in records),
            "source_D_negative_count":sum(
                r["secondary_order_score_D_difference"]< -TOL for r in records),
            "source_D_zero_within_tolerance_count":sum(
                abs(r["secondary_order_score_D_difference"])<=TOL for r in records),
        })
    return {
        "schema":"chapter2_Q2_source_aggregated_original_six_class_v1",
        "status":"SOURCE_LEVEL_SIX_CLASS_VECTOR_ARITHMETIC_ONLY",
        "new_biological_futures_generated":0,
        "raw_genomes_or_genuine_source_independence_verified":False,
        "required_upstream_validation":"source genome archive -> 201 census means -> exact six-class readback -> paired source/history categories",
        "number_source_clusters_assumed_distinct":n,
        "n_paired_histories_per_source":validated["paired_histories_per_source"],
        "six_classes_in_original_order":list(CLASSES),
        "primary_estimand":"source-mean signed vector of six class-probability contrasts, by ecology",
        "secondary_contrasts":["D score by ecology","population-level TV after source averaging","mean source-conditional TV as heterogeneity"],
        "no_p_values_or_simultaneous_intervals":True,
        "no_Q2_sustained_response_confirmed":True,
        "no_Q4_persistence_inference":True,
        "interpretation":[
            "Mean source-conditional TV may be large even if the population-averaged arm difference is exactly zero",
            "The population TV is computed AFTER taking source means of the full six-class vectors",
            "Mean source-conditional TV is reported separately as a source-heterogeneity diagnostic, never substituted for the pooled-population estimand",
            "The full six-category probability vector is primary. TV and D are secondary, not new posthoc outcome families",
            "Different hashes do not prove true source independence or provide raw Model3 genomics provenance",
            "This tool only aggregates supplied categories and has not produced biological data",
        ],
        "original_visitor_context_summaries":summaries,
    }


def aggregate_supplied_paired_six_class_rows(rows:list[dict])->dict:
    """All row-level pairing and six-category guards run before aggregation."""
    validated=paired_source_level_class_contrasts(rows)
    return aggregate_validated_source_vectors(validated)


if __name__=="__main__":
    raise SystemExit(
        "No registered Q2 co-carriage futures exist. "
        "Pass only already source-verified and replayed categories."
    )
