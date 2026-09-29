import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "results" / "seychelles_pollination_effectiveness_summary.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_seychelles_expands_real_data_scale_without_fake_independence():
    data = load_data()
    assert data["scale"] == {
        "plant_species": 3,
        "source_csv_files": 9,
        "raw_rows": 2292,
        "visual_census_hours": 174.83333333333331,
        "single_visit_exclusion_rows": 489,
        "breeding_treatment_rows": 557,
    }
    assert "not independent archipelagos" in data["claim_boundary"]


def test_ant_disturbance_is_associated_with_lower_non_ant_visitation_in_two_plants():
    plants = load_data()["plants"]
    assert plants["Polyscias crassa"]["ant_disturbed_to_undisturbed_non_ant_visit_rate_ratio"] < 0.5
    assert plants["Syzygium wrightii"]["ant_disturbed_to_undisturbed_non_ant_visit_rate_ratio"] < 0.5


def test_single_visit_outcomes_are_plant_and_visitor_specific():
    plants = load_data()["plants"]
    p = plants["Polyscias crassa"]["single_visit_mature_fruit"]
    assert p["Phelsuma"]["proportion"] > p["Sunbird"]["proportion"]
    t = plants["Thespesia populnea"]["single_visit_recorded_fruit"]
    assert t["Insects"]["proportion"] > t["Birds"]["proportion"] > t["Reptiles"]["proportion"]
    assert plants["Polyscias crassa"]["published_overall_effectiveness_headline"] != plants["Syzygium wrightii"]["published_overall_effectiveness_headline"]
    assert plants["Syzygium wrightii"]["published_overall_effectiveness_headline"] != plants["Thespesia populnea"]["published_overall_effectiveness_headline"]


def test_source_labeled_auto_treatments_are_not_promoted_to_izu_dependency():
    plants = load_data()["plants"]
    assert plants["Polyscias crassa"]["source_labeled_auto_treatment_present"] is False
    assert plants["Syzygium wrightii"]["source_labeled_auto_treatment"]["n"] == 56
    assert plants["Thespesia populnea"]["source_labeled_auto_treatment"]["n"] == 39
    assert "not automatically treated as transportable Izu direct-dependency estimates" in load_data()["claim_boundary"]


def test_source_bytes_are_locked_for_all_nine_csvs():
    hashes = load_data()["source_file_sha256"]
    assert len(hashes) == 9
    assert all(len(value) == 64 for value in hashes.values())
