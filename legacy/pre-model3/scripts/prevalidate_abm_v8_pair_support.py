from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

from channel_id.external_archipelago_network import network_metrics

ROOT = Path(__file__).resolve().parents[1]
V8_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V4_SCRIPT = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V4_GRADIENT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
OUT = ROOT / "data/results/abm_v8_pair_support_prevalidation.json"
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


def realized_pairs_are_source_subset(opportunity, realized) -> bool:
    if realized is None:
        return True
    source = {
        (plant, pollinator)
        for row_index, plant in enumerate(opportunity.plant_names)
        for column_index, pollinator in enumerate(opportunity.pollinator_names)
        if opportunity.matrix[row_index][column_index] > 0.0
    }
    return set(support_signature(realized)).issubset(source)


def build(evolution_replicates: int, context_replicates: int, seed: int) -> dict:
    if evolution_replicates < 1 or context_replicates < 2:
        raise ValueError("invalid replicate counts")
    v8 = load(V8_SCRIPT, "abm_v8_prevalidation_core")
    v5 = load(V5_SCRIPT, "abm_v8_prevalidation_v5")
    v4 = load(V4_SCRIPT, "abm_v8_prevalidation_v4")

    inherited = json.loads(V4_GRADIENT.read_text())
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    inherited_ok = all(inherited["tests"].get(key) for key in required_v4)
    if not inherited_ok:
        raise RuntimeError("frozen v4 opportunity contract failed before v8")

    failures = {
        "zero_support_v5_identity": [],
        "retained_row_budget": [],
        "taxon_or_pair_subset": [],
        "unexpected_exception": [],
    }
    state_rows = []
    metric_ranges = []
    sparse_context_count = 0
    plant_dropout_context_count = 0
    pollinator_dropout_context_count = 0
    empty_context_count = 0

    for sat_index, saturation in enumerate(SATURATIONS):
        for iso_index, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + sat_index * 100_000 + iso_index * 10_000 + replicate
                state_id = f"sat={saturation}|iso={isolation}|rep={replicate}"
                opportunity = v4.run_weighted_network(isolation, evolution_seed, saturation)
                baseline_positive_pairs = len(support_signature(opportunity))
                baseline_plants = plant_signature(opportunity)
                baseline_pollinators = pollinator_signature(opportunity)

                for weight_index, weight_strength in enumerate(v8.WEIGHT_STRENGTHS):
                    weight_seed = seed + 1_000_000 + weight_index * 10_000 + replicate
                    expected = v5.realize_local_context(
                        opportunity,
                        context_seed=weight_seed,
                        context_strength=weight_strength,
                    )
                    actual, audit = v8.realize_local_context(
                        opportunity,
                        support_seed=seed + 7,
                        support_strength=0.0,
                        weight_seed=weight_seed,
                        weight_strength=weight_strength,
                    )
                    if actual != expected or audit.get("dropped_partnerless_positive_plant_count", 0) != 0:
                        failures["zero_support_v5_identity"].append((state_id, weight_strength))

                support_summaries = []
                for strength_index, support_strength in enumerate(SUPPORT_STRENGTHS):
                    pair_sets = []
                    plant_sets = []
                    pollinator_sets = []
                    active_pair_counts = []
                    dropped_plant_counts = []
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
                            realized, audit = v8.realize_local_context(
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

                        error = max_retained_budget_error(opportunity, realized)
                        if error > 1e-11 or audit.get("max_retained_row_budget_error", 0.0) > 1e-11:
                            failures["retained_row_budget"].append(
                                (state_id, support_strength, context_index, max(error, audit.get("max_retained_row_budget_error", 0.0)))
                            )
                        if realized is not None:
                            if not set(realized.plant_names).issubset(set(opportunity.plant_names)):
                                failures["taxon_or_pair_subset"].append((state_id, support_strength, context_index, "plant"))
                            if not set(realized.pollinator_names).issubset(set(opportunity.pollinator_names)):
                                failures["taxon_or_pair_subset"].append((state_id, support_strength, context_index, "pollinator"))
                            if not realized_pairs_are_source_subset(opportunity, realized):
                                failures["taxon_or_pair_subset"].append((state_id, support_strength, context_index, "pair"))

                        pairs = support_signature(realized)
                        plants = plant_signature(realized)
                        pollinators = pollinator_signature(realized)
                        pair_sets.append(pairs)
                        plant_sets.append(plants)
                        pollinator_sets.append(pollinators)
                        active_pair_counts.append(len(pairs))
                        dropped_plant_counts.append(len(set(baseline_plants) - set(plants)))

                        if len(pairs) < baseline_positive_pairs:
                            sparse_context_count += 1
                        if len(plants) < len(baseline_plants):
                            plant_dropout_context_count += 1
                        if len(pollinators) < len(baseline_pollinators):
                            pollinator_dropout_context_count += 1
                        if realized is None or positive_total(realized) <= 0.0:
                            empty_context_count += 1

                        metrics = metric_pair_or_none(realized)
                        if metrics is not None:
                            shannon_values.append(metrics[0])
                            overlap_values.append(metrics[1])

                    support_summaries.append({
                        "support_strength": support_strength,
                        "distinct_pair_support_sets": len(set(pair_sets)),
                        "distinct_plant_support_sets": len(set(plant_sets)),
                        "distinct_pollinator_support_sets": len(set(pollinator_sets)),
                        "min_active_pairs": min(active_pair_counts) if active_pair_counts else None,
                        "max_active_pairs": max(active_pair_counts) if active_pair_counts else None,
                        "max_dropped_plants": max(dropped_plant_counts) if dropped_plant_counts else None,
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
                    "baseline_positive_pairs": baseline_positive_pairs,
                    "baseline_positive_plants": len(baseline_plants),
                    "baseline_positive_pollinators": len(baseline_pollinators),
                    "support_summaries": support_summaries,
                })

    positive_summaries = [
        summary
        for state in state_rows if state["positive"]
        for summary in state["support_summaries"]
    ]
    tests = {
        "zero_support_exact_v5_identity": not failures["zero_support_v5_identity"],
        "retained_positive_plant_row_budgets_conserved": not failures["retained_row_budget"],
        "all_realized_taxa_and_pairs_are_opportunity_subsets": not failures["taxon_or_pair_subset"],
        "no_unexpected_pair_support_exceptions": not failures["unexpected_exception"],
        "nonzero_support_generates_sparse_pair_topology": sparse_context_count > 0,
        "repeated_contexts_branch_pair_support": any(row["distinct_pair_support_sets"] >= 2 for row in positive_summaries),
        "repeated_contexts_branch_plant_support": any(row["distinct_plant_support_sets"] >= 2 for row in positive_summaries),
        "repeated_contexts_branch_pollinator_support": any(row["distinct_pollinator_support_sets"] >= 2 for row in positive_summaries),
        "pair_support_can_induce_local_plant_inactivity": plant_dropout_context_count > 0,
        "hierarchical_support_can_induce_local_pollinator_inactivity": pollinator_dropout_context_count > 0,
        "support_variation_can_change_shannon": any(row["shannon_range"] > EPS for row in metric_ranges),
        "support_variation_can_change_plant_overlap": any(row["overlap_range"] > EPS for row in metric_ranges),
        "frozen_v4_opportunity_contract_remains_true": inherited_ok,
    }
    passed = all(tests.values())
    return {
        "schema_version": "1.0",
        "analysis": "abm_v8_hierarchical_pair_support_synthetic_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v8_fit",
        "empirical_inputs_loaded": [],
        "menorca_values_loaded": False,
        "giannutri_values_loaded": False,
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
            "sparse_pair_contexts": sparse_context_count,
            "plant_dropout_contexts": plant_dropout_context_count,
            "pollinator_dropout_contexts": pollinator_dropout_context_count,
            "empty_local_contexts": empty_context_count,
        },
        "tests": tests,
        "failure_details": failures,
        "metric_range_rows": metric_ranges,
        "decision": (
            "v8_separates_pair_support_from_opportunity_and_opens_joint_local_branching"
            if passed
            else "v8_hierarchical_pair_support_fails_synthetic_prevalidation"
        ),
        "next_gate": "Only after synthetic prevalidation passes: select and freeze a new independent repeated-local quantitative island system before v8 target inspection. Menorca and Giannutri remain consumed failures.",
        "claim_boundary": "Passing establishes mechanism capability only. It shows that hierarchical pair support can create sparse realized support and joint species turnover without fitting empirical outcomes; it does not identify real habitat or phenology processes or establish v8 empirical adequacy.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evolution-replicates", type=int, default=4)
    parser.add_argument("--context-replicates", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260820)
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
