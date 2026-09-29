import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/design/external_bridge_ogasawara_psychotria_source_audit.json"


def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_psychotria_is_partial_bridge_not_complete_or_formal_fit():
    data = load()
    assert data["admission_state"] == "bridge_system_partial"
    assert data["bridge_complete"] is False
    assert data["formal_cross_system_model_eligible"] is False
    assert data["independent_geographic_stratum"] is True


def test_source_construct_is_categorical_access_not_invented_signed_numeric_position():
    data = load()
    construct = data["source_native_construct"]
    assert construct["type"] == "categorical_physical_access_mismatch_not_numeric_signed_trait_position"
    assert construct["numeric_signed_position_available"] is False
    assert "must not be substituted" in construct["why_not_signed_numeric"]


def test_published_hand_and_open_fruit_values_are_preserved():
    data = load()
    table = next(source for source in data["sources"] if source["source_id"] == "watanabe_sugawara_2015_aobplants_table3")
    values = table["published_table_values"]
    assert values["intermorph_hand_fruit_set_percent_L_to_S"] == 82.4
    assert values["intermorph_hand_fruit_set_percent_S_to_L"] == 82.6
    assert values["open_fruit_set_percent_L_range"] == [2.8, 8.9]
    assert values["open_fruit_set_percent_S_range"] == [0.2, 1.4]


def test_effectiveness_link_is_directional_but_not_standardized_single_visit_numeric():
    data = load()
    links = data["measured_links"]
    assert links["categorical_physical_access"] is True
    assert links["directional_pollen_transfer"] is True
    assert links["single_visit_effectiveness_numeric"] is False
    assert links["controlled_all_pollinator_dependency_numeric"] is False
    assert links["same_tagged_individual_full_chain"] is False


def test_gate_admits_partial_bridge_without_claiming_historical_causation():
    data = load()
    assert data["source_gate_decision"] == "admit_article_and_published_table_level_partial_propagation_bridge_numeric_signed_position_still_missing"
    blocked = " ".join(data["blocked_claims"]).lower()
    assert "historical pollinator replacement" in blocked
    assert "numeric signed-position" in blocked
    assert "controlled all-pollinator dependency" in blocked
