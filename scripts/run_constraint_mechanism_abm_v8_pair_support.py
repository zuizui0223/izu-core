from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_WEIGHTED = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v8_pair_support.json"
SUPPORT_STRENGTHS = (0.0, 0.25, 0.5, 0.75)
WEIGHT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)
PAIR_SEED_OFFSET = 30_000_000


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def draw_hierarchical_pair_support_mask(
    opportunity_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
) -> tuple[tuple[tuple[bool, ...], ...], tuple[int, ...]]:
    """Draw v6 pollinator availability, then pair availability inside it.

    The same frozen support-strength envelope is reused at both hierarchy levels;
    no independent pair-support parameter is introduced. Zero strength retains
    every positive opportunity pair exactly.
    """
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    if not opportunity_network.pollinator_names:
        raise ValueError("opportunity network requires at least one pollinator column")

    v6 = load_module(V6_SCRIPT, "abm_v8_v6_support_source")
    active_pollinators = v6.active_pollinator_indices(
        len(opportunity_network.pollinator_names),
        rng=random.Random(support_seed),
        support_strength=support_strength,
    )
    active_set = set(active_pollinators)
    pair_rng = random.Random(support_seed + PAIR_SEED_OFFSET)
    keep_probability = 1.0 - support_strength
    mask = []
    for row in opportunity_network.matrix:
        mask.append(tuple(
            (column in active_set)
            and (value > 0.0)
            and (
                True if support_strength == 0.0 else pair_rng.random() < keep_probability
            )
            for column, value in enumerate(row)
        ))
    return tuple(mask), tuple(active_pollinators)


def apply_pair_support_mask(
    opportunity_network: WeightedNetwork,
    pair_mask: tuple[tuple[bool, ...], ...] | list[list[bool]],
) -> tuple[WeightedNetwork | None, dict]:
    if len(pair_mask) != len(opportunity_network.matrix):
        raise ValueError("pair mask row dimension mismatch")
    if any(len(mask_row) != len(opportunity_network.pollinator_names) for mask_row in pair_mask):
        raise ValueError("pair mask column dimension mismatch")

    retained_plant_names: list[str] = []
    retained_rows_full_columns: list[list[float]] = []
    dropped_partnerless_positive_plants: list[str] = []
    max_budget_error = 0.0
    active_pair_count = 0

    for plant_name, row, mask_row in zip(
        opportunity_network.plant_names,
        opportunity_network.matrix,
        pair_mask,
    ):
        baseline_total = sum(row)
        selected = [
            value if bool(active) and value > 0.0 else 0.0
            for value, active in zip(row, mask_row)
        ]
        selected_total = sum(selected)
        if baseline_total <= 0.0:
            retained_plant_names.append(plant_name)
            retained_rows_full_columns.append([0.0 for _ in selected])
            continue
        if selected_total <= 0.0:
            dropped_partnerless_positive_plants.append(plant_name)
            continue
        scale = baseline_total / selected_total
        realized = [value * scale for value in selected]
        error = abs(sum(realized) - baseline_total)
        max_budget_error = max(max_budget_error, error)
        if not math.isclose(sum(realized), baseline_total, rel_tol=1e-12, abs_tol=1e-14):
            raise RuntimeError("pair support failed retained-row budget conservation")
        active_pair_count += sum(value > 0.0 for value in realized)
        retained_plant_names.append(plant_name)
        retained_rows_full_columns.append(realized)

    if not retained_plant_names:
        return None, {
            "retained_plant_count": 0,
            "retained_pollinator_count": 0,
            "dropped_partnerless_positive_plant_count": len(dropped_partnerless_positive_plants),
            "dropped_partnerless_positive_plants": dropped_partnerless_positive_plants,
            "active_pair_count": 0,
            "max_retained_row_budget_error": max_budget_error,
            "empty_local_network": True,
            "new_taxa_created": False,
            "new_links_created": False,
        }

    active_columns = [
        column
        for column in range(len(opportunity_network.pollinator_names))
        if any(row[column] > 0.0 for row in retained_rows_full_columns)
    ]
    if not active_columns or active_pair_count <= 0:
        return None, {
            "retained_plant_count": len(retained_plant_names),
            "retained_pollinator_count": 0,
            "dropped_partnerless_positive_plant_count": len(dropped_partnerless_positive_plants),
            "dropped_partnerless_positive_plants": dropped_partnerless_positive_plants,
            "active_pair_count": 0,
            "max_retained_row_budget_error": max_budget_error,
            "empty_local_network": True,
            "new_taxa_created": False,
            "new_links_created": False,
        }

    active_pollinator_names = [
        opportunity_network.pollinator_names[column] for column in active_columns
    ]
    compact_rows = [
        [row[column] for column in active_columns]
        for row in retained_rows_full_columns
    ]
    network = WeightedNetwork.from_rows(
        retained_plant_names,
        active_pollinator_names,
        compact_rows,
    )
    return network, {
        "retained_plant_count": len(retained_plant_names),
        "retained_pollinator_count": len(active_pollinator_names),
        "dropped_partnerless_positive_plants": dropped_partnerless_positive_plants,
        "dropped_partnerless_positive_plant_count": len(dropped_partnerless_positive_plants),
        "active_pollinators_after_pair_projection": list(active_pollinator_names),
        "active_pair_count": active_pair_count,
        "max_retained_row_budget_error": max_budget_error,
        "empty_local_network": False,
        "new_taxa_created": False,
        "new_links_created": False,
    }


