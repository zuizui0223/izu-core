import json
from pathlib import Path

from scripts.audit_buffer_candidate_portfolio import build


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/buffer_candidate_portfolio_admission_frozen.json"
PORTFOLIO = ROOT / "data/design/buffer_candidate_portfolio.json"
GUAIACUM = ROOT / "data/design/buffer_candidate_guaiacum_service_redundancy.json"


def test_current_buffer_candidate_portfolio_matches_frozen_result():
    generated = build()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    for key in ("schema_version", "analysis", "interface", "candidates", "summary", "decision"):
        assert generated[key] == frozen[key]


def test_only_demonstrated_buffer_candidates_remain_in_portfolio():
    result = build()
    assert result["summary"]["candidate_count"] == 2
    assert result["summary"]["mapping_ready_count"] == 0
    assert result["summary"]["empirically_admitted_count"] == 0
    assert result["summary"]["state_counts"] == {"candidate_only_no_abm_admission": 2}
    ids = {row["system_id"] for row in result["candidates"]}
    assert ids == {
        "hawaii_lobelioid_post_extinction_pollination_2026",
        "california_channel_islands_nicotiana_glauca",
    }


def test_two_remaining_candidates_share_matched_transition_and_mapping_gaps():
    result = build()
    missing = result["summary"]["missing_prerequisite_counts"]
    assert missing == {
        "mapping_frozen_before_target_outcome_test": 2,
        "mapping_to_abm_component_predeclared": 2,
        "matched_transition_or_prospectively_matched_units": 2,
    }


def test_guaiacum_is_retired_from_buffer_portfolio_but_retained_as_network_mapping_reference():
    portfolio = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    guaiacum = json.loads(GUAIACUM.read_text(encoding="utf-8"))
    assert "data/design/buffer_candidate_guaiacum_service_redundancy.json" not in portfolio["candidates"]
    assert portfolio["network_context_mapping_references"] == ["puerto_rico_mona_guaiacum"]
    assert guaiacum["retired_from_buffer_portfolio"] is True
    assert guaiacum["current_role"] == "network_context_service_mapping_reference"
    assert "not evidence that whole reproductive performance was buffered" in guaiacum["evidence_scope"]
