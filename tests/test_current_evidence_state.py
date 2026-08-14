from pathlib import Path

from channel_id.current_evidence_state import render_markdown, summarize_current_evidence

ROOT = Path(__file__).resolve().parents[1]


def test_current_evidence_state_keeps_focal_contract_and_reads_current_gates() -> None:
    state = summarize_current_evidence(ROOT)

    assert state.project_stage == (
        "focal_three_channel_calibration_established_independent_holdout_blocked"
    )
    assert state.focal_channel_shapes == (
        ("autonomous_assurance", "source_locked", "second_transition_step"),
        ("floral_size", "source_locked", "continuous_erosion"),
        ("outcrossing", "source_locked", "continuous_erosion"),
    )
    assert state.excluded_future_channels == (
        ("visible_signal", "blocked_unmeasured", "prospective_only"),
    )
    assert state.quantitative_effect_count == 0
    assert state.positive_specialist_holdout_lineages == 0
    assert state.usable_generalist_negative_control_lineages == 1
    assert state.roi_proposals_eligible_for_specialist_holdout == 0

    assert state.direct_dependency_field_status == "implementation_ready_field_data_missing"
    assert state.external_partial_bridge_systems == 3
    assert state.external_near_complete_systems == 1
    assert state.external_complete_bridge_systems == 0
    assert state.formal_cross_system_mechanism_fit_ready is False

    assert state.primary_source_access_state == "blocked_external_source_delivery"
    assert state.source_triggered_primary_source_ids == (
        "hosta_yamada_2014",
        "ligustrum_yamada_2014",
        "weigela_yamada_2010",
    )
    assert state.source_triggered_primary_source_taxa == (
        "Hosta longipes",
        "Ligustrum ovalifolium",
        "Weigela coraeensis",
    )


def test_current_evidence_next_work_starts_with_issue_91_not_exhausted_source_search() -> None:
    state = summarize_current_evidence(ROOT)
    assert state.next_actions[0].startswith("Issue #91:")
    assert "first real linked Campanula field bundle" in state.next_actions[0]
    assert any("source-triggered reopen gates" in action for action in state.next_actions)
    assert not state.next_actions[0].startswith("Recover and source-lock")


def test_committed_current_state_document_is_generated_from_tables() -> None:
    state = summarize_current_evidence(ROOT)
    expected = render_markdown(state)
    actual = (ROOT / "docs" / "CURRENT_EVIDENCE_STATE.md").read_text(
        encoding="utf-8"
    )
    assert actual == expected
