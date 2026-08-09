import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERATION = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_functional_moderation.json"
READINESS = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_pollen_target_dependency_readiness.csv"


def load_moderation():
    return json.loads(MODERATION.read_text(encoding="utf-8"))


def test_available_source_native_moderators_are_not_promoted_to_dependency():
    data = load_moderation()
    assert data["direct_dependency_status"] == "unresolved_for_all_10_source_defined_targets"
    assert "not effective pollinator-dependency classes" in data["claim_boundary"]
    rows = list(csv.DictReader(READINESS.open(encoding="utf-8")))
    assert len(rows) == 10
    assert all(row["direct_effective_dependency_resolved"] == "no" for row in rows)
    assert all(row["dependency_moderation_eligible"] == "no" for row in rows)


def test_realized_breadth_interaction_is_not_stable():
    result = load_moderation()["mainland_realized_interaction_breadth"]
    assert abs(result["fdq_x_moderator_coefficient"]) < 0.02
    assert result["interaction_sign_stable_leave_one_site"] is False
    assert result["interaction_sign_stable_leave_one_plant"] is False
    assert result["leave_one_site_interaction_range"][0] < 0 < result["leave_one_site_interaction_range"][1]
    assert result["leave_one_plant_interaction_range"][0] < 0 < result["leave_one_plant_interaction_range"][1]


def test_tube_length_interaction_is_not_stable():
    result = load_moderation()["mainland_corolla_tube_length"]
    assert result["fdq_x_moderator_coefficient"] > 0
    assert result["interaction_sign_stable_leave_one_site"] is False
    assert result["interaction_sign_stable_leave_one_plant"] is False
    assert result["leave_one_site_interaction_range"][0] < 0 < result["leave_one_site_interaction_range"][1]
    assert result["leave_one_plant_interaction_range"][0] < 0 < result["leave_one_plant_interaction_range"][1]


def test_claim_is_noncausal_and_does_not_read_null_moderation_as_no_dependency_effect():
    text = load_moderation()["claim_boundary"].lower()
    assert "do not conclude that dependency has no effect" in text
    assert "contemporary observational" in text
    assert "historical dependency-by-boundary evolutionary effect" in text
