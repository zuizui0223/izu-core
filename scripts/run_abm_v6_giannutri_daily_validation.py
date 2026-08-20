from __future__ import annotations

import importlib.util
import json
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    canonical_label,
    network_metrics,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_giannutri_daily_validation_v1.json"
AUDIT_SCRIPT = ROOT / "scripts/audit_giannutri2025_daily_reconstruction_structure.py"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT = ROOT / "data/results/abm_v6_giannutri_daily_validation.json"
SEED = 20260820
EPS = 1e-12
POLLINATORS = ("Apis_mellifera", "Anthophora_dispar", "Bombus_terrestris")
FORCED_ACTIVE = ("Anthophora_dispar", "Bombus_terrestris")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def finite_nonnegative(value: object, *, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"{label} must be numeric") from exc
    if not math.isfinite(number) or number < 0:
        raise RuntimeError(f"{label} must be finite and non-negative")
    return number


def literal_source_rows(design: dict) -> tuple[list[dict[str, str]], dict]:
    audit = load_module(AUDIT_SCRIPT, "giannutri_validation_source_audit")
    rows = audit.fetch_rows()
    prefiltered = audit.source_prefilter(rows)
    # Frozen literal source semantics: tab$numero does not resolve the declared
    # 'number' column, so line 198 contributes no <=2-transect dates.
    after_pool = audit.pool_rows(prefiltered, set())
    final_rows, low_observation_dates = audit.minimum_observation_filter(after_pool)
    final_dates = sorted({row["Date"] for row in final_rows})
    locked_dates = design["source_native_reconstruction"]["locked_final_dates"]
    if final_dates != locked_dates:
        raise RuntimeError(
            "source-native Giannutri final dates drifted before target calculation: "
            f"observed={final_dates}, locked={locked_dates}"
        )
    conditions = {
        date: sorted({row["hives.condition"] for row in final_rows if row["Date"] == date})
        for date in final_dates
    }
    nonunique = [date for date, values in conditions.items() if len(values) != 1]
    if nonunique:
        raise RuntimeError(f"final dates have nonunique hive condition: {nonunique}")
    return final_rows, {
        "raw_rows": len(rows),
        "prefiltered_rows": len(prefiltered),
        "final_rows": len(final_rows),
        "low_observation_dates_removed": sorted(low_observation_dates),
        "final_dates": final_dates,
        "conditions_by_date": conditions,
        "exact_locked_date_match_before_target_calculation": True,
    }


def build_network(rows: list[dict[str, str]], *, label: str) -> tuple[WeightedNetwork, dict]:
    pair_weight: dict[tuple[str, str], float] = defaultdict(float)
    display_by_key: dict[str, str] = {}
    variants: dict[str, set[str]] = defaultdict(set)
    for row_index, row in enumerate(rows, start=1):
        species = " ".join(str(row["species"]).split())
        if species not in POLLINATORS:
            raise RuntimeError(f"{label}: unexpected pollinator after frozen filter: {species}")
        plant_raw = " ".join(str(row["plant"]).split())
        if canonical_label(plant_raw) == "volo":
            continue
        if not plant_raw:
            raise RuntimeError(f"{label}: blank plant identity at source row {row_index}")
        weight = finite_nonnegative(row["total"], label=f"{label} source total row {row_index}")
        plant_key = canonical_label(plant_raw)
        display_by_key.setdefault(plant_key, plant_raw)
        variants[plant_key].add(plant_raw)
        pair_weight[(plant_key, species)] += weight

    plant_keys = sorted(display_by_key)
    if not plant_keys:
        raise RuntimeError(f"{label}: no plant rows after frozen reconstruction")
    matrix = [
        [pair_weight.get((plant_key, pollinator), 0.0) for pollinator in POLLINATORS]
        for plant_key in plant_keys
    ]
    network = WeightedNetwork.from_rows(
        [display_by_key[key] for key in plant_keys],
        POLLINATORS,
        matrix,
    )
    collision_rows = [
        {"canonical_identity": key, "source_spellings": sorted(values)}
        for key, values in sorted(variants.items())
        if len(values) > 1
    ]
    return network, {
        "canonical_identity_function": "channel_id.external_archipelago_network.canonical_label",
        "source_plant_identity_count": len(plant_keys),
        "plant_variant_collision_count": len(collision_rows),
        "plant_variant_collisions": collision_rows,
    }


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
        raise RuntimeError(f"{label} target metric non-finite")
    return shannon, overlap_value, metrics


