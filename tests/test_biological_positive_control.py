import csv
from pathlib import Path

from channel_id.biological_positive_control import evaluate_pre_key_gate

ROOT = Path(__file__).resolve().parent.parent
BLIND = ROOT / "data/predictive_meta/campanula_biological_positive_control_blind.csv"


def test_current_campanula_candidate_fails_before_key_join():
    gate = evaluate_pre_key_gate(BLIND)
    assert gate.cards_reviewed == 4
    assert gate.stage0_eligible_cards == 0
    assert gate.scored_cards == 0
    assert gate.pre_key_status == "insufficient_stage0"
    assert gate.regional_key_join_permitted == "no"
    assert gate.eligible_for_roi_selection == "no"
    assert gate.eligible_for_broad_specialist_holdout == "no"


def test_excluded_cards_are_not_interpreted_as_zero_scores(tmp_path):
    path = tmp_path / "blind.csv"
    fields = [
        "card_id", "flowering_state", "focal_flower_visible",
        "interior_visible", "comparable_for_guide_score", "guide_score_0_3",
    ]
    rows = [
        {"card_id": "a", "flowering_state": "open", "focal_flower_visible": "yes", "interior_visible": "no", "comparable_for_guide_score": "no", "guide_score_0_3": ""},
        {"card_id": "b", "flowering_state": "open", "focal_flower_visible": "yes", "interior_visible": "no", "comparable_for_guide_score": "no", "guide_score_0_3": ""},
        {"card_id": "c", "flowering_state": "open", "focal_flower_visible": "yes", "interior_visible": "no", "comparable_for_guide_score": "no", "guide_score_0_3": ""},
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    gate = evaluate_pre_key_gate(path)
    assert gate.scored_cards == 0
    assert gate.distinct_score_levels == 0
