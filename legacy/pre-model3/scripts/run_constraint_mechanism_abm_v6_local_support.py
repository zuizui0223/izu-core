from __future__ import annotations

import argparse
import functools
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_WEIGHTED = ROOT / "scripts/run_abm_v4_weighted_architecture_emulator.py"
V5 = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v6_local_support.json"
SUPPORT_STRENGTHS = (0.0, 0.25, 0.5, 0.75)
WEIGHT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)


@functools.lru_cache(maxsize=None)
def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def active_pollinator_indices(
    n_pollinators: int,
    *,
    rng: random.Random,
    support_strength: float,
) -> tuple[int, ...]:
    """Draw a context-specific subset of the island-feasible pollinator pool."""
    if n_pollinators <= 0:
        raise ValueError("n_pollinators must be positive")
    if not 0.0 <= support_strength < 1.0:
        raise ValueError("support_strength must be in [0, 1)")
    if support_strength == 0.0:
        return tuple(range(n_pollinators))

    keep_probability = 1.0 - support_strength
    active = [
        index for index in range(n_pollinators)
        if rng.random() < keep_probability
    ]
    if not active:
        # Condition on at least one locally active member of the already-feasible
        # island pool. This prevents context from manufacturing a new partner and
        # avoids turning fixed-budget redistribution into a zero-service state.
        active = [rng.randrange(n_pollinators)]
    return tuple(active)


def apply_active_pollinator_indices(
    feasible_network: WeightedNetwork,
    active_indices: tuple[int, ...] | list[int],
) -> WeightedNetwork:
    """Apply one already-drawn shared local-support mask with v6 hard invariants.

    This is the deterministic support-mask step used by ``apply_local_support``.
    Exposing it separately allows independently frozen ascertainment rules to
    condition the support draw without bypassing v6's row-budget/admissibility
    checks or changing the stochastic v6 support model.
    """
    if not feasible_network.pollinator_names:
        raise ValueError("feasible network requires at least one pollinator column")
    active = tuple(sorted(int(index) for index in active_indices))
    if not active:
        raise ValueError("local support requires at least one active feasible pollinator")
    if len(set(active)) != len(active):
        raise ValueError("active pollinator indices must be unique")
    if active[0] < 0 or active[-1] >= len(feasible_network.pollinator_names):
        raise ValueError("active pollinator index lies outside feasible network")

    active_names = [feasible_network.pollinator_names[index] for index in active]
    rows = []
    for row_index, row in enumerate(feasible_network.matrix):
        baseline_total = sum(row)
        selected = [row[index] for index in active]
        selected_total = sum(selected)
        if baseline_total <= 0.0:
            rows.append([0.0 for _ in selected])
            continue
        if selected_total <= 0.0:
            raise RuntimeError(
                f"local support removed every positive partner for plant row {row_index}"
            )
        scale = baseline_total / selected_total
        realized = [value * scale for value in selected]
        if not math.isclose(
            sum(realized), baseline_total, rel_tol=1e-12, abs_tol=1e-14
        ):
            raise RuntimeError("local support layer failed fixed row-budget conservation")
        rows.append(realized)

    return WeightedNetwork.from_rows(
        feasible_network.plant_names,
        active_names,
        rows,
    )


def apply_local_support(
    feasible_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
) -> WeightedNetwork:
    if not feasible_network.pollinator_names:
        raise ValueError("feasible network requires at least one pollinator column")
    if support_strength == 0.0:
        return feasible_network

    rng = random.Random(support_seed)
    active = active_pollinator_indices(
        len(feasible_network.pollinator_names),
        rng=rng,
        support_strength=support_strength,
    )
    return apply_active_pollinator_indices(feasible_network, active)


