from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
import statistics
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
V7_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v7_support_closure.py"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V4_SCRIPT = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V4_GRADIENT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
OUT = ROOT / "data/results/abm_v7_support_closure_prevalidation.json"
ISOLATIONS = (0.0, 0.5, 1.0)
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)
SUPPORT_STRENGTHS = (0.25, 0.5, 0.75)
WEIGHT_STRENGTH = 0.5
EPS = 1e-12


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def positive_total(network: WeightedNetwork | None) -> float:
    if network is None:
        return 0.0
    return sum(sum(row) for row in network.matrix)


def metric_pair_or_none(network: WeightedNetwork | None):
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


def toy_resolution(v7, v6) -> dict:
    toy = WeightedNetwork.from_rows(
        ["shared_plant", "apis_only"],
        ["Apis_mellifera", "Anthophora_dispar", "Bombus_terrestris"],
        [
            [1.0, 1.0, 1.0],
            [2.0, 0.0, 0.0],
        ],
    )
    active = (1, 2)
    v6_failed = False
    try:
        v6.apply_active_pollinator_indices(toy, active)
    except RuntimeError as exc:
        v6_failed = "removed every positive partner" in str(exc)
    closed, audit = v7.apply_joint_support_closure(toy, active)
    retained_budget_ok = False
    if closed is not None:
        index = {name: i for i, name in enumerate(closed.plant_names)}
        if "shared_plant" in index:
            retained_budget_ok = math.isclose(
                sum(closed.matrix[index["shared_plant"]]),
                3.0,
                rel_tol=1e-12,
                abs_tol=1e-14,
            )
    return {
        "v6_canonical_partnerless_row_failure_reproduced": v6_failed,
        "v7_drops_only_partnerless_positive_plant": audit["dropped_partnerless_positive_plants"] == ["apis_only"],
        "v7_retains_shared_plant_budget": retained_budget_ok,
        "v7_toy_network_nonempty": closed is not None and positive_total(closed) > 0,
        "audit": audit,
    }


