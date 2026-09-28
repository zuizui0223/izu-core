import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/design/issue91_propagation_buffering_prediction_freeze.json"
READINESS = ROOT / "data/design/effective_pollinator_dependency_field_readiness.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def model(model_id):
    return next(row for row in load(FREEZE)["predeclared_candidate_models"] if row["id"] == model_id)


def test_freeze_precedes_real_issue91_field_outcomes():
    data = load(FREEZE)
    inspected = data["inputs_inspected_before_freeze"]
    assert inspected["real_issue91_field_rows"] is False
    assert inspected["pilot_dispersion"] is False
    assert inspected["future_open_bagged_supplemental_outcomes"] is False
    assert inspected["future_svd_values"] is False
    assert inspected["future_fdq_values"] is False
    assert data["status"] == "prediction_structure_frozen_before_real_field_bundle_no_decision_thresholds_locked"


def test_prediction_freeze_reuses_existing_field_estimands_and_plant_replication_unit():
    data = load(FREEZE)
    estimands = data["existing_estimands_only"]
    readiness = load(READINESS)
    assert estimands["independent_unit"] == readiness["precision_planning"]["independent_unit"] == "plant"
    assert set(estimands["within_plant_subsamples"]) == set(readiness["precision_planning"]["within_plant_subsamples"])
    assert "bagged_autonomous" in estimands["autonomous_ratio"]
    assert "supplemental_outcross" in estimands["autonomous_ratio"]
    assert "open_pollinated" in estimands["open_ratio"]
    assert estimands["direct_dependency_target"] == "direct_reproductive_dependency_0_1 from the existing field/reliability contract"


def test_service_and_visit_rate_are_not_collapsed():
    m1 = model("M1_service_propagation_dependency_filter")
    assert "visit rate alone may disagree with effective service" in m1["expected_signature"][-1]
    m3 = model("M3_network_service_allocation")
    assert "visit rate" in m3["distinguishing_measurements"]
    assert "background-adjusted SVD" in m3["distinguishing_measurements"]
    assert "rate-weighted effective service" in m3["distinguishing_measurements"]


def test_non_assurance_buffer_is_not_given_an_unmeasured_cause():
    m4 = model("M4_non_assurance_buffer")
    assert "do not assign resource compensation" in m4["interpretation_if_seen"]
    table = load(FREEZE)["predeclared_interpretation_table"]
    row = next(item for item in table if item["primary_interpretation"] == "non_assurance_buffer_or_unmeasured_filter_candidate")
    assert "do not label the missing mechanism" in row["forbidden_overclaim"]


def test_fdq_has_no_predeclared_universal_reproductive_sign():
    m5 = model("M5_functional_exposure_is_upstream_not_effectiveness")
    assert "without a predetermined universal sign for open_ratio" in m5["expected_signature"][1]
    assert "dropping unresolved or missing-trait visitors" in m5["would_be_invalidated_by_analysis_error"]


def test_pilot_is_not_allowed_to_decide_causation_or_final_reliability():
    boundary = load(FREEZE)["pilot_vs_confirmatory_boundary"]
    assert boundary["decision_thresholds_locked_now"] is False
    forbidden = " ".join(boundary["ordinary_pilot_may_not_do"]).lower()
    assert "declare a causal mechanism" in forbidden
    assert "final dependency reliability" in forbidden
    assert "cross-lineage dependency x fdq" in forbidden


def test_no_numeric_decision_threshold_is_locked_before_pilot_dispersion():
    data = load(FREEZE)
    boundary = data["pilot_vs_confirmatory_boundary"]
    assert boundary["decision_thresholds_locked_now"] is False
    assert data["inputs_inspected_before_freeze"]["pilot_dispersion"] is False
    assert data["next_gate"].startswith("collect the first real linked Issue #91 Campanula bundle")
    assert "only then lock precision thresholds" in data["next_gate"]


def test_historical_izu_pattern_cannot_be_used_for_tuning():
    rules = " ".join(load(FREEZE)["anti_leakage_rules"]).lower()
    assert "8/8" in rules
    assert "4/4" in rules
    assert "do not tune" in rules
    assert "scientific null/adverse result" in rules
