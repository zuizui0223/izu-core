from __future__ import annotations

import csv
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v5_aride_seasonal_validation_v1.json"
SOURCE_LOCK = ROOT / "data/results/aride2026_dryad_source_lock.json"
GEO_LOCK = ROOT / "data/results/aride2026_gift_opportunity_lock.json"
RAW_DIR = ROOT / "data/external/aride_2026"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT = ROOT / "data/results/abm_v5_aride_seasonal_validation.json"
SEED = 20260819


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_network(path: Path) -> WeightedNetwork:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise RuntimeError(f"{path.name} is not a labeled matrix")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise RuntimeError(f"{path.name} has ragged rows")
    pollinators = [cell.strip() for cell in rows[0][1:]]
    plants = [row[0].strip() for row in rows[1:]]
    matrix = [[float(cell) for cell in row[1:]] for row in rows[1:]]
    return WeightedNetwork.from_rows(plants, pollinators, matrix)


def metric_pair(network: WeightedNetwork) -> tuple[float, float]:
    metrics = network_metrics(network)
    shannon = float(metrics["interaction_shannon"])
    overlap = metrics["mean_plant_niche_overlap_morisita_horn"]
    if overlap is None:
        raise RuntimeError("plant niche overlap undefined because fewer than two positive plant rows remain")
    return shannon, float(overlap)


def percentile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("percentile requires values")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lo, hi = math.floor(position), math.ceil(position)
    if lo == hi:
        return ordered[lo]
    fraction = position - lo
    return ordered[lo] * (1 - fraction) + ordered[hi] * fraction


def positive_total(network: WeightedNetwork) -> float:
    return sum(sum(row) for row in network.matrix)


def empirical_summary(design: dict) -> dict:
    order = design["held_out_system"]["network_order"]
    filename_by_label = {"Early_Oct": "Early_Oct.csv", "Mid_Nov": "Mid_Nov.csv", "Late_Dec": "Late_Dec.csv"}
    networks = []
    for label in order:
        filename = filename_by_label[label]
        network = parse_network(RAW_DIR / filename)
        metrics = network_metrics(network)
        overlap = metrics["mean_plant_niche_overlap_morisita_horn"]
        if overlap is None:
            raise RuntimeError(f"{filename} has undefined plant niche overlap")
        networks.append({
            "label": label,
            "filename": filename,
            "source_dimensions": {"n_source_plants": len(network.plant_names), "n_source_pollinators": len(network.pollinator_names)},
            "positive_dimensions": {"n_plants": metrics["n_plants"], "n_pollinators": metrics["n_pollinators"], "n_positive_links": metrics["n_positive_links"]},
            "interaction_shannon": float(metrics["interaction_shannon"]),
            "plant_niche_overlap": float(overlap),
            "total_visitation_rate": float(metrics["total_visitation_rate"]),
        })
    shannon = [row["interaction_shannon"] for row in networks]
    overlap = [row["plant_niche_overlap"] for row in networks]
    return {
        "seasonal_networks": networks,
        "all_three_structurally_single_pollinator": all(row["positive_dimensions"]["n_pollinators"] == 1 for row in networks),
        "interaction_shannon_range": max(shannon) - min(shannon),
        "plant_niche_overlap_range": max(overlap) - min(overlap),
        "transition_signs": {
            "interaction_shannon": [shannon[1] - shannon[0], shannon[2] - shannon[1]],
            "plant_niche_overlap": [overlap[1] - overlap[0], overlap[2] - overlap[1]],
        },
    }


