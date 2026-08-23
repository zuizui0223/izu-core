import json
from pathlib import Path

from scripts.audit_buffer_candidate_portfolio import build


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/buffer_candidate_portfolio_admission_frozen.json"


def test_current_buffer_candidate_portfolio_matches_frozen_result():
    generated = build()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert generated == frozen


def test_no_current_buffer_candidate_is_mapping_ready():
    result = build()
    assert result["summary"]["candidate_count"] == 3
    assert result["summary"]["mapping_ready_count"] == 0
    assert result["summary"]["empirically_admitted_count"] == 0
    assert result["summary"]["state_counts"] == {"candidate_only_no_abm_admission": 3}


def test_portfolio_exposes_different_missing_links_instead_of_one_generic_gap():
    result = build()
    missing = result["summary"]["missing_prerequisite_counts"]
    assert missing["matched_transition_or_prospectively_matched_units"] == 2
    assert missing["propagation_step_directly_measured"] == 1
    assert missing["candidate_filter_directly_measured"] == 1
    assert missing["mapping_to_abm_component_predeclared"] == 3
    assert missing["mapping_frozen_before_target_outcome_test"] == 3
