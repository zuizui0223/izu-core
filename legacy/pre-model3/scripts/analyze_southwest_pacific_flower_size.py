#!/usr/bin/env python3
"""Analyse the source-native Southwest Pacific island-mainland flower pairs.

The analysis reads the exact ``Flower dataframe`` sheet from Supplementary Data
S2 without reconstructing values from figures.  It preserves the source-coded
pollination syndrome, reports the one unresolved syndrome as a sensitivity, and
keeps the released-workbook counts separate from the article's printed counts.

The main estimate is an ordinary-least-squares audit of
``LR = log10(FI / FM)`` against ``log10(FM)``.  Event, island-cluster and
family-cluster bootstrap intervals, leave-one-island sensitivities, a
log-island-on-log-mainland coupling check, and a standardized-major-axis method
sensitivity are reported.  These are morphology effects, not estimates of
pollinator effectiveness or effective dependency.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "pr": PKG_REL_NS}

EXPECTED_HEADERS = [
    "Pair number",
    "Family",
    "FI",
    "FM",
    "R",
    "LR",
    "Island",
    "Mainland",
    "Degree",
    "Unit of pollination",
    "Flower morphology",
    "Syndrome",
    "System",
    "Flo num",
    "FR",
    "LFR",
    "LI",
    "LM",
    "SI",
    "SM",
    "Mean of identification of sister taxa",
]


def column_index(reference: str) -> int:
    letters = "".join(character for character in reference if character.isalpha())
    value = 0
    for character in letters.upper():
        value = value * 26 + ord(character) - 64
    return value - 1


def parse_scalar(
    value: str | None,
    cell_type: str | None,
    shared_strings: Sequence[str],
) -> Any:
    if value is None:
        return None
    if cell_type == "s":
        return shared_strings[int(value)]
    if cell_type == "b":
        return value == "1"
    text = value.strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return text
    return int(number) if number.is_integer() else number


def read_xlsx_sheet(path: Path, sheet_name: str) -> list[list[Any]]:
    """Read values and cached formula results from one XLSX sheet."""
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", NS):
                shared_strings.append(
                    "".join(
                        node.text or "" for node in item.findall(".//m:t", NS)
                    )
                )

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(
            archive.read("xl/_rels/workbook.xml.rels")
        )
        relationship_targets = {
            relationship.attrib["Id"]: relationship.attrib["Target"]
            for relationship in relationships.findall("pr:Relationship", NS)
        }
        target: str | None = None
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            if sheet.attrib.get("name") == sheet_name:
                relationship_id = sheet.attrib[f"{{{REL_NS}}}id"]
                target = relationship_targets[relationship_id]
                break
        if target is None:
            raise ValueError(f"sheet not found: {sheet_name!r}")
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"

        sheet = ET.fromstring(archive.read(target))
        output: list[list[Any]] = []
        for source_row in sheet.findall("m:sheetData/m:row", NS):
            values: list[Any] = []
            for cell in source_row.findall("m:c", NS):
                index = column_index(cell.attrib.get("r", "A1"))
                while len(values) <= index:
                    values.append(None)
                cell_type = cell.attrib.get("t")
                if cell_type == "inlineStr":
                    parsed = "".join(
                        node.text or ""
                        for node in cell.findall(".//m:t", NS)
                    )
                else:
                    node = cell.find("m:v", NS)
                    parsed = parse_scalar(
                        node.text if node is not None else None,
                        cell_type,
                        shared_strings,
                    )
                values[index] = parsed
            output.append(values)
        return output


def clean_text(value: Any) -> str:
    return str(value or "").strip()


def numeric(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        result = float(value)
        return result if math.isfinite(result) else None
    text = str(value).strip().casefold()
    if text in {"", "n/a", "na", "none", "null", "-", "–", "—"}:
        return None
    try:
        result = float(text)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def category(value: Any) -> str:
    if value is None:
        return "unresolved"
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        number = float(value)
        return str(int(number)) if number.is_integer() else str(number)
    text = str(value).strip()
    return text if text else "unresolved"


def read_source_rows(path: Path) -> list[dict[str, Any]]:
    source = read_xlsx_sheet(path, "Flower dataframe")
    if not source:
        raise ValueError("the source sheet is empty")
    headers = [clean_text(value) for value in source[0]]
    if headers != EXPECTED_HEADERS:
        raise ValueError(f"unexpected source headers: {headers}")

    rows: list[dict[str, Any]] = []
    for raw_row in source[1:]:
        padded = list(raw_row) + [None] * (len(headers) - len(raw_row))
        row = dict(zip(headers, padded[: len(headers)]))
        pair_number = numeric(row["Pair number"])
        if pair_number is None:
            continue
        row["Pair number"] = int(pair_number)
        rows.append(row)
    if [row["Pair number"] for row in rows] != list(range(1, 130)):
        raise ValueError("source pair numbers are not exactly 1..129")
    return rows


def pollination_syndrome(row: Mapping[str, Any]) -> str:
    value = category(row.get("Syndrome")).casefold()
    if value in {"1", "animal", "yes"}:
        return "animal"
    if value in {"0", "wind", "no"}:
        return "wind"
    return "unresolved"


def valid_flower_size(row: Mapping[str, Any]) -> bool:
    island = numeric(row.get("FI"))
    mainland = numeric(row.get("FM"))
    log_ratio = numeric(row.get("LR"))
    return bool(
        island is not None
        and mainland is not None
        and log_ratio is not None
        and island > 0
        and mainland > 0
    )


def evidence_type(row: Mapping[str, Any]) -> str:
    return clean_text(row.get("Mean of identification of sister taxa")).casefold()


def model_vectors(
    rows: Sequence[Mapping[str, Any]],
    *,
    response: str = "LR",
) -> tuple[list[float], list[float]]:
    predictors: list[float] = []
    responses: list[float] = []
    for row in rows:
        mainland = numeric(row.get("FM"))
        outcome = numeric(row.get(response))
        if mainland is None or mainland <= 0 or outcome is None:
            continue
        predictors.append(math.log10(mainland))
        responses.append(outcome)
    return predictors, responses


def ordinary_least_squares(
    predictors: Sequence[float], responses: Sequence[float]
) -> dict[str, float | int | None]:
    if len(predictors) != len(responses) or len(predictors) < 3:
        raise ValueError("OLS requires at least three paired values")
    count = len(predictors)
    predictor_mean = statistics.fmean(predictors)
    response_mean = statistics.fmean(responses)
    predictor_ss = sum((value - predictor_mean) ** 2 for value in predictors)
    response_ss = sum((value - response_mean) ** 2 for value in responses)
    if predictor_ss <= 1e-15:
        raise ValueError("predictor has zero variance")
    cross_product = sum(
        (predictor - predictor_mean) * (response - response_mean)
        for predictor, response in zip(predictors, responses)
    )
    slope = cross_product / predictor_ss
    intercept = response_mean - slope * predictor_mean
    residual_ss = sum(
        (response - intercept - slope * predictor) ** 2
        for predictor, response in zip(predictors, responses)
    )
    slope_se = math.sqrt((residual_ss / (count - 2)) / predictor_ss)
    pearson_r = (
        cross_product / math.sqrt(predictor_ss * response_ss)
        if response_ss > 1e-15
        else math.nan
    )
    return {
        "n": count,
        "intercept": intercept,
        "slope": slope,
        "slope_se": slope_se,
        "pearson_r": pearson_r,
        "r_squared": pearson_r * pearson_r if math.isfinite(pearson_r) else None,
        "predictor_mean": predictor_mean,
        "response_mean": response_mean,
    }


def standard_major_axis(
    predictors: Sequence[float], responses: Sequence[float]
) -> dict[str, float | int]:
    if len(predictors) < 3:
        raise ValueError("SMA requires at least three paired values")
    ordinary = ordinary_least_squares(predictors, responses)
    correlation = float(ordinary["pearson_r"])
    predictor_sd = statistics.stdev(predictors)
    response_sd = statistics.stdev(responses)
    if predictor_sd <= 0 or response_sd <= 0 or not math.isfinite(correlation):
        raise ValueError("SMA is degenerate")
    slope = math.copysign(response_sd / predictor_sd, correlation)
    predictor_mean = statistics.fmean(predictors)
    response_mean = statistics.fmean(responses)
    return {
        "n": len(predictors),
        "intercept": response_mean - slope * predictor_mean,
        "slope": slope,
        "pearson_r": correlation,
    }


def percentile(sorted_values: Sequence[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires values")
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


def stable_seed(label: str) -> int:
    return int(hashlib.sha256(label.encode("utf-8")).hexdigest()[:16], 16)


def bootstrap_slope(
    rows: Sequence[Mapping[str, Any]],
    *,
    cluster: str | None,
    repetitions: int,
    seed_label: str,
) -> dict[str, Any]:
    if repetitions < 100:
        raise ValueError("bootstrap repetitions must be at least 100")
    source_rows = list(rows)
    random_generator = random.Random(stable_seed(seed_label))
    estimates: list[float] = []
    attempts = 0
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    cluster_keys: list[str] = []
    if cluster is not None:
        for row in source_rows:
            grouped[clean_text(row.get(cluster))].append(row)
        cluster_keys = sorted(grouped)

    while len(estimates) < repetitions and attempts < repetitions * 5:
        attempts += 1
        if cluster is None:
            sample = [
                source_rows[random_generator.randrange(len(source_rows))]
                for _ in source_rows
            ]
        else:
            sample = []
            for _ in cluster_keys:
                sample.extend(grouped[random_generator.choice(cluster_keys)])
        predictors, responses = model_vectors(sample)
        try:
            estimates.append(
                float(ordinary_least_squares(predictors, responses)["slope"])
            )
        except ValueError:
            continue

    if len(estimates) < max(100, repetitions // 2):
        raise RuntimeError("too few non-degenerate bootstrap replicates")
    estimates.sort()
    return {
        "repetitions_requested": repetitions,
        "repetitions_valid": len(estimates),
        "ci_95": [percentile(estimates, 0.025), percentile(estimates, 0.975)],
        "median": percentile(estimates, 0.5),
    }


def bootstrap_mean(
    values: Sequence[float], *, repetitions: int, seed_label: str
) -> dict[str, Any]:
    source = list(values)
    if not source:
        raise ValueError("mean bootstrap requires values")
    random_generator = random.Random(stable_seed(seed_label))
    count = len(source)
    estimates = sorted(
        statistics.fmean(
            source[random_generator.randrange(count)] for _ in range(count)
        )
        for _ in range(repetitions)
    )
    return {
        "n": count,
        "mean": statistics.fmean(source),
        "ci_95": [percentile(estimates, 0.025), percentile(estimates, 0.975)],
        "median_bootstrap_mean": percentile(estimates, 0.5),
    }


def leave_one_island(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    islands = sorted({clean_text(row.get("Island")) for row in rows})
    results: list[dict[str, Any]] = []
    for island in islands:
        subset = [row for row in rows if clean_text(row.get("Island")) != island]
        predictors, responses = model_vectors(subset)
        try:
            slope = float(ordinary_least_squares(predictors, responses)["slope"])
        except ValueError:
            continue
        results.append(
            {"island_omitted": island, "n": len(predictors), "slope": slope}
        )
    slopes = [float(result["slope"]) for result in results]
    return {
        "results": results,
        "range": [min(slopes), max(slopes)],
        "all_negative": all(value < 0 for value in slopes),
        "all_positive": all(value > 0 for value in slopes),
    }


def estimate_model(
    rows: Sequence[Mapping[str, Any]],
    *,
    label: str,
    repetitions: int,
) -> dict[str, Any]:
    admitted = [row for row in rows if valid_flower_size(row)]
    predictors, responses = model_vectors(admitted)
    if len(predictors) < 3:
        return {"status": "blocked_n_too_small", "n": len(predictors)}

    ordinary = ordinary_least_squares(predictors, responses)
    major_axis = standard_major_axis(predictors, responses)
    transformed: list[dict[str, Any]] = []
    coupling_predictors: list[float] = []
    coupling_responses: list[float] = []
    for row in admitted:
        island = float(numeric(row["FI"]))
        mainland = float(numeric(row["FM"]))
        coupling_predictors.append(math.log10(mainland))
        coupling_responses.append(math.log10(island))
        copy = dict(row)
        copy["LR"] = math.log10(island)
        transformed.append(copy)
    coupling = ordinary_least_squares(
        coupling_predictors, coupling_responses
    )
    event_bootstrap = bootstrap_slope(
        admitted,
        cluster=None,
        repetitions=repetitions,
        seed_label=f"{label}:event",
    )
    island_bootstrap = bootstrap_slope(
        admitted,
        cluster="Island",
        repetitions=repetitions,
        seed_label=f"{label}:island",
    )
    family_bootstrap = bootstrap_slope(
        admitted,
        cluster="Family",
        repetitions=repetitions,
        seed_label=f"{label}:family",
    )
    coupling_island_bootstrap = bootstrap_slope(
        transformed,
        cluster="Island",
        repetitions=repetitions,
        seed_label=f"{label}:coupling:island",
    )
    crossover = None
    if float(ordinary["slope"]) != 0:
        crossover = 10 ** (
            -float(ordinary["intercept"]) / float(ordinary["slope"])
        )
    return {
        "status": "estimated",
        "n": len(admitted),
        "islands": len({clean_text(row["Island"]) for row in admitted}),
        "families": len({clean_text(row["Family"]) for row in admitted}),
        "ols_fsLR_on_log10_mainland": ordinary,
        "standard_major_axis_fsLR_on_log10_mainland": major_axis,
        "predicted_isometry_crossover_mainland_mm": crossover,
        "event_bootstrap_slope": event_bootstrap,
        "island_cluster_bootstrap_slope": island_bootstrap,
        "family_cluster_bootstrap_slope": family_bootstrap,
        "leave_one_island": leave_one_island(admitted),
        "coupling_check_log10_island_on_log10_mainland": coupling,
        "coupling_check_island_cluster_bootstrap_slope": (
            coupling_island_bootstrap
        ),
        "mean_fsLR": bootstrap_mean(
            responses,
            repetitions=repetitions,
            seed_label=f"{label}:mean",
        ),
    }


def source_file_lock(path: Path) -> dict[str, Any]:
    files: dict[str, dict[str, Any]] = {}
    for candidate in sorted(path.parent.iterdir()):
        if candidate.is_file() and candidate.suffix.casefold() in {
            ".xlsx",
            ".docx",
        }:
            files[candidate.name] = {
                "size_bytes": candidate.stat().st_size,
                "sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
            }
    return {
        "schema_version": "1.0",
        "status": "source_files_checksum_locked",
        "source_id": "southwest_pacific_mainland_island_floral_pairs",
        "article_doi": "10.1093/aob/mcaf005",
        "pmcid": "PMC12445859",
        "acquisition_route": "oup_article_minimal_public_supplement_links",
        "analysis_file": path.name,
        "analysis_sheet": "Flower dataframe",
        "files": files,
    }


def write_subgroup_csv(path: Path, analysis: Mapping[str, Any]) -> None:
    records: list[dict[str, Any]] = []

    def collect(prefix: str, value: Mapping[str, Any]) -> None:
        if value.get("status") in {"estimated", "blocked_n_too_small"}:
            record: dict[str, Any] = {
                "group": prefix,
                "status": value.get("status"),
                "n": value.get("n"),
            }
            if value.get("status") == "estimated":
                record.update(
                    {
                        "ols_slope": value["ols_fsLR_on_log10_mainland"][
                            "slope"
                        ],
                        "ols_se": value["ols_fsLR_on_log10_mainland"][
                            "slope_se"
                        ],
                        "event_ci_low": value["event_bootstrap_slope"][
                            "ci_95"
                        ][0],
                        "event_ci_high": value["event_bootstrap_slope"][
                            "ci_95"
                        ][1],
                        "island_ci_low": value[
                            "island_cluster_bootstrap_slope"
                        ]["ci_95"][0],
                        "island_ci_high": value[
                            "island_cluster_bootstrap_slope"
                        ]["ci_95"][1],
                        "family_ci_low": value[
                            "family_cluster_bootstrap_slope"
                        ]["ci_95"][0],
                        "family_ci_high": value[
                            "family_cluster_bootstrap_slope"
                        ]["ci_95"][1],
                        "sma_slope": value[
                            "standard_major_axis_fsLR_on_log10_mainland"
                        ]["slope"],
                        "coupling_slope": value[
                            "coupling_check_log10_island_on_log10_mainland"
                        ]["slope"],
                    }
                )
            records.append(record)
            return
        for key, child in value.items():
            if isinstance(child, dict):
                collect(f"{prefix}/{key}" if prefix else key, child)

    collect("primary", analysis["primary_models"])
    collect("sensitivity", analysis["sensitivities"])
    columns = [
        "group",
        "status",
        "n",
        "ols_slope",
        "ols_se",
        "event_ci_low",
        "event_ci_high",
        "island_ci_low",
        "island_ci_high",
        "family_ci_low",
        "family_ci_high",
        "sma_slope",
        "coupling_slope",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)


def effect_document(analysis: Mapping[str, Any]) -> dict[str, Any]:
    animal = analysis["primary_models"]["animal_source_coded"]
    wind = analysis["primary_models"]["wind_source_coded"]
    display = analysis["animal_floral_display"]["mean_LFR"]
    common = {
        "system_id": "southwest_pacific_flower_size",
        "system_cluster": "southwest_pacific_ten_archipelagos",
        "row_role": "external_effect",
        "cross_system_model_eligible": True,
        "causal_claim_allowed": False,
    }
    return {
        "schema_version": "1.0",
        "status": "effect_rows_ready_single_external_morphology_system",
        "effects": [
            {
                **common,
                "effect_id": (
                    "southwest_pacific_animal_flower_size_starting_value_slope"
                ),
                "evidence_family": (
                    "animal_pollinated_island_mainland_"
                    "flower_size_starting_value_slope"
                ),
                "response": "flower_size_log10_response_ratio",
                "predictor_or_contrast": "log10 mainland flower size",
                "estimate": animal["ols_fsLR_on_log10_mainland"]["slope"],
                "uncertainty_type": (
                    "island_cluster_bootstrap_percentile_interval"
                ),
                "uncertainty_value": animal[
                    "island_cluster_bootstrap_slope"
                ]["ci_95"],
                "unit": (
                    "change in log10(FI/FM) per log10 mainland-mm unit"
                ),
                "independent_unit": (
                    "source-defined colonisation events nested in ten island groups"
                ),
                "admission_status": (
                    "empirical_numeric_effect_with_island_cluster_"
                    "uncertainty_single_system"
                ),
                "notes": (
                    "Eligible only for a future same-response starting-size "
                    "synthesis; not commensurate with visit-network effects or "
                    "effective dependency."
                ),
            },
            {
                **common,
                "effect_id": (
                    "southwest_pacific_wind_flower_size_starting_value_slope"
                ),
                "evidence_family": (
                    "wind_pollinated_island_mainland_"
                    "flower_size_starting_value_slope"
                ),
                "response": "flower_size_log10_response_ratio",
                "predictor_or_contrast": "log10 mainland flower size",
                "estimate": wind["ols_fsLR_on_log10_mainland"]["slope"],
                "uncertainty_type": (
                    "island_cluster_bootstrap_percentile_interval"
                ),
                "uncertainty_value": wind[
                    "island_cluster_bootstrap_slope"
                ]["ci_95"],
                "unit": (
                    "change in log10(FI/FM) per log10 mainland-mm unit"
                ),
                "independent_unit": (
                    "source-defined colonisation events nested in ten island groups"
                ),
                "admission_status": (
                    "empirical_numeric_effect_with_island_cluster_"
                    "uncertainty_single_system"
                ),
                "notes": (
                    "The interval overlaps zero in the source-coded transparent "
                    "reanalysis; no wind-gigantism mechanism is inferred."
                ),
            },
            {
                **common,
                "effect_id": (
                    "southwest_pacific_animal_floral_display_mean_log_ratio"
                ),
                "evidence_family": (
                    "animal_pollinated_island_mainland_"
                    "floral_display_mean_log_ratio"
                ),
                "response": "floral_display_log10_response_ratio",
                "predictor_or_contrast": "island versus mainland",
                "estimate": display["mean"],
                "uncertainty_type": (
                    "event_bootstrap_percentile_interval_for_mean"
                ),
                "uncertainty_value": display["ci_95"],
                "unit": "mean log10 island/mainland floral-display ratio",
                "independent_unit": (
                    "source-defined animal-pollinated colonisation events "
                    "with display data"
                ),
                "admission_status": (
                    "empirical_numeric_effect_with_event_"
                    "uncertainty_single_system"
                ),
                "notes": (
                    "Flower number and flower size combine into display; this "
                    "does not measure pollinator service or dependency."
                ),
            },
        ],
        "formal_cross_system_fit_ready": False,
        "claim_boundary": analysis["claim_boundary"],
    }


def run_analysis(
    source_path: Path,
    output_dir: Path,
    *,
    bootstrap_repetitions: int,
) -> dict[str, Any]:
    rows = read_source_rows(source_path)
    syndrome_counts = Counter(pollination_syndrome(row) for row in rows)
    valid_counts = Counter(
        pollination_syndrome(row) for row in rows if valid_flower_size(row)
    )
    formula_mismatches: list[int] = []
    for row in rows:
        island = numeric(row.get("FI"))
        mainland = numeric(row.get("FM"))
        log_ratio = numeric(row.get("LR"))
        if (
            island is not None
            and mainland is not None
            and island > 0
            and mainland > 0
            and log_ratio is not None
            and abs(log_ratio - math.log10(island / mainland)) > 1e-9
        ):
            formula_mismatches.append(int(row["Pair number"]))

    animal = [
        row
        for row in rows
        if pollination_syndrome(row) == "animal" and valid_flower_size(row)
    ]
    wind = [
        row
        for row in rows
        if pollination_syndrome(row) == "wind" and valid_flower_size(row)
    ]
    phylogenetic_animal = [
        row for row in animal if "phylogenetic" in evidence_type(row)
    ]
    phylogenetic_wind = [
        row for row in wind if "phylogenetic" in evidence_type(row)
    ]

    analysis: dict[str, Any] = {
        "schema_version": "1.0",
        "status": "source_native_129_pair_analysis_complete",
        "source_id": "southwest_pacific_mainland_island_floral_pairs",
        "article_doi": "10.1093/aob/mcaf005",
        "source_file": source_path.name,
        "source_file_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "source_sheet": "Flower dataframe",
        "n_source_rows": len(rows),
        "source_integrity": {
            "pair_numbers_exactly_1_to_129": True,
            "formula_lr_log10_fi_over_fm_mismatch_pair_numbers": (
                formula_mismatches
            ),
            "syndrome_counts": dict(syndrome_counts),
            "valid_size_counts_by_syndrome": dict(valid_counts),
            "invalid_or_missing_size_pair_numbers": [
                row["Pair number"] for row in rows if not valid_flower_size(row)
            ],
            "unresolved_syndrome_pair_numbers": [
                row["Pair number"]
                for row in rows
                if pollination_syndrome(row) == "unresolved"
            ],
            "paper_reported_counts": {
                "animal_pairs": 90,
                "wind_pairs": 39,
                "animal_analysis_n": 87,
                "wind_analysis_n": 36,
            },
            "source_count_discrepancy_retained": True,
            "count_alignment_reading": (
                "Assigning unresolved pair 54 to animal pollination reproduces "
                "the paper total of 90 animal pairs and display-data n=80. "
                "Transparent size-data counts remain 89 valid animal and 38 "
                "valid wind before any undocumented exclusions."
            ),
        },
        "response_definition": {
            "fsLR": "log10(mean island flower size / mean mainland flower size)",
            "predictor": "log10(mean mainland flower size in mm)",
            "coupling_check": (
                "log10(mean island flower size) ~ "
                "log10(mean mainland flower size)"
            ),
        },
        "primary_models": {
            "animal_source_coded": estimate_model(
                animal,
                label="animal source coded",
                repetitions=bootstrap_repetitions,
            ),
            "wind_source_coded": estimate_model(
                wind,
                label="wind source coded",
                repetitions=bootstrap_repetitions,
            ),
        },
        "sensitivities": {
            "phylogenetic_evidence_only": {
                "animal": estimate_model(
                    phylogenetic_animal,
                    label="animal phylogenetic",
                    repetitions=bootstrap_repetitions,
                ),
                "wind": estimate_model(
                    phylogenetic_wind,
                    label="wind phylogenetic",
                    repetitions=bootstrap_repetitions,
                ),
            },
            "animal_flower_morphology": {
                "actinomorphic_fused_petals_1": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Flower morphology")) == "1"
                    ],
                    label="animal morphology 1",
                    repetitions=bootstrap_repetitions,
                ),
                "actinomorphic_free_petals_2": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Flower morphology")) == "2"
                    ],
                    label="animal morphology 2",
                    repetitions=bootstrap_repetitions,
                ),
                "zygomorphic_3": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Flower morphology")) == "3"
                    ],
                    label="animal morphology 3",
                    repetitions=bootstrap_repetitions,
                ),
            },
            "animal_breeding_system": {
                "monomorphic_M": estimate_model(
                    [row for row in animal if category(row.get("System")) == "M"],
                    label="animal breeding M",
                    repetitions=bootstrap_repetitions,
                ),
                "dimorphic_D": estimate_model(
                    [row for row in animal if category(row.get("System")) == "D"],
                    label="animal breeding D",
                    repetitions=bootstrap_repetitions,
                ),
            },
            "animal_mainland_source": {
                "new_zealand_1": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Mainland")) == "1"
                    ],
                    label="animal mainland 1",
                    repetitions=bootstrap_repetitions,
                ),
                "australia_2": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Mainland")) == "2"
                    ],
                    label="animal mainland 2",
                    repetitions=bootstrap_repetitions,
                ),
            },
            "animal_taxonomic_degree": {
                "subspecies_0": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Degree")) == "0"
                    ],
                    label="animal degree 0",
                    repetitions=bootstrap_repetitions,
                ),
                "species_1": estimate_model(
                    [
                        row
                        for row in animal
                        if category(row.get("Degree")) == "1"
                    ],
                    label="animal degree 1",
                    repetitions=bootstrap_repetitions,
                ),
            },
        },
    }

    unresolved_valid = [
        row
        for row in rows
        if pollination_syndrome(row) == "unresolved" and valid_flower_size(row)
    ]
    analysis["sensitivities"]["assign_unresolved_syndrome_to_animal"] = {
        "pair_numbers": [row["Pair number"] for row in unresolved_valid],
        "model": estimate_model(
            animal + unresolved_valid,
            label="animal plus unresolved",
            repetitions=bootstrap_repetitions,
        ),
        "claim_boundary": (
            "The unresolved source syndrome is included only as an explicit "
            "sensitivity, never silently recoded."
        ),
    }

    display_values = [numeric(row.get("LFR")) for row in animal]
    display_values = [
        float(value) for value in display_values if value is not None
    ]
    analysis["animal_floral_display"] = {
        "n": len(display_values),
        "mean_LFR": bootstrap_mean(
            display_values,
            repetitions=bootstrap_repetitions,
            seed_label="animal floral display",
        ),
        "negative": sum(value < 0 for value in display_values),
        "positive": sum(value > 0 for value in display_values),
        "zero": sum(abs(value) < 1e-12 for value in display_values),
        "reading": (
            "The aggregate display log ratio is evaluated separately from "
            "flower-size starting-value dependence."
        ),
    }

    animal_model = analysis["primary_models"]["animal_source_coded"]
    wind_model = analysis["primary_models"]["wind_source_coded"]
    analysis["regression_method_audit"] = {
        "source_methods_label": (
            "The article states that reduced major axis regressions were "
            "conducted with lmodel2."
        ),
        "source_reported_animal_slope": -0.15,
        "source_reported_animal_ci_95": [-0.27, -0.04],
        "source_reported_wind_slope": -0.09,
        "source_reported_wind_ci_95": [-0.23, 0.06],
        "workbook_ols_animal_slope": animal_model[
            "ols_fsLR_on_log10_mainland"
        ]["slope"],
        "workbook_sma_animal_slope": animal_model[
            "standard_major_axis_fsLR_on_log10_mainland"
        ]["slope"],
        "workbook_ols_wind_slope": wind_model[
            "ols_fsLR_on_log10_mainland"
        ]["slope"],
        "workbook_sma_wind_slope": wind_model[
            "standard_major_axis_fsLR_on_log10_mainland"
        ]["slope"],
        "reported_animal_slope_absolute_difference_from_ols": abs(
            -0.15
            - float(
                animal_model["ols_fsLR_on_log10_mainland"]["slope"]
            )
        ),
        "reported_animal_slope_absolute_difference_from_sma": abs(
            -0.15
            - float(
                animal_model[
                    "standard_major_axis_fsLR_on_log10_mainland"
                ]["slope"]
            )
        ),
        "reading": (
            "The printed animal coefficient is numerically reproduced by OLS "
            "on the released workbook, whereas a conventional standardized-"
            "major-axis calculation is materially steeper. This is a method "
            "sensitivity, not a correction of author intent; mixed-model and "
            "source-exclusion details may account for differences."
        ),
    }
    analysis["interpretation"] = {
        "supported": [
            "Animal-pollinated pairs show negative starting-size dependence "
            "under OLS, retained under event-, island-, and family-resampling.",
            "The animal coupling check estimates a log-island-on-log-mainland "
            "slope below one.",
            "Both common actinomorphic morphology classes have negative point "
            "slopes; the pattern is not restricted to two zygomorphic pairs.",
            "Wind-pollinated starting-size slope intervals overlap zero in the "
            "released-workbook analysis.",
            "Animal floral display has no common directional shift in the "
            "released-workbook analysis.",
        ],
        "not_supported_or_not_identified": [
            "The source-coded wind mean is positive but its transparent event-"
            "bootstrap interval overlaps zero; the paper-significant gigantism "
            "result is not reproduced without additional source exclusions.",
            "The dataset does not directly measure pollinator functional "
            "diversity, per-visit effectiveness, effective dependency, pollen "
            "deposition, reproductive success, or the Izu transition.",
            "Flower morphology categories are not direct specialist/generalist "
            "or dependency measurements.",
            "Archipelago, mainland-source, island, and lineage effects are partly "
            "confounded and are not causal moderators in this audit.",
            "The source workbook and article analysis counts are not identical; "
            "no hidden exclusions are invented.",
        ],
    }
    analysis["effect_registry_eligible"] = False
    analysis["claim_boundary"] = (
        "This source supports an independent colonisation-event morphology "
        "response and robustness audit. It is not pooled with visit-network "
        "effects and does not identify pollinator dependency or geological-"
        "origin causation."
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    source_lock = source_file_lock(source_path)
    source_lock["n_source_rows"] = len(rows)
    source_lock["claim_boundary"] = analysis["claim_boundary"]
    (output_dir / "source_lock.json").write_text(
        json.dumps(source_lock, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_subgroup_csv(output_dir / "subgroup_slopes.csv", analysis)
    (output_dir / "effect_rows.json").write_text(
        json.dumps(effect_document(analysis), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return analysis


def resolve_input(input_path: Path | None, input_dir: Path | None) -> Path:
    if input_path is not None:
        return input_path
    if input_dir is None:
        raise ValueError("provide --input or --input-dir")
    candidates = sorted(input_dir.rglob("*supplementary_data_s2.xlsx"))
    if len(candidates) != 1:
        raise ValueError(
            f"expected exactly one Supplementary Data S2 workbook; "
            f"found {len(candidates)}"
        )
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()
    source = resolve_input(args.input, args.input_dir)
    result = run_analysis(
        source,
        args.output_dir,
        bootstrap_repetitions=args.bootstrap_repetitions,
    )
    animal = result["primary_models"]["animal_source_coded"]
    wind = result["primary_models"]["wind_source_coded"]
    print(f"source rows: {result['n_source_rows']}")
    print(
        "animal OLS slope: "
        f"{animal['ols_fsLR_on_log10_mainland']['slope']:.6f}"
    )
    print(
        "wind OLS slope: "
        f"{wind['ols_fsLR_on_log10_mainland']['slope']:.6f}"
    )
    print(args.output_dir / "analysis.json")


if __name__ == "__main__":
    main()
