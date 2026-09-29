import json
from pathlib import Path

from scripts.apply_southwest_pacific_effect_admission_gate import apply_admission_gate

ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "data/results/southwest_pacific_pairs"
STARTING_IDS = {
    "southwest_pacific_animal_flower_size_starting_value_slope",
    "southwest_pacific_wind_flower_size_starting_value_slope",
}
DISPLAY_ID = "southwest_pacific_animal_floral_display_mean_log_ratio"


def test_checked_effect_rows_match_coupling_gate():
    effect_document = json.loads((RESULT_DIR / "effect_rows.json").read_text(encoding="utf-8"))
    coupling_summary = json.loads(
        (RESULT_DIR / "measurement_error_coupling_sensitivity_summary.json").read_text(encoding="utf-8")
    )
    assert apply_admission_gate(effect_document, coupling_summary) == effect_document

    by_id = {row["effect_id"]: row for row in effect_document["effects"]}
    assert all(by_id[effect_id]["cross_system_model_eligible"] is False for effect_id in STARTING_IDS)
    assert by_id[DISPLAY_ID]["cross_system_model_eligible"] is True


def test_gate_blocks_only_denominator_coupled_starting_size_rows():
    effects = [
        {"effect_id": effect_id, "cross_system_model_eligible": True, "admission_status": "candidate"}
        for effect_id in sorted(STARTING_IDS)
    ]
    effects.append({"effect_id": DISPLAY_ID, "cross_system_model_eligible": True, "admission_status": "candidate"})
    coupling = {
        "status": "classical_measurement_error_coupling_sensitivity_complete",
        "reliability_is_empirically_estimated_here": False,
        "effect_registry_eligible": False,
        "animal_point_negative_reliability_threshold": 0.849,
        "animal_ci_negative_reliability_threshold": 0.926,
        "claim_boundary": "partial-identification sensitivity",
    }
    gated = apply_admission_gate({"effects": effects}, coupling)
    by_id = {row["effect_id"]: row for row in gated["effects"]}
    assert all(by_id[effect_id]["cross_system_model_eligible"] is False for effect_id in STARTING_IDS)
    assert by_id[DISPLAY_ID]["cross_system_model_eligible"] is True
    assert gated["admission_gate"]["starting_size_effects_model_eligible"] is False
