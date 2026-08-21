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
    """Draw locally available positive plant/resource rows before v8 support."""
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    if support_strength == 0.0:
        return tuple(range(len(opportunity_network.plant_names)))

    rng = random.Random(plant_seed)
    keep_probability = 1.0 - support_strength
    active: list[int] = []
    for row_index, row in enumerate(opportunity_network.matrix):
        # Zero-only placeholders carry no local biological opportunity. They are
        # retained only by the exact zero-support bypass contract below.
        if sum(row) <= 0.0:
            continue
        if rng.random() < keep_probability:
            active.append(row_index)
    # Do not condition on at least one active plant. An empty flowering/resource
    # context is a legal local ecological state and must not be redrawn.
    return tuple(active)


def apply_local_plant_availability(
    opportunity_network: WeightedNetwork,
    *,
    plant_seed: int,
    support_strength: float,
) -> tuple[WeightedNetwork | None, dict]:
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")

    if support_strength == 0.0:
        return opportunity_network, {
            "support_strength": 0.0,
            "active_plant_indices": list(range(len(opportunity_network.plant_names))),
            "active_plant_names_before_v8": list(opportunity_network.plant_names),
            "dropped_local_plant_names_before_v8": [],
            "active_positive_plant_count_before_v8": sum(sum(row) > 0.0 for row in opportunity_network.matrix),
            "empty_plant_opportunity": False,
            "zero_support_exact_opportunity_bypass": True,
            "new_taxa_created": False,
            "new_links_created": False,
        }

    active = draw_local_plant_indices(
        opportunity_network,
        plant_seed=plant_seed,
        support_strength=support_strength,
    )
    active_set = set(active)
    positive_indices = [index for index, row in enumerate(opportunity_network.matrix) if sum(row) > 0.0]
    dropped = [
        opportunity_network.plant_names[index]
        for index in positive_indices
        if index not in active_set
    ]
    if not active:
        return None, {
            "support_strength": support_strength,
            "active_plant_indices": [],
            "active_plant_names_before_v8": [],
            "dropped_local_plant_names_before_v8": dropped,
            "active_positive_plant_count_before_v8": 0,
            "empty_plant_opportunity": True,
            "zero_support_exact_opportunity_bypass": False,
            "new_taxa_created": False,
            "new_links_created": False,
        }

    network = WeightedNetwork.from_rows(
        [opportunity_network.plant_names[index] for index in active],
        opportunity_network.pollinator_names,
        [opportunity_network.matrix[index] for index in active],
    )
    return network, {
        "support_strength": support_strength,
        "active_plant_indices": list(active),
        "active_plant_names_before_v8": list(network.plant_names),
        "dropped_local_plant_names_before_v8": dropped,
        "active_positive_plant_count_before_v8": len(active),
        "empty_plant_opportunity": False,
        "zero_support_exact_opportunity_bypass": False,
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
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    v8 = load_module(V8_SCRIPT, "abm_v9_v8_source")

    # Exact nesting: no local-support stress means v9 is exactly v8, including
    # zero-only placeholder states and the complete audit-independent object.
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
                "active_plant_names_before_v8": list(opportunity_network.plant_names),
                "dropped_local_plant_names_before_v8": [],
                "empty_plant_opportunity": False,
                "zero_support_exact_opportunity_bypass": True,
            },
            "v8_layer": v8_audit,
            "zero_support_exact_v8_bypass": True,
            "new_taxa_created": False,
            "new_links_created": False,
        }

    plant_network, plant_audit = apply_local_plant_availability(
        opportunity_network,
        plant_seed=support_seed + PLANT_SEED_OFFSET,
        support_strength=support_strength,
    )
    if plant_network is None:
        return None, {
            "support_strength": support_strength,
            "weight_strength": weight_strength,
            "plant_layer": plant_audit,
            "v8_layer": None,
            "zero_support_exact_v8_bypass": False,
            "empty_local_network": True,
            "new_taxa_created": False,
            "new_links_created": False,
            "max_retained_row_budget_error": 0.0,
        }

    realized, v8_audit = v8.realize_local_context(
        plant_network,
        support_seed=support_seed,
        support_strength=support_strength,
        weight_seed=weight_seed,
        weight_strength=weight_strength,
    )
    return realized, {
        "support_strength": support_strength,
        "weight_strength": weight_strength,
        "plant_layer": plant_audit,
        "v8_layer": v8_audit,
        "zero_support_exact_v8_bypass": False,
        "empty_local_network": realized is None,
        "new_taxa_created": bool(v8_audit.get("new_taxa_created", False)),
        "new_links_created": bool(v8_audit.get("new_links_created", False)),
        "max_retained_row_budget_error": float(v8_audit.get("max_retained_row_budget_error", 0.0)),
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
            "local_pollinator_and_pair_support": "unchanged v8 pollinator availability and pair-level support operate only on locally active plant rows",
            "local_weight_realization": "unchanged v5 weight realization follows support projection",
            "observation_layer": "not part of v9 biology; future empirical validation must freeze standardized exposure or an observation/detection layer before target inspection",
        },
        "shared_generic_strength": (
            "The same existing generic support-strength envelope controls plant, pollinator and pair availability. "
            "This is a mechanism sensitivity axis, not an estimate that the three ecological processes have equal real-world probabilities."
        ),
        "plant_draw_independence": "The plant draw uses an independent fixed RNG stream offset from v8 pollinator/pair draws while sharing only the generic support-strength value.",
        "hard_invariants": [
            "support_strength=0 reproduces v8 exactly for every weight_strength, including zero-only placeholders",
            "local plants are always a subset of v4 feasible plants",
            "local pollinators and positive pairs are always subsets of v4 opportunity",
            "no new taxon or pair can be created",
            "every retained positive plant row preserves its exact original v4 opportunity total after support projection and v5 realization",
            "all-local-plant-absent and later empty local networks are legal states and are not repaired or redrawn",
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
