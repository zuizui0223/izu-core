#!/usr/bin/env python3
"""Exact no-biology mathematical audit for a proposed founder-access design."""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/design/chapter2_colonisation_genetic_access_draft_20261014.json"


def validate(data: dict) -> None:
    if data.get("status") != "DESIGN_CANDIDATE_NO_EXECUTION_NO_CONFIRMATION":
        raise ValueError("This is a design-only, non-confirmatory proposal")
    source = data["illustrative_mainland_source"]
    if source.get("real_observed_mainland_data") is not False:
        raise ValueError("Virtual mainland source falsely claimed as empirical")
    if (source.get("adults"), source.get("A_heterozygote_adults"),
            source.get("A_neutral_homozygote_adults")) != (48, 12, 36):
        raise ValueError("The illustrative source pool changed")
    if source.get("expressed_A_for_every_adult") != 0.5:
        raise ValueError("The source adult A phenotype is not matched")
    if data.get("candidate_founder_samples") != [2, 8, 24, 48]:
        raise ValueError("Unexpected founding sample counts")
    control = data["controlled_genetic_only"]
    if (control["initial_plant_census"], control["carrying_capacity"],
            control["all_adult_expressed_A"]) != (48, 48, 0.5):
        raise ValueError("The fixed-census genetic control has changed")
    if data["naturalistic_founder_sample"]["source_pool_heterogeneity_mandatory"] is not True:
        raise ValueError("Genetically homogeneous A source would not test this question")
    target = data["outcome"]
    if (target["response_increment_A"], target["response_increment_I"],
            target["sustained_occupied_censuses"],
            target["near_simultaneous_cutoff"]) != (0.05, -0.05, 20, 5):
        raise ValueError("Original biological outcome definition changed")
    if target["classes"] != ["assurance_first", "investment_first",
                              "near_simultaneous", "assurance_only",
                              "investment_only", "neither"]:
        raise ValueError("Six-class readout labels changed")
    approval = data["approval"]
    if (approval.get("author_approval_for_new_biology") is not False or
            approval.get("new_biological_histories") != 0 or
            approval.get("source_genotypes_and_rng_frozen") is not False):
        raise ValueError("No biological execution or scientific permission was granted")


def no_heterozygote_probability(source_count: int, heterozygotes: int, founders: int) -> Fraction:
    if not (0 <= heterozygotes <= source_count and 0 <= founders <= source_count):
        raise ValueError("Impossible founder sample")
    if founders > source_count - heterozygotes:
        return Fraction(0)
    return Fraction(comb(source_count - heterozygotes, founders),
                    comb(source_count, founders))


def ideal_segregation_variance(h: Fraction, q: Fraction) -> Fraction:
    """Unselected Mendelian ideal q*h*h/2; not an empirical Model3 output."""
    if h <= 0 or q < 0 or q > 1:
        raise ValueError("Invalid ideal-genotype proportion or allele width")
    return q * h * h / 2


def report(data: dict) -> dict:
    validate(data)
    source = data["illustrative_mainland_source"]
    n, k = source["adults"], source["A_heterozygote_adults"]
    p = [no_heterozygote_probability(n, k, draw) for draw in data["candidate_founder_samples"]]
    halfwidths = [Fraction(str(v)) for v in data["controlled_genetic_only"]["halfwidths"]]
    fractions = [Fraction(str(v)) for v in data["controlled_genetic_only"]["heterozygote_fractions"]]
    if halfwidths != [Fraction(1,16), Fraction(1,8)] or fractions != [Fraction(1,4), Fraction(1)]:
        raise ValueError("Illustrative variance/support test was modified")
    cells = [
        {"h": float(h), "q": float(q), "ideal_F1_A_variance": float(ideal_segregation_variance(h, q)),
         "mutation_free_0p05_individual_support": h >= Fraction(1,20)}
        for h in halfwidths for q in fractions
    ]
    if ideal_segregation_variance(halfwidths[0], fractions[1]) != ideal_segregation_variance(halfwidths[1],fractions[0]):
        raise ValueError("The matched-variance negative control is no longer matched")
    return {
        "status": data["status"],
        "biology_histories_run": 0,
        "type": "MATHEMATICAL_ILLUSTRATION_NOT_BIOLOGICAL_RESULT",
        "p_original_A_heterozygote_total_loss": [
            {"founders": founders, "exact": str(chance), "decimal": float(chance)}
            for founders, chance in zip(data["candidate_founder_samples"], p)
        ],
        "A_support_vs_ideal_variance_cells": cells,
        "this_does_not_identify_selection_vs_drift_or_speed_mediation": True,
    }


def main() -> None:
    print(json.dumps(report(json.loads(SPEC.read_text(encoding="utf-8"))),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
