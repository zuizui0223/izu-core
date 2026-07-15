from pathlib import Path

from channel_id.current_evidence_state import render_markdown, summarize_current_evidence

ROOT = Path(__file__).resolve().parents[1]


def test_current_evidence_state_excludes_unfinished_guide_channel() -> None:
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
    assert state.unresolved_primary_source_ids == (
        "ligustrum_yamada_2014",
        "weigela_yamada_2010",
    )


def test_committed_current_state_document_is_generated_from_tables() -> None:
    state = summarize_current_evidence(ROOT)
    expected = render_markdown(state)
    actual = (ROOT / "docs" / "CURRENT_EVIDENCE_STATE.md").read_text(
        encoding="utf-8"
    )
    assert actual == expected
