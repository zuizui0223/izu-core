import json
from pathlib import Path


def load_search():
    return json.loads(
        Path("data/design/external_bridge_cordia_dong_followup_search.json")
        .read_text(encoding="utf-8")
    )


def test_dong_followup_search_does_not_complete_the_bridge():
    record = load_search()
    assert record["status"] == "targeted_public_followup_no_dong_direct_effectiveness_or_dependency_recovered"
    assert record["bridge_admission_change"] is False
    assert record["bridge_system_complete"] is False
    assert record["formal_cross_system_model_eligible"] is False


def test_source_gap_is_not_promoted_to_data_nonexistence():
    record = load_search()
    assert record["not_a_nonexistence_claim"] is True
    assert "does not show" in record["claim_boundary"]


def test_dong_reopen_requires_direct_missing_channel_evidence():
    record = load_search()
    text = " ".join(record["reopen_conditions"])
    assert "Dong single-visit pollen-function data" in text
    assert "Dong controlled bagging/hand-pollination data" in text
