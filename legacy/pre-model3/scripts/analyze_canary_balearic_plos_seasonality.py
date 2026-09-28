#!/usr/bin/env python3
"""Summarise selected-species seasonality in the open Canary–Balearic source.

The recovered PLOS package contains monthly partner-trait summaries for species
selected from extreme linkage or selectiveness classes. It does not contain the
complete plant-by-visitor interaction matrices. This analysis therefore remains
a within-source descriptive screen:

1. calculate first-to-last observed-month changes within species x community x
   selection class;
2. average repeated community changes within species before uncertainty is
   calculated;
3. summarise medians with species-cluster bootstrap intervals and exact sign
   tests;
4. control the 24 domain x class x partner-trait screening families with the
   Benjamini-Hochberg procedure.

None of these rows is eligible for a cross-archipelago effect model.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Iterable, Mapping, Sequence


METRICS = (
    "partner_functional_richness",
    "partner_rank_abundance",
    "partner_abundance_evenness",
)
PROFILE_COLUMNS = (
    "resolved_domain",
    "specificity",
    "metric",
    "n_species",
    "n_species_community_units",
    "median_first_last_delta",
    "bootstrap_ci_low",
    "bootstrap_ci_high",
    "mean_first_last_delta",
    "negative_species",
    "positive_species",
    "tied_species",
    "exact_sign_test_two_sided",
    "bh_q_value",
    "median_direction",
    "row_role",
    "cross_system_model_eligible",
    "causal_claim_allowed",
)


def optional_float(value: object) -> float | None:
    text = str(value or "").strip()
    if not text:
        return None
    number = float(text)
    if not math.isfinite(number):
        raise ValueError(f"value must be finite: {value!r}")
    return number


def load_rows(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "resolved_domain",
            "specificity",
            "zone",
            "species_code",
            "month_index",
            *METRICS,
        }
        missing = sorted(required - set(reader.fieldnames or ()))
        if missing:
            raise ValueError(f"input is missing required columns: {missing}")
        rows: list[dict[str, object]] = []
        for line_number, source in enumerate(reader, start=2):
            row = dict(source)
            row["month_index"] = int(str(source["month_index"]).strip())
            if row["month_index"] not in {1, 2, 3, 4}:
                raise ValueError(
                    f"unexpected relative month on input line {line_number}: "
                    f"{row['month_index']!r}"
                )
            for metric in METRICS:
                row[metric] = optional_float(source.get(metric))
            rows.append(row)
    if not rows:
        raise ValueError("seasonality analysis requires at least one input row")
    return rows


def first_last_community_deltas(
    rows: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[
        tuple[str, str, str, str], list[Mapping[str, object]]
    ] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row["resolved_domain"]),
                str(row["specificity"]),
                str(row["zone"]),
                str(row["species_code"]),
            )
        ].append(row)

    output: list[dict[str, object]] = []
    for (domain, specificity, zone, species_code), group in sorted(grouped.items()):
        for metric in METRICS:
            by_month: dict[int, list[float]] = defaultdict(list)
            for row in group:
                value = row.get(metric)
                if value is not None:
                    by_month[int(row["month_index"])].append(float(value))
            months = sorted(by_month)
            if len(months) < 2:
                continue
            first_month = months[0]
            last_month = months[-1]
            first_value = mean(by_month[first_month])
            last_value = mean(by_month[last_month])
            output.append(
                {
                    "resolved_domain": domain,
                    "specificity": specificity,
                    "zone": zone,
                    "species_code": species_code,
                    "metric": metric,
                    "first_month": first_month,
                    "last_month": last_month,
                    "first_value": first_value,
                    "last_value": last_value,
                    "delta": last_value - first_value,
                }
            )
    if not output:
        raise ValueError("no species-community unit had two observed months")
    return output


def aggregate_species_deltas(
    rows: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[
        tuple[str, str, str, str], list[Mapping[str, object]]
    ] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row["resolved_domain"]),
                str(row["specificity"]),
                str(row["species_code"]),
                str(row["metric"]),
            )
        ].append(row)
    output: list[dict[str, object]] = []
    for (domain, specificity, species_code, metric), group in sorted(grouped.items()):
        output.append(
            {
                "resolved_domain": domain,
                "specificity": specificity,
                "species_code": species_code,
                "metric": metric,
                "n_communities": len({str(row["zone"]) for row in group}),
                "delta": mean(float(row["delta"]) for row in group),
            }
        )
    return output


def exact_two_sided_sign_test(negative: int, positive: int) -> float | None:
    if negative < 0 or positive < 0:
        raise ValueError("sign counts must be non-negative")
    n = negative + positive
    if n == 0:
        return None
    smaller = min(negative, positive)
    probability = 2.0 * sum(
        math.comb(n, index) for index in range(smaller + 1)
    ) / (2**n)
    return min(1.0, probability)


def percentile(sorted_values: Sequence[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires values")
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between zero and one")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return (
        float(sorted_values[lower]) * (1.0 - fraction)
        + float(sorted_values[upper]) * fraction
    )


def bootstrap_median_interval(
    values: Sequence[float],
    *,
    repetitions: int,
    seed: int,
) -> tuple[float, float]:
    if not values:
        raise ValueError("bootstrap requires values")
    if repetitions < 100:
        raise ValueError("bootstrap repetitions must be at least 100")
    generator = random.Random(seed)
    n = len(values)
    estimates = sorted(
        median(values[generator.randrange(n)] for _ in range(n))
        for _ in range(repetitions)
    )
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def stable_seed(parts: Iterable[str]) -> int:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def benjamini_hochberg(p_values: Sequence[float | None]) -> list[float | None]:
    indexed = [
        (index, float(value))
        for index, value in enumerate(p_values)
        if value is not None
    ]
    if not indexed:
        return [None for _ in p_values]
    indexed.sort(key=lambda item: item[1])
    m = len(indexed)
    adjusted: dict[int, float] = {}
    running = 1.0
    for rank_index in range(m - 1, -1, -1):
        original_index, value = indexed[rank_index]
        rank = rank_index + 1
        running = min(running, value * m / rank)
        adjusted[original_index] = min(1.0, running)
    return [adjusted.get(index) for index in range(len(p_values))]


def build_profiles(
    input_rows: Sequence[Mapping[str, object]],
    *,
    bootstrap_repetitions: int = 10_000,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    community_rows = first_last_community_deltas(input_rows)
    species_rows = aggregate_species_deltas(community_rows)
    grouped: dict[tuple[str, str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in species_rows:
        grouped[
            (
                str(row["resolved_domain"]),
                str(row["specificity"]),
                str(row["metric"]),
            )
        ].append(row)
    community_counts = Counter(
        (
            str(row["resolved_domain"]),
            str(row["specificity"]),
            str(row["metric"]),
        )
        for row in community_rows
    )

    profiles: list[dict[str, object]] = []
    p_values: list[float | None] = []
    for (domain, specificity, metric), group in sorted(grouped.items()):
        values = [float(row["delta"]) for row in group]
        negative = sum(value < -1e-12 for value in values)
        positive = sum(value > 1e-12 for value in values)
        tied = len(values) - negative - positive
        sign_probability = exact_two_sided_sign_test(negative, positive)
        ci_low, ci_high = bootstrap_median_interval(
            values,
            repetitions=bootstrap_repetitions,
            seed=stable_seed((domain, specificity, metric)),
        )
        centre = median(values)
        direction = "positive" if centre > 0 else "negative" if centre < 0 else "zero"
        profiles.append(
            {
                "resolved_domain": domain,
                "specificity": specificity,
                "metric": metric,
                "n_species": len(values),
                "n_species_community_units": community_counts[
                    (domain, specificity, metric)
                ],
                "median_first_last_delta": centre,
                "bootstrap_ci_low": ci_low,
                "bootstrap_ci_high": ci_high,
                "mean_first_last_delta": mean(values),
                "negative_species": negative,
                "positive_species": positive,
                "tied_species": tied,
                "exact_sign_test_two_sided": sign_probability,
                "bh_q_value": None,
                "median_direction": direction,
                "row_role": "selected_species_within_source_descriptive",
                "cross_system_model_eligible": "no",
                "causal_claim_allowed": "no",
            }
        )
        p_values.append(sign_probability)

    adjusted = benjamini_hochberg(p_values)
    for profile, q_value in zip(profiles, adjusted):
        profile["bh_q_value"] = q_value

    domains = sorted({str(row["resolved_domain"]) for row in input_rows})
    species_by_domain = {
        domain: len(
            {
                str(row["species_code"])
                for row in input_rows
                if row["resolved_domain"] == domain
            }
        )
        for domain in domains
    }
    nominal = [
        profile
        for profile in profiles
        if profile["exact_sign_test_two_sided"] is not None
        and float(profile["exact_sign_test_two_sided"]) < 0.05
    ]
    multiplicity_robust = [
        profile
        for profile in profiles
        if profile["bh_q_value"] is not None
        and float(profile["bh_q_value"]) < 0.05
    ]
    finite_q = [
        float(profile["bh_q_value"])
        for profile in profiles
        if profile["bh_q_value"] is not None
    ]
    summary = {
        "schema_version": "1.0",
        "status": "selected_species_seasonality_screen_complete",
        "source_id": "castro_urgal_traveset_2016_plos_same_communities",
        "article_doi": "10.1371/journal.pone.0150824",
        "target_source_id": "castro_urgal_traveset_2014_canary_balearic_networks",
        "target_article_doi": "10.1111/boj.12134",
        "n_input_rows": len(input_rows),
        "unique_species_codes_by_domain": species_by_domain,
        "n_species_community_delta_rows": len(community_rows),
        "n_species_level_delta_rows": len(species_rows),
        "n_profile_rows": len(profiles),
        "bootstrap_repetitions": bootstrap_repetitions,
        "n_nominal_sign_tests_below_0_05": len(nominal),
        "n_bh_q_values_below_0_05": len(multiplicity_robust),
        "minimum_bh_q_value": min(finite_q) if finite_q else None,
        "nominal_profile_keys": [
            {
                "resolved_domain": profile["resolved_domain"],
                "specificity": profile["specificity"],
                "metric": profile["metric"],
                "median_first_last_delta": profile["median_first_last_delta"],
                "exact_sign_test_two_sided": profile[
                    "exact_sign_test_two_sided"
                ],
                "bh_q_value": profile["bh_q_value"],
            }
            for profile in nominal
        ],
        "raw_interaction_edges_available": False,
        "full_network_matrix_available": False,
        "effect_registry_eligible": False,
        "selection_boundary": (
            "Species were deliberately selected from extreme linkage or "
            "selectiveness classes and had to occur in at least two temporal "
            "networks. Generalized/specialized and opportunistic/selective are "
            "overlapping selection axes, so the 24 profile rows are not "
            "independent biological replicates."
        ),
        "independence_boundary": (
            "First-last changes are calculated within species x community x "
            "selection class, then averaged within species across communities. "
            "Monthly rows are repeated observations; two communities on one "
            "island do not create independent geological-origin replicates."
        ),
        "reading": (
            f"The selected-species screen produced {len(nominal)} nominal "
            f"sign-test results below 0.05 across {len(profiles)} profile "
            f"families, but {len(multiplicity_robust)} remained below a "
            "Benjamini-Hochberg q-value of 0.05. The source therefore supports "
            "heterogeneous seasonal partner-trait trajectories, not a common "
            "multiplicity-robust direction or a geological-origin effect."
        ),
        "claim_boundary": (
            "This is a selected-species, within-source seasonal description. "
            "It does not reconstruct plant-by-visitor edges, estimate a full "
            "network response, measure pollinator effectiveness or effective "
            "dependency, or identify continental-versus-oceanic island "
            "causation."
        ),
    }
    return profiles, summary


def write_profiles(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROFILE_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/results/canary_balearic/plos_derived_partner_traits.csv"
        ),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path(
            "data/results/canary_balearic/"
            "plos_selected_species_seasonality.csv"
        ),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path(
            "data/results/canary_balearic/"
            "plos_selected_species_seasonality_summary.json"
        ),
    )
    parser.add_argument("--bootstrap-repetitions", type=int, default=10_000)
    args = parser.parse_args()

    rows = load_rows(args.input)
    profiles, summary = build_profiles(
        rows,
        bootstrap_repetitions=args.bootstrap_repetitions,
    )
    write_profiles(args.output_csv, profiles)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"input rows: {summary['n_input_rows']}")
    print(f"profile rows: {summary['n_profile_rows']}")
    print(
        "BH q < 0.05: "
        f"{summary['n_bh_q_values_below_0_05']}"
    )
    print(args.summary_output)


if __name__ == "__main__":
    main()