def synthetic_ranges(design: dict, isolation_index: float) -> dict:
    v5 = load_module(V5_SCRIPT, "abm_v5_aride_core")
    v4 = v5.load_module(v5.V4_WEIGHTED, "abm_v5_aride_v4_weighted")
    saturations = [float(value) for value in design["v5_predictive_distribution"]["v4_saturations"]]
    strengths = [float(value) for value in design["v5_predictive_distribution"]["context_strengths"]]
    replicates = int(design["v5_predictive_distribution"]["replicates_per_setting"])
    shannon_ranges, overlap_ranges = [], []
    setting_summary = {}
    counts = {"empty": 0, "single_pollinator": 0, "branchable": 0}
    for sat_i, saturation in enumerate(saturations):
        feasible_cache = []
        for replicate in range(replicates):
            feasible = v4.run_weighted_network(isolation_index, SEED + sat_i * 100_000 + replicate, saturation)
            category = "empty" if positive_total(feasible) <= 0 else "single_pollinator" if len(feasible.pollinator_names) == 1 else "branchable"
            feasible_cache.append((replicate, feasible, category))
        for strength_i, strength in enumerate(strengths):
            local_shannon, local_overlap = [], []
            local_counts = {"empty": 0, "single_pollinator": 0, "branchable": 0}
            for replicate, feasible, category in feasible_cache:
                local_counts[category] += 1
                counts[category] += 1
                if category != "branchable":
                    sh_range = ov_range = 0.0
                else:
                    sh_values, ov_values = [], []
                    for context_index in range(3):
                        realized = v5.realize_local_context(
                            feasible,
                            context_seed=SEED + 20_000_000 + sat_i * 1_000_000 + strength_i * 100_000 + replicate * 10 + context_index,
                            context_strength=strength,
                        )
                        sh, ov = metric_pair(realized)
                        sh_values.append(sh); ov_values.append(ov)
                    sh_range = max(sh_values) - min(sh_values)
                    ov_range = max(ov_values) - min(ov_values)
                shannon_ranges.append(sh_range); overlap_ranges.append(ov_range)
                local_shannon.append(sh_range); local_overlap.append(ov_range)
            setting_summary[f"saturation={saturation}|strength={strength}"] = {
                "replicates": replicates,
                "state_counts": local_counts,
                "median_shannon_range": statistics.median(local_shannon),
                "median_overlap_range": statistics.median(local_overlap),
            }
    expected = len(saturations) * len(strengths) * replicates
    if len(shannon_ranges) != expected:
        raise RuntimeError("predictive mixture size drifted")
    return {
        "n_predictive_draws": expected,
        "equal_setting_weights": True,
        "interaction_shannon_range_envelope": {"p2_5": percentile(shannon_ranges, .025), "median": percentile(shannon_ranges, .5), "p97_5": percentile(shannon_ranges, .975)},
        "plant_niche_overlap_range_envelope": {"p2_5": percentile(overlap_ranges, .025), "median": percentile(overlap_ranges, .5), "p97_5": percentile(overlap_ranges, .975)},
        "state_draw_counts_across_setting_mixture": counts,
        "setting_summary": setting_summary,
    }


def inside(value: float, interval: dict) -> bool:
    return interval["p2_5"] - 1e-12 <= value <= interval["p97_5"] + 1e-12


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    source = json.loads(SOURCE_LOCK.read_text())
    # Source access is the first admission gate. Do not even require or inspect
    # geography/empirical matrices when the exact source bytes are unavailable.
    if not source.get("all_required_files_recovered"):
        write({
            "schema_version": "1.1",
            "analysis": "abm_v5_aride_seasonal_validation",
            "status": "blocked_before_target_metric_inspection",
            "decision": "blocked_aride_source_bytes_require_authenticated_dryad_download",
            "source_lock": source,
            "target_metrics_inspected": False,
            "geography_required_for_blocked_decision": False,
            "next_gate": source.get("next_gate"),
            "claim_boundary": "The frozen Aride validation exists, but the exact source-native matrix bytes were not available to the unauthenticated public runner. No Shannon diversity, plant niche overlap, v5 predictive fit, or biological direction was calculated.",
        })
        return

    geo = json.loads(GEO_LOCK.read_text())
    if geo.get("status") != "locked":
        write({"schema_version": "1.0", "analysis": "abm_v5_aride_seasonal_validation", "decision": "blocked_aride_gift_opportunity_not_locked", "geography": geo, "claim_boundary": design["claim_boundary"]})
        return

    empirical = empirical_summary(design)
    predictive = synthetic_ranges(design, float(geo["isolation_index"]))
    sh_interval = predictive["interaction_shannon_range_envelope"]
    ov_interval = predictive["plant_niche_overlap_range_envelope"]
    exception = empirical["all_three_structurally_single_pollinator"]
    tests = {
        "interaction_shannon_variation_necessary_condition": empirical["interaction_shannon_range"] > 0 or exception,
        "plant_niche_overlap_variation_necessary_condition": empirical["plant_niche_overlap_range"] > 0 or exception,
        "interaction_shannon_range_inside_frozen_v5_envelope": inside(empirical["interaction_shannon_range"], sh_interval),
        "plant_niche_overlap_range_inside_frozen_v5_envelope": inside(empirical["plant_niche_overlap_range"], ov_interval),
    }
    passed = all(tests.values())
    write({
        "schema_version": "1.0",
        "analysis": "abm_v5_aride_seasonal_validation",
        "status": "held_out_raw_weighted_target_estimand_validation",
        "design_source": str(DESIGN),
        "source_lock": source,
        "geography_lock": geo,
        "empirical": empirical,
        "predictive": predictive,
        "tests": tests,
        "decision": "v5_survives_aride_heldout_seasonal_raw_architecture_test" if passed else "v5_fails_aride_heldout_seasonal_raw_architecture_test",
        "interpretation_rule": design["decision_rule"]["headline"],
        "selection_caveat": design["selection_caveat"],
        "claim_boundary": design["claim_boundary"],
    })


if __name__ == "__main__":
    main()
