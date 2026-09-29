from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V5 = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy_network():
    return WeightedNetwork.from_rows(
        ["plant_a", "plant_b"],
        ["pollinator_1", "pollinator_2", "pollinator_3", "pollinator_4"],
        [
            [0.2, 0.3, 0.1, 0.4],
            [0.4, 0.1, 0.3, 0.2],
        ],
    )


def test_zero_support_zero_weight_is_exact_identity():
    module = load(SCRIPT, "v6_test_identity")
    network = toy_network()
    realized = module.realize_local_context(
        network,
        support_seed=1,
        support_strength=0.0,
        weight_seed=2,
        weight_strength=0.0,
    )
    assert realized == network


def test_zero_support_reproduces_v5_exactly():
    module = load(SCRIPT, "v6_test_v5_identity")
    v5 = load(V5, "v6_test_v5_source")
    network = toy_network()
    for strength in module.WEIGHT_STRENGTHS:
        expected = v5.realize_local_context(network, context_seed=77, context_strength=strength)
        actual = module.realize_local_context(
            network,
            support_seed=99,
            support_strength=0.0,
            weight_seed=77,
            weight_strength=strength,
        )
        assert actual == expected


def test_positive_support_filters_only_existing_pollinators_and_conserves_rows():
    module = load(SCRIPT, "v6_test_filter")
    network = toy_network()
    realized = module.realize_local_context(
        network,
        support_seed=11,
        support_strength=0.75,
        weight_seed=12,
        weight_strength=0.5,
    )
    assert set(realized.pollinator_names).issubset(set(network.pollinator_names))
    assert realized.plant_names == network.plant_names
    assert 1 <= len(realized.pollinator_names) <= len(network.pollinator_names)
    for before, after in zip(network.matrix, realized.matrix):
        assert math.isclose(sum(before), sum(after), rel_tol=1e-12, abs_tol=1e-14)


def test_support_draw_is_shared_context_mask_not_plant_specific():
    module = load(SCRIPT, "v6_test_shared_mask")
    network = toy_network()
    support_only = module.apply_local_support(
        network,
        support_seed=23,
        support_strength=0.5,
    )
    assert len(support_only.matrix[0]) == len(support_only.pollinator_names)
    assert all(len(row) == len(support_only.pollinator_names) for row in support_only.matrix)
    assert set(support_only.pollinator_names).issubset(set(network.pollinator_names))


def test_support_strength_bounds_and_forced_nonempty_subset():
    module = load(SCRIPT, "v6_test_bounds")
    for invalid in (-0.01, 1.0, 1.1):
        try:
            module.active_pollinator_indices(3, rng=random.Random(1), support_strength=invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid support strength must fail")
    active = module.active_pollinator_indices(3, rng=random.Random(4), support_strength=0.75)
    assert active
    assert set(active).issubset({0, 1, 2})


def test_contract_uses_menorca_only_as_failure_class_not_fit():
    module = load(SCRIPT, "v6_test_contract")
    contract = module.build_contract()
    assert contract["failure_source"]["pr"] == 195
    assert "no Menorca metric value" in contract["failure_source"]["use_of_failure"]
    assert contract["support_field"]["empirical_context_categories_loaded"] == []
    assert "cannot create" in contract["hierarchy"]["local_support_scale"]
    assert "cannot be reused" in contract["next_empirical_gate"]
