from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V8_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v9_local_plant_opportunity.json"
SUPPORT_STRENGTHS = (0.0, 0.25, 0.5, 0.75)
WEIGHT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)
PLANT_SEED_OFFSET = 70_000_000


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def draw_local_plant_indices(
    opportunity_network: WeightedNetwork,
    *,
    plant_seed: int,
    support_strength: float,
) -> tuple[int, ...]:
    """Draw locally available positive plant/resource rows before pair support."""
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    if support_strength == 0.0:
        return tuple(range(len(opportunity_network.plant_names)))

    rng = random.Random(plant_seed)
    keep_probability = 1.0 - support_strength
    active: list[int] = []
    for row_index, row in enumerate(opportunity_network.matrix):
        # Zero-only placeholders carry no positive local resource opportunity.
        # The exact zero-support contract preserves them through the bypass below.
        if sum(row) <= 0.0:
            continue
        if rng.random() < keep_probability:
            active.append(row_index)
    # Do not condition on at least one locally active plant. Empty plant-resource
    # contexts are legal ecological states and must not be repaired or redrawn.
    return tuple(active)


def plant_availability_audit(
    opportunity_network: WeightedNetwork,
    active_indices: tuple[int, ...],
    *,
    support_strength: float,
) -> dict:
    active_set = set(active_indices)
    positive_indices = [
        index for index, row in enumerate(opportunity_network.matrix) if sum(row) > 0.0
    ]
    return {
        "support_strength": support_strength,
        "active_plant_indices": list(active_indices),
        "active_plant_names_before_pair_projection": [
            opportunity_network.plant_names[index] for index in active_indices
        ],
        "dropped_local_plant_names_before_pair_projection": [
            opportunity_network.plant_names[index]
            for index in positive_indices
            if index not in active_set
        ],
        "baseline_positive_plant_count": len(positive_indices),
        "active_positive_plant_count_before_pair_projection": sum(
            index in active_set for index in positive_indices
        ),
        "empty_plant_opportunity": not any(index in active_set for index in positive_indices),
        "new_taxa_created": False,
        "new_links_created": False,
    }


def combine_plant_and_v8_pair_masks(
    opportunity_network: WeightedNetwork,
    *,
    active_plant_indices: tuple[int, ...],
    v8_pair_mask: tuple[tuple[bool, ...], ...],
) -> tuple[tuple[bool, ...], ...]:
    """Intersect an independent local-plant mask with the unchanged full v8 pair draw."""
    if len(v8_pair_mask) != len(opportunity_network.matrix):
        raise ValueError("v8 pair mask row dimension mismatch")
    active_set = set(active_plant_indices)
    return tuple(
        tuple(bool(pair_active) and row_index in active_set for pair_active in mask_row)
        for row_index, mask_row in enumerate(v8_pair_mask)
    )


