import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/canary_lotus_effectiveness_summary.json"
CONFIG = ROOT / "config/canary_lotus_effectiveness_figshare_source.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_workbook_is_locked():
    source = load(CONFIG)["expected_source_file"]
    assert source["figshare_file_id"] == 45510765
    assert source["bytes"] == 17784
    assert source["sha256"] == "b0d99b066e78618301322f33aa899671465304043f76a790c27cc31bab9706d8"


def test_exclusion_is_direct_strong_dependency_evidence():
    result = load(RESULT)
    assert result["scale"]["exclusion_flower_rows"] == 120
    assert result["scale"]["exclusion_plants"] == 20
    control = result["visitor_exclusion"]["by_treatment"]["Control"]
    excluded = result["visitor_exclusion"]["by_treatment"]["Exclusion"]
    assert control["fruits"] == 46 and control["n_flower_rows"] == 60
    assert excluded["fruits"] == 1 and excluded["n_flower_rows"] == 60
    assert result["visitor_exclusion"]["exclusion_to_control_fruit_set_ratio"] < 0.03


def test_lizard_handling_and_pollen_transport_are_directly_observed():
    result = load(RESULT)
    gallotia = result["visit_legitimacy"]["Gallotia galloti"]
    assert gallotia == {"legitimate": 183, "illegitimate": 0, "total": 183, "legitimate_fraction": 1.0}
    pollen = result["lizard_pollen_load"]
    assert pollen["n_lizards"] == 34
    assert pollen["positive_pollen_load"] == 18
    assert pollen["total_pollen_grains"] == 3244


def test_visitor_identity_does_not_equal_effectiveness():
    result = load(RESULT)
    assert result["visit_legitimacy"]["Apis mellifera"]["total"] > result["visit_legitimacy"]["Gallotia galloti"]["total"]
    assert result["visit_legitimacy"]["Apis mellifera"]["legitimate_fraction"] < 0.01
    associations = result["plant_level_visitation_and_reproduction"]["visit_association"]
    assert associations["Gallotia galloti"]["pearson_with_plant_fruit_set"] > associations["Lasioglossum arctifrons"]["pearson_with_plant_fruit_set"]
    assert associations["Gallotia galloti"]["pearson_with_plant_fruit_set"] > 0.6


def test_claim_boundary_blocks_historical_and_transport_overclaim():
    result = load(RESULT)
    assert "does not establish historical floral evolution" in result["claim_boundary"]
    assert "doescriptive" not in result["claim_boundary"]
    assert "descriptive" in result["analysis_boundary"]
