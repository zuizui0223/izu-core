from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
from pathlib import Path

from channel_id.external_archipelago_network import network_metrics

ROOT = Path(__file__).resolve().parents[1]
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V4_WEIGHTED = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V4_GRADIENT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
OUT = ROOT / "data/results/abm_v6_local_support_prevalidation.json"
ISOLATIONS = (0.0, 0.5, 1.0)
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def positive_total(network) -> float:
    return sum(sum(row) for row in network.matrix)


def max_row_budget_error(left, right) -> float:
    if len(left.matrix) != len(right.matrix):
        return float("inf")
    return max(
        abs(sum(before) - sum(after))
        for before, after in zip(left.matrix, right.matrix)
    ) if left.matrix else 0.0


def metric_pair_or_none(network):
    try:
        metrics = network_metrics(network)
    except ValueError as exc:
        if "no positive interactions" in str(exc):
            return None
        raise
    overlap = metrics["mean_plant_niche_overlap_morisita_horn"]
    if overlap is None:
        return None
    return float(metrics["interaction_shannon"]), float(overlap)


def build(
    evolution_replicates: int = 4,
    context_replicates: int = 10,
    seed: int = 20260820,
) -> dict:
    if evolution_replicates < 1:
        raise ValueError("evolution_replicates must be positive")
    if context_replicates < 2:
        raise ValueError("context_replicates must be >=2")

    v6 = load_module(V6_SCRIPT, "abm_v6_prevalidation_core")
    v4 = load_module(V4_WEIGHTED, "abm_v6_prevalidation_v4")
    v5 = load_module(V5_SCRIPT, "abm_v6_prevalidation_v5")
    inherited = json.loads(V4_GRADIENT.read_text())
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    inherited_ok = all(inherited["tests"].get(key) for key in required_v4)
    if not inherited_ok:
        raise RuntimeError("frozen v4 opportunity contract is not satisfied")

    zero_v4_failures = []
    zero_support_v5_failures = []
    plant_identity_failures = []
    partner_subset_failures = []
    row_budget_failures = []
    active_zero_row_failures = []
    state_rows = []
    context_metric_ranges = []

    for sat_index, saturation in enumerate(SATURATIONS):
        for iso_index, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + sat_index * 100_000 + iso_index * 10_000 + replicate
                state_id = f"sat={saturation}|iso={isolation}|rep={replicate}"
                feasible = v4.run_weighted_network(isolation, evolution_seed, saturation)
                feasible_pollinators = set(feasible.pollinator_names)
                positive = positive_total(feasible) > 0
                reducible = positive and len(feasible.pollinator_names) >= 2

                exact_v4 = v6.realize_local_context(
                    feasible,
                    support_seed=seed + 1,
                    support_strength=0.0,
                    weight_seed=seed + 2,
                    weight_strength=0.0,
                )
                if exact_v4 != feasible:
                    zero_v4_failures.append(state_id)

                for weight_index, weight_strength in enumerate(v6.WEIGHT_STRENGTHS):
                    weight_seed = seed + 1_000_000 + weight_index * 10_000 + replicate
                    direct_v5 = v5.realize_local_context(
                        feasible,
                        context_seed=weight_seed,
                        context_strength=weight_strength,
                    )
                    via_v6 = v6.realize_local_context(
                        feasible,
                        support_seed=seed + 3,
                        support_strength=0.0,
                        weight_seed=weight_seed,
                        weight_strength=weight_strength,
                    )
                    if via_v6 != direct_v5:
                        zero_support_v5_failures.append((state_id, weight_strength))

                support_summaries = []
                for support_index, support_strength in enumerate(v6.SUPPORT_STRENGTHS):
                    support_sets = []
                    active_counts = []
                    shannon = []
                    overlap = []
                    for context_index in range(context_replicates):
                        support_seed = (
                            seed + 20_000_000 + sat_index * 1_000_000
                            + iso_index * 100_000 + replicate * 1_000
                            + support_index * 100 + context_index
                        )
                        weight_seed = support_seed + 50_000_000
                        realized = v6.realize_local_context(
                            feasible,
                            support_seed=support_seed,
                            support_strength=support_strength,
                            weight_seed=weight_seed,
                            weight_strength=0.5,
                        )
                        if realized.plant_names != feasible.plant_names:
                            plant_identity_failures.append((state_id, support_strength, context_index))
                        if not set(realized.pollinator_names).issubset(feasible_pollinators):
                            partner_subset_failures.append((state_id, support_strength, context_index))
                        error = max_row_budget_error(feasible, realized)
                        if error > 1e-11:
                            row_budget_failures.append((state_id, support_strength, context_index, error))
                        if positive and positive_total(realized) <= 0:
                            active_zero_row_failures.append((state_id, support_strength, context_index))
                        support_sets.append(tuple(realized.pollinator_names))
                        active_counts.append(len(realized.pollinator_names))
                        metrics = metric_pair_or_none(realized)
                        if metrics is not None:
                            shannon.append(metrics[0])
                            overlap.append(metrics[1])

                    summary = {
                        "support_strength": support_strength,
                        "distinct_support_sets": len(set(support_sets)),
                        "mean_active_pollinators": statistics.mean(active_counts),
                        "min_active_pollinators": min(active_counts),
                        "max_active_pollinators": max(active_counts),
                    }
                    support_summaries.append(summary)
                    if reducible and support_strength > 0 and shannon and overlap:
                        context_metric_ranges.append({
                            "state_id": state_id,
                            "support_strength": support_strength,
                            "shannon_range": max(shannon) - min(shannon),
                            "overlap_range": max(overlap) - min(overlap),
                            "distinct_support_sets": len(set(support_sets)),
                        })

                state_rows.append({
                    "state_id": state_id,
                    "positive": positive,
                    "reducible": reducible,
                    "feasible_pollinator_count": len(feasible.pollinator_names),
                    "support_summaries": support_summaries,
                })

    reducible_states = [row for row in state_rows if row["reducible"]]
    positive_support_rows = [
        summary
        for row in reducible_states
        for summary in row["support_summaries"]
        if summary["support_strength"] > 0
    ]
    support_reduction_present = any(
        summary["mean_active_pollinators"]
        < row["feasible_pollinator_count"] - EPS
        for row in reducible_states
        for summary in row["support_summaries"]
        if summary["support_strength"] > 0
    )
    support_branching_present = any(
        summary["distinct_support_sets"] >= 2
        for summary in positive_support_rows
    )
    shannon_branching_present = any(
        row["shannon_range"] > EPS for row in context_metric_ranges
    )
    overlap_branching_present = any(
        row["overlap_range"] > EPS for row in context_metric_ranges
    )

    tests = {
        "zero_support_zero_weight_exact_v4_identity": not zero_v4_failures,
        "zero_support_exact_v5_identity_across_weight_envelope": not zero_support_v5_failures,
        "plant_identities_invariant": not plant_identity_failures,
        "local_pollinators_always_subset_of_island_feasible_pool": not partner_subset_failures,
        "fixed_plant_row_budget_conserved": not row_budget_failures,
        "positive_feasible_states_do_not_become_zero_total": not active_zero_row_failures,
        "positive_support_strength_can_reduce_local_support": support_reduction_present,
        "repeated_contexts_can_branch_into_distinct_local_support_sets": support_branching_present,
        "support_varying_contexts_can_change_shannon": shannon_branching_present,
        "support_varying_contexts_can_change_plant_overlap": overlap_branching_present,
        "frozen_v4_opportunity_contract_remains_true": inherited_ok,
    }
    passed = all(tests.values())
    return {
        "schema_version": "1.0",
        "analysis": "abm_v6_local_support_synthetic_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v6_fit",
        "empirical_inputs_loaded": [],
        "menorca_values_loaded": False,
        "grid": {
            "isolations": list(ISOLATIONS),
            "saturations": list(SATURATIONS),
            "support_strengths": list(v6.SUPPORT_STRENGTHS),
            "weight_strengths_for_identity": list(v6.WEIGHT_STRENGTHS),
            "weight_strength_for_support_branching_probe": 0.5,
            "evolution_replicates": evolution_replicates,
            "context_replicates": context_replicates,
        },
        "state_counts": {
            "total": len(state_rows),
            "positive": sum(row["positive"] for row in state_rows),
            "reducible": len(reducible_states),
        },
        "tests": tests,
        "failure_details": {
            "zero_v4_failures": zero_v4_failures,
            "zero_support_v5_failures": zero_support_v5_failures,
            "plant_identity_failures": plant_identity_failures,
            "partner_subset_failures": partner_subset_failures,
            "row_budget_failures": row_budget_failures,
            "active_zero_row_failures": active_zero_row_failures,
        },
        "support_branching_summary": {
            "positive_support_state_strength_rows": len(positive_support_rows),
            "rows_with_multiple_support_sets": sum(
                row["distinct_support_sets"] >= 2 for row in positive_support_rows
            ),
            "metric_range_rows": context_metric_ranges,
        },
        "decision": (
            "v6_preserves_v4_v5_invariants_and_opens_local_support_branching"
            if passed
            else "v6_local_support_fails_synthetic_prevalidation"
        ),
        "next_gate": "Only after this synthetic gate passes: select and freeze a new independent quantitative island network system before its v6 target metrics are inspected. Menorca must not be reused to tune or confirm v6.",
        "claim_boundary": "Passing establishes mechanism support only. It does not estimate local partner-availability probabilities, explain Menorca quantitatively, or validate a habitat/season mechanism.",
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
        "tests": payload["tests"],
        "support_branching_summary": {
            "positive_support_state_strength_rows": payload["support_branching_summary"]["positive_support_state_strength_rows"],
            "rows_with_multiple_support_sets": payload["support_branching_summary"]["rows_with_multiple_support_sets"],
        },
    }, indent=2))


if __name__ == "__main__":
    main()
