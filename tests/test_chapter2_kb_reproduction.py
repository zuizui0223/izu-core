"""Static complete-ledger and finite-population tests for independent K/B controls.

All tests run on synthetic old/fixed states and never access prospective
40110901-40110964 visitor histories or infer primary effects.
"""
from dataclasses import replace

import numpy as np
import pytest

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import subset
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN, config, founders, load_design


@pytest.fixture(scope="module")
def controlled_case():
    design = load_design(DEFAULT_DESIGN)
    full = founders(design)
    state = subset(full, np.arange(8))
    visitors = VisitorState(
        ids=np.array([8, 9], dtype=np.int64),
        optima=np.array([0.4, 0.6]),
        breadths=np.array([0.6, 0.7]),
        effectiveness=np.array([0.9, 0.85]),
    )
    return design, state, visitors


@pytest.mark.parametrize("setting", [
    "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
])
@pytest.mark.parametrize("K", [8, 48])
def test_full_ledger_bitwise_parity_for_B_equals_K(controlled_case, setting, K):
    design, state, visitors = controlled_case
    cfg = replace(config(design, setting, 0.01, "evolving"), capacity=K)
    original = reproduce(state, visitors, cfg)
    adjusted = reproduce_kb(state, visitors, cfg, background_denominator_capacity=K)
    for field in original.__dataclass_fields__:
        np.testing.assert_array_equal(getattr(original, field), getattr(adjusted, field))


@pytest.mark.parametrize("K", [8,48])
def test_pollen_sharing_dilution_changes_seed_receipt_without_changing_export(controlled_case, K):
    design, state, visitors = controlled_case
    cfg = replace(config(design, "delayed_control", 0.01, "evolving"), capacity=K)
    b8 = reproduce_kb(state, visitors, cfg, background_denominator_capacity=8)
    b48 = reproduce_kb(state, visitors, cfg, background_denominator_capacity=48)
    np.testing.assert_array_equal(b8.exported, b48.exported)
    assert b8.outcross.sum() > b48.outcross.sum()
    assert b8.self_viable.sum() < b48.self_viable.sum()


def test_K_changes_only_population_ceiling_at_fixed_B_initial_reproduction(controlled_case):
    design, state, visitors = controlled_case
    cfg8 = replace(config(design, "delayed_control", 0.01, "evolving"), capacity=8)
    cfg48 = replace(cfg8, capacity=48)
    led8 = reproduce_kb(state, visitors, cfg8, background_denominator_capacity=48)
    led48 = reproduce_kb(state, visitors, cfg48, background_denominator_capacity=48)
    for field in led8.__dataclass_fields__:
        np.testing.assert_array_equal(getattr(led8, field), getattr(led48, field))


def test_independent_B_never_weakens_population_capacity_guard(controlled_case):
    design, state, visitors = controlled_case
    invalid_population = founders(design)  # 48 individuals
    cfg = replace(config(design, "delayed_control", 0.01, "evolving"), capacity=8)
    with pytest.raises(ValueError, match="population exceeds capacity"):
        reproduce_kb(invalid_population, visitors, cfg, background_denominator_capacity=48)


@pytest.mark.parametrize("bad_B", [0,9,47,49,8.0,True,None])
def test_reject_unregistered_background_normalizer(controlled_case, bad_B):
    design, state, visitors = controlled_case
    cfg = replace(config(design, "delayed_control", 0.01, "evolving"), capacity=8)
    with pytest.raises(ValueError):
        reproduce_kb(state, visitors, cfg, background_denominator_capacity=bad_B)


def test_frozen_prospective_design_has_no_exposed_histories():
    import json
    from pathlib import Path
    d = json.loads(Path("data/design/chapter2_kb_decoupled_20261009.json").read_text())
    h = d["independent_cohort"]
    assert (h["visitor_history_first"], h["visitor_history_last"]) == (40110901, 40110964)
    assert h["full_diploid_t400_source_count"] == 2048
    assert d["full_grid"]["n_raw_future_trajectories"] == 229376
    assert d["full_grid"]["n_futures_per_source"] == 112
    assert d["primary_estimand"]["focal_contrast"] == "tau(K8,B8)-tau(K8,B48)"
    assert d["status"] == "FROZEN_PROSPECTIVE_DESIGN_NO_NEW_OUTCOMES"
