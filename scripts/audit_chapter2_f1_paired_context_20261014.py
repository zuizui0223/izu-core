#!/usr/bin/env python3
"""Read-only paired-context audit of source-verified original 2,304 Model3 histories.

No model execution, parameter fitting, retuning, or inferential p-values.
Inputs are original-case summaries already independently replayed from raw genomes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/first_meiosis_access_20261014/data/results/chapter2_original_first_meiosis_access_2304_case_20261014.csv"
SOURCE_GIT_BLOB = "ea2c4009fc77cc59813dda0142e8da73c33a26fd"
FOUNDERS = ("main", "confirmation")
CONTEXTS = range(9)
REPLICATES = range(128)
CATEGORIES = {
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
}
FIELDS = [
    "case", "founder", "original_context", "replicate", "N_first_offspring",
    "A_t0_expressed_variance", "A_t1_expressed_variance",
    "A_t1_any_individual_above_0p05", "A_F1_A_mutated_offspring",
    "A_F1_has_unmutated_individual_above0p05", "A_transient_first",
    "I_transient_first", "A_sustained_first", "I_sustained_first",
    "category", "A_f1_mean_change",
]
F1_FIELDS = [
    "N_first_offspring", "A_t0_expressed_variance",
    "A_t1_expressed_variance", "A_t1_any_individual_above_0p05",
    "A_F1_A_mutated_offspring",
    "A_F1_has_unmutated_individual_above0p05", "A_f1_mean_change",
]


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def audit_bytes(raw: bytes, *, require_pinned_blob: bool = True) -> dict:
    blob = git_blob_sha1(raw)
    if require_pinned_blob and blob != SOURCE_GIT_BLOB:
        raise ValueError(f"Source bytes differ from admitted original CSV blob: {blob}")

    reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
    if reader.fieldnames != FIELDS:
        raise ValueError("Original CSV schema changed")
    rows = list(reader)
    if len(rows) != 2304:
        raise ValueError(f"Expected 2304 original cases; got {len(rows)}")

    by_key = {}
    all_category_counts = Counter()
    n_no_A_mutation_at_f1 = 0
    for row in rows:
        try:
            founder = row["founder"]
            context = int(row["original_context"])
            replicate = int(row["replicate"])
            n_first = int(row["N_first_offspring"])
            mut_count = int(row["A_F1_A_mutated_offspring"])
            v0 = float(row["A_t0_expressed_variance"])
            v1 = float(row["A_t1_expressed_variance"])
            delta = float(row["A_f1_mean_change"])
        except (TypeError, ValueError) as err:
            raise ValueError("Invalid original-case numeric or identifying field") from err

        key = (founder, context, replicate)
        if (founder not in FOUNDERS or context not in CONTEXTS
                or replicate not in REPLICATES):
            raise ValueError(f"Unexpected founder/context/replicate: {key}")
        if row["case"] != f"{founder}_c{context}_r{replicate}":
            raise ValueError(f"Case ID disagrees with source labels: {row['case']}")
        if key in by_key:
            raise ValueError(f"Duplicate case: {key}")
        if (n_first != 48 or mut_count < 0 or not math.isfinite(v0)
                or v0 != 0.0 or not math.isfinite(v1) or v1 <= 0
                or not math.isfinite(delta)):
            raise ValueError(f"Invalid F1 source state: {key}")
        if (row["A_t1_any_individual_above_0p05"] != "True"
                or row["A_F1_has_unmutated_individual_above0p05"] != "True"):
            raise ValueError(f"Unexpected first-offspring A access: {key}")

        category = row["category"]
        if category not in CATEGORIES:
            raise ValueError(f"Unrecognized original six-class category: {category}")
        has_A = bool(row["A_sustained_first"])
        has_I = bool(row["I_sustained_first"])
        expected_presence = {
            "assurance_first": (True, True),
            "investment_first": (True, True),
            "near_simultaneous": (True, True),
            "assurance_only": (True, False),
            "investment_only": (False, True),
            "neither": (False, False),
        }
        if (has_A, has_I) != expected_presence[category]:
            raise ValueError(f"Sustained-event presence disagrees with category: {key}")
        for field in ("A_transient_first", "I_transient_first",
                      "A_sustained_first", "I_sustained_first"):
            if row[field] and not (0 <= int(row[field]) <= 200):
                raise ValueError(f"Invalid original event year: {key}/{field}")
        by_key[key] = row
        all_category_counts[category] += 1
        n_no_A_mutation_at_f1 += (mut_count == 0)

    expected_keys = {
        (founder, context, replicate)
        for founder in FOUNDERS for context in CONTEXTS
        for replicate in REPLICATES
    }
    if set(by_key) != expected_keys:
        raise ValueError("Original 2x9x128 domain incomplete or substituted")

    counts_by_distinct_category = Counter()
    varied_category = varied_A = varied_I = identical_f1 = 0
    by_founder = {}
    invariant_pairs = []
    for founder in FOUNDERS:
        group_stats = {
            "paired_clusters": 0, "different_category": 0,
            "different_A_sustained_incidence": 0,
            "different_I_sustained_incidence": 0,
        }
        for replicate in REPLICATES:
            members = [by_key[(founder, c, replicate)] for c in CONTEXTS]
            f1_signatures = {
                tuple(row[field] for field in F1_FIELDS) for row in members
            }
            if len(f1_signatures) != 1:
                raise ValueError(f"First-offspring A summary varies by context: {founder}/{replicate}")
            identical_f1 += 1
            distinct_category = len({row["category"] for row in members})
            counts_by_distinct_category[distinct_category] += 1
            differs_category = distinct_category > 1
            differs_A = len({bool(row["A_sustained_first"]) for row in members}) > 1
            differs_I = len({bool(row["I_sustained_first"]) for row in members}) > 1
            varied_category += differs_category
            varied_A += differs_A
            varied_I += differs_I
            group_stats["paired_clusters"] += 1
            group_stats["different_category"] += differs_category
            group_stats["different_A_sustained_incidence"] += differs_A
            group_stats["different_I_sustained_incidence"] += differs_I
            if not differs_category:
                invariant_pairs.append(f"{founder}_r{replicate}")
        by_founder[founder] = group_stats

    return {
        "status": "SOURCE_LOCKED_POST_OUTCOME_DESCRIPTIVE_NOT_CAUSAL",
        "source_git_blob": blob,
        "original_case_rows": len(rows),
        "original_founder_by_context_cells": len(FOUNDERS) * len(CONTEXTS),
        "paired_founder_by_replicate_clusters": len(FOUNDERS) * len(REPLICATES),
        "identical_7_field_F1_A_signatures_across_all_9_contexts": identical_f1,
        "different_six_class_outcome_across_contexts": varied_category,
        "different_A_sustained_incidence_across_contexts": varied_A,
        "different_I_sustained_incidence_across_contexts": varied_I,
        "number_of_distinct_categories_within_pair": {
            str(n): counts_by_distinct_category[n] for n in range(1, 7)
        },
        "pairs_with_identical_six_class_category": invariant_pairs,
        "A_F1_zero_flagged_mutant_offspring_cases": n_no_A_mutation_at_f1,
        "original_six_class_counts": {
            category: all_category_counts[category] for category in sorted(CATEGORIES)
        },
        "by_founder": by_founder,
        "limitations": [
            "F1 A summaries are not full F1 genotypes or all-locus state equality",
            "The repeated visitor settings and common RNG streams are paired, not 2304 independent natural units",
            "Post-outcome descriptive audit, no prospective clock/p-value/causal decomposition",
            "Original 1536-case prospective pilot is a separate cohort, not pooled here",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    args = parser.parse_args()
    print(json.dumps(audit_bytes(args.source.read_bytes()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
