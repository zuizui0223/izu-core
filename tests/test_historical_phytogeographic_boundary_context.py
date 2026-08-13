import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "design" / "historical_phytogeographic_boundary_context.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_historical_floristic_boundary_is_not_oshima_toshima():
    limits = load_data()["source_inferred_floristic_limits"]
    assert limits["southern_elements_northern_limit"] == "Miyakejima"
    assert limits["northern_elements_southern_limit"] == "Mikurajima"
    assert limits["historical_general_phytogeographic_transition_zone"] == "Miyakejima-Mikurajima"
    assert limits["focal_pollinator_second_boundary"] == "Oshima-Toshima"
    assert limits["coincident_with_focal_pollinator_boundary"] is False


def test_historical_source_is_not_promoted_to_modern_occupancy_matrix():
    data = load_data()
    assert data["analysis_role"] == "historical_external_control_for_generic_floristic_boundary"
    assert any("cannot substitute" in item for item in data["limitations"])
    assert any("Taxonomy" in item for item in data["limitations"])
    assert "Do not treat it as a modern occupancy matrix" in data["claim_boundary"]


def test_source_scope_preserves_historical_caveats():
    scope = load_data()["source_scope"]
    assert scope["archipelago_total_taxa_reported"] == 1038
    assert scope["southern_element_taxa_marked"] == 103
    assert scope["northern_element_taxa_marked"] == 43
    assert "some transplanted and naturalized plants remained" in scope["source_caveat"]
    assert "judgement" in scope["source_caveat"]