def build(evolution_replicates: int, context_replicates: int, seed: int) -> dict:
    if evolution_replicates < 1 or context_replicates < 2:
        raise ValueError("invalid replicate counts")
    v7 = load(V7_SCRIPT, "abm_v7_prevalidation_core")
    v6 = load(V6_SCRIPT, "abm_v7_prevalidation_v6")
    v5 = load(V5_SCRIPT, "abm_v7_prevalidation_v5")
    v4 = load(V4_SCRIPT, "abm_v7_prevalidation_v4")

    inherited = json.loads(V4_GRADIENT.read_text())
    required_v4 = (
        "partner_types_decline",
        "effective_links_decline",
        "interaction_diversity_declines",
        "plant_niche_overlap_increases",
    )
    inherited_ok = all(inherited["tests"].get(key) for key in required_v4)
    if not inherited_ok:
        raise RuntimeError("frozen v4 opportunity contract failed before v7")

    toy = toy_resolution(v7, v6)
    failures = {
        "full_support_v5_identity": [],
        "v6_admissible_mask_identity": [],
        "retained_row_budget": [],
        "taxon_subset": [],
        "unexpected_v7_exception": [],
    }
    state_rows = []
    metric_ranges = []
    v6_structural_failure_masks = 0
    v7_resolved_v6_failure_masks = 0
    synthetic_partnerless_drop_masks = 0

    for sat_index, saturation in enumerate(SATURATIONS):
        for iso_index, isolation in enumerate(ISOLATIONS):
            for replicate in range(evolution_replicates):
                evolution_seed = seed + sat_index * 100_000 + iso_index * 10_000 + replicate
                state_id = f"sat={saturation}|iso={isolation}|rep={replicate}"
                feasible = v4.run_weighted_network(isolation, evolution_seed, saturation)

                for weight_index, weight_strength in enumerate(v7.WEIGHT_STRENGTHS):
                    context_seed = seed + 1_000_000 + weight_index * 10_000 + replicate
                    direct_v5 = v5.realize_local_context(
                        feasible,
                        context_seed=context_seed,
                        context_strength=weight_strength,
                    )
                    via_v7, audit = v7.realize_local_context(
                        feasible,
                        support_seed=seed + 5,
                        support_strength=0.0,
                        weight_seed=context_seed,
                        weight_strength=weight_strength,
                    )
                    if via_v7 != direct_v5 or audit["dropped_partnerless_positive_plant_count"] != 0:
                        failures["full_support_v5_identity"].append((state_id, weight_strength))

                support_summaries = []
                for strength_index, support_strength in enumerate(SUPPORT_STRENGTHS):
                    pollinator_support_sets = []
                    plant_support_sets = []
                    shannon_values = []
                    overlap_values = []
                    dropped_counts = []
                    for context_index in range(context_replicates):
                        support_seed = (
                            seed + 20_000_000 + sat_index * 1_000_000
                            + iso_index * 100_000 + replicate * 1_000
                            + strength_index * 100 + context_index
                        )
                        weight_seed = support_seed + 50_000_000
                        active = v6.active_pollinator_indices(
                            len(feasible.pollinator_names),
                            rng=random.Random(support_seed),
                            support_strength=support_strength,
                        )
                        v6_support = None
                        v6_failed = False
                        try:
                            v6_support = v6.apply_active_pollinator_indices(feasible, active)
                        except RuntimeError:
                            v6_failed = True
                            v6_structural_failure_masks += 1

                        try:
                            closed, audit = v7.apply_joint_support_closure(feasible, active)
                        except Exception as exc:
                            failures["unexpected_v7_exception"].append((state_id, support_strength, context_index, type(exc).__name__, str(exc)))
                            continue

                        if v6_failed:
                            if audit["dropped_partnerless_positive_plant_count"] > 0:
                                v7_resolved_v6_failure_masks += 1
                        elif closed != v6_support:
                            failures["v6_admissible_mask_identity"].append((state_id, support_strength, context_index))

                        if audit["max_retained_row_budget_error"] > 1e-11:
                            failures["retained_row_budget"].append((state_id, support_strength, context_index, audit["max_retained_row_budget_error"]))
                        if not set(audit["active_pollinators"]).issubset(set(feasible.pollinator_names)):
                            failures["taxon_subset"].append((state_id, support_strength, context_index, "pollinator"))
                        if closed is not None and not set(closed.plant_names).issubset(set(feasible.plant_names)):
                            failures["taxon_subset"].append((state_id, support_strength, context_index, "plant"))

                        if audit["dropped_partnerless_positive_plant_count"] > 0:
                            synthetic_partnerless_drop_masks += 1
                        pollinator_support_sets.append(tuple(audit["active_pollinators"]))
                        plant_support_sets.append(tuple(closed.plant_names) if closed is not None else tuple())
                        dropped_counts.append(audit["dropped_partnerless_positive_plant_count"])

                        realized = None
                        if closed is not None and positive_total(closed) > 0:
                            realized = v5.realize_local_context(
                                closed,
                                context_seed=weight_seed,
                                context_strength=WEIGHT_STRENGTH,
                            )
                        metrics = metric_pair_or_none(realized)
                        if metrics is not None:
                            shannon_values.append(metrics[0])
                            overlap_values.append(metrics[1])

                    support_summaries.append({
                        "support_strength": support_strength,
                        "distinct_pollinator_support_sets": len(set(pollinator_support_sets)),
                        "distinct_joint_plant_support_sets": len(set(plant_support_sets)),
                        "mean_dropped_partnerless_positive_plants": statistics.mean(dropped_counts) if dropped_counts else None,
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
                    "positive": positive_total(feasible) > 0,
                    "feasible_plants": len(feasible.plant_names),
                    "feasible_pollinators": len(feasible.pollinator_names),
                    "support_summaries": support_summaries,
                })

    positive_support_summaries = [
        summary
        for state in state_rows if state["positive"]
        for summary in state["support_summaries"]
    ]
    tests = {
        "full_pollinator_support_exact_v5_identity": not failures["full_support_v5_identity"],
        "v6_admissible_masks_unchanged_by_joint_closure": not failures["v6_admissible_mask_identity"],
        "retained_positive_plant_row_budgets_conserved": not failures["retained_row_budget"],
        "all_realized_taxa_are_feasible_subsets": not failures["taxon_subset"],
        "v7_support_closure_has_no_unexpected_exceptions": not failures["unexpected_v7_exception"],
        "canonical_v6_partnerless_plant_failure_is_resolved": all(
            toy[key]
            for key in (
                "v6_canonical_partnerless_row_failure_reproduced",
                "v7_drops_only_partnerless_positive_plant",
                "v7_retains_shared_plant_budget",
                "v7_toy_network_nonempty",
            )
        ),
        "every_observed_v6_failure_mask_is_resolved_by_partnerless_plant_dropout": (
            v6_structural_failure_masks == v7_resolved_v6_failure_masks
        ),
        "nonzero_support_branches_pollinator_support": any(
            row["distinct_pollinator_support_sets"] >= 2 for row in positive_support_summaries
        ),
        "nonzero_support_can_branch_joint_plant_support": any(
            row["distinct_joint_plant_support_sets"] >= 2 for row in positive_support_summaries
        ),
        "support_closure_can_change_shannon": any(row["shannon_range"] > EPS for row in metric_ranges),
        "support_closure_can_change_plant_overlap": any(row["overlap_range"] > EPS for row in metric_ranges),
        "frozen_v4_opportunity_contract_remains_true": inherited_ok,
    }
    passed = all(tests.values())
    return {
        "schema_version": "1.0",
        "analysis": "abm_v7_joint_support_closure_synthetic_prevalidation",
        "status": "synthetic_mechanism_prevalidation_no_empirical_v7_fit",
        "empirical_inputs_loaded": [],
        "giannutri_values_loaded": False,
        "grid": {
            "isolations": list(ISOLATIONS),
            "saturations": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "weight_strength_for_branching_probe": WEIGHT_STRENGTH,
            "evolution_replicates": evolution_replicates,
            "context_replicates": context_replicates,
        },
        "state_counts": {
            "total": len(state_rows),
            "positive": sum(row["positive"] for row in state_rows),
        },
        "toy_failure_class_resolution": toy,
        "v6_structural_failure_masks_in_synthetic_grid": v6_structural_failure_masks,
        "v7_resolved_v6_failure_masks": v7_resolved_v6_failure_masks,
        "synthetic_masks_with_partnerless_plant_dropout": synthetic_partnerless_drop_masks,
        "tests": tests,
        "failure_details": failures,
        "metric_range_rows": metric_ranges,
        "decision": (
            "v7_preserves_prior_invariants_and_closes_joint_local_support"
            if passed
            else "v7_joint_support_closure_fails_synthetic_prevalidation"
        ),
        "next_gate": "Only after this synthetic gate passes: select and freeze another independent repeated-local quantitative island system before v7 targets are inspected. Giannutri cannot be reused to confirm v7.",
        "claim_boundary": "Passing establishes mechanism capability only. It shows that partnerless positive plant rows can become locally inactive without changing retained row budgets; it does not establish independent plant phenology/resource dynamics or empirical v7 adequacy.",
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
        "v6_structural_failure_masks": payload["v6_structural_failure_masks_in_synthetic_grid"],
        "v7_resolved_v6_failure_masks": payload["v7_resolved_v6_failure_masks"],
        "synthetic_partnerless_dropout_masks": payload["synthetic_masks_with_partnerless_plant_dropout"],
        "tests": payload["tests"],
    }, indent=2))


if __name__ == "__main__":
    main()