def positive_pollinator_support(network: WeightedNetwork) -> tuple[str, ...]:
    return tuple(
        name
        for column, name in enumerate(network.pollinator_names)
        if sum(network.matrix[row][column] for row in range(len(network.plant_names))) > 0
    )


def empirical_summary(design: dict, final_rows: list[dict[str, str]], structure: dict) -> tuple[dict, WeightedNetwork]:
    rows_by_date: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in final_rows:
        rows_by_date[row["Date"]].append(row)

    local_results = []
    pooled_rows = []
    support_sets = []
    for date in structure["final_dates"]:
        date_rows = rows_by_date[date]
        pooled_rows.extend(date_rows)
        network, identity_audit = build_network(date_rows, label=f"daily_{date}")
        shannon, overlap, metrics = metric_pair(network, label=f"daily_{date}")
        support = positive_pollinator_support(network)
        support_sets.append(support)
        local_results.append({
            "date": date,
            "hives_condition": structure["conditions_by_date"][date][0],
            "source_rows": len(date_rows),
            "source_total": sum(finite_nonnegative(row["total"], label=f"daily_{date} total") for row in date_rows if canonical_label(row["plant"]) != "volo"),
            "positive_pollinator_support": list(support),
            "all_three_pollinators_positive": len(support) == 3,
            "interaction_shannon": shannon,
            "plant_niche_overlap": overlap,
            "positive_dimensions": {
                "n_plants": metrics["n_plants"],
                "n_pollinators": metrics["n_pollinators"],
                "n_positive_links": metrics["n_positive_links"],
            },
            "source_identity_audit": identity_audit,
        })

    pooled_network, pooled_identity_audit = build_network(pooled_rows, label="pooled_29_day_baseline")
    pooled_shannon, pooled_overlap, pooled_metrics = metric_pair(
        pooled_network, label="pooled_29_day_baseline"
    )
    if pooled_shannon <= EPS or pooled_overlap <= EPS:
        raise RuntimeError("pooled Giannutri target denominator is non-positive")

    shannon_values = [row["interaction_shannon"] for row in local_results]
    overlap_values = [row["plant_niche_overlap"] for row in local_results]
    support_fraction = sum(row["all_three_pollinators_positive"] for row in local_results) / len(local_results)
    distinct_support_sets = sorted({tuple(support) for support in support_sets})
    shannon_range = max(shannon_values) - min(shannon_values)
    overlap_range = max(overlap_values) - min(overlap_values)

    return {
        "daily_network_count": len(local_results),
        "daily_networks": local_results,
        "three_pollinator_positive_support_fraction": support_fraction,
        "distinct_positive_pollinator_support_set_count": len(distinct_support_sets),
        "distinct_positive_pollinator_support_sets": [list(values) for values in distinct_support_sets],
        "pooled_baseline": {
            "source_rows": len(pooled_rows),
            "interaction_shannon": pooled_shannon,
            "plant_niche_overlap": pooled_overlap,
            "positive_dimensions": {
                "n_plants": pooled_metrics["n_plants"],
                "n_pollinators": pooled_metrics["n_pollinators"],
                "n_positive_links": pooled_metrics["n_positive_links"],
            },
            "source_identity_audit": pooled_identity_audit,
        },
        "interaction_shannon_daily_range": shannon_range,
        "plant_niche_overlap_daily_range": overlap_range,
        "interaction_shannon_relative_daily_range": shannon_range / pooled_shannon,
        "plant_niche_overlap_relative_daily_range": overlap_range / pooled_overlap,
    }, pooled_network


