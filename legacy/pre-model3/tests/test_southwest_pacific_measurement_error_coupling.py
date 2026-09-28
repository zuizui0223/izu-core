import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "swp_measurement_error_coupling",
    ROOT / "scripts" / "audit_southwest_pacific_measurement_error_coupling.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_classical_error_formula_has_expected_threshold():
    observed_lr_slope = -0.15
    coupling = 1.0 + observed_lr_slope
    assert MODULE.corrected_lr_slope(coupling, coupling) == pytest.approx(0.0)
    assert MODULE.corrected_lr_slope(coupling, 0.95) < 0
    assert MODULE.corrected_lr_slope(coupling, 0.80) > 0


def test_invalid_reliability_is_rejected():
    with pytest.raises(ValueError, match="reliability"):
        MODULE.corrected_lr_slope(0.85, 0.0)
    with pytest.raises(ValueError, match="reliability"):
        MODULE.corrected_lr_slope(0.85, 1.01)


def test_current_source_animal_thresholds_are_locked():
    path = ROOT / "data/results/southwest_pacific_pairs/analysis_summary.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    rows, summary = MODULE.analyse(document)
    assert summary["animal_point_negative_reliability_threshold"] == pytest.approx(
        0.8490052881072875
    )
    assert summary["animal_ci_negative_reliability_threshold"] == pytest.approx(
        0.9258005353502381
    )
    assert summary["wind_point_negative_reliability_threshold"] == pytest.approx(
        0.9238856751525703
    )
    assert summary["wind_ci_negative_reliability_threshold"] == pytest.approx(
        1.1163143136258074
    )
    assert summary["effect_registry_eligible"] is False
    assert summary["causal_claim_allowed"] is False

    animal_95 = next(
        row
        for row in rows
        if row["model"] == "animal_source_coded"
        and row["assumed_mainland_log_size_reliability"] == 0.95
    )
    assert animal_95["implied_true_lr_slope"] == pytest.approx(
        -0.1063102230449603
    )
    assert animal_95["implied_true_lr_ci_high"] == pytest.approx(
        -0.025473120683959904
    )
    assert animal_95["interval_entirely_negative"] is True

    animal_925 = next(
        row
        for row in rows
        if row["model"] == "animal_source_coded"
        and row["assumed_mainland_log_size_reliability"] == 0.925
    )
    assert animal_925["implied_true_lr_ci_high"] > 0
    assert animal_925["interval_entirely_negative"] is False


def test_lr_and_log_island_slopes_are_algebraically_linked():
    document = json.loads(
        (ROOT / "data/results/southwest_pacific_pairs/analysis_summary.json").read_text(
            encoding="utf-8"
        )
    )
    result = document["primary_models"]["animal_source_coded"]
    record = MODULE.model_record("animal_source_coded", result)
    assert record["observed_log_island_on_log_mainland_slope"] == pytest.approx(
        1.0 + record["observed_lr_slope"]
    )
