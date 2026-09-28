from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_constraint_mechanism_abm_v12_residual_trait_causes.py"


def load_v12():
    spec = importlib.util.spec_from_file_location("abm_v12_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_residual_factorial_has_eight_cells():
    v12 = load_v12()
    configs = v12.all_configs()
    assert len(configs) == 8
    assert len({v12.config_id(config) for config in configs}) == 8


def test_all_residual_factors_off_make_templates_identical_on_declared_fields():
    v12 = load_v12()
    v4 = v12.load_module(v12.V4_CORE, "abm_v12_test_v4")
    base = v4.make_lineages(random.Random(1), 4)
    config = {factor: False for factor in v12.FACTORS}
    transformed = v12.transform_templates(base, config)
    assert {template.trait for template in transformed} == {v12.COMMON_TRAIT}
    assert {template.trait_adjustment for template in transformed} == {v12.COMMON_TRAIT_ADJUSTMENT}
    assert {template.assurance_ceiling for template in transformed} == {v12.COMMON_ASSURANCE_CEILING}
    assert {template.pollinator_dependency for template in transformed} == {v12.COMMON_DEPENDENCY}
    assert {template.assurance_responsiveness for template in transformed} == {0.0}


def test_identical_lineages_have_no_within_run_branching():
    v12 = load_v12()
    v4 = v12.load_module(v12.V4_CORE, "abm_v12_test_v4_identical")
    gradient = v12.load_module(v12.GRADIENT, "abm_v12_test_gradient")
    base = v4.make_lineages(random.Random(123), 6)
    templates = v12.transform_templates(base, {factor: False for factor in v12.FACTORS})
    values = v12.paired_deltas(
        v4=v4,
        gradient=gradient,
        templates=templates,
        seed=123,
        saturation=2.0,
        steps=8,
    )
    assert len({round(value, 14) for value in values}) == 1
    assert v12.within_run_balance(values) == 0.0


def test_row_sum_reproduction_is_order_invariant():
    v12 = load_v12()
    left = v12.reproduction_from_row((0.1, 0.2, 0.3), saturation=2.0, assurance_ceiling=0.5)
    right = v12.reproduction_from_row((0.3, 0.1, 0.2), saturation=2.0, assurance_ceiling=0.5)
    assert left == right
