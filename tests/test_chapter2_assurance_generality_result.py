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


ARM_RESULT = ROOT / "data/results/chapter2_assurance_attenuation_decomposition_20261006.json"


def test_attenuation_decomposition_localizes_the_interaction_in_all_four_settings():
    result = json.loads(ARM_RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "complete_arm_decomposition"
    assert result["source_cases_verified"] == 8448
    assert result["independent_visitor_histories"] == 64
    assert {row["setting"] for row in result["settings"]} == {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    }

    for row in result["settings"]:
        assert row["common_four_cell_histories"] == 64
        assert row["common_replicates_per_history_min"] == 8
        assert row["common_replicates_per_history_max"] == 8
        assert row["max_attenuation_identity_error"] < 1e-12
        est = row["estimates"]
        near = est["evolution_effect_near"]
        far = est["evolution_effect_far"]
        attenuation = est["attenuation"]
        assert near["mean"] < 0
        assert near["bootstrap95"][1] < 0
        assert far["mean"] > 0
        assert far["bootstrap95"][0] > 0
        assert abs((far["mean"] - near["mean"]) - attenuation["mean"]) < 1e-12
        assert row["localization"] == "near_decline_plus_far_relief"


def test_attenuation_decomposition_retains_source_provenance():
    result = json.loads(ARM_RESULT.read_text(encoding="utf-8"))
    provenance = result["workflow_provenance"]
    assert provenance["run_id"] == 37460223485
    assert provenance["job_id"] == 112257683838
    assert provenance["artifact_id"] == 11412296873
    assert provenance["artifact_sha256"] == (
        "4d9f3f017149218d17ba643734c28345daa1aef40119a5cfee0743e8a3669323"
    )
