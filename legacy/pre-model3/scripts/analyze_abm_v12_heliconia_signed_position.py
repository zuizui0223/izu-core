#!/usr/bin/env python3
"""Run the frozen Heliconia signed-position projection of ABM v12.

The source gate fixes the independent 2011 bill-to-corolla mapping, the 2013
population/year/morph visitation weights, workbook schema, and target model.
This script verifies the Dryad package bytes, reconstructs the source-method
selection gradients from plant-level XLS rows, and then runs the declared
cross-unit signed-position test.  It does not tune the mapping to the outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Iterable

import numpy as np
import xlrd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATE = ROOT / "data" / "design" / "abm_v12_heliconia_source_gate.json"
DEFAULT_PACKAGE = (
    ROOT
    / "artifacts"
    / "abm_v12_heliconia_dryad"
    / "package"
    / "doi_10_5061_dryad_64835__v20121024.zip"
)
DEFAULT_OUT = ROOT / "data" / "results" / "abm_v12_heliconia_signed_position_test_frozen.json"

PUBLISHED_BETA_MULTI = {
    "bihai_boeri_2008": (0.24, 0.11),
    "bihai_freshwater_2008": (0.48, 0.16),
    "bihai_boeri_2009": (0.16, 0.26),
    "bihai_freshwater_2009": (0.26, 0.13),
    "caribaea_red_syndicate_2008": (0.52, 0.23),
    "caribaea_red_carholme_2008": (0.05, 0.16),
    "caribaea_red_carholme_2009": (-0.01, 0.14),
    "caribaea_red_la_savanne_2009": (-0.13, 0.21),
    "caribaea_yellow_syndicate_2008": (0.34, 0.22),
    "caribaea_yellow_carholme_2008": (-0.08, 0.30),
    "caribaea_yellow_carholme_2009": (-0.09, 0.31),
    "caribaea_yellow_la_savanne_2009": (-0.38, 0.18),
}


def digest(payload: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, payload).hexdigest()


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return str(resolved)


def finite_number(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        output = float(value)
    except (TypeError, ValueError):
        return None
    return output if math.isfinite(output) else None


def sample_sd(values: Iterable[float]) -> float:
    array = np.asarray(list(values), dtype=float)
    if array.size < 2:
        raise ValueError("sample standard deviation requires at least two values")
    return float(np.std(array, ddof=1))


def fit_linear(y: np.ndarray, x: np.ndarray, weights: np.ndarray | None = None) -> dict[str, float | int]:
    """Fit y ~ 1 + x and return conventional small-sample OLS/WLS inference."""
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    design = np.column_stack([np.ones(y.size), x])
    weights = np.ones(y.size) if weights is None else np.asarray(weights, dtype=float)
    cross = design.T @ (weights[:, None] * design)
    coefficients = np.linalg.solve(cross, design.T @ (weights * y))
    residual = y - design @ coefficients
    df_resid = int(y.size - design.shape[1])
    scale = float(np.sum(weights * residual**2) / df_resid)
    covariance = scale * np.linalg.inv(cross)
    standard_errors = np.sqrt(np.diag(covariance))
    t_value = float(coefficients[1] / standard_errors[1])
    p_value = float(2.0 * stats.t.sf(abs(t_value), df=df_resid))
    critical = float(stats.t.ppf(0.975, df=df_resid))
    fitted = design @ coefficients
    total = float(np.sum(weights * (y - np.average(y, weights=weights)) ** 2))
    residual_sum = float(np.sum(weights * residual**2))
    r_squared = 1.0 - residual_sum / total if total > 0 else 0.0
    return {
        "n_units": int(y.size),
        "intercept": float(coefficients[0]),
        "slope": float(coefficients[1]),
        "slope_standard_error": float(standard_errors[1]),
        "slope_t": t_value,
        "slope_p_two_sided_naive": p_value,
        "slope_ci95_naive": [
            float(coefficients[1] - critical * standard_errors[1]),
            float(coefficients[1] + critical * standard_errors[1]),
        ],
        "r_squared": r_squared,
        "fitted_mean": float(np.mean(fitted)),
    }


def fit_selection(corolla: list[float], bracts: list[float], seeds: list[float]) -> dict[str, float]:
    """Reconstruct source-method beta_uni and beta_multi selection gradients."""
    corolla_array = np.asarray(corolla, dtype=float)
    bracts_array = np.asarray(bracts, dtype=float)
    seeds_array = np.asarray(seeds, dtype=float)
    z_corolla = (corolla_array - np.mean(corolla_array)) / sample_sd(corolla_array)
    z_bracts = (bracts_array - np.mean(bracts_array)) / sample_sd(bracts_array)
    relative_fitness = seeds_array / np.mean(seeds_array)

    uni = np.column_stack([np.ones(relative_fitness.size), z_corolla])
    uni_coef = np.linalg.lstsq(uni, relative_fitness, rcond=None)[0]
    uni_residual = relative_fitness - uni @ uni_coef
    uni_scale = float(uni_residual @ uni_residual / (relative_fitness.size - uni.shape[1]))
    uni_covariance = uni_scale * np.linalg.inv(uni.T @ uni)

    multi = np.column_stack([np.ones(relative_fitness.size), z_corolla, z_bracts])
    multi_coef = np.linalg.lstsq(multi, relative_fitness, rcond=None)[0]
    multi_residual = relative_fitness - multi @ multi_coef
    multi_scale = float(multi_residual @ multi_residual / (relative_fitness.size - multi.shape[1]))
    multi_covariance = multi_scale * np.linalg.inv(multi.T @ multi)

    return {
        "mean_corolla_mm": float(np.mean(corolla_array)),
        "sample_sd_corolla_mm": sample_sd(corolla_array),
        "mean_bracts_per_inflorescence": float(np.mean(bracts_array)),
        "mean_seeds_per_plant": float(np.mean(seeds_array)),
        "beta_uni_corolla": float(uni_coef[1]),
        "beta_uni_corolla_standard_error": float(math.sqrt(uni_covariance[1, 1])),
        "beta_multi_corolla": float(multi_coef[1]),
        "beta_multi_corolla_standard_error": float(math.sqrt(multi_covariance[1, 1])),
        "beta_multi_bracts": float(multi_coef[2]),
        "beta_multi_bracts_standard_error": float(math.sqrt(multi_covariance[2, 2])),
    }


def source_rows(book: xlrd.book.Book, unit: dict[str, object]) -> tuple[list[float], list[float], list[float]]:
    sheet = book.sheet_by_index(0)
    lineage = str(unit["lineage"])
    block_width = 5 if lineage == "bihai" else 6
    start = int(unit["block_index"]) * block_width
    plant_offset, corolla_offset, bracts_offset, seeds_offset = (
        (1, 2, 3, 4) if lineage == "bihai" else (2, 3, 4, 5)
    )
    corolla: list[float] = []
    bracts: list[float] = []
    seeds: list[float] = []
    for row_index in range(1, sheet.nrows):
        values = [
            finite_number(sheet.cell_value(row_index, start + offset))
            for offset in (plant_offset, corolla_offset, bracts_offset, seeds_offset)
        ]
        if all(value is None for value in values):
            continue
        if any(value is None for value in values):
            raise ValueError(f"partial essential row in {unit['unit_id']} at source row {row_index + 1}")
        _, corolla_value, bracts_value, seeds_value = values
        corolla.append(float(corolla_value))
        bracts.append(float(bracts_value))
        seeds.append(float(seeds_value))
    if len(corolla) != int(unit["n_plants"]):
        raise ValueError(f"{unit['unit_id']} has {len(corolla)} plants, expected {unit['n_plants']}")
    return corolla, bracts, seeds


def build(package_path: Path, gate_path: Path) -> dict[str, object]:
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    package_payload = package_path.read_bytes()
    package_lock = gate["selection_source"]["current_byte_recovery"]["full_dataset_package_route"]
    package_audit = {
        "path": portable_path(package_path),
        "bytes": len(package_payload),
        "sha256": digest(package_payload, "sha256"),
        "expected_bytes": int(package_lock["package_bytes"]),
        "expected_sha256": str(package_lock["package_sha256"]),
    }
    package_audit["passes"] = bool(
        package_audit["bytes"] == package_audit["expected_bytes"]
        and package_audit["sha256"] == package_audit["expected_sha256"]
    )
    if not package_audit["passes"]:
        raise ValueError("Dryad package byte lock failed")

    file_specs = {row["lineage"]: row for row in gate["selection_source"]["dryad_files"]}
    units = list(gate["workbook_schema_lock"]["units"])
    visits = gate["source_native_visit_weights"]["units"]
    mapping = gate["frozen_signed_position_mapping"]
    female_bill = float(gate["independent_mapping_source"]["dominica_bill_anchors_mm"]["Eulampis_jugularis_female"]["mean"])
    male_bill = float(gate["independent_mapping_source"]["dominica_bill_anchors_mm"]["Eulampis_jugularis_male"]["mean"])
    intercept = float(mapping["intercept_mm"])
    slope = float(mapping["slope_corolla_per_bill"])

    file_audits: list[dict[str, object]] = []
    unit_results: list[dict[str, object]] = []
    with zipfile.ZipFile(BytesIO(package_payload)) as archive:
        members = set(archive.namelist())
        for lineage, spec in file_specs.items():
            member = str(spec["package_member"])
            if member not in members:
                raise ValueError(f"missing package member {member}")
            payload = archive.read(member)
            audit = {
                "lineage": lineage,
                "package_member": member,
                "bytes": len(payload),
                "md5": digest(payload, "md5"),
                "sha256": digest(payload, "sha256"),
            }
            audit["passes"] = bool(
                audit["bytes"] == int(spec["bytes"])
                and audit["md5"] == spec["md5"]
                and audit["sha256"] == spec["sha256"]
            )
            if not audit["passes"]:
                raise ValueError(f"source byte lock failed for {member}")
            file_audits.append(audit)
            book = xlrd.open_workbook(file_contents=payload)
            if book.nsheets != 1 or book.sheet_names() != [gate["workbook_schema_lock"]["sheet_name"]]:
                raise ValueError(f"unexpected workbook sheets for {member}: {book.sheet_names()}")
            for unit in [row for row in units if row["lineage"] == lineage]:
                corolla, bracts, seeds = source_rows(book, unit)
                selection = fit_selection(corolla, bracts, seeds)
                visit = visits[unit["unit_id"]]
                female_fraction = float(visit["female_fraction"])
                bill_center = female_fraction * female_bill + (1.0 - female_fraction) * male_bill
                expected_corolla = intercept + slope * bill_center
                signed_position = float(selection["mean_corolla_mm"] - expected_corolla)
                published_beta, published_se = PUBLISHED_BETA_MULTI[unit["unit_id"]]
                expected_sign = 1 if signed_position < 0 else -1 if signed_position > 0 else 0
                observed_beta = float(selection["beta_multi_corolla"])
                observed_sign = 1 if observed_beta > 0 else -1 if observed_beta < 0 else 0
                unit_results.append(
                    {
                        **unit,
                        **selection,
                        "female_visit_fraction": female_fraction,
                        "female_visits": visit["female_visits"],
                        "male_visits": visit["male_visits"],
                        "visit_count_scope": visit["count_scope"],
                        "pollinator_bill_center_mm": bill_center,
                        "expected_corolla_mm": expected_corolla,
                        "signed_position_mm": signed_position,
                        "published_beta_multi_corolla": published_beta,
                        "published_beta_multi_corolla_standard_error": published_se,
                        "absolute_beta_reconstruction_delta": abs(observed_beta - published_beta),
                        "absolute_se_reconstruction_delta": abs(float(selection["beta_multi_corolla_standard_error"]) - published_se),
                        "expected_selection_sign_from_position": expected_sign,
                        "observed_beta_multi_sign": observed_sign,
                        "sign_concordant": observed_sign == expected_sign,
                    }
                )

    tolerance = 0.015
    reconstruction_passes = all(
        row["absolute_beta_reconstruction_delta"] <= tolerance
        and row["absolute_se_reconstruction_delta"] <= tolerance
        for row in unit_results
    )
    if not reconstruction_passes:
        raise ValueError("source selection model reconstruction failed")

    signed_position = np.asarray([row["signed_position_mm"] for row in unit_results], dtype=float)
    beta_multi = np.asarray([row["beta_multi_corolla"] for row in unit_results], dtype=float)
    beta_multi_se = np.asarray([row["beta_multi_corolla_standard_error"] for row in unit_results], dtype=float)
    beta_uni = np.asarray([row["beta_uni_corolla"] for row in unit_results], dtype=float)

    primary = fit_linear(beta_multi, signed_position)
    primary["pearson_correlation"] = float(np.corrcoef(signed_position, beta_multi)[0, 1])
    primary["predeclared_supported_direction"] = "negative"
    primary["direction_supported"] = bool(primary["slope"] < 0)
    weighted = fit_linear(beta_multi, signed_position, weights=1.0 / beta_multi_se**2)
    weighted["weighting"] = "inverse_beta_multi_variance"
    univariate = fit_linear(beta_uni, signed_position)
    univariate["response"] = "source_method_beta_uni_corolla"

    leave_one_unit = []
    for index, row in enumerate(unit_results):
        keep = np.arange(len(unit_results)) != index
        fit = fit_linear(beta_multi[keep], signed_position[keep])
        leave_one_unit.append({"omitted_unit_id": row["unit_id"], "slope": fit["slope"]})

    leave_one_lineage = []
    for lineage in sorted({str(row["lineage"]) for row in unit_results}):
        keep = np.asarray([row["lineage"] != lineage for row in unit_results], dtype=bool)
        fit = fit_linear(beta_multi[keep], signed_position[keep])
        leave_one_lineage.append({"omitted_lineage": lineage, "slope": fit["slope"]})

    concordant = sum(bool(row["sign_concordant"]) for row in unit_results)
    primary_negative = bool(primary["slope"] < 0)
    decision = (
        "heliconia_signed_position_projection_supports_declared_negative_direction"
        if primary_negative
        else "heliconia_signed_position_projection_fails_declared_negative_direction"
    )
    return {
        "schema_version": "1.0",
        "analysis": "abm_v12_heliconia_signed_position_test_frozen",
        "run_date": "2026-08-22",
        "gate": portable_path(gate_path),
        "mapping_frozen_before_target_commit": mapping["mapping_frozen_before_target_commit"],
        "validation_class": gate["known_literature_context_not_used_for_mapping"]["validation_class"],
        "source_audit": {
            "package": package_audit,
            "xls_files": file_audits,
            "all_source_byte_locks_pass": bool(package_audit["passes"] and all(row["passes"] for row in file_audits)),
        },
        "source_model_reconstruction": {
            "published_tables": "Temeles et al. 2013 Tables 3 and 4",
            "tolerance_absolute": tolerance,
            "all_12_beta_and_standard_error_pairs_pass": reconstruction_passes,
            "max_absolute_beta_delta": max(float(row["absolute_beta_reconstruction_delta"]) for row in unit_results),
            "max_absolute_standard_error_delta": max(float(row["absolute_se_reconstruction_delta"]) for row in unit_results),
        },
        "unit_count": len(unit_results),
        "plant_row_count": sum(int(row["n_plants"]) for row in unit_results),
        "units": unit_results,
        "primary_test": primary,
        "secondary_sensitivities": {
            "inverse_variance_weighted": weighted,
            "univariate_corolla_selection": univariate,
            "sign_concordance": {
                "concordant_units": concordant,
                "total_units": len(unit_results),
                "fraction": concordant / len(unit_results),
            },
            "leave_one_unit": {
                "slopes": leave_one_unit,
                "minimum": min(float(row["slope"]) for row in leave_one_unit),
                "maximum": max(float(row["slope"]) for row in leave_one_unit),
                "negative_count": sum(float(row["slope"]) < 0 for row in leave_one_unit),
            },
            "leave_one_lineage": leave_one_lineage,
        },
        "decision": decision,
        "interpretation": (
            "The exact Dominica two-anchor signed-position projection is not supported: the primary point estimate is positive rather than the predeclared negative direction. This is an informative failure of this empirical projection, not a reason to retune the mapping."
        ),
        "claim_boundary": (
            "The 12 units contain repeated populations, years and three lineage/morph classes, so conventional OLS intervals are descriptive and not a definitive cross-lineage causal test. The 2013 outcome pattern was literature-known. This result rejects the declared direction for this exact cross-sectional Dominica mapping; it does not by itself falsify the synthetic v12 mechanism, identify an island transition, or estimate a universal plant-pollinator optimum."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--gate", type=Path, default=DEFAULT_GATE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build(args.package, args.gate)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "primary_slope": result["primary_test"]["slope"],
                "primary_ci95_naive": result["primary_test"]["slope_ci95_naive"],
                "sign_concordance": result["secondary_sensitivities"]["sign_concordance"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
