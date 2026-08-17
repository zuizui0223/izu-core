import json
from pathlib import Path

from scripts.audit_hiraiwa_ushimaru_cross_study_triangulation import build_audit, read_csv

ROOT = Path(__file__).resolve().parents[1]
SENSITIVITY = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_2017_reproductive_sensitivity.csv"
CHANNELS = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_cross_channel_concordance.csv"
RESULT = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_cross_study_triangulation.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def recompute():
    return build_audit(read_csv(SENSITIVITY), read_csv(CHANNELS))


def test_shared_reproductive_sensitivity_panel_has_zero_uniform_three_channel_cascades():
    data = load_result()
    assert data["n_shared_taxa"] == 3
    assert data["shared_taxa"] == [
        "Calystegia soldanella",
        "Lysimachia mauritiana",
        "Vitex rotundifolia",
    ]
    assert data["uniform_matching_tube_pollen_decline_n"] == 0
    assert data["uniform_matching_tube_pollen_decline_taxa"] == []


def test_heterogeneity_recurs_at_dataset_level_but_not_as_same_estimand_replication():
    data = load_result()
    recurrence = data["heterogeneity_recurrence"]
    assert recurrence["study_2017_has_multiple_reproductive_response_modes"] is True
    assert recurrence["study_2024_shared_panel_has_multiple_pollen_directions"] is True
    assert recurrence["study_2024_shared_panel_has_multiple_tube_directions"] is True
    assert recurrence["dataset_level_response_heterogeneity_recurs"] is True
    assert "not species-specific sign replication" in data["claim_boundary"]


def test_recomputed_rows_preserve_expected_cross_study_profiles():
    rows, summary = recompute()
    by_taxon = {row["taxon"]: row for row in rows}
    locked = load_result()["shared_taxon_profiles"]
    for taxon, expected in locked.items():
        observed = by_taxon[taxon]
        assert observed["study_2017_response_mode"] == expected["study_2017_response_mode"]
        assert observed["study_2024_matching_direction"] == expected["study_2024_matching_direction"]
        assert observed["study_2024_tube_direction"] == expected["study_2024_tube_direction"]
        assert observed["study_2024_pollen_direction"] == expected["study_2024_pollen_direction"]
        assert observed["uniform_matching_tube_pollen_decline"] is expected["uniform_matching_tube_pollen_decline"]
    assert summary["uniform_matching_tube_pollen_decline_n"] == 0
    assert summary["heterogeneity_recurrence"]["dataset_level_response_heterogeneity_recurs"] is True


def test_2017_modes_are_context_only_not_numeric_dependency_values():
    data = load_result()
    assert data["study_2017_source"]["oshima_reproductive_data_available"] is False
    assert "cannot be transported as numeric dependency values" in data["mechanistic_implication"]
    assert "2017 lacks Oshima reproductive observations" in data["claim_boundary"]
    assert "historical Bombus causation" in data["claim_boundary"]