def realize_local_context(
    opportunity_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
    weight_seed: int,
    weight_strength: float,
) -> tuple[WeightedNetwork | None, dict]:
    mask, globally_active = draw_hierarchical_pair_support_mask(
        opportunity_network,
        support_seed=support_seed,
        support_strength=support_strength,
    )
    supported, audit = apply_pair_support_mask(opportunity_network, mask)
    audit["support_strength"] = support_strength
    audit["weight_strength"] = weight_strength
    audit["globally_active_pollinators_before_pair_projection"] = [
        opportunity_network.pollinator_names[index] for index in globally_active
    ]
    if supported is None:
        return None, audit
    v5 = load_module(V5_SCRIPT, "abm_v8_v5_source")
    realized = v5.realize_local_context(
        supported,
        context_seed=weight_seed,
        context_strength=weight_strength,
    )
    return realized, audit


def run_weighted_network(
    isolation_index: float,
    evolution_seed: int,
    saturation: float,
    *,
    support_seed: int,
    support_strength: float,
    weight_seed: int,
    weight_strength: float,
    n_lineages: int = 24,
    steps: int = 120,
) -> tuple[WeightedNetwork, WeightedNetwork | None, dict]:
    v4 = load_module(V4_WEIGHTED, "abm_v8_v4_source")
    opportunity = v4.run_weighted_network(
        isolation_index,
        evolution_seed,
        saturation,
        n_lineages=n_lineages,
        steps=steps,
    )
    realized, audit = realize_local_context(
        opportunity,
        support_seed=support_seed,
        support_strength=support_strength,
        weight_seed=weight_seed,
        weight_strength=weight_strength,
    )
    return opportunity, realized, audit


def build_contract() -> dict:
    return {
        "model": "constraint_mechanism_abm_v8_hierarchical_pair_support",
        "status": "failure_driven_mechanism_freeze_before_new_empirical_validation",
        "failure_sources": [
            {
                "pr": 200,
                "finding": "pollinator support can become incompatible with a fixed positive plant row",
            },
            {
                "pr": 201,
                "finding": "v4 positive pair-support is complete bipartite, so plant-support closure is dormant on native synthetic states",
            },
        ],
        "use_of_failures": "Only the missing support granularity is used. No Menorca or Giannutri target amplitude, taxon identity, fitted threshold, or habitat effect is loaded.",
        "new_parameter_count": 0,
        "support_strengths": list(SUPPORT_STRENGTHS),
        "support_hierarchy": {
            "pollinator_level": "reuse the unchanged v6 draw: each extant pollinator is locally active with probability 1-support_strength, conditioned only on at least one globally active pollinator",
            "pair_level": "within globally active pollinators, every positive v4 opportunity pair is independently supported with probability 1-support_strength",
            "shared_strength": "the same pre-existing generic support strength controls both unresolved availability layers; there is no independently fitted pair-support strength",
            "zero_strength_identity": "support_strength=0 retains all pollinators and every positive v4 opportunity pair exactly",
            "no_pair_nonempty_conditioning": "pair masks are not redrawn when they create partnerless plants, interactionless pollinators, or an empty local network",
        },
        "support_projection": {
            "plant_support": "a positive plant remains locally active iff at least one positive pair survives both support levels",
            "pollinator_support": "a globally active pollinator remains in the realized network iff at least one retained plant has a positive supported pair to it",
            "pair_support": "realized support is a subset of the positive v4 opportunity field rather than being equated with every positive weight",
        },
        "row_budget_rule": "For every retained positive plant row, supported opportunity weights are rescaled to preserve that plant's exact pre-context total opportunity. Partnerless positive plants are locally inactive instead of receiving manufactured service.",
        "weight_realization": "unchanged v5 positive affinity reweighting is applied only after hierarchical support projection",
        "hard_invariants": [
            "support_strength=0 and any weight_strength reproduce v5 exactly",
            "no new plant, pollinator or positive pair absent from the v4 opportunity network can be created",
            "every retained positive plant row preserves its exact opportunity total",
            "partnerless positive plants and interactionless pollinators may become locally inactive",
            "empty local networks are allowed and recorded rather than repaired",
            "the frozen v4 island-scale opportunity process is unchanged",
            "Menorca and Giannutri empirical target values are not loaded by v8 synthetic prevalidation",
        ],
        "predeclared_synthetic_falsification": [
            "reject v8 if zero-support identity with v5 fails",
            "reject v8 if retained positive plant row budgets drift",
            "reject v8 if any new taxon or link is created",
            "reject v8 if nonzero support cannot generate sparse pair topology from native dense v4 opportunity states",
            "reject v8 if repeated contexts cannot branch pair, plant and pollinator support in structurally reducible states",
            "reject v8 if support variation cannot change Shannon and plant niche overlap",
            "reject v8 if the frozen v4 opportunity-direction contract no longer holds",
        ],
        "next_empirical_gate": "Only after synthetic prevalidation passes, freeze another independent repeated-local quantitative island system before target inspection. Menorca and Giannutri are consumed failures and cannot confirm v8.",
        "claim_boundary": "v8 separates local interaction support from positive opportunity magnitude using nested generic pollinator- and pair-level Bernoulli support. Its shared support strength is a mechanism sensitivity envelope, not an empirical estimate, and it does not identify habitat, phenology or species-specific support processes.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_contract()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