def percentile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("percentile requires values")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def interval(values: list[float]) -> dict:
    return {
        "p2_5": percentile(values, 0.025),
        "median": percentile(values, 0.5),
        "p97_5": percentile(values, 0.975),
    }


def inside(value: float, bounds: dict) -> bool:
    return bounds["p2_5"] - EPS <= value <= bounds["p97_5"] + EPS


def conditioned_active_indices(pooled: WeightedNetwork, support_strength: float, seed: int) -> tuple[int, ...]:
    index = {name: i for i, name in enumerate(pooled.pollinator_names)}
    if set(index) != set(POLLINATORS):
        raise RuntimeError(f"pooled baseline pollinator scope drifted: {pooled.pollinator_names}")
    rng = random.Random(seed)
    active_names = list(FORCED_ACTIVE)
    if rng.random() < 1.0 - support_strength:
        active_names.append("Apis_mellifera")
    return tuple(sorted(index[name] for name in active_names))


def predictive_summary(design: dict, pooled: WeightedNetwork) -> dict:
    v6 = load_module(V6_SCRIPT, "giannutri_validation_v6")
    v5 = load_module(V5_SCRIPT, "giannutri_validation_v5")
    predictive = design["v6_predictive_distribution"]
    strengths = [float(value) for value in predictive["support_strengths"]]
    weight_strengths = [float(value) for value in predictive["weight_strengths"]]
    replicates = int(predictive["replicates_per_support_x_weight_setting"])
    contexts = int(predictive["contexts_per_replicate"])

    baseline_shannon, baseline_overlap, _ = metric_pair(pooled, label="synthetic_conditioning_baseline")
    if baseline_shannon <= EPS or baseline_overlap <= EPS:
        raise RuntimeError("synthetic conditioning baseline denominator non-positive")

    support_distribution: list[float] = []
    shannon_distribution: list[float] = []
    overlap_distribution: list[float] = []
    setting_summary: dict[str, dict] = {}
    completed_draws = 0

    for support_index, support_strength in enumerate(strengths):
        for weight_index, weight_strength in enumerate(weight_strengths):
            local_support_stats = []
            local_shannon_stats = []
            local_overlap_stats = []
            for replicate in range(replicates):
                support_all_three = 0
                shannon_values = []
                overlap_values = []
                for context_index in range(contexts):
                    support_seed = (
                        SEED + 10_000_000 + support_index * 1_000_000
                        + weight_index * 100_000 + replicate * 100 + context_index
                    )
                    weight_seed = support_seed + 50_000_000
                    active = conditioned_active_indices(pooled, support_strength, support_seed)
                    active_names = [pooled.pollinator_names[index] for index in active]
                    if len(active_names) == 3:
                        support_all_three += 1
                    try:
                        support_network = v6.apply_active_pollinator_indices(pooled, active)
                    except RuntimeError as exc:
                        match = re.search(r"plant row (\d+)", str(exc))
                        row_index = int(match.group(1)) if match else None
                        plant_name = (
                            pooled.plant_names[row_index]
                            if row_index is not None and 0 <= row_index < len(pooled.plant_names)
                            else None
                        )
                        return {
                            "structural_gate_passed": False,
                            "decision": "v6_fails_giannutri_conditional_local_support_structural_gate",
                            "predictive_draws_completed_before_failure": completed_draws,
                            "failure": {
                                "support_strength": support_strength,
                                "weight_strength": weight_strength,
                                "replicate": replicate,
                                "context_index": context_index,
                                "active_pollinators": active_names,
                                "error": str(exc),
                                "plant_row_index": row_index,
                                "plant_name": plant_name,
                                "plant_baseline_weights": (
                                    list(pooled.matrix[row_index]) if row_index is not None else None
                                ),
                                "rule": design["v6_predictive_distribution"]["row_budget_rule"],
                            },
                            "claim_boundary": "A frozen source-conditioned support mask violated the existing v6 row-budget/admissibility invariant. The context was not skipped, redrawn, repaired, or replaced.",
                        }
                    realized = v5.realize_local_context(
                        support_network,
                        context_seed=weight_seed,
                        context_strength=weight_strength,
                    )
                    shannon, overlap, _ = metric_pair(
                        realized,
                        label=(
                            f"synthetic_support{support_strength}_weight{weight_strength}_"
                            f"rep{replicate}_ctx{context_index}"
                        ),
                    )
                    shannon_values.append(shannon)
                    overlap_values.append(overlap)

                support_fraction = support_all_three / contexts
                shannon_relative_range = (max(shannon_values) - min(shannon_values)) / baseline_shannon
                overlap_relative_range = (max(overlap_values) - min(overlap_values)) / baseline_overlap
                support_distribution.append(support_fraction)
                shannon_distribution.append(shannon_relative_range)
                overlap_distribution.append(overlap_relative_range)
                local_support_stats.append(support_fraction)
                local_shannon_stats.append(shannon_relative_range)
                local_overlap_stats.append(overlap_relative_range)
                completed_draws += 1

            setting_summary[f"support={support_strength}|weight={weight_strength}"] = {
                "replicates": replicates,
                "median_three_pollinator_positive_support_fraction": percentile(local_support_stats, 0.5),
                "median_interaction_shannon_relative_daily_range": percentile(local_shannon_stats, 0.5),
                "median_plant_niche_overlap_relative_daily_range": percentile(local_overlap_stats, 0.5),
            }

    expected = int(predictive["predictive_draw_count"])
    if completed_draws != expected:
        raise RuntimeError(f"predictive draw count drifted: {completed_draws} != {expected}")
    return {
        "structural_gate_passed": True,
        "predictive_draw_count": completed_draws,
        "equal_support_and_weight_strength_weights": True,
        "three_pollinator_positive_support_fraction_envelope": interval(support_distribution),
        "interaction_shannon_relative_daily_range_envelope": interval(shannon_distribution),
        "plant_niche_overlap_relative_daily_range_envelope": interval(overlap_distribution),
        "setting_summary": setting_summary,
    }


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    final_rows, structure = literal_source_rows(design)
    empirical, pooled = empirical_summary(design, final_rows, structure)
    if empirical["daily_network_count"] != 29:
        raise RuntimeError("Giannutri daily network count drifted after target reconstruction")

    predictive = predictive_summary(design, pooled)
    base_payload = {
        "schema_version": "1.0",
        "analysis": "abm_v6_giannutri_daily_network_validation",
        "status": "held_out_conditional_local_support_validation",
        "design_source": str(DESIGN),
        "target_metrics_inspected": True,
        "source_structure": structure,
        "empirical": empirical,
        "predictive": predictive,
        "selection_caveat": design["selection_caveat"],
        "claim_boundary": design["claim_boundary"],
    }

    if not predictive.get("structural_gate_passed"):
        base_payload["tests"] = {
            "exact_locked_29_day_reconstruction": True,
            "v6_structural_gate": False,
            "support_adequacy": None,
            "shannon_adequacy": None,
            "plant_niche_overlap_adequacy": None,
        }
        base_payload["decision"] = predictive["decision"]
        write(base_payload)
        return

    support_interval = predictive["three_pollinator_positive_support_fraction_envelope"]
    shannon_interval = predictive["interaction_shannon_relative_daily_range_envelope"]
    overlap_interval = predictive["plant_niche_overlap_relative_daily_range_envelope"]
    tests = {
        "exact_locked_29_day_reconstruction": True,
        "v6_structural_gate": True,
        "support_adequacy": inside(empirical["three_pollinator_positive_support_fraction"], support_interval),
        "shannon_adequacy": inside(empirical["interaction_shannon_relative_daily_range"], shannon_interval),
        "plant_niche_overlap_adequacy": inside(empirical["plant_niche_overlap_relative_daily_range"], overlap_interval),
    }
    passed = all(value is True for value in tests.values())
    base_payload["tests"] = tests
    base_payload["decision"] = (
        "v6_survives_giannutri_conditional_local_support_test"
        if passed
        else "v6_fails_giannutri_conditional_local_support_predictive_adequacy"
    )
    write(base_payload)


if __name__ == "__main__":
    main()
