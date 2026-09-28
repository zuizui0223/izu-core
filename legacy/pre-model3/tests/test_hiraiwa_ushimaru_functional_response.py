import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_functional_response_summary.json"
CONTRASTS = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_functional_response.csv"


def load_summary():
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


def load_rows():
    with CONTRASTS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_all_network_plants_do_not_show_universal_trait_matching_step():
    summary = load_summary()["all_network_plants"]["corrected_trait_matching"]
    assert summary == {"eligible": 16, "lower_post": 10, "higher_post": 6, "equal": 0}
    assert load_summary()["all_network_plants"]["shared_second_step_reading"] == "heterogeneous_not_universal"


def test_source_defined_pollen_targets_have_coherent_trait_matching_but_mixed_other_channels():
    summary = load_summary()["pollen_success_target_plants"]
    assert summary["corrected_trait_matching"] == {"eligible": 8, "lower_post": 8, "higher_post": 0, "equal": 0}
    assert summary["functional_generality"] == {"eligible": 8, "lower_post": 3, "higher_post": 5, "equal": 0}
    assert summary["pollen_receipt"] == {"eligible": 9, "lower_post": 5, "higher_post": 4, "equal": 0}


def test_campanula_contemporary_network_channels_do_not_mimic_autonomous_step():
    rows = {(row["plant"], row["response_domain"]): row for row in load_rows()}
    assert float(rows[("Campanula microdonta", "functional_generality")]["second_delta_post_minus_oshima"]) > 0
    assert float(rows[("Campanula microdonta", "corrected_trait_matching")]["second_delta_post_minus_oshima"]) > 0
    assert "not floral evolution" in rows[("Campanula microdonta", "corrected_trait_matching")]["claim_boundary"]


def test_farfugium_separates_interaction_breadth_matching_and_pollen_function():
    rows = {(row["plant"], row["response_domain"]): row for row in load_rows()}
    fg = float(rows[("Farfugium japonicum", "functional_generality")]["second_delta_post_minus_oshima"])
    tm = float(rows[("Farfugium japonicum", "corrected_trait_matching")]["second_delta_post_minus_oshima"])
    pollen = float(rows[("Farfugium japonicum", "pollen_receipt")]["second_delta_post_minus_oshima"])
    assert abs(fg) < 0.01
    assert tm < -2.0
    assert pollen < -0.5


def test_source_defined_subset_is_not_silently_generalized_to_all_plants():
    summary = load_summary()
    assert summary["all_network_plants"]["corrected_trait_matching"]["higher_post"] == 6
    assert summary["pollen_success_target_plants"]["corrected_trait_matching"]["higher_post"] == 0
    assert "Species share the same site-level environments" in summary["claim_boundary"]
