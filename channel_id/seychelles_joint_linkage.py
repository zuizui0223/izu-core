"""Audit individual-level exposure/dependency overlap in the Seychelles Thespesia source.

The raw source tables are not redistributed here. This module consumes a small
source-derived plant ledger whose rows retain the exact census/breeding IDs,
visitor-group counts and Auto/Xenogamy fruit outcomes needed for the audit.

The purpose is to distinguish three statements that must not be collapsed:
1. raw individual-level exposure + dependency measurements can coexist;
2. an analyst-derived visitor-group diversity metric is not automatically Izu FDQ;
3. raw overlap therefore does not by itself identify a cross-lineage
   dependency x functional-exposure coefficient.
"""
from __future__ import annotations

import csv
import itertools
import math
from pathlib import Path


def load_joint_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 8:
        raise ValueError("expected 8 Thespesia plants with census + Auto + Xenogamy coverage")
    for row in rows:
        norm = row["plant_id_normalized"]
        if row["plant_id_raw_census"] != f"ID{norm}":
            raise ValueError(f"unsafe census ID normalization for {norm}")
        if row["plant_id_raw_breeding"] != norm:
            raise ValueError(f"unsafe breeding ID normalization for {norm}")
    return rows


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(values):
        j = i
        while j + 1 < len(values) and values[order[j + 1]] == values[order[i]]:
            j += 1
        rank = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = rank
        i = j + 1
    return ranks


def _pearson(x: list[float], y: list[float]) -> float:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    dx = [value - mean_x for value in x]
    dy = [value - mean_y for value in y]
    denominator = math.sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    if denominator == 0:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / denominator


def spearman(x: list[float], y: list[float]) -> float:
    return _pearson(_ranks(x), _ranks(y))


def exact_permutation_test(x: list[float], y: list[float]) -> dict[str, float | int]:
    """Two-sided exact permutation p while collapsing duplicate y assignments.

    Duplicate y values make many of the n! permutations identical. Each unique
    assignment has the same multiplicity, so evaluating the unique assignments
    gives the same exact p while avoiding repeated work. ``permutations`` still
    reports the conceptual n! randomization count used by the original audit.
    """
    observed = spearman(x, y)
    unique_permutations = set(itertools.permutations(y))
    extreme = sum(
        abs(spearman(x, list(permutation))) >= abs(observed) - 1e-12
        for permutation in unique_permutations
    )
    return {
        "spearman_rho": observed,
        "two_sided_exact_permutation_p": extreme / len(unique_permutations),
        "permutations": math.factorial(len(y)),
    }


def build_report(rows: list[dict[str, str]]) -> dict[str, object]:
    auto_successes = sum(int(row["auto_successes"]) for row in rows)
    auto_n = sum(int(row["auto_n"]) for row in rows)
    xeno_successes = sum(int(row["xeno_successes"]) for row in rows)
    xeno_n = sum(int(row["xeno_n"]) for row in rows)

    dependency_difference = [float(row["dependency_difference_xeno_minus_auto"]) for row in rows]
    metrics = (
        "visits_per_flower_hour",
        "functional_group_shannon",
        "functional_group_gini_simpson",
        "vertebrate_visit_share",
    )
    diagnostics = {
        metric: exact_permutation_test(
            [float(row[metric]) for row in rows],
            dependency_difference,
        )
        for metric in metrics
    }

    full_auto = 3 / 39
    full_xeno = 15 / 30
    return {
        "schema_version": "1.0",
        "analysis": "seychelles_individual_joint_audit",
        "source": {
            "article_doi": "10.1002/ajb2.1499",
            "dataset_doi": "10.6084/m9.figshare.12029580.v2",
            "github_artifact_run": 31944425554,
            "github_artifact_id": 9262914774,
            "artifact_digest": "sha256:c335b92482ee65774904d5c1296cf7a12f95d1ebb7977e155e22bc861d73fa78",
            "taxon": "Thespesia populnea",
            "raw_id_rule": "census ID{integer} is linked only to breeding {integer}; no fuzzy matching",
        },
        "raw_linkage": {
            "census_unique_plants": 16,
            "breeding_unique_plants": 14,
            "normalized_census_breeding_overlap": 12,
            "plants_with_census_and_both_auto_xenogamy": 8,
            "raw_joint_measurement_exact": True,
        },
        "species_level_direct_dependency": {
            "full_species_auto_fruit": {"successes": 3, "n": 39, "proportion": full_auto},
            "full_species_xenogamy_fruit": {"successes": 15, "n": 30, "proportion": full_xeno},
            "auto_to_xenogamy_ratio": full_auto / full_xeno,
            "dependency_shortfall_one_minus_ratio": 1 - full_auto / full_xeno,
            "estimand": "1 - autonomous fruit-set proportion / xenogamy fruit-set proportion; source scale only",
        },
        "linked_eight_plant_scope": {
            "auto_fruit": {
                "successes": auto_successes,
                "n": auto_n,
                "proportion": auto_successes / auto_n,
            },
            "xenogamy_fruit": {
                "successes": xeno_successes,
                "n": xeno_n,
                "proportion": xeno_successes / xeno_n,
            },
            "dependency_metric_for_diagnostic": "plant-level xenogamy proportion minus autonomous proportion",
            "functional_exposure_metrics": {
                "visits_per_flower_hour": "direct quantity from four source visitor columns",
                "functional_group_shannon": "derived exploratory diversity over Insects/Sunbird/Fody/Skink counts",
                "functional_group_gini_simpson": "derived exploratory diversity over the same four groups",
                "vertebrate_visit_share": "derived exploratory share of Sunbird+Fody+Skink visits",
            },
            "association_diagnostics": diagnostics,
        },
        "decision": {
            "raw_individual_exposure_dependency_overlap": "identified",
            "harmonized_fdq_like_functional_exposure": "not_identified",
            "within_lineage_dependency_moderation_signal": "not_detected_in_small_exploratory_diagnostic",
            "cross_lineage_dependency_x_functional_exposure": "not_identified",
        },
        "scientific_reading": (
            "The previous panel-level matrix hid a real individual-level linkage: eight Thespesia plants "
            "have census exposure plus both Auto and Xenogamy fruit outcomes after an exact ID-prefix "
            "normalization. This upgrades raw joint measurement, not the cross-lineage moderation claim. "
            "Broad visitor-group diversity metrics are analyst-derived and are not equivalent to Izu FDQ; "
            "the n=8 exploratory permutation diagnostics show no clear exposure-dependency association and "
            "are too small/sparse to falsify the moderator hypothesis."
        ),
        "next_gate": (
            "Keep Issue #91 as the prospective Izu joint design. Use the Seychelles linkage as an external "
            "raw-architecture prototype; do not treat it as a harmonized second FDQ-like replicate until an "
            "exposure estimand is prespecified and made comparable across systems."
        ),
        "claim_boundary": (
            "No external dependency magnitude is transported to Izu. No FDQ is reconstructed from coarse "
            "Seychelles visitor groups. Plant-level flower observations are subsamples, and the exact "
            "permutation diagnostics are exploratory within one lineage, not a cross-system test."
        ),
    }
