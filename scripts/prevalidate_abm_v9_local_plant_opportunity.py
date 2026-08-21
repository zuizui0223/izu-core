from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

from channel_id.external_archipelago_network import network_metrics

ROOT = Path(__file__).resolve().parents[1]
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V8_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
V4_SCRIPT = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V4_GRADIENT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
OUT = ROOT / "data/results/abm_v9_local_plant_opportunity_prevalidation.json"
ISOLATIONS = (0.0, 0.5, 1.0)
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)
SUPPORT_STRENGTHS = (0.25, 0.5, 0.75)
WEIGHT_PROBE = 0.5
EPS = 1e-12


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def positive_total(network) -> float:
    if network is None:
        return 0.0
    return sum(sum(row) for row in network.matrix)


def support_signature(network) -> tuple[tuple[str, str], ...]:
    if network is None:
        return tuple()
    return tuple(sorted(
        (plant, pollinator)
        for row_index, plant in enumerate(network.plant_names)
        for column_index, pollinator in enumerate(network.pollinator_names)
        if network.matrix[row_index][column_index] > 0.0
    ))


def plant_signature(network) -> tuple[str, ...]:
    if network is None:
        return tuple()
    return tuple(sorted(
        plant
        for row_index, plant in enumerate(network.plant_names)
        if sum(network.matrix[row_index]) > 0.0
    ))


def pollinator_signature(network) -> tuple[str, ...]:
    if network is None:
        return tuple()
    return tuple(sorted(
        pollinator
        for column_index, pollinator in enumerate(network.pollinator_names)
        if sum(network.matrix[row][column_index] for row in range(len(network.plant_names))) > 0.0
    ))


def metric_pair_or_none(network):
    if network is None or positive_total(network) <= 0.0:
        return None
    try:
        metrics = network_metrics(network)
    except ValueError:
        return None
    overlap = metrics["mean_plant_niche_overlap_morisita_horn"]
    if overlap is None:
        return None
    return float(metrics["interaction_shannon"]), float(overlap)


def max_retained_budget_error(opportunity, realized) -> float:
    if realized is None:
        return 0.0
    source = {
        plant: sum(opportunity.matrix[index])
        for index, plant in enumerate(opportunity.plant_names)
    }
    errors = []
    for index, plant in enumerate(realized.plant_names):
        if plant not in source:
            return float("inf")
        errors.append(abs(sum(realized.matrix[index]) - source[plant]))
    return max(errors) if errors else 0.0


def realized_is_opportunity_subset(opportunity, realized) -> bool:
    if realized is None:
        return True
    source_pairs = {
        (plant, pollinator)
        for row_index, plant in enumerate(opportunity.plant_names)
        for column_index, pollinator in enumerate(opportunity.pollinator_names)
        if opportunity.matrix[row_index][column_index] > 0.0
    }
    return (
        set(realized.plant_names).issubset(set(opportunity.plant_names))
        and set(realized.pollinator_names).issubset(set(opportunity.pollinator_names))
        and set(support_signature(realized)).issubset(source_pairs)
    )


