from __future__ import annotations

import importlib.util
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import xlrd

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v5_menorca_nine_local_validation_v1.json"
SOURCE_AUDIT = ROOT / "data/results/menorca2023_figshare_source_audit.json"
GEO_LOCK = ROOT / "data/results/menorca2023_gift_opportunity_lock.json"
RAW_DIR = ROOT / "data/external/menorca2023"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT = ROOT / "data/results/abm_v5_menorca_nine_local_validation.json"
SEED = 20260820
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def compact_label(value: object) -> str:
    return " ".join(str(value).split())


def finite_nonnegative(value: object, *, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"{label} must be numeric") from exc
    if not math.isfinite(number) or number < 0:
        raise RuntimeError(f"{label} must be finite and non-negative")
    return number


def locate_frozen_workbook(design: dict, source_audit: dict) -> Path:
    expected_sha = design["source_recovery_gate"]["required_source_file_sha256"]
    expected_bytes = int(design["held_out_system"]["source_file_bytes"])
    audit_files = source_audit.get("files") or []
    matches = [
        row for row in audit_files
        if row.get("sha256") == expected_sha and int(row.get("bytes", -1)) == expected_bytes
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one checksum-locked Menorca workbook in source audit, found {len(matches)}")
    candidates = []
    for path in RAW_DIR.glob("*.xls"):
        import hashlib

        payload = path.read_bytes()
        if len(payload) == expected_bytes and hashlib.sha256(payload).hexdigest() == expected_sha:
            candidates.append(path)
    if len(candidates) != 1:
        raise RuntimeError(f"expected one checksum-locked Menorca workbook on disk, found {len(candidates)}")
    return candidates[0]


def sheet_rows(book: xlrd.book.Book, sheet_name: str, required_columns: list[str]) -> list[tuple[str, str, float]]:
    if sheet_name not in book.sheet_names():
        raise RuntimeError(f"required sheet missing: {sheet_name}")
    sheet = book.sheet_by_name(sheet_name)
    if sheet.nrows < 2:
        raise RuntimeError(f"sheet has no data rows: {sheet_name}")
    headers = [compact_label(sheet.cell_value(0, column)) for column in range(sheet.ncols)]
    missing = [column for column in required_columns if column not in headers]
    if missing:
        raise RuntimeError(f"{sheet_name} missing required columns: {missing}")
    index = {header: headers.index(header) for header in required_columns}
    rows = []
    for row_index in range(1, sheet.nrows):
        plant = compact_label(sheet.cell_value(row_index, index["Plant_sp"]))
        visitor = compact_label(sheet.cell_value(row_index, index["Visitor_sp"]))
        raw_weight = sheet.cell_value(row_index, index["FVR"])
        if not plant or not visitor:
            raise RuntimeError(f"missing Plant_sp/Visitor_sp in {sheet_name} row {row_index + 1}")
        weight = finite_nonnegative(raw_weight, label=f"{sheet_name} row {row_index + 1} FVR")
        rows.append((plant, visitor, weight))
    return rows


def network_from_rows(rows: list[tuple[str, str, float]]) -> WeightedNetwork:
    pair_weight = defaultdict(float)
    plant_order = []
    visitor_order = []
    seen_plants = set()
    seen_visitors = set()
    for plant, visitor, weight in rows:
        if plant not in seen_plants:
            seen_plants.add(plant)
            plant_order.append(plant)
        if visitor not in seen_visitors:
            seen_visitors.add(visitor)
            visitor_order.append(visitor)
        pair_weight[(plant, visitor)] += weight
    matrix = [
        [pair_weight.get((plant, visitor), 0.0) for visitor in visitor_order]
        for plant in plant_order
    ]
    return WeightedNetwork.from_rows(plant_order, visitor_order, matrix)


def metric_pair(network: WeightedNetwork, *, label: str) -> tuple[float, float, dict]:
    try:
        metrics = network_metrics(network)
    except ValueError as exc:
        raise RuntimeError(f"{label} structural comparability failure: {exc}") from exc
    overlap = metrics["mean_plant_niche_overlap_morisita_horn"]
    if overlap is None:
        raise RuntimeError(f"{label} plant niche overlap undefined")
    shannon = float(metrics["interaction_shannon"])
    overlap_value = float(overlap)
    if not math.isfinite(shannon) or not math.isfinite(overlap_value):
        raise RuntimeError(f"{label} target metric is non-finite")
    return shannon, overlap_value, metrics


def empirical_summary(design: dict, workbook: Path) -> dict:
    book = xlrd.open_workbook(workbook)
    required = design["source_recovery_gate"]["required_columns_local"]
    local_sheets = design["held_out_system"]["source_defined_local_sheets"]
    if len(local_sheets) != 9 or len(set(local_sheets)) != 9:
        raise RuntimeError("frozen local sheet list must contain exactly nine unique sheets")

    local_results = []
    pooled_rows = []
    for sheet_name in local_sheets:
        rows = sheet_rows(book, sheet_name, required)
        pooled_rows.extend(rows)
        network = network_from_rows(rows)
        shannon, overlap, metrics = metric_pair(network, label=sheet_name)
        local_results.append({
            "sheet": sheet_name,
            "source_rows": len(rows),
            "source_fvr_total": sum(weight for _, _, weight in rows),
            "interaction_shannon": shannon,
            "plant_niche_overlap": overlap,
            "positive_dimensions": {
                "n_plants": metrics["n_plants"],
                "n_pollinators": metrics["n_pollinators"],
                "n_positive_links": metrics["n_positive_links"],
            },
        })

    pooled_network = network_from_rows(pooled_rows)
    pooled_shannon, pooled_overlap, pooled_metrics = metric_pair(
        pooled_network, label="pooled_nine_sheet_metaweb"
    )
    if pooled_shannon <= EPS or pooled_overlap <= EPS:
        raise RuntimeError("pooled metaweb target denominator is non-positive")

    shannon_values = [row["interaction_shannon"] for row in local_results]
    overlap_values = [row["plant_niche_overlap"] for row in local_results]
    shannon_range = max(shannon_values) - min(shannon_values)
    overlap_range = max(overlap_values) - min(overlap_values)

    return {
        "local_networks": local_results,
        "pooled_metaweb": {
            "source_rows": len(pooled_rows),
            "interaction_shannon": pooled_shannon,
            "plant_niche_overlap": pooled_overlap,
            "positive_dimensions": {
                "n_plants": pooled_metrics["n_plants"],
                "n_pollinators": pooled_metrics["n_pollinators"],
                "n_positive_links": pooled_metrics["n_positive_links"],
            },
        },
        "interaction_shannon_local_range": shannon_range,
        "plant_niche_overlap_local_range": overlap_range,
        "interaction_shannon_relative_local_range": shannon_range / pooled_shannon,
        "plant_niche_overlap_relative_local_range": overlap_range / pooled_overlap,
    }


def percentile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("percentile requires values")
    if not 0 <= probability <= 1:
        raise ValueError(probability)
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def positive_total(network: WeightedNetwork) -> float:
    return sum(sum(row) for row in network.matrix)


def synthetic_summary(design: dict, isolation_index: float) -> dict:
    v5 = load_module(V5_SCRIPT, "abm_v5_menorca_core")
    v4 = v5.load_module(v5.V4_WEIGHTED, "abm_v5_menorca_v4_weighted")
    strengths = [float(value) for value in design["v5_predictive_distribution"]["context_strengths"]]
    saturations = [float(value) for value in design["v5_predictive_distribution"]["v4_saturations"]]
    replicates = int(design["v5_predictive_distribution"]["replicates_per_setting"])

    shannon_distribution = []
    overlap_distribution = []
    setting_summary = {}
    total_state_counts = {"empty": 0, "single_pollinator": 0, "branchable": 0}

    for saturation_index, saturation in enumerate(saturations):
        feasible_cache = []
        for replicate in range(replicates):
            evolution_seed = SEED + saturation_index * 100_000 + replicate
            feasible = v4.run_weighted_network(isolation_index, evolution_seed, saturation)
            if positive_total(feasible) <= 0:
                feasible_cache.append((replicate, feasible, "empty", None, None))
                continue
            baseline_shannon, baseline_overlap, _ = metric_pair(
                feasible, label=f"synthetic_baseline_sat{saturation}_rep{replicate}"
            )
            if len(feasible.pollinator_names) == 1:
                category = "single_pollinator"
            else:
                category = "branchable"
                if baseline_shannon <= EPS or baseline_overlap <= EPS:
                    raise RuntimeError("positive branchable synthetic baseline has non-positive denominator")
            feasible_cache.append(
                (replicate, feasible, category, baseline_shannon, baseline_overlap)
            )

        for strength_index, strength in enumerate(strengths):
            local_shannon = []
            local_overlap = []
            state_counts = {"empty": 0, "single_pollinator": 0, "branchable": 0}
            for replicate, feasible, category, baseline_shannon, baseline_overlap in feasible_cache:
                state_counts[category] += 1
                total_state_counts[category] += 1
                if category in ("empty", "single_pollinator"):
                    shannon_relative_range = 0.0
                    overlap_relative_range = 0.0
                else:
                    shannon_values = []
                    overlap_values = []
                    for context_index in range(9):
                        context_seed = (
                            SEED
                            + 20_000_000
                            + saturation_index * 1_000_000
                            + strength_index * 100_000
                            + replicate * 100
                            + context_index
                        )
                        realized = v5.realize_local_context(
                            feasible,
                            context_seed=context_seed,
                            context_strength=strength,
                        )
                        shannon, overlap, _ = metric_pair(
                            realized,
                            label=(
                                f"synthetic_context_sat{saturation}_strength{strength}_"
                                f"rep{replicate}_ctx{context_index}"
                            ),
                        )
                        shannon_values.append(shannon)
                        overlap_values.append(overlap)
                    shannon_relative_range = (
                        max(shannon_values) - min(shannon_values)
                    ) / float(baseline_shannon)
                    overlap_relative_range = (
                        max(overlap_values) - min(overlap_values)
                    ) / float(baseline_overlap)

                shannon_distribution.append(shannon_relative_range)
                overlap_distribution.append(overlap_relative_range)
                local_shannon.append(shannon_relative_range)
                local_overlap.append(overlap_relative_range)

            setting_summary[f"saturation={saturation}|strength={strength}"] = {
                "replicates": replicates,
                "state_counts": state_counts,
                "median_interaction_shannon_relative_local_range": statistics.median(local_shannon),
                "median_plant_niche_overlap_relative_local_range": statistics.median(local_overlap),
            }

    expected = len(strengths) * len(saturations) * replicates
    if len(shannon_distribution) != expected or len(overlap_distribution) != expected:
        raise RuntimeError("synthetic equal-weight mixture size drifted")

    return {
        "predictive_draw_count": expected,
        "equal_strength_and_saturation_weights": True,
        "state_draw_counts": total_state_counts,
        "interaction_shannon_relative_local_range_envelope": {
            "p2_5": percentile(shannon_distribution, 0.025),
            "median": percentile(shannon_distribution, 0.5),
            "p97_5": percentile(shannon_distribution, 0.975),
        },
        "plant_niche_overlap_relative_local_range_envelope": {
            "p2_5": percentile(overlap_distribution, 0.025),
            "median": percentile(overlap_distribution, 0.5),
            "p97_5": percentile(overlap_distribution, 0.975),
        },
        "setting_summary": setting_summary,
    }


def inside(value: float, interval: dict) -> bool:
    return interval["p2_5"] - EPS <= value <= interval["p97_5"] + EPS


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    source_audit = json.loads(SOURCE_AUDIT.read_text())
    if source_audit.get("source_admission_succeeds") is not True:
        write({
            "schema_version": "1.0",
            "analysis": "abm_v5_menorca_nine_local_validation",
            "status": "blocked_before_target_metric_inspection",
            "decision": "blocked_menorca_source_admission_not_satisfied",
            "target_metrics_inspected": False,
            "claim_boundary": design["claim_boundary"],
        })
        return

    workbook = locate_frozen_workbook(design, source_audit)
    geography = json.loads(GEO_LOCK.read_text())
    if geography.get("status") != "locked":
        write({
            "schema_version": "1.0",
            "analysis": "abm_v5_menorca_nine_local_validation",
            "status": "blocked_before_target_metric_inspection",
            "decision": "blocked_menorca_gift_opportunity_not_locked",
            "target_metrics_inspected": False,
            "geography": geography,
            "claim_boundary": design["claim_boundary"],
        })
        return

    empirical = empirical_summary(design, workbook)
    predictive = synthetic_summary(design, float(geography["isolation_index"]))
    shannon_empirical = empirical["interaction_shannon_relative_local_range"]
    overlap_empirical = empirical["plant_niche_overlap_relative_local_range"]
    shannon_interval = predictive["interaction_shannon_relative_local_range_envelope"]
    overlap_interval = predictive["plant_niche_overlap_relative_local_range_envelope"]

    tests = {
        "interaction_shannon_local_variation_positive": shannon_empirical > EPS,
        "plant_niche_overlap_local_variation_positive": overlap_empirical > EPS,
        "interaction_shannon_relative_range_inside_frozen_v5_envelope": inside(
            shannon_empirical, shannon_interval
        ),
        "plant_niche_overlap_relative_range_inside_frozen_v5_envelope": inside(
            overlap_empirical, overlap_interval
        ),
    }
    passed = all(tests.values())
    decision = (
        "v5_survives_menorca_nine_local_raw_architecture_test"
        if passed
        else "v5_fails_menorca_nine_local_raw_architecture_test"
    )

    write({
        "schema_version": "1.0",
        "analysis": "abm_v5_menorca_nine_local_validation",
        "status": "held_out_nine_local_network_target_validation",
        "design_source": str(DESIGN),
        "source_audit_source": str(SOURCE_AUDIT),
        "source_workbook_sha256": design["held_out_system"]["source_file_sha256"],
        "geography": geography,
        "empirical": empirical,
        "predictive": predictive,
        "tests": tests,
        "decision": decision,
        "target_metrics_inspected": True,
        "headline_rule": design["decision_rule"]["headline"],
        "failure_interpretation": design["failure_interpretation"],
        "selection_caveat": design["selection_caveat"],
        "claim_boundary": design["claim_boundary"],
    })


if __name__ == "__main__":
    main()
