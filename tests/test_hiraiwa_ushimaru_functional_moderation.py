import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERATION = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_functional_moderation.json"
READINESS = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_pollen_target_dependency_readiness.csv"
DESIGN = ROOT / "data" / "design" / "pollen_target_dependency_moderation_readiness.json"


def load_moderation():
    return json.loads(MODERATION.read_text(encoding="utf-8"))


def load_design():
    return json.loads(DESIGN.read_text(encoding="utf-8"))


def test_available_source_native_moderators_are_not_promoted_to_dependency():
    data = load_moderation()
    assert data["direct_dependency_status"] == "insufficient_target_matched_dependency_gradient_for_moderation"
    assert "two available source-native continuous proxies" in data["claim_boundary"]
    rows = list(csv.DictReader(READINESS.open(encoding="utf-8")))
    assert len(rows) == 10
    assert all(row["direct_dependency_moderation_eligible"] == "no" for row in rows)


def test_dependency_readiness_resolves_some_systems_but_not_a_bombus_gradient():
    rows = list(csv.DictReader(READINESS.open(encoding="utf-8")))
    counts = Counter(row["resolution_status"] for row in rows)
    assert counts == {
        "resolved_external_species_level": 4,
        "partial": 3,
        "unresolved": 3,
    }
    resolved = {row["taxon"]: row["effective_pollinator_or_dependency_class"] for row in rows if row["resolution_status"] == "resolved_external_species_level"}
    assert set(resolved) == {
        "Ampelopsis glandulosa var. hancei",
        "Calystegia soldanella",
        "Lonicera japonica",
        "Vitex rotundifolia",
    }
    assert not any("bombus" in value.lower() and "dependent" in value.lower() for value in resolved.values())
    design = load_design()
    assert design["resolved_high_dependency_bombus_targets"] == 0
    assert design["direct_dependency_moderation_eligible"] is False
    assert design["survivor_conditioning"] is True


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


def test_claim_is_noncausal_and_does_not_read_proxy_moderation_as_dependency_test():
    text = load_moderation()["claim_boundary"].lower()
    assert "do not conclude that dependency has no effect" in text
    assert "lacks a resolved high-dependency bombus end of the gradient" in text
    assert "contemporary observational" in text
    assert "historical dependency-by-boundary evolutionary effect" in text
    design = load_design()
    assert "code legacy floral-form or family labels" in design["what_is_not_allowed"]
    assert "interpret unstable proxy moderation as evidence that dependency does not matter" in design["what_is_not_allowed"]
