import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "design" / "source_reviewed_occupancy_readiness.json"


def load_readiness():
    return json.loads(READINESS.read_text(encoding="utf-8"))


def test_modern_occupancy_analysis_is_blocked_until_reviewed_multisland_matrix_exists():
    data = load_readiness()
    assert data["status"] == "blocked_missing_multisland_source_reviewed_species_matrix"
    flora = next(source for source in data["candidate_sources"] if source["source_id"] == "sugiyama_izu_flora_4th_1987")
    assert flora["analysis_ready"] is False
    assert "species-by-island contents" in flora["current_access"]
    assert "not recovered" in flora["current_access"]


def test_historical_external_control_is_ready_without_becoming_modern_occupancy():
    data = load_readiness()
    historical = data["historical_external_control"]
    assert historical["status"] == "ready_as_context_not_occupancy_matrix"
    assert "Miyakejima-Mikurajima" in historical["focal_result"]
    assert "Oshima-Toshima" in historical["focal_result"]
    assert "generic whole-flora phytogeographic boundary" in historical["interpretation"]
    source = next(source for source in data["candidate_sources"] if source["source_id"] == "suzuki_1956_izu_distribution")
    assert source["historical_external_control_ready"] is True
    assert source["analysis_ready"] is False


def test_public_occurrence_zeros_are_not_allowed_as_absence():
    rejected = load_readiness()["explicitly_rejected_shortcuts"]
    assert any("GBIF" in item and "non-detection" in item for item in rejected)
    assert any("iNaturalist" in item and "absence" in item for item in rejected)
    assert any("native establishment" in item for item in rejected)
    assert any("1956" in item and "complete modern" in item for item in rejected)


def test_future_occupancy_layer_remains_separate_from_trait_evolution():
    plan = load_readiness()["planned_analysis_once_open"]
    assert plan["response_domain"] == "source-reviewed establishment/occupancy"
    assert "hybrid replacement" in plan["separate_modes"]
    assert "not within-population floral evolution" in plan["claim_boundary"]
