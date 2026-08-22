import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "results" / "abm_v12_heliconia_signed_position_test_frozen.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_source_bytes_and_source_selection_models_are_reconstructed():
    result = load_result()
    assert result["source_audit"]["all_source_byte_locks_pass"] is True
    reconstruction = result["source_model_reconstruction"]
    assert reconstruction["all_12_beta_and_standard_error_pairs_pass"] is True
    assert reconstruction["max_absolute_beta_delta"] < 0.006
    assert reconstruction["max_absolute_standard_error_delta"] < 0.008
    assert result["unit_count"] == 12
    assert result["plant_row_count"] == 281


def test_declared_negative_direction_fails_in_primary_exact_projection():
    result = load_result()
    primary = result["primary_test"]
    assert primary["predeclared_supported_direction"] == "negative"
    assert primary["direction_supported"] is False
    assert math.isclose(primary["slope"], 0.05230812133389483, abs_tol=1e-12)
    assert primary["slope_ci95_naive"][0] < 0 < primary["slope_ci95_naive"][1]
    assert result["decision"] == "heliconia_signed_position_projection_fails_declared_negative_direction"


def test_failure_is_not_rescued_by_declared_sensitivities():
    result = load_result()
    sensitivity = result["secondary_sensitivities"]
    assert sensitivity["inverse_variance_weighted"]["slope"] > 0
    assert sensitivity["univariate_corolla_selection"]["slope"] > 0
    assert sensitivity["sign_concordance"] == {
        "concordant_units": 6,
        "total_units": 12,
        "fraction": 0.5,
    }
    assert sensitivity["leave_one_unit"]["negative_count"] == 1


def test_result_does_not_overclaim_whole_model_falsification():
    result = load_result()
    boundary = result["claim_boundary"]
    assert "not a definitive cross-lineage causal test" in boundary
    assert "does not by itself falsify the synthetic v12 mechanism" in boundary
    assert "not supported" in result["interpretation"]
