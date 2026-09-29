from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_abm_v9_martinique_validation.py"


def load_script():
    spec = importlib.util.spec_from_file_location("martinique_v9_validation_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_missing_sentinels_are_not_identity():
    module = load_script()
    assert module.identity(None) == ""
    assert module.identity("NA") == ""
    assert module.identity("nan") == ""
    assert module.identity("Plant A") == "Plant A"


def test_shannon_zero_and_even_two_pair_cases():
    module = load_script()
    assert module.shannon([]) == 0.0
    assert module.shannon([0, 0]) == 0.0
    assert abs(module.shannon([1, 1]) - 0.6931471805599453) < 1e-12


def test_jaccard_turnover_handles_empty_sets_without_dropping_contexts():
    module = load_script()
    pair = {("p", "q")}
    value = module.jaccard_turnover([set(), pair])
    assert value == 1.0
    assert module.jaccard_turnover([set(), set()]) == 0.0


def test_fast_supported_context_matches_frozen_v9_on_toy_network():
    module = load_script()
    v9 = module.load_module(module.V9_SCRIPT, "martinique_v9_test_core")
    v8 = module.load_module(module.V8_SCRIPT, "martinique_v9_test_v8")
    v6 = module.load_module(module.V6_SCRIPT, "martinique_v9_test_v6")
    v5 = module.load_module(module.V5_SCRIPT, "martinique_v9_test_v5")
    baseline = WeightedNetwork.from_rows(
        ["p1", "p2"],
        ["q1", "q2", "q3"],
        [
            [2.0, 1.0, 3.0],
            [1.0, 4.0, 2.0],
        ],
    )
    for index, strength in enumerate((0.25, 0.5, 0.75)):
        support_seed = 20260821 + index
        weight_seed = 20260921 + index
        expected, _ = v9.realize_local_context(
            baseline,
            support_seed=support_seed,
            support_strength=strength,
            weight_seed=weight_seed,
            weight_strength=0.5,
        )
        supported, _active, _audit = module.fast_supported_context(
            v9, v8, v6, baseline,
            support_seed=support_seed,
            support_strength=strength,
        )
        actual = None if supported is None else v5.realize_local_context(
            supported,
            context_seed=weight_seed,
            context_strength=0.5,
        )
        assert actual == expected


def test_envelope_and_inside_are_inclusive():
    module = load_script()
    interval = module.envelope([0.0, 1.0, 2.0, 3.0, 4.0])
    assert interval["p2.5"] <= interval["median"] <= interval["p97.5"]
    assert module.inside(interval["p2.5"], interval)
    assert module.inside(interval["p97.5"], interval)
