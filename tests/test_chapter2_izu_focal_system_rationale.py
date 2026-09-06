import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATIONALE = ROOT / "data/design/chapter2_izu_focal_system_rationale_20260906.json"


def test_izu_focal_selection_is_scientific_continuity_not_convenience():
    data = json.loads(RATIONALE.read_text(encoding="utf-8"))
    assert data["selection_timing"] == "after geography-first world-confrontation saturation and small-island supplementation"
    assert "measurement continuity" in data["selection_rule"]
    rejected = " ".join(data["explicitly_not_selection_reasons"]).lower()
    assert "geographic proximity" in rejected
    assert "japan-based accessibility" in rejected
    assert "representative of all islands" in rejected
    assert "strongest positive match" in rejected

    continuity = data["izu_measurement_continuity"]
    assert continuity["same_regional_series"]["status"] == "available"
    assert continuity["historical_focal_lineage_response"]["status"] == "available_but_causally_bounded"
    assert continuity["contemporary_repeated_networks"]["status"] == "available"
    assert continuity["pollinator_functional_traits"]["status"] == "high_coverage_species_level"
    assert continuity["contemporary_functional_chain"]["status"] == "partially_resolved"
    assert continuity["within_lineage_phenotypic_endpoint"]["chapter2_use"].startswith("rationale and downstream handoff only")
    assert continuity["prospective_missing_link"]["status"] == "implementation_ready_field_data_missing"

    assert data["falsification_value"]["signed_position_null_corrected_result_supported"] is False
    assert data["falsification_value"]["oshima_source_sensitivity_supported"] is False
    assert data["chapter_boundary"]["forbidden_chapter2_upgrade"].startswith("do not import Chapter 3 phenotype")
