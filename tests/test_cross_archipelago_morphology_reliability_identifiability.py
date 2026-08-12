import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/cross_archipelago_morphology_reliability_identifiability.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_completed_eiv_envelope_is_not_misrepresented_as_empirical_reliability():
    result = load_result()
    consequence = result["formal_consequence"]
    assert consequence["classical_EIV_envelope_complete"] is True
    assert consequence["empirical_reliability_gate_complete"] is False
    assert consequence["effect_registry_eligible"] is False
    assert result["completed_sensitivity_result"]["these_are_estimated_reliabilities"] is False


def test_southwest_pacific_trait_ranges_do_not_satisfy_reliability_gate():
    swp = result = load_result()["systems"]["southwest_pacific_ciarle_2025_animal"]
    structure = swp["source_native_structure"]
    assert structure["flower_dataframe_has_pair_level_FM_mean"] is True
    assert structure["flower_dataframe_has_replicate_n_for_FM"] is False
    assert structure["flower_dataframe_has_sd_or_se_for_FM"] is False
    assert structure["flower_dataframe_has_repeat_measurement_identifier_for_FM"] is False
    assert structure["island_mainland_pairs_table_has_trait_min_max"] is True
    assert structure["trait_min_max_is_valid_reliability_replication"] is False
    assert swp["identifiability"] == "blocked"


def test_hendriks_pair_means_do_not_identify_predictor_reliability():
    hendriks = load_result()["systems"]["new_zealand_hendriks_2019"]
    structure = hendriks["source_native_structure"]
    assert structure["appendix_has_pair_level_mainland_values"] is True
    assert structure["appendix_has_replicate_n_for_mainland_flower_area"] is False
    assert structure["appendix_has_sd_or_se_for_mainland_flower_area"] is False
    assert structure["appendix_has_repeat_measurement_identifier_for_mainland_flower_area"] is False
    assert hendriks["identifiability"] == "blocked"
