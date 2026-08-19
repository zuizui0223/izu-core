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
V5 = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V4_WEIGHTED = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V4_GRADIENT_RESULT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
OUT = ROOT / "data/results/abm_v5_hierarchical_context_prevalidation.json"
ISOLATIONS = (0.0, 0.5, 1.0)
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def support(network):
    return tuple(tuple(value > 0 for value in row) for row in network.matrix)


def max_row_sum_error(left, right) -> float:
    return max(
        abs(sum(a) - sum(b))
        for a, b in zip(left.matrix, right.matrix)
    )


def metric_or_none(network):
    try:
        return network_metrics(network)
    except ValueError as exc:
        if "no positive interactions" not in str(exc):
            raise
        return None


def sign_counts(values: list[float], tolerance: float = 1e-12) -> dict:
    return {
        "positive": sum(value > tolerance for value in values),
        "negative": sum(value < -tolerance for value in values),
        "near_zero": sum(abs(value) <= tolerance for value in values),
    }


def build(evolution_replicates: int = 6, context_replicates: int = 12, seed: int = 20260819) -> dict:
    if context_replicates < 2 or context_replicates % 2:
        raise ValueError("context_replicates must be an even integer >= 2")
    v5 = load_module(V5, "abm_v5_prevalidation_core")
    v4 = load_module(V4_WEIGHTED, "abm_v5_prevalidation_v4_weighted")
    inherited = json.loads(V4_GRADIENT_RESULT.read_text())
    inherited_tests = inherited["tests"]
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    if not all(inherited_tests.get(key) for key in required_v4):
        raise RuntimeError("frozen v4 directional contract is not satisfied")

    identity_failures = []
    dimension_failures = []
    support_failures = []
    maximum_row_budget_error = 0.0
    maximum_total_weight_error = 0.0
    positive_state_count = 0
    empty_state_count = 0
    by_strength = {
        str(strength): {
            "state_metric_spreads": [],
            "paired_context_deltas_shannon": [],
            "paired_context_deltas_overlap": [],
        }
        for strength in v5.CONTEXT_STRENGTHS
    }

    for saturation_index, saturation in enumerate(SATURATIONS):
        for isolation_index, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + saturation_index * 100_000 + isolation_index * 10_000 + replicate
                feasible = v4.run_weighted_network(isolation, evolution_seed, saturation)
                zero = v5.realize_local_context(feasible, context_seed=seed + 9_000_000, context_strength=0.0)
                if zero != feasible:
                    identity_failures.append({
                        "saturation": saturation,
                        "isolation_index": isolation,
                        "replicate": replicate,
                    })

                feasible_metrics = metric_or_none(feasible)
                if feasible_metrics is None:
                    empty_state_count += 1
                else:
                    positive_state_count += 1

                for strength_index, strength in enumerate(v5.CONTEXT_STRENGTHS):
                    metrics = []
                    for context_replicate in range(context_replicates):
                        context_seed = (
                            seed
                            + 20_000_000
                            + saturation_index * 1_000_000
                            + isolation_index * 100_000
                            + replicate * 1_000
                            + strength_index * 100
                            + context_replicate
                        )
                        realized = v5.realize_local_context(
                            feasible,
                            context_seed=context_seed,
                            context_strength=strength,
                        )
                        if realized.plant_names != feasible.plant_names or realized.pollinator_names != feasible.pollinator_names:
                            dimension_failures.append({
                                "saturation": saturation,
                                "isolation_index": isolation,
                                "replicate": replicate,
                                "strength": strength,
                                "context_replicate": context_replicate,
                            })
                        if support(realized) != support(feasible):
                            support_failures.append({
                                "saturation": saturation,
                                "isolation_index": isolation,
                                "replicate": replicate,
                                "strength": strength,
                                "context_replicate": context_replicate,
                            })
                        maximum_row_budget_error = max(maximum_row_budget_error, max_row_sum_error(feasible, realized))
                        maximum_total_weight_error = max(
                            maximum_total_weight_error,
                            abs(
                                sum(sum(row) for row in feasible.matrix)
                                - sum(sum(row) for row in realized.matrix)
                            ),
                        )
                        current = metric_or_none(realized)
                        if current is not None:
                            metrics.append(current)

                    if feasible_metrics is None:
                        continue
                    if len(metrics) != context_replicates:
                        raise RuntimeError("positive feasible state produced missing realized metrics")
                    shannon = [float(row["interaction_shannon"]) for row in metrics]
                    overlap = [float(row["mean_plant_niche_overlap_morisita_horn"]) for row in metrics]
                    by_strength[str(strength)]["state_metric_spreads"].append({
                        "saturation": saturation,
                        "isolation_index": isolation,
                        "replicate": replicate,
                        "shannon_range": max(shannon) - min(shannon),
                        "shannon_sd": statistics.pstdev(shannon),
                        "overlap_range": max(overlap) - min(overlap),
                        "overlap_sd": statistics.pstdev(overlap),
                    })
                    for pair_index in range(0, context_replicates, 2):
                        by_strength[str(strength)]["paired_context_deltas_shannon"].append(
                            shannon[pair_index + 1] - shannon[pair_index]
                        )
                        by_strength[str(strength)]["paired_context_deltas_overlap"].append(
                            overlap[pair_index + 1] - overlap[pair_index]
                        )

    strength_summary = {}
    for strength in v5.CONTEXT_STRENGTHS:
        raw = by_strength[str(strength)]
        spreads = raw["state_metric_spreads"]
        shannon_ranges = [row["shannon_range"] for row in spreads]
        overlap_ranges = [row["overlap_range"] for row in spreads]
        strength_summary[str(strength)] = {
            "positive_state_count": len(spreads),
            "median_shannon_range_across_contexts": statistics.median(shannon_ranges) if shannon_ranges else None,
            "minimum_shannon_range_across_contexts": min(shannon_ranges) if shannon_ranges else None,
            "median_overlap_range_across_contexts": statistics.median(overlap_ranges) if overlap_ranges else None,
            "minimum_overlap_range_across_contexts": min(overlap_ranges) if overlap_ranges else None,
            "paired_context_shannon_signs": sign_counts(raw["paired_context_deltas_shannon"]),
            "paired_context_overlap_signs": sign_counts(raw["paired_context_deltas_overlap"]),
        }

    nonzero = [strength_summary[str(s)] for s in v5.CONTEXT_STRENGTHS if s > 0]
    measurable_variation = all(
        row["minimum_shannon_range_across_contexts"] is not None
        and row["minimum_shannon_range_across_contexts"] > 1e-12
        and row["minimum_overlap_range_across_contexts"] is not None
        and row["minimum_overlap_range_across_contexts"] > 1e-12
        for row in nonzero
    )
    full = strength_summary["1.0"]
    shannon_branching = full["paired_context_shannon_signs"]["positive"] > 0 and full["paired_context_shannon_signs"]["negative"] > 0
    overlap_branching = full["paired_context_overlap_signs"]["positive"] > 0 and full["paired_context_overlap_signs"]["negative"] > 0
    identity_pass = not identity_failures
    dimensions_pass = not dimension_failures
    support_pass = not support_failures
    budget_pass = maximum_row_budget_error <= 1e-12 and maximum_total_weight_error <= 1e-11

    tests = {
        "zero_strength_exact_v4_identity": identity_pass,
        "plant_pollinator_dimensions_invariant": dimensions_pass,
        "positive_link_support_invariant": support_pass,
        "fixed_row_budget_conserved": budget_pass,
        "all_nonzero_strengths_generate_shannon_and_overlap_variation": measurable_variation,
        "full_strength_independent_context_pairs_branch_both_shannon_directions": shannon_branching,
        "full_strength_independent_context_pairs_branch_both_overlap_directions": overlap_branching,
        "frozen_v4_opportunity_contract_remains_true": all(inherited_tests.get(key) for key in required_v4),
    }
    passed = all(tests.values())
    return {
        "analysis": "abm_v5_hierarchical_context_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v5_fit",
        "empirical_inputs_loaded": [],
        "frozen_v4_result_source": str(V4_GRADIENT_RESULT),
        "isolation_grid": list(ISOLATIONS),
        "saturation_envelope": list(SATURATIONS),
        "context_strength_envelope": list(v5.CONTEXT_STRENGTHS),
        "evolution_replicates_per_cell": evolution_replicates,
        "context_replicates_per_state_strength": context_replicates,
        "positive_feasible_states": positive_state_count,
        "empty_feasible_states": empty_state_count,
        "maximum_row_budget_error": maximum_row_budget_error,
        "maximum_total_weight_error": maximum_total_weight_error,
        "strength_summary": strength_summary,
        "failure_details": {
            "identity_failures": identity_failures,
            "dimension_failures": dimension_failures,
            "support_failures": support_failures,
        },
        "tests": tests,
        "decision": (
            "v5_preserves_v4_opportunity_and_opens_local_architecture_branching"
            if passed
            else "v5_hierarchical_context_fails_prevalidation"
        ),
        "next_gate": "Only if all prevalidation tests pass: freeze an independent empirical validation design before inspecting the new system's raw weighted outcomes. Ogasawara is consumed as prior falsification/diagnosis and cannot serve as v5 confirmatory evidence.",
        "claim_boundary": "Passing this synthetic gate shows only that the hierarchical mechanism has the required support while exactly preserving v4 opportunity totals and support. It is not empirical evidence that a real local context follows the synthetic affinity distribution or that context strength has any fitted value.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evolution-replicates", type=int, default=6)
    parser.add_argument("--context-replicates", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260819)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(args.evolution_replicates, args.context_replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "decision": payload["decision"],
        "tests": payload["tests"],
        "strength_summary": payload["strength_summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
