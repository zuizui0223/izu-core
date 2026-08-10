import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "design" / "cross_archipelago_external_validation.json"
CONFIG = ROOT / "config" / "wanshan_yongxing_dryad_source.json"


def test_registry_keeps_izu_as_anchor_and_external_systems_as_validation():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["mechanistic_anchor"]["system"] == "Izu Islands"
    assert "within-system" in data["analysis_rule"]
    systems = {row["system_id"]: row for row in data["systems"]}
    assert systems["wanshan_yongxing_2025"]["priority"] == 1
    assert systems["ogasawara_quitian_2026"]["dataset_doi"] == "10.5281/zenodo.19221853"
    assert systems["galapagos_nnakenyi_2019"]["dataset_doi"] == "10.5061/dryad.0c3cn5f"
    assert all(row["direct_dependency_available"] is False for row in systems.values())
    assert "do not retroactively identify" in data["claim_boundary"].lower()


def test_wanshan_config_preserves_one_pair_and_different_year_boundary():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert data["expected_shared_plant_count"] == 7
    assert len(data["sheet_roles"]) == 4
    assert data["source_reported_site_context"]["Wanshan"]["distance_to_source_km"] == 40
    assert data["source_reported_site_context"]["Yongxing"]["distance_to_source_km"] == 350
    boundary = data["claim_boundary"].lower()
    assert "different years" in boundary
    assert "not fdq" in boundary
    assert "effective pollinator dependency" in boundary
