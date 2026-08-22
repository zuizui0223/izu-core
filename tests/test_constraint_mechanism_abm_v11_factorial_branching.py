from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_constraint_mechanism_abm_v11_factorial_branching.py"


def load_v11():
    spec = importlib.util.spec_from_file_location("abm_v11_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_factorial_contains_all_16_unique_configurations():
    v11 = load_v11()
    configs = v11.all_configs()
    assert len(configs) == 16
    assert len({v11.config_id(config) for config in configs}) == 16


def test_branching_balance_has_expected_bounds():
    v11 = load_v11()
    assert v11.branching_balance(0, 0) == 0.0
    assert v11.branching_balance(10, 0) == 0.0
    assert v11.branching_balance(10, 10) == 1.0
    assert v11.branching_balance(5, 15) == 0.5


def test_dependency_and_assurance_ablations_change_only_declared_template_fields():
    v11 = load_v11()
    v4 = v11.load_module(v11.V4_SCRIPT, "abm_v11_test_v4")
    base = v4.make_lineages(__import__("random").Random(1), 3)
    config = {name: True for name in v11.FACTORS}
    config["dependency_heterogeneity"] = False
    config["assurance_responsiveness"] = False
    modified = v11.modified_templates(base, config)
    for original, changed in zip(base, modified):
        assert changed.pollinator_dependency == v11.DEPENDENCY_COMMON_VALUE
        assert changed.assurance_responsiveness == 0.0
        assert changed.assurance_ceiling == original.assurance_ceiling
        assert changed.trait == original.trait
        assert changed.trait_adjustment == original.trait_adjustment


def test_small_factorial_build_is_target_blind_and_has_drop_one_results():
    v11 = load_v11()
    payload = v11.build(replicates=1, contexts=1, n_lineages=5, steps=4, seed=4321)
    assert payload["design"]["factorial_configurations"] == 16
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert payload["design"]["izu_target_frequencies_loaded"] is False
    assert payload["design"]["external_target_values_loaded"] is False
    assert set(payload["drop_one_ablation"]) == set(v11.FACTORS)
    assert set(payload["factor_ranking_by_branching_balance_loss"]) == set(v11.FACTORS)
    full = payload["full_model_summary"]
    assert 0.0 <= full["branching_balance"] <= 1.0
    assert 0.0 <= full["mixed_sign_run_fraction"] <= 1.0