def build(evolution_replicates: int, context_replicates: int, seed: int) -> dict:
    if evolution_replicates < 1 or context_replicates < 2:
        raise ValueError("invalid replicate counts")
    v9 = load(V9_SCRIPT, "abm_v9_prevalidation_core")
    v8 = load(V8_SCRIPT, "abm_v9_prevalidation_v8")
    v4 = load(V4_SCRIPT, "abm_v9_prevalidation_v4")

    inherited = json.loads(V4_GRADIENT.read_text())
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    inherited_ok = all(inherited["tests"].get(key) for key in required_v4)
    if not inherited_ok:
        raise RuntimeError("frozen v4 opportunity contract failed before v9")

    failures = {
        "zero_support_v8_identity": [],
        "retained_row_budget": [],
        "opportunity_subset": [],
        "unexpected_exception": [],
        "matched_v8_pair_draw_changed": [],
    }
    state_rows = []
    metric_ranges = []
    positive_plant_drop_contexts = 0
    empty_plant_opportunity_contexts = 0
    empty_final_contexts = 0
    matched_v9_sparser_than_v8 = 0
    matched_equal_pair_count = 0
    matched_v9_denser_than_v8 = 0
    matched_pair_count_ratios = []

    for sat_index, saturation in enumerate(SATURATIONS):
        for iso_index, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + sat_index * 100_000 + iso_index * 10_000 + replicate
                state_id = f"sat={saturation}|iso={isolation}|rep={replicate}"
                opportunity = v4.run_weighted_network(isolation, evolution_seed, saturation)
                baseline_plants = plant_signature(opportunity)

                for weight_index, weight_strength in enumerate(v9.WEIGHT_STRENGTHS):
                    weight_seed = seed + 1_000_000 + weight_index * 10_000 + replicate
                    expected, _ = v8.realize_local_context(
                        opportunity,
                        support_seed=seed + 17,
                        support_strength=0.0,
                        weight_seed=weight_seed,
                        weight_strength=weight_strength,
                    )
                    actual, audit = v9.realize_local_context(
                        opportunity,
                        support_seed=seed + 17,
                        support_strength=0.0,
                        weight_seed=weight_seed,
                        weight_strength=weight_strength,
                    )
                    if actual != expected or not audit.get("zero_support_exact_v8_bypass"):
                        failures["zero_support_v8_identity"].append((state_id, weight_strength))

                support_summaries = []
                for strength_index, support_strength in enumerate(SUPPORT_STRENGTHS):
                    pre_pair_plant_sets = []
                    final_pair_sets = []
                    final_plant_sets = []
                    final_pollinator_sets = []
                    shannon_values = []
                    overlap_values = []
                    for context_index in range(context_replicates):
                        support_seed = (
                            seed + 20_000_000 + sat_index * 1_000_000
                            + iso_index * 100_000 + replicate * 1_000
                            + strength_index * 100 + context_index
                        )
                        weight_seed = support_seed + 50_000_000
                        try:
                            v8_realized, _ = v8.realize_local_context(
                                opportunity,
                                support_seed=support_seed,
                                support_strength=support_strength,
                                weight_seed=weight_seed,
                                weight_strength=WEIGHT_PROBE,
                            )
                            v9_realized, audit = v9.realize_local_context(
                                opportunity,
                                support_seed=support_seed,
                                support_strength=support_strength,
                                weight_seed=weight_seed,
                                weight_strength=WEIGHT_PROBE,
                            )
                        except Exception as exc:
                            failures["unexpected_exception"].append(
                                (state_id, support_strength, context_index, type(exc).__name__, str(exc))
                            )
                            continue

                        # Verify the inherited full v8 pair draw did not move under the v9 plant mask.
                        v8_mask, _ = v8.draw_hierarchical_pair_support_mask(
                            opportunity,
                            support_seed=support_seed,
                            support_strength=support_strength,
                        )
                        active_indices = tuple(audit["plant_layer"]["active_plant_indices"])
                        expected_combined = v9.combine_plant_and_v8_pair_masks(
                            opportunity,
                            active_plant_indices=active_indices,
                            v8_pair_mask=v8_mask,
                        )
                        direct_active = set(active_indices)
                        # Every active pair in v9 must have been active in the original v8 mask and on an active plant.
                        for row_index, mask_row in enumerate(expected_combined):
                            if row_index not in direct_active and any(mask_row):
                                failures["matched_v8_pair_draw_changed"].append(
                                    (state_id, support_strength, context_index, "inactive_plant_has_pair")
                                )

                        error = max_retained_budget_error(opportunity, v9_realized)
                        if error > 1e-11 or audit.get("max_retained_row_budget_error", 0.0) > 1e-11:
                            failures["retained_row_budget"].append(
                                (state_id, support_strength, context_index, max(error, audit.get("max_retained_row_budget_error", 0.0)))
                            )
                        if not realized_is_opportunity_subset(opportunity, v9_realized):
                            failures["opportunity_subset"].append((state_id, support_strength, context_index))

                        pre_pair_plants = tuple(sorted(audit["plant_layer"]["active_plant_names_before_pair_projection"]))
                        v9_pairs = support_signature(v9_realized)
                        v8_pairs = support_signature(v8_realized)
                        v9_plants = plant_signature(v9_realized)
                        v9_pollinators = pollinator_signature(v9_realized)
                        pre_pair_plant_sets.append(pre_pair_plants)
                        final_pair_sets.append(v9_pairs)
                        final_plant_sets.append(v9_plants)
                        final_pollinator_sets.append(v9_pollinators)

                        if len(pre_pair_plants) < len(baseline_plants):
                            positive_plant_drop_contexts += 1
                        if audit["plant_layer"].get("empty_plant_opportunity"):
                            empty_plant_opportunity_contexts += 1
                        if v9_realized is None or positive_total(v9_realized) <= 0.0:
                            empty_final_contexts += 1

                        if len(v9_pairs) < len(v8_pairs):
                            matched_v9_sparser_than_v8 += 1
                        elif len(v9_pairs) == len(v8_pairs):
                            matched_equal_pair_count += 1
                        else:
                            matched_v9_denser_than_v8 += 1
                        if len(v8_pairs) > 0:
                            matched_pair_count_ratios.append(len(v9_pairs) / len(v8_pairs))

                        metrics = metric_pair_or_none(v9_realized)
                        if metrics is not None:
                            shannon_values.append(metrics[0])
                            overlap_values.append(metrics[1])

                    support_summaries.append({
                        "support_strength": support_strength,
                        "distinct_pre_pair_plant_sets": len(set(pre_pair_plant_sets)),
                        "distinct_final_pair_sets": len(set(final_pair_sets)),
                        "distinct_final_plant_sets": len(set(final_plant_sets)),
                        "distinct_final_pollinator_sets": len(set(final_pollinator_sets)),
                    })
                    if len(shannon_values) >= 2 and len(overlap_values) >= 2:
                        metric_ranges.append({
                            "state_id": state_id,
                            "support_strength": support_strength,
                            "shannon_range": max(shannon_values) - min(shannon_values),
                            "overlap_range": max(overlap_values) - min(overlap_values),
                        })

                state_rows.append({
                    "state_id": state_id,
                    "positive": positive_total(opportunity) > 0.0,
                    "baseline_positive_plants": len(baseline_plants),
                    "support_summaries": support_summaries,
                })

    positive_summaries = [
        summary
        for state in state_rows if state["positive"]
        for summary in state["support_summaries"]
    ]
    tests = {
        "zero_support_exact_v8_identity": not failures["zero_support_v8_identity"],
        "matched_full_v8_pair_draw_is_unchanged_before_plant_intersection": not failures["matched_v8_pair_draw_changed"],
        "retained_positive_plant_row_budgets_conserved": not failures["retained_row_budget"],
        "all_realized_taxa_and_pairs_are_v4_opportunity_subsets": not failures["opportunity_subset"],
        "no_unexpected_v9_exceptions": not failures["unexpected_exception"],
        "nonzero_plant_availability_removes_feasible_positive_plants": positive_plant_drop_contexts > 0,
        "repeated_contexts_branch_pre_pair_plant_availability": any(
            row["distinct_pre_pair_plant_sets"] >= 2 for row in positive_summaries
        ),
        "repeated_contexts_branch_final_pair_support": any(
            row["distinct_final_pair_sets"] >= 2 for row in positive_summaries
        ),
        "repeated_contexts_branch_final_plant_support": any(
            row["distinct_final_plant_sets"] >= 2 for row in positive_summaries
        ),
        "repeated_contexts_branch_final_pollinator_support": any(
            row["distinct_final_pollinator_sets"] >= 2 for row in positive_summaries
        ),
        "plant_layer_can_make_matched_context_sparser_than_v8": (
            matched_v9_sparser_than_v8 > 0 and matched_v9_denser_than_v8 == 0
        ),
        "support_variation_can_change_shannon": any(row["shannon_range"] > EPS for row in metric_ranges),
        "support_variation_can_change_plant_overlap": any(row["overlap_range"] > EPS for row in metric_ranges),
        "frozen_v4_opportunity_contract_remains_true": inherited_ok,
    }
    passed = all(tests.values())
    return {
        "schema_version": "1.0",
        "analysis": "abm_v9_local_plant_opportunity_synthetic_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v9_fit",
        "empirical_inputs_loaded": [],
        "menorca_values_loaded": False,
        "giannutri_values_loaded": False,
        "cabrera_values_loaded": False,
        "grid": {
            "isolations": list(ISOLATIONS),
            "saturations": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "weight_strength_for_branching_probe": WEIGHT_PROBE,
            "evolution_replicates": evolution_replicates,
            "context_replicates": context_replicates,
        },
        "state_counts": {
            "total": len(state_rows),
            "positive": sum(row["positive"] for row in state_rows),
        },
        "context_diagnostics": {
            "positive_plant_drop_contexts": positive_plant_drop_contexts,
            "empty_plant_opportunity_contexts": empty_plant_opportunity_contexts,
            "empty_final_contexts": empty_final_contexts,
            "matched_v9_sparser_than_v8_contexts": matched_v9_sparser_than_v8,
            "matched_equal_pair_count_contexts": matched_equal_pair_count,
            "matched_v9_denser_than_v8_contexts": matched_v9_denser_than_v8,
            "matched_pair_count_ratio_median_v9_over_v8": (
                float(statistics.median(matched_pair_count_ratios)) if matched_pair_count_ratios else None
            ),
        },
        "tests": tests,
        "failure_details": failures,
        "metric_range_rows": metric_ranges,
        "decision": (
            "v9_opens_local_plant_opportunity_before_pair_support"
            if passed
            else "v9_local_plant_opportunity_fails_synthetic_prevalidation"
        ),
        "next_gate": (
            "Only after this synthetic gate passes: select a new independent repeated-local quantitative island system. "
            "Its sampling exposure must be standardized or assigned a frozen observation layer before target inspection."
        ),
        "claim_boundary": (
            "Passing establishes only that an independent local plant/resource opportunity layer can be added upstream of unchanged v8 support without empirical fitting, "
            "while preserving nested identities and opportunity constraints. It does not validate the process empirically."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evolution-replicates", type=int, default=4)
    parser.add_argument("--context-replicates", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(args.evolution_replicates, args.context_replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "decision": payload["decision"],
        "state_counts": payload["state_counts"],
        "context_diagnostics": payload["context_diagnostics"],
        "tests": payload["tests"],
    }, indent=2))


if __name__ == "__main__":
    main()