def realize_local_context(
    feasible_network: WeightedNetwork,
    *,
    support_seed: int,
    support_strength: float,
    weight_seed: int,
    weight_strength: float,
) -> WeightedNetwork:
    support_network = apply_local_support(
        feasible_network,
        support_seed=support_seed,
        support_strength=support_strength,
    )
    v5 = load_module(V5, "abm_v6_v5_source")
    return v5.realize_local_context(
        support_network,
        context_seed=weight_seed,
        context_strength=weight_strength,
    )


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
) -> tuple[WeightedNetwork, WeightedNetwork]:
    v4 = load_module(V4_WEIGHTED, "abm_v6_v4_weighted_source")
    feasible = v4.run_weighted_network(
        isolation_index,
        evolution_seed,
        saturation,
        n_lineages=n_lineages,
        steps=steps,
    )
    realized = realize_local_context(
        feasible,
        support_seed=support_seed,
        support_strength=support_strength,
        weight_seed=weight_seed,
        weight_strength=weight_strength,
    )
    return feasible, realized


def build_contract() -> dict:
    return {
        "model": "constraint_mechanism_abm_v6_local_support_and_realization",
        "status": "failure_driven_mechanism_freeze_before_new_empirical_validation",
        "failure_source": {
            "pr": 195,
            "decision": "v5_fails_menorca_nine_local_raw_architecture_test",
            "use_of_failure": "Menorca identifies the missing mechanism class (support can vary locally); no Menorca metric value is loaded or used to select v6 strengths, probabilities or thresholds.",
        },
        "inherits": [
            "ABM v4 fixed-total-visit-budget island opportunity process unchanged",
            "ABM v5 positive within-support affinity reweighting unchanged after support selection",
        ],
        "hierarchy": {
            "island_scale": "v4 defines the feasible pollinator pool and pair-opportunity weights",
            "local_support_scale": "each local context activates a random subset of the already-feasible pollinator pool; it cannot create a partner absent from the island-feasible pool",
            "local_realization_scale": "v5 then redistributes weights only within the locally active support",
        },
        "support_field": {
            "biological_label": None,
            "empirical_context_categories_loaded": [],
            "support_strengths": list(SUPPORT_STRENGTHS),
            "rule": "each feasible pollinator is locally active with probability 1-support_strength, conditioned on at least one active feasible pollinator",
            "mask_application": "the stochastic draw and deterministic support-mask application are separate functions; both generic and externally conditioned masks use the same row-budget/admissibility checks",
            "reason_for_excluding_strength_1": "support_strength=1 would deterministically collapse every positive context to one forced partner after conditioning and is excluded from the generic stress envelope rather than treated as an empirical estimate",
        },
        "weight_field": {
            "strengths": list(WEIGHT_STRENGTHS),
            "implementation": "unchanged v5 Uniform(0.1,1.9) positive affinity field followed by exact row normalization",
        },
        "hard_invariants": [
            "support_strength=0 reproduces the v5 support exactly",
            "support_strength=0 and weight_strength=0 reproduces the v4 weighted-network observation layer exactly",
            "a local context may delete feasible pollinator columns but can never introduce a pollinator absent from the island-feasible pool",
            "plant identities are unchanged by the local support layer",
            "each plant's total pair weight is exactly conserved whenever its baseline row total is positive",
            "the local support mask is shared across plants within a context, representing local partner availability rather than plant-specific post-hoc link deletion",
            "Menorca, Ogasawara and other empirical network outcomes are not loaded by the v6 mechanism or synthetic prevalidation",
        ],
        "predeclared_synthetic_falsification": [
            "reject v6 if zero-support identity with v5 fails",
            "reject v6 if zero-support/zero-weight identity with v4 fails",
            "reject v6 if any local pollinator identity lies outside the feasible island pool",
            "reject v6 if row-budget conservation fails",
            "reject v6 if positive support_strength cannot reduce local pollinator support in any structurally reducible synthetic state",
            "reject v6 if repeated local contexts cannot produce at least two distinct support sets in structurally reducible states",
            "reject v6 if the inherited frozen v4 opportunity-direction contract no longer holds",
        ],
        "next_empirical_gate": "If synthetic invariants pass, freeze a new independent empirical system before target inspection. Menorca is consumed as the failure that motivated v6 and cannot be reused as confirmatory validation or to tune the support-strength envelope.",
        "claim_boundary": "v6 is a minimal mechanism-class response to the Menorca high-side failure. It does not claim that any specific habitat, season or disturbance causes partner filtering, and its support-strength values are a generic sensitivity envelope rather than fitted ecological parameters.",
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
