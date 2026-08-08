import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "design" / "source_reviewed_occupancy_readiness.json"


def load_readiness():
    return json.loads(READINESS.read_text(encoding="utf-8"))


def test_occupancy_analysis_is_blocked_until_reviewed_multisland_matrix_exists():
    data = load_readiness()
    assert data["status"] == "blocked_missing_multisland_source_reviewed_species_matrix"
    flora = next(source for source in data["candidate_sources"] if source["source_id"] == "sugiyama_izu_flora_4th_1987")
    assert flora["analysis_ready"] is False
    assert "species-by-island contents not recovered" in flora["current_access"]


def test_public_occurrence_zeros_are_not_allowed_as_absence():
    rejected = load_readiness()["explicitly_rejected_shortcuts"]
    assert any("GBIF" in item and "non-detection" in item for item in rejected)
    assert any("iNaturalist" in item and "absence" in item for item in rejected)
    assert any("native establishment" in item for item in rejected)


def test_future_occupancy_layer_remains_separate_from_trait_evolution():
    plan = load_readiness()["planned_analysis_once_open"]
    assert plan["response_domain"] == "source-reviewed establishment/occupancy"
    assert "hybrid replacement" in plan["separate_modes"]
    assert "not within-population floral evolution" in plan["claim_boundary"]
