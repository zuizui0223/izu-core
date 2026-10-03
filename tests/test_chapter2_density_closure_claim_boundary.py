import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
INTEGRATED = ROOT / "docs/CHAPTER2_MANUSCRIPT_INTEGRATED_MODEL3_SYNDROME_20261003.md"
CANONICAL = ROOT / "docs/CHAPTER2_CANONICAL_STORY_INTEGRATED_MODEL3_20261003.md"
AUDIT = ROOT / "data/results/chapter2_bridge_population_scale_diagnostic_20261003.json"


def test_original_dep050_headline_is_not_quasi_extinction():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    d50 = audit["depression_0_50_at_200"]
    assert d50["deterministic_far_density_mass"]["median"] == 48.0
    assert d50["deterministic_far_density_mass"]["below_1_fraction"] == 0.0
    assert d50["finite_far_population_demo_101"]["occupied_fraction"] == 1.0
    assert d50["frozen_all_repeat_context"]["far_occupancy"] == 1.0


def test_dep075_history_labels_are_not_population_repeatability_evidence():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    d75 = audit["depression_0_75_at_200"]
    assert d75["deterministic_far_density_mass"]["below_1_fraction"] > 0.98
    assert d75["finite_far_population_demo_101"]["occupied_fraction"] == 0.0

    integrated = INTEGRATED.read_text(encoding="utf-8").lower()
    assert "retain the depression-0.75 labels only as a mathematical closure sensitivity" in integrated
    assert "not as evidence of non-uniform evolution among persisting populations" in integrated


def test_density_is_never_called_the_stochastic_mean():
    active = ACTIVE.read_text(encoding="utf-8").lower()
    integrated = INTEGRATED.read_text(encoding="utf-8").lower()
    canonical = CANONICAL.read_text(encoding="utf-8").lower()
    assert "conditional deterministic closure, not the stochastic mean of the finite abm" in active
    assert "density layer is a conditional deterministic closure rather than the stochastic mean" in integrated
    assert "not the stochastic mean" in canonical


def test_41pct_gap_closure_is_descriptive_only():
    active = ACTIVE.read_text(encoding="utf-8").lower()
    assert "41.5% of the trait-effect gap" in active
    assert "descriptive only" in active
    assert "not interpreted as convergence to a stochastic expectation" in active
