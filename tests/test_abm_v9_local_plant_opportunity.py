from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V9 = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V8 = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy() -> WeightedNetwork:
    return WeightedNetwork.from_rows(
        ["p1", "p2", "p3"],
        ["a", "b", "c"],
        [[3.0, 2.0, 1.0], [1.0, 4.0, 2.0], [2.0, 1.0, 5.0]],
    )


def test_zero_support_is_exact_v8_identity_across_weight_strengths():
    v9 = load(V9, "v9_test_zero")
    v8 = load(V8, "v9_test_v8_zero")
    network = toy()
    for weight_strength in v9.WEIGHT_STRENGTHS:
        expected, _ = v8.realize_local_context(
            network,
            support_seed=17,
            support_strength=0.0,
            weight_seed=91,
            weight_strength=weight_strength,
        )
        actual, audit = v9.realize_local_context(
            network,
            support_seed=17,
            support_strength=0.0,
            weight_seed=91,
            weight_strength=weight_strength,
        )
        assert actual == expected
        assert audit["zero_support_exact_v8_bypass"] is True


def test_v9_plant_mask_only_removes_rows_from_unchanged_v8_pair_draw():
    v9 = load(V9, "v9_test_mask")
    v8 = load(V8, "v9_test_v8_mask")
    network = toy()
    support_seed = 23
    strength = 0.5
    active = v9.draw_local_plant_indices(
        network,
        plant_seed=support_seed + v9.PLANT_SEED_OFFSET,
        support_strength=strength,
    )
    v8_mask, _ = v8.draw_hierarchical_pair_support_mask(
        network,
        support_seed=support_seed,
        support_strength=strength,
    )
    combined = v9.combine_plant_and_v8_pair_masks(
        network,
        active_plant_indices=active,
        v8_pair_mask=v8_mask,
    )
    active_set = set(active)
    for row_index, (source_row, combined_row) in enumerate(zip(v8_mask, combined)):
        if row_index in active_set:
            assert combined_row == source_row
        else:
            assert not any(combined_row)


def test_all_local_plants_can_be_absent_without_redraw():
    v9 = load(V9, "v9_test_empty")
    network = toy()
    chosen_seed = None
    for seed in range(10000):
        active = v9.draw_local_plant_indices(
            network,
            plant_seed=seed,
            support_strength=0.75,
        )
        if not active:
            chosen_seed = seed
            break
    assert chosen_seed is not None
    # Convert plant RNG seed back to the support seed used by realize_local_context.
    support_seed = chosen_seed - v9.PLANT_SEED_OFFSET
    realized, audit = v9.realize_local_context(
        network,
        support_seed=support_seed,
        support_strength=0.75,
        weight_seed=11,
        weight_strength=0.5,
    )
    assert realized is None
    assert audit["plant_layer"]["empty_plant_opportunity"] is True
    assert audit["empty_local_network"] is True


def test_contract_adds_no_fitted_plant_or_observation_parameter():
    v9 = load(V9, "v9_test_contract")
    contract = v9.build_contract()
    assert contract["new_parameter_count"] == 0
    assert contract["support_strengths"] == [0.0, 0.25, 0.5, 0.75]
    assert "mechanism sensitivity axis" in contract["shared_generic_strength"]
    assert "not part of v9 biology" in contract["hierarchy"]["observation_layer"]
    assert "Cabrera" in contract["failure_source"]["use_of_failure"]
    assert "No Cabrera target value" in contract["failure_source"]["use_of_failure"]


def test_v9_core_does_not_import_empirical_result_files():
    text = V9.read_text()
    assert "data/results/abm_v8_cabrera_validation.json" not in text
    assert "cabrera_v8_failure_layer_diagnosis.json" not in text
    assert "0.040677966" not in text
    assert "0.720058" not in text
    assert "0.906811" not in text
