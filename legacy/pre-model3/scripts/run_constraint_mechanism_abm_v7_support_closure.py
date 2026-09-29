from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_WEIGHTED = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v7_support_closure.json"
SUPPORT_STRENGTHS = (0.0, 0.25, 0.5, 0.75)
WEIGHT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def apply_joint_support_closure(
    feasible_network: WeightedNetwork,
    active_pollinator_indices: tuple[int, ...] | list[int],
) -> tuple[WeightedNetwork | None, dict]:
    """Close a local pollinator-support mask across the plant guild.

    Positive plant rows that retain at least one positive active pollinator keep
    their exact baseline row budget. Positive plant rows with no active positive
    partner become locally inactive rather than receiving manufactured service.
    No new plant, pollinator, or link can be created.
    """
    if not feasible_network.pollinator_names:
        raise ValueError("feasible network requires at least one pollinator column")
    active = tuple(sorted(int(index) for index in active_pollinator_indices))
    if not active:
        raise ValueError("support closure requires at least one active feasible pollinator")
    if len(set(active)) != len(active):
        raise ValueError("active pollinator indices must be unique")
    if active[0] < 0 or active[-1] >= len(feasible_network.pollinator_names):
        raise ValueError("active pollinator index lies outside feasible network")

    active_names = tuple(feasible_network.pollinator_names[index] for index in active)
    retained_names: list[str] = []
    retained_rows: list[list[float]] = []
    dropped_partnerless: list[str] = []
    retained_zero_baseline: list[str] = []
    max_budget_error = 0.0

    for plant_name, row in zip(feasible_network.plant_names, feasible_network.matrix):
        baseline_total = sum(row)
        selected = [row[index] for index in active]
        selected_total = sum(selected)
        if baseline_total <= 0.0:
            retained_names.append(plant_name)
            retained_rows.append([0.0 for _ in selected])
            retained_zero_baseline.append(plant_name)
            continue
        if selected_total <= 0.0:
            dropped_partnerless.append(plant_name)
            continue
        scale = baseline_total / selected_total
        realized = [value * scale for value in selected]
        error = abs(sum(realized) - baseline_total)
        max_budget_error = max(max_budget_error, error)
        if not math.isclose(sum(realized), baseline_total, rel_tol=1e-12, abs_tol=1e-14):
            raise RuntimeError("joint support closure failed retained-row budget conservation")
        retained_names.append(plant_name)
        retained_rows.append(realized)

    audit = {
        "active_pollinators": list(active_names),
        "retained_plant_count": len(retained_names),
        "dropped_partnerless_positive_plant_count": len(dropped_partnerless),
        "dropped_partnerless_positive_plants": dropped_partnerless,
        "retained_zero_baseline_plant_count": len(retained_zero_baseline),
        "max_retained_row_budget_error": max_budget_error,
        "new_taxa_created": False,
        "new_links_created": False,
    }
    if not retained_names:
        audit["empty_local_network"] = True
        return None, audit

    network = WeightedNetwork.from_rows(retained_names, active_names, retained_rows)
    audit["empty_local_network"] = sum(sum(row) for row in network.matrix) <= 0.0
    return network, audit


def realize_local_context(
    feasible_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
    weight_seed: int,
    weight_strength: float,
) -> tuple[WeightedNetwork | None, dict]:
    v6 = load_module(V6_SCRIPT, "abm_v7_v6_source")
    v5 = load_module(V5_SCRIPT, "abm_v7_v5_source")
    import random

    active = v6.active_pollinator_indices(
        len(feasible_network.pollinator_names),
        rng=random.Random(support_seed),
        support_strength=support_strength,
    )
    closed, audit = apply_joint_support_closure(feasible_network, active)
    audit["support_strength"] = support_strength
    audit["weight_strength"] = weight_strength
    if closed is None or audit["empty_local_network"]:
        return closed, audit
    realized = v5.realize_local_context(
        closed,
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
    v4 = load_module(V4_WEIGHTED, "abm_v7_v4_source")
    feasible = v4.run_weighted_network(
        isolation_index,
        evolution_seed,
        saturation,
        n_lineages=n_lineages,
        steps=steps,
    )
    realized, audit = realize_local_context(
        feasible,
        support_seed=support_seed,
        support_strength=support_strength,
        weight_seed=weight_seed,
        weight_strength=weight_strength,
    )
    return feasible, realized, audit


def build_contract() -> dict:
    return {
        "model": "constraint_mechanism_abm_v7_joint_support_closure",
        "status": "failure_driven_mechanism_freeze_before_new_empirical_validation",
        "failure_source": {
            "pr": 200,
            "decision": "v6_fails_giannutri_conditional_local_support_structural_gate",
            "use_of_failure": "Giannutri identifies the missing mechanism class: pollinator support cannot vary while every positive plant row is forced to remain locally active. No Giannutri target amplitude, plant identity, or fitted support probability is loaded by v7.",
        },
        "inherits": [
            "ABM v4 island-scale feasible opportunity process unchanged",
            "ABM v6 pollinator-support draw unchanged",
            "ABM v5 within-support positive affinity reweighting unchanged for retained plant rows",
        ],
        "hierarchy": {
            "island_scale": "v4 defines feasible plants, pollinators and pair-opportunity weights",
            "local_pollinator_support": "v6 selects a subset of already-feasible pollinators",
            "joint_support_closure": "a positive plant row remains locally active only if at least one of its positive feasible pollinator partners is locally active; otherwise the plant row becomes locally inactive",
            "local_realization": "retained plants preserve their exact baseline row budgets and v5 redistributes weight only among their active positive partners",
        },
        "new_parameter_count": 0,
        "joint_support_rule": {
            "independent_plant_dropout_probability": None,
            "rule": "plant inactivity is induced only by loss of all positive locally active partners; v7 does not add a fitted or free plant-support-strength parameter",
            "empty_local_network": "allowed as a structural local state and recorded explicitly rather than repaired",
        },
        "hard_invariants": [
            "no plant or pollinator absent from the feasible island network can be created",
            "no positive link absent from the feasible island network can be created",
            "every retained positive plant row keeps its exact pre-context total interaction budget",
            "a positive plant row with zero active positive partners is dropped rather than assigned manufactured interaction weight",
            "when a v6 support mask is already admissible for every positive plant row, v7 support closure must reproduce the exact v6 support-filtered network",
            "with full pollinator support, v7 reduces to the inherited v5 realization layer",
            "Giannutri empirical target values are not loaded to choose any v7 parameter because v7 adds no new parameter",
        ],
        "predeclared_synthetic_falsification": [
            "reject v7 if full-support identity with v5 fails",
            "reject v7 if any retained plant row changes total budget beyond numerical tolerance",
            "reject v7 if any new taxon or link is created",
            "reject v7 if a v6-admissible mask is changed by support closure",
            "reject v7 if a canonical partnerless-positive-plant v6 failure cannot be represented by dropping that plant without changing other retained row budgets",
            "reject v7 if repeated nonzero support contexts cannot branch in pollinator or joint plant support in structurally reducible states",
            "reject v7 if the frozen v4 opportunity-direction contract no longer holds",
        ],
        "next_empirical_gate": "After synthetic prevalidation, choose a new independent repeated-local quantitative island system before inspecting v7 targets. Giannutri is consumed as the structural falsification that motivated joint support closure and cannot confirm v7.",
        "claim_boundary": "v7 is the minimum structural response to the Giannutri v6 failure. It permits induced local plant inactivity when all locally active pollinator partners are lost, but it does not yet posit independent flowering/resource dynamics, plant-support probabilities, habitat effects, or fitted temporal processes.",
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
