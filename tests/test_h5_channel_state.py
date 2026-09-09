from __future__ import annotations

import pytest

from channel_id.h5_channel_state import audit_channel_state_rows, classify_channel_state


def _row(**overrides: str) -> dict[str, str]:
    row = {
        "island_id": "Oshima",
        "site_id": "site1",
        "field_event_id": "event1",
        "channel_id": "large_bumblebee_pollination_channel",
        "survey_method": "standardized_transect",
        "survey_effort_hours": "4",
        "independent_channel_detections": "2",
        "detection_model_id": "occ_v1",
        "estimated_detection_probability_if_present": "0.98",
        "source_state": "available",
        "source_evidence_id": "inoue_source_lock",
        "notes": "",
    }
    row.update(overrides)
    return row


def test_positive_independent_detection_is_retained() -> None:
    state, basis = classify_channel_state(_row())
    assert state == "retained"
    assert basis == "independent_detection"


def test_high_power_zero_detection_is_disrupted() -> None:
    state, basis = classify_channel_state(
        _row(independent_channel_detections="0", estimated_detection_probability_if_present="0.97")
    )
    assert state == "disrupted"
    assert basis == "adequate_independent_non_detection"


def test_low_power_zero_detection_stays_unresolved() -> None:
    state, basis = classify_channel_state(
        _row(independent_channel_detections="0", estimated_detection_probability_if_present="0.80")
    )
    assert state == "unresolved"
    assert basis == "non_detection_below_detection_probability_gate"


def test_structural_absence_is_not_loss() -> None:
    state, basis = classify_channel_state(
        _row(
            source_state="structurally_absent",
            independent_channel_detections="0",
            estimated_detection_probability_if_present="1.0",
        )
    )
    assert state == "structurally_absent"
    assert basis == "source_channel_not_available"


def test_resolved_source_requires_provenance() -> None:
    with pytest.raises(ValueError, match="source_evidence_id"):
        classify_channel_state(_row(source_evidence_id=""))


def test_summary_opens_retained_disrupted_contrast_only_when_both_exist() -> None:
    retained = _row(island_id="Oshima", field_event_id="e1")
    disrupted = _row(
        island_id="Kozushima",
        field_event_id="e2",
        independent_channel_detections="0",
        estimated_detection_probability_if_present="0.99",
    )
    audit = audit_channel_state_rows([retained, disrupted])
    assert audit.summary["counts"]["retained"] == 1
    assert audit.summary["counts"]["disrupted"] == 1
    assert audit.summary["retained_disrupted_contrast_present"] is True


def test_duplicate_survey_unit_fails_closed() -> None:
    row = _row()
    with pytest.raises(ValueError, match="duplicate"):
        audit_channel_state_rows([row, dict(row)])
