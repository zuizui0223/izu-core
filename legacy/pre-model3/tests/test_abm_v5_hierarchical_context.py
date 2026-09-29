from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_v5_context_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy_network():
    return WeightedNetwork.from_rows(
        ["plant_a", "plant_b"],
        ["pollinator_1", "pollinator_2", "pollinator_3"],
        [
            [0.2, 0.5, 0.3],
            [0.6, 0.1, 0.3],
        ],
    )


def test_zero_strength_is_exact_identity():
    module = load_module()
    network = toy_network()
    realized = module.realize_local_context(network, context_seed=7, context_strength=0.0)
    assert realized == network


def test_nonzero_context_preserves_row_budgets_and_support():
    module = load_module()
    network = toy_network()
    realized = module.realize_local_context(network, context_seed=11, context_strength=1.0)
    assert realized.plant_names == network.plant_names
    assert realized.pollinator_names == network.pollinator_names
    assert tuple(tuple(v > 0 for v in row) for row in realized.matrix) == tuple(
        tuple(v > 0 for v in row) for row in network.matrix
    )
    for before, after in zip(network.matrix, realized.matrix):
        assert math.isclose(sum(before), sum(after), rel_tol=1e-12, abs_tol=1e-14)
    assert realized != network


def test_local_affinity_is_bounded_positive_and_mean_centered_in_large_draw():
    module = load_module()
    rng = random.Random(123)
    values = [module.local_affinity(rng) for _ in range(10000)]
    assert min(values) >= 0.1
    assert max(values) <= 1.9
    assert abs(sum(values) / len(values) - 1.0) < 0.02


def test_context_strength_out_of_bounds_is_rejected():
    module = load_module()
    row = (0.2, 0.3, 0.5)
    for strength in (-0.01, 1.01):
        try:
            module.redistribute_row(row, random.Random(1), strength)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-bounds context strength must fail")


def test_contract_contains_no_empirical_context_fit():
    module = load_module()
    contract = module.build_contract()
    assert contract["context_field"]["empirical_context_categories_loaded"] == []
    assert contract["context_field"]["biological_label"] is None
    assert "Ogasawara" in contract["hard_invariants"][-1]
    assert "not fitted" in contract["claim_boundary"]
