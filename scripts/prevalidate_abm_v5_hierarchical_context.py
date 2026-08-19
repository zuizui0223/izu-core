from __future__ import annotations

import argparse
import importlib.util
import json
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
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def support(network):
    return tuple(tuple(value > 0 for value in row) for row in network.matrix)


def metric_or_none(network):
    try:
        return network_metrics(network)
    except ValueError as exc:
        if "no positive interactions" not in str(exc):
            raise
        return None


def sign_counts(values: list[float]) -> dict:
    return {
        "positive": sum(value > EPS for value in values),
        "negative": sum(value < -EPS for value in values),
        "near_zero": sum(abs(value) <= EPS for value in values),
    }


def build(evolution_replicates: int = 6, context_replicates: int = 12, seed: int = 20260819) -> dict:
    if context_replicates < 2 or context_replicates % 2:
        raise ValueError("context_replicates must be an even integer >= 2")
    v5 = load_module(V5, "abm_v5_prevalidation_core")
    v4 = load_module(V4_WEIGHTED, "abm_v5_prevalidation_v4_weighted")
    inherited = json.loads(V4_GRADIENT_RESULT.read_text())
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    inherited_ok = all(inherited["tests"].get(key) for key in required_v4)
    if not inherited_ok:
        raise RuntimeError("frozen v4 directional contract is not satisfied")

    identity_failures = []
    dimension_failures = []
    support_failures = []
    max_row_budget_error = 0.0
    max_total_weight_error = 0.0
    empty_states = []
    single_partner_states = []
    branchable_states = []
    by_strength = {
        str(strength): {
            "spreads": [],
            "paired_shannon": [],
            "paired_overlap": [],
        }
        for strength in v5.CONTEXT_STRENGTHS
    }

    for sat_i, saturation in enumerate(SATURATIONS):
        for iso_i, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + sat_i * 100_000 + iso_i * 10_000 + replicate
                state_id = f"sat={saturation}|iso={isolation}|rep={replicate}"
                feasible = v4.run_weighted_network(isolation, evolution_seed, saturation)
                zero = v5.realize_local_context(
                    feasible,
                    context_seed=seed + 9_000_000,
                    context_strength=0.0,
                )
                if zero != feasible:
                    identity_failures.append(state_id)

                feasible_metrics = metric_or_none(feasible)
                if feasible_metrics is None:
                    empty_states.append(state_id)
                    branchable = False
                elif len(feasible.pollinator_names) == 1:
                    single_partner_states.append(state_id)
                    branchable = False
                else:
                    branchable_states.append(state_id)
                    branchable = True

                for strength_i, strength in enumerate(v5.CONTEXT_STRENGTHS):
                    metrics = []
                    for context_rep in range(context_replicates):
                        context_seed = (
                            seed + 20_000_000 + sat_i * 1_000_000 + iso_i * 100_000
                            + replicate * 1_000 + strength_i * 100 + context_rep
                        )
                        realized = v5.realize_local_context(
                            feasible,
                            context_seed=context_seed,
                            context_strength=strength,
                        )
                        if (
                            realized.plant_names != feasible.plant_names
                            or realized.pollinator_names != feasible.pollinator_names
                        ):
                            dimension_failures.append((state_id, strength, context_rep))
                        if support(realized) != support(feasible):
                            support_failures.append((state_id, strength, context_rep))
                        for before, after in zip(feasible.matrix, realized.matrix):
                            max_row_budget_error = max(
                                max_row_budget_error,
                                abs(sum(before) - sum(after)),
                            )
                        max_total_weight_error = max(
                            max_total_weight_error,
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
                    spread = {
                        "state_id": state_id,
                        "n_pollinators": len(feasible.pollinator_names),
                        "branchable": branchable,
                        "shannon_range": max(shannon) - min(shannon),
                        "overlap_range": max(overlap) - min(overlap),
                    }
                    by_strength[str(strength)]["spreads"].append(spread)
                    if branchable:
                        for pair_i in range(0, context_replicates, 2):
                            by_strength[str(strength)]["paired_shannon"].append(
                                shannon[pair_i + 1] - shannon[pair_i]
                            )
                            by_strength[str(strength)]["paired_overlap"].append(
                                overlap[pair_i + 1] - overlap[pair_i]
                            )

    strength_summary = {}
    for strength in v5.CONTEXT_STRENGTHS:
        raw = by_strength[str(strength)]
        branchable = [row for row in raw["spreads"] if row["branchable"]]
        nonbranchable = [row for row in raw["spreads"] if not row["branchable"]]
        b_shannon = [row["shannon_range"] for row in branchable]
        b_overlap = [row["overlap_range"] for row in branchable]
        nb_shannon = [row["shannon_range"] for row in nonbranchable]
        nb_overlap = [row["overlap_range"] for row in nonbranchable]
        strength_summary[str(strength)] = {
            "branchable_state_count": len(branchable),
            "single_partner_nonbranchable_state_count": len(nonbranchable),
            "median_branchable_shannon_range": statistics.median(b_shannon) if b_shannon else None,
            "minimum_branchable_shannon_range": min(b_shannon) if b_shannon else None,
            "median_branchable_overlap_range": statistics.median(b_overlap) if b_overlap else None,
            "minimum_branchable_overlap_range": min(b_overlap) if b_overlap else None,
            "maximum_nonbranchable_shannon_range": max(nb_shannon) if nb_shannon else None,
            "maximum_nonbranchable_overlap_range": max(nb_overlap) if nb_overlap else None,
            "branchable_context_shannon_signs": sign_counts(raw["paired_shannon"]),
            "branchable_context_overlap_signs": sign_counts(raw["paired_overlap"]),
        }

    nonzero = [strength_summary[str(s)] for s in v5.CONTEXT_STRENGTHS if s > 0]
    variation_in_every_branchable_state = all(
        row["minimum_branchable_shannon_range"] is not None
        and row["minimum_branchable_shannon_range"] > EPS
        and row["minimum_branchable_overlap_range"] is not None
        and row["minimum_branchable_overlap_range"] > EPS
        for row in nonzero
    )
    single_partner_states_remain_nonbranchable = all(
        (row["maximum_nonbranchable_shannon_range"] is None or row["maximum_nonbranchable_shannon_range"] <= EPS)
        and (row["maximum_nonbranchable_overlap_range"] is None or row["maximum_nonbranchable_overlap_range"] <= EPS)
        for row in nonzero
    )
    full = strength_summary["1.0"]
    shannon_signs = full["branchable_context_shannon_signs"]
    overlap_signs = full["branchable_context_overlap_signs"]

    tests = {
        "zero_strength_exact_v4_identity": not identity_failures,
        "plant_pollinator_dimensions_invariant": not dimension_failures,
        "positive_link_support_invariant": not support_failures,
        "fixed_row_budget_conserved": max_row_budget_error <= 1e-12 and max_total_weight_error <= 1e-11,
        "every_branchable_state_varies_at_all_nonzero_strengths": variation_in_every_branchable_state,
        "single_partner_states_correctly_remain_nonbranchable": single_partner_states_remain_nonbranchable,
        "full_strength_branchable_context_pairs_span_both_shannon_directions": (
            shannon_signs["positive"] > 0 and shannon_signs["negative"] > 0
        ),
        "full_strength_branchable_context_pairs_span_both_overlap_directions": (
            overlap_signs["positive"] > 0 and overlap_signs["negative"] > 0
        ),
        "frozen_v4_opportunity_contract_remains_true": inherited_ok,
    }
    passed = all(tests.values())
    return {
        "analysis": "abm_v5_hierarchical_context_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v5_fit",
        "prevalidation_revision": "The first gate incorrectly required variation in single-pollinator positive states. Under fixed support and fixed row totals a one-column state has no redistribution degree of freedom. The model was not changed; v2 of the gate tests every state with >=2 pollinators and requires single-pollinator states to remain invariant.",
        "empirical_inputs_loaded": [],
        "frozen_v4_result_source": str(V4_GRADIENT_RESULT),
        "isolation_grid": list(ISOLATIONS),
        "saturation_envelope": list(SATURATIONS),
        "context_strength_envelope": list(v5.CONTEXT_STRENGTHS),
        "evolution_replicates_per_cell": evolution_replicates,
        "context_replicates_per_state_strength": context_replicates,
        "state_counts": {
            "branchable_positive": len(branchable_states),
            "single_partner_positive": len(single_partner_states),
            "empty": len(empty_states),
        },
        "single_partner_state_ids": single_partner_states,
        "empty_state_ids": empty_states,
        "maximum_row_budget_error": max_row_budget_error,
        "maximum_total_weight_error": max_total_weight_error,
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
        "claim_boundary": "Passing this synthetic gate shows only that the hierarchical mechanism has the required support while exactly preserving v4 opportunity totals and support. Single-pollinator states are explicitly non-branchable. This is not empirical evidence for the affinity distribution or any fitted context-strength value.",
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
        "state_counts": payload["state_counts"],
        "tests": payload["tests"],
        "strength_summary": payload["strength_summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
