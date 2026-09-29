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
OUT = ROOT / "data/results/constraint_mechanism_abm_v5_hierarchical_context.json"
CONTEXT_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)


@functools.lru_cache(maxsize=None)
def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def local_affinity(rng: random.Random) -> float:
    """Generic bounded local pair affinity with mean one and no biological label."""
    return 0.1 + 1.8 * rng.random()


def redistribute_row(row: tuple[float, ...], rng: random.Random, context_strength: float) -> tuple[float, ...]:
    if not 0.0 <= context_strength <= 1.0:
        raise ValueError("context_strength must be in [0, 1]")
    total = sum(row)
    if context_strength == 0.0 or total <= 0.0:
        return tuple(row)
    factors = [
        (1.0 - context_strength) + context_strength * local_affinity(rng)
        for _ in row
    ]
    raw = [value * factor for value, factor in zip(row, factors)]
    raw_total = sum(raw)
    if raw_total <= 0.0:
        raise RuntimeError("positive context affinities produced a non-positive row total")
    scale = total / raw_total
    realized = tuple(value * scale for value in raw)
    if not math.isclose(sum(realized), total, rel_tol=1e-12, abs_tol=1e-14):
        raise RuntimeError("local realization failed fixed row-budget conservation")
    return realized


def realize_local_context(
    feasible_network: WeightedNetwork,
    *,
    context_seed: int,
    context_strength: float,
) -> WeightedNetwork:
    rng = random.Random(context_seed)
    matrix = [redistribute_row(row, rng, context_strength) for row in feasible_network.matrix]
    return WeightedNetwork.from_rows(
        feasible_network.plant_names,
        feasible_network.pollinator_names,
        matrix,
    )


def run_weighted_network(
    isolation_index: float,
    evolution_seed: int,
    saturation: float,
    *,
    context_seed: int,
    context_strength: float,
    n_lineages: int = 24,
    steps: int = 120,
) -> tuple[WeightedNetwork, WeightedNetwork]:
    v4 = load_module(V4_WEIGHTED, "abm_v5_v4_weighted_source")
    feasible = v4.run_weighted_network(
        isolation_index,
        evolution_seed,
        saturation,
        n_lineages=n_lineages,
        steps=steps,
    )
    realized = realize_local_context(
        feasible,
        context_seed=context_seed,
        context_strength=context_strength,
    )
    return feasible, realized


def build_contract() -> dict:
    return {
        "model": "constraint_mechanism_abm_v5_hierarchical_context",
        "status": "mechanism_freeze_before_new_empirical_validation",
        "inherits": "ABM v4 fixed-total-visit-budget opportunity process unchanged",
        "hierarchy": {
            "island_scale": "v4 determines feasible pollinator pool, arrival/loss, partner traits and plant adaptation",
            "local_scale": "a generic pair-level context field redistributes realized interaction weight within each plant's already-feasible partner set",
        },
        "context_field": {
            "biological_label": None,
            "empirical_context_categories_loaded": [],
            "raw_affinity_distribution": "Uniform(0.1, 1.9), mean 1; mechanism stress-test distribution, not an empirical estimate",
            "strength_envelope": list(CONTEXT_STRENGTHS),
            "mixing_rule": "factor=(1-strength)+strength*local_affinity",
            "normalization": "each plant row is rescaled to its exact v4 pair-weight total",
        },
        "hard_invariants": [
            "context_strength=0 is exactly the v4 weighted-network observation layer",
            "plant and pollinator identities/dimensions are unchanged by local context",
            "all local affinity factors stay positive, so context does not create or delete feasible partners",
            "each plant's total realized pair weight is identical before and after context redistribution",
            "a positive state with only one feasible pollinator is structurally non-branchable and must remain unchanged rather than inventing a partner",
            "no Ogasawara, forest, anole, or other empirical outcome is loaded to define the context field",
        ],
        "predeclared_falsification": [
            "reject v5 if zero-strength identity with v4 fails",
            "reject v5 if row-budget conservation fails",
            "reject v5 if local context changes feasible partner dimensions or positive-link support",
            "reject v5 if any structurally branchable state with at least two feasible pollinators cannot generate measurable Shannon and plant-overlap variation at nonzero context strength",
            "reject v5 if zero-variation positive states are not exactly the structurally non-branchable single-pollinator states",
            "reject v5 as a branching realization layer if independent context pairs cannot produce both signs of Shannon and overlap differences across the frozen synthetic envelope",
        ],
        "prevalidation_correction_note": "The first synthetic gate incorrectly required context variation even when v4 ended with exactly one pollinator. Under fixed support and fixed row totals, a one-column network has no redistribution degree of freedom. The model was not changed to force variation; the gate was corrected to test only structurally branchable states and to require degenerate states to remain non-branchable.",
        "claim_boundary": "v5 does not assert that forest disturbance or anole presence causes a particular network change. Context strength is not fitted to Ogasawara. The local layer represents unresolved realization heterogeneity within an island-scale opportunity set and conserves total plant opportunity by construction.",
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
