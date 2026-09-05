import json
from pathlib import Path

from scripts.audit_chapter2_manuscript_value_promotion_review import build_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_manuscript_value_promotion_review_audit_20260905.json"
DOC = ROOT / "docs/CHAPTER2_MANUSCRIPT_VALUE_PROMOTION_REVIEW_20260905.md"


def test_promotion_review_matches_deterministic_audit():
    computed = build_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["review_precondition"]["systematic_search_targets"] == 111
    assert computed["review_precondition"]["source_work_queue"] == 0
    assert computed["review_precondition"]["source_review_complete_under_current_protocol"] is True
    assert computed["candidate_review"]["reviewed_candidates"] == 29
    assert computed["candidate_review"]["full_chapter2_contract_passes"] == 0


def test_promotion_shortlist_is_small_clean_and_high_value():
    payload = build_audit()
    review = payload["candidate_review"]
    assert review["decision_counts"] == {
        "do_not_promote": 1,
        "hold_overlap": 3,
        "promote_next_integration": 3,
        "retain_si_only": 22,
    }
    assert review["falsification_value_counts"] == {"high": 6, "low": 3, "medium": 20}
    assert set(review["promote_next_integration_ids"]) == {
        "wave5_crete",
        "wave5_iceland",
        "wave5_trinidad_tobago",
    }
    assert set(review["promote_next_integration_targets"]) == {
        "Crete",
        "Iceland",
        "Trinidad and Tobago",
    }


def test_review_does_not_silently_change_active_manuscript_counts_or_prediction_gate():
    payload = build_audit()
    boundary = payload["active_manuscript_boundary"]
    assert boundary["source_backed_research_entries_before_integration"] == 39
    assert boundary["exact_geographic_labels_before_integration"] == 34
    assert boundary["changed_by_review_only"] is False
    assert boundary["formal_external_prediction"] == "not_evaluable"
    assert boundary["frozen_full_contracts"] == "0_of_25"


def test_documentation_states_selection_and_future_counts_without_reopening_frozen_audit():
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "29 source-resolved" in lower
    assert "crete" in lower
    assert "trinidad and tobago" in lower
    assert "iceland" in lower
    assert "39 source-backed research entries" in lower
    assert "34 exact geographic labels" in lower
    assert "0/25" in lower
    assert "not_evaluable" in lower
    assert "post-freeze breadth entries: **17**" in lower
    assert "combined descriptive research entries before cross-layer de-duplication: **42**" in lower