def realize_local_context(
    opportunity_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
    weight_seed: int,
    weight_strength: float,
) -> tuple[WeightedNetwork | None, dict]:
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    v8 = load_module(V8_SCRIPT, "abm_v9_v8_source")

    # Exact nesting: no support stress means v9 is exactly v8, including any
    # zero-only placeholders and all inherited v5 behavior.
    if support_strength == 0.0:
        realized, v8_audit = v8.realize_local_context(
            opportunity_network,
            support_seed=support_seed,
            support_strength=0.0,
            weight_seed=weight_seed,
            weight_strength=weight_strength,
        )
        return realized, {
            "support_strength": 0.0,
            "weight_strength": weight_strength,
            "plant_layer": {
                "active_plant_names_before_pair_projection": list(opportunity_network.plant_names),
                "dropped_local_plant_names_before_pair_projection": [],
                "empty_plant_opportunity": False,
            },
            "v8_layer": v8_audit,
            "zero_support_exact_v8_bypass": True,
            "new_taxa_created": False,
            "new_links_created": False,
            "max_retained_row_budget_error": 0.0,
        }

    active_plants = draw_local_plant_indices(
        opportunity_network,
        plant_seed=support_seed + PLANT_SEED_OFFSET,
        support_strength=support_strength,
    )
    plant_audit = plant_availability_audit(
        opportunity_network,
        active_plants,
        support_strength=support_strength,
    )

    # Draw v8 support on the complete opportunity object with the exact inherited
    # seed and RNG ordering, then intersect with the independent plant mask. This
    # makes same-seed v8/v9 differences attributable to plant availability rather
    # than to shifted pair-RNG positions after physically deleting rows.
    v8_pair_mask, globally_active_pollinators = v8.draw_hierarchical_pair_support_mask(
        opportunity_network,
        support_seed=support_seed,
        support_strength=support_strength,
    )
    combined_mask = combine_plant_and_v8_pair_masks(
        opportunity_network,
        active_plant_indices=active_plants,
        v8_pair_mask=v8_pair_mask,
    )
    supported, projection_audit = v8.apply_pair_support_mask(
        opportunity_network,
        combined_mask,
    )
    projection_audit["globally_active_pollinators_before_pair_projection"] = [
        opportunity_network.pollinator_names[index]
        for index in globally_active_pollinators
    ]

    if supported is None:
        return None, {
            "support_strength": support_strength,
            "weight_strength": weight_strength,
            "plant_layer": plant_audit,
            "v8_layer": projection_audit,
            "zero_support_exact_v8_bypass": False,
            "empty_local_network": True,
            "new_taxa_created": bool(projection_audit.get("new_taxa_created", False)),
            "new_links_created": bool(projection_audit.get("new_links_created", False)),
            "max_retained_row_budget_error": float(projection_audit.get("max_retained_row_budget_error", 0.0)),
        }

    v5 = load_module(V5_SCRIPT, "abm_v9_v5_source")
    realized = v5.realize_local_context(
        supported,
        context_seed=weight_seed,
        context_strength=weight_strength,
    )
    return realized, {
        "support_strength": support_strength,
        "weight_strength": weight_strength,
        "plant_layer": plant_audit,
        "v8_layer": projection_audit,
        "zero_support_exact_v8_bypass": False,
        "empty_local_network": False,
        "new_taxa_created": bool(projection_audit.get("new_taxa_created", False)),
        "new_links_created": bool(projection_audit.get("new_links_created", False)),
        "max_retained_row_budget_error": float(projection_audit.get("max_retained_row_budget_error", 0.0)),
    }


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
    v4 = load_module(V4_SCRIPT, "abm_v9_v4_source")
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
        "model": "constraint_mechanism_abm_v9_local_plant_opportunity_then_pair_support",
        "status": "failure_driven_mechanism_freeze_before_new_empirical_validation",
        "failure_source": {
            "pr": 205,
            "decision": "v8_fails_cabrera_conditional_pair_support_predictive_adequacy",
            "diagnosis_pr": 206,
            "use_of_failure": (
                "Cabrera is used only to identify the missing mechanism class: source-observed local plant/resource opportunity precedes pair realization. "
                "No Cabrera target value, support fraction, correlation, taxon identity, habitat coefficient, or fitted probability is loaded by v9."
            ),
        },
        "new_parameter_count": 0,
        "support_strengths": list(SUPPORT_STRENGTHS),
        "weight_strengths": list(WEIGHT_STRENGTHS),
        "hierarchy": {
            "island_scale": "unchanged v4 continuous opportunity field",
            "local_plant_resource_availability": "each positive feasible plant/resource row is independently locally active with probability 1-support_strength; zero active plants is allowed and never redrawn",
            "local_pollinator_and_pair_support": "unchanged v8 pollinator availability and full-opportunity pair Bernoulli draw are intersected with the independent local plant mask",
            "local_weight_realization": "unchanged v5 weight realization follows support projection",
            "observation_layer": "not part of v9 biology; future empirical validation must freeze standardized exposure or an observation/detection layer before target inspection",
        },
        "shared_generic_strength": (
            "The same existing generic support-strength envelope controls plant, pollinator and pair availability. "
            "This is a mechanism sensitivity axis, not an estimate that the three ecological processes have equal real-world probabilities."
        ),
        "plant_draw_independence": (
            "The plant draw uses a fixed RNG stream offset independent of the unchanged v8 full-opportunity pollinator/pair draw. "
            "For a matched support seed, v8 pair Bernoulli outcomes are therefore unchanged and v9 only removes pairs whose plant endpoint is locally unavailable."
        ),
        "hard_invariants": [
            "support_strength=0 reproduces v8 exactly for every weight_strength, including zero-only placeholders",
            "local plants are always a subset of v4 feasible plants",
            "local pollinators and positive pairs are always subsets of v4 opportunity",
            "no new taxon or pair can be created",
            "every retained positive plant row preserves its exact original v4 opportunity total after support projection and v5 realization",
            "all-local-plant-absent and later empty local networks are legal states and are not repaired or redrawn",
            "the matched full-opportunity v8 pollinator/pair draw is unchanged by adding the plant mask",
            "v4 opportunity, v8 pollinator/pair rules and v5 weight rules are otherwise unchanged",
            "Cabrera, Menorca and Giannutri target values are not loaded by v9 synthetic prevalidation",
        ],
        "predeclared_synthetic_falsification": [
            "reject v9 if zero-support identity with v8 fails",
            "reject v9 if any retained positive plant row budget drifts relative to v4 opportunity",
            "reject v9 if any realized plant, pollinator or positive pair lies outside v4 opportunity",
            "reject v9 if nonzero plant availability cannot remove feasible positive plant rows in native v4 states",
            "reject v9 if repeated nonzero contexts cannot branch pre-pair plant availability and final plant, pollinator and pair support",
            "reject v9 if adding the plant layer never makes any matched v9 context sparser than the same-seed v8 context",
            "reject v9 if support variation cannot change Shannon and plant niche overlap",
            "reject v9 if the frozen v4 opportunity-direction contract no longer holds",
        ],
        "next_empirical_gate": (
            "Only after synthetic prevalidation passes, freeze a new independent repeated-local quantitative island system before v9 target inspection. "
            "Menorca, Giannutri and Cabrera are consumed failures and cannot confirm v9. Any heterogeneous sampling exposure must be standardized or modeled by a prespecified observation layer before outcomes are inspected."
        ),
        "claim_boundary": (
            "v9 is the minimum biological response to the Cabrera failure diagnosis: local plant/resource availability becomes an upstream support layer. "
            "It does not claim that plant phenology is the sole driver, does not fit plant availability to Cabrera, and does not treat sampling/detection as ecology."
        ),
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
