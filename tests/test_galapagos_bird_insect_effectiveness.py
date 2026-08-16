import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/galapagos_bird_insect_effectiveness_summary.json"
CONFIG = ROOT / "config/galapagos_bird_insect_effectiveness_figshare_source.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_workbook_is_locked():
    src = load(CONFIG)["expected_source_file"]
    assert src["bytes"] == 775168
    assert src["sha256"] == "0c5af09a0744e94777ed3c9ae9bf7dde364f5b54da31b46a68399f053fbb7d8a"
    assert src["figshare_file_id"] == 11089004


def test_scale_preserves_quantity_and_fitness_units():
    assert load(RESULT)["scale"] == {
        "census_species": 4,
        "census_rows": 693,
        "fitness_species_with_nonempty_raw_sheet": 3,
        "fitness_raw_rows": 2601,
        "id_treatment_units": 102,
    }


def test_cordia_fitness_missingness_is_not_reconstructed():
    result = load(RESULT)
    assert set(result["quantitative_component_by_plant"]) == {"Cordia lutea", "Cryptocarpus pyriformis", "Opuntia echios", "Waltheria ovata"}
    assert "C. lutea" not in result["qualitative_component_by_raw_treatment_code"]
    assert "empty C. lutea sheet" in result["missing_raw_fitness_sheet"]["Cordia lutea"]


def test_visitor_quantity_and_fitness_treatments_remain_separate():
    result = load(RESULT)
    cp = result["quantitative_component_by_plant"]["Cryptocarpus pyriformis"]["by_class"]
    assert cp["Insecta"]["mean_FVR"] > cp["Birds"]["mean_FVR"]
    assert result["qualitative_component_by_raw_treatment_code"]["O. echios"]["n_id_treatment_units"] == 42
    assert "opaque labels" in result["treatment_code_boundary"]


def test_claim_boundary_blocks_pseudoreplication_and_historical_causation():
    boundary = load(RESULT)["claim_boundary"]
    assert "not four independent archipelagos" in boundary
    assert "do not identify historical floral evolution" in boundary
