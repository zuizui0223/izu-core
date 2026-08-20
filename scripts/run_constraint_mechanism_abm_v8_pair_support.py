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
OUT = ROOT / "data/results/constraint_mechanism_abm_v8_pair_support.json"
SUPPORT_STRENGTHS = (0.0, 0.25, 0.5, 0.75)
WEIGHT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def draw_pair_support_mask(
    opportunity_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
) -> tuple[tuple[bool, ...], ...]:
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    rng = random.Random(support_seed)
    keep_probability = 1.0 - support_strength
    mask = []
    for row in opportunity_network.matrix:
        mask.append(tuple(
            (value > 0.0) and (
                True if support_strength == 0.0 else rng.random() < keep_probability
            )
            for value in row
        ))
    return tuple(mask)


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
            # Zero-opportunity plant rows do not become positive through support.
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
        "active_pollinators": list(active_pollinator_names),
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
    mask = draw_pair_support_mask(
        opportunity_network,
        support_seed=support_seed,
        support_strength=support_strength,
    )
    supported, audit = apply_pair_support_mask(opportunity_network, mask)
    audit["support_strength"] = support_strength
    audit["weight_strength"] = weight_strength
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
        "model": "constraint_mechanism_abm_v8_pair_level_local_support",
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
        "support_rule": {
            "unit": "plant x pollinator pair",
            "probability": "for every positive v4 opportunity pair, local support is independently active with probability 1-support_strength",
            "zero_strength_identity": "support_strength=0 retains every positive v4 opportunity pair exactly",
            "no_nonempty_conditioning": "empty pair support, partnerless plants and interactionless pollinators are retained as structural local outcomes rather than redrawn",
            "parameter_reuse": "the existing generic support-strength envelope is reused; no independent pair-support parameter is added",
        },
        "support_projection": {
            "plant_support": "a positive plant remains locally active iff at least one of its positive opportunity pairs is supported",
            "pollinator_support": "a pollinator remains locally active iff at least one retained plant has a positive supported interaction with it",
            "pair_support": "supported positive pairs are a subset of v4 positive opportunity pairs",
        },
        "row_budget_rule": "For every retained positive plant row, supported opportunity weights are rescaled to preserve that plant's exact pre-context total opportunity. Partnerless positive plants are locally inactive instead of receiving manufactured service.",
        "weight_realization": "unchanged v5 positive affinity reweighting is applied only after pair-support projection",
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
            "reject v8 if nonzero pair support cannot generate sparse pair topology from native dense v4 opportunity states",
            "reject v8 if repeated contexts cannot branch pair, plant and pollinator support in structurally reducible states",
            "reject v8 if support variation cannot change Shannon and plant niche overlap",
            "reject v8 if the frozen v4 opportunity-direction contract no longer holds",
        ],
        "next_empirical_gate": "Only after synthetic prevalidation passes, freeze another independent repeated-local quantitative island system before target inspection. Menorca and Giannutri are consumed failures and cannot confirm v8.",
        "claim_boundary": "v8 separates local interaction support from positive opportunity magnitude using a generic pair-level Bernoulli mask. Its support strength is a mechanism sensitivity envelope, not an empirical estimate, and it does not yet identify habitat, phenology or species-specific support processes.",
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
