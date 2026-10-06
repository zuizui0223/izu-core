import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_assurance_generality_20261006.json"


def test_four_setting_generality_result_is_complete_and_passed():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "complete_generality_readout"
    assert result["declared_cases"] == 8448
    assert result["independent_visitor_histories"] == 64
    assert result["nested_demographic_repeats"] == 8
    assert result["structural_control"]["status"] == "passed"
    assert result["structural_control"]["mismatches"] == []
    assert result["adjudication"]["status"] == "all_four_confirmed"
    assert result["adjudication"]["n_passed"] == 4
    assert set(result["adjudication"]["passed_settings"]) == {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    }


def test_every_setting_passes_frozen_nonnecessity_and_attenuation_rule():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    for row in result["settings"]:
        assert row["admissible"] is True
        assert row["eligible_histories_fixed_pair"] == 64
        assert row["eligible_histories_four_cell"] == 64
        assert row["passes_frozen_rule"] is True
        assert row["fixed_far_minus_near"]["mean"] < 0
        assert row["fixed_far_minus_near"]["bootstrap95"][1] < 0
        assert row["attenuation_evolving_minus_fixed"]["mean"] > 0
        assert row["attenuation_evolving_minus_fixed"]["bootstrap95"][0] > 0
        for mode in ("fixed", "evolving"):
            assert row["occupancy"][mode]["near"] == 1.0
            assert row["occupancy"][mode]["far"] == 1.0


def test_result_retains_claim_boundaries_and_workflow_provenance():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    boundary = result["claim_boundary"]["claim_boundary"]
    assert "not a mediation fraction" in boundary
    assert "does not establish an empirical flower-size causal effect" in boundary
    provenance = result["workflow_provenance"]
    assert provenance["run_id"] == 37458098483
    assert provenance["artifact_id"] == 11411525163
    assert provenance["artifact_sha256"] == "34bedf03e6cde0b3d7f5140b7f352227b5dd1550c097e66e42022aa9830d3d8c"
