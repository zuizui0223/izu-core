from pathlib import Path

import pytest

from channel_id.current_evidence_state import render_markdown, summarize_current_evidence

ROOT = Path(__file__).resolve().parents[1]


def test_current_evidence_state_demotes_unreviewed_guide_summary() -> None:
    state = summarize_current_evidence(ROOT)

    assert state.project_stage == (
        "focal_core_calibration_established_guide_reaggregation_required_"
        "independent_holdout_blocked"
    )
    assert state.guide_source_stage == "initial_auto_segmentation_summary"
    assert state.guide_reviewed_reaggregation_status == "not_completed"
    assert state.guide_locked_source_commit == "6343d152a743c240348c736baf5c65768c9b7020"
    assert state.guide_locked_summary_blob_sha == "822fb14d8bb7cc481800d58be503eb9308687304"
    assert state.focal_guide_oshima_mean_pct == pytest.approx(28.39)
    assert state.focal_guide_no_bombus_equal_island_mean_pct == pytest.approx(5.9325)
    assert state.focal_guide_second_transition_delta_pp == pytest.approx(-22.4575)
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
