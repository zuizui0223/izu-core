from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V8 = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
V5 = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy():
    return WeightedNetwork.from_rows(
        ["p1", "p2"],
        ["a", "b", "c"],
        [[1.0, 2.0, 3.0], [2.0, 1.0, 1.0]],
    )


def test_zero_support_reproduces_v5_exactly():
    v8 = load(V8, "v8_test_zero")
    v5 = load(V5, "v8_test_v5")
    source = toy()
    for strength in v8.WEIGHT_STRENGTHS:
        expected = v5.realize_local_context(source, context_seed=77, context_strength=strength)
        actual, audit = v8.realize_local_context(
            source,
            support_seed=11,
            support_strength=0.0,
            weight_seed=77,
            weight_strength=strength,
        )
        assert actual == expected
        assert audit["dropped_partnerless_positive_plant_count"] == 0


def test_pair_mask_can_drop_plant_and_pollinator_without_creating_links():
    v8 = load(V8, "v8_test_mask")
    source = toy()
    mask = (
        (False, True, False),
        (False, False, False),
    )
    realized, audit = v8.apply_pair_support_mask(source, mask)
    assert realized is not None
    assert realized.plant_names == ("p1",)
    assert realized.pollinator_names == ("b",)
    assert audit["dropped_partnerless_positive_plants"] == ["p2"]
    assert math.isclose(sum(realized.matrix[0]), 6.0, rel_tol=1e-12)
    assert realized.matrix[0][0] > 0.0


def test_pair_mask_allows_empty_network_without_redraw():
    v8 = load(V8, "v8_test_empty")
    source = toy()
    mask = tuple(tuple(False for _ in source.pollinator_names) for _ in source.plant_names)
    realized, audit = v8.apply_pair_support_mask(source, mask)
    assert realized is None
    assert audit["empty_local_network"] is True
    assert audit["dropped_partnerless_positive_plant_count"] == 2


def test_hierarchical_draw_never_activates_pair_outside_global_pollinator_support():
    v8 = load(V8, "v8_test_hierarchy")
    source = toy()
    mask, global_active = v8.draw_hierarchical_pair_support_mask(
        source, support_seed=4, support_strength=0.75
    )
    global_active = set(global_active)
    for row in mask:
        for column, active in enumerate(row):
            if active:
                assert column in global_active


def test_contract_reuses_support_strength_and_loads_no_empirical_fit():
    v8 = load(V8, "v8_test_contract")
    contract = v8.build_contract()
    assert contract["new_parameter_count"] == 0
    assert contract["support_strengths"] == [0.0, 0.25, 0.5, 0.75]
    assert "same pre-existing generic support strength" in contract["support_hierarchy"]["shared_strength"]
    assert "No Menorca or Giannutri target amplitude" in contract["use_of_failures"]
    assert "cannot confirm v8" in contract["next_empirical_gate"]
