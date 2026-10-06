import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_1005_confirmatory_replication_20261006.json"
DESIGN = ROOT / "data/design/chapter2_1005_confirmatory_replication_20261006.json"


def test_confirmatory_result_passes_frozen_primary_rules():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "confirmed"
    assert result["declared_cases"] == 4096
    assert result["independent_visitor_histories"] == 64
    assert result["nested_demographic_repeats"] == 8
    assert result["adjudication"] == {
        "status": "confirmed",
        "sequence_success": True,
        "fixed_assurance_success": True,
    }

    seq = result["primary_sequence"]
    assert seq["counts"] == {"assurance_first": 51, "near_simultaneous": 13}
    assert seq["assurance_first_proportion_all_histories"] == 0.796875
    assert seq["assurance_first_bootstrap95"][0] > 0.5

    fixed = result["fixed_assurance"][0]
    assert fixed["setting"] == "assurance_cost"
    assert fixed["admissible"] is True
    assert fixed["occupancy"] == {"near": 1.0, "far": 1.0}
    assert fixed["eligible_histories_far"] == 64
    assert fixed["eligible_histories_paired"] == 64
    assert fixed["far_investment_change"]["mean"] < 0
    assert fixed["far_investment_change"]["bootstrap95"][1] < 0
    assert fixed["far_minus_near_investment"]["mean"] < 0
    assert fixed["far_minus_near_investment"]["bootstrap95"][1] < 0


def test_sequence_generalization_boundary_is_preserved():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows = {
        (row["setting"], row["mutation_rate"], row["threshold"]): row
        for row in result["threshold_sensitivity"]
    }
    delayed = rows[("assurance_cost", 0.01, 0.05)]
    prior = rows[("prior_selfing", 0.01, 0.05)]
    assert delayed["proportion"] == 51 / 64
    assert delayed["bootstrap95"][0] > 0.5
    for threshold in (0.025, 0.05, 0.1):
        row = rows[("assurance_cost", 0.01, threshold)]
        assert row["proportion"] > 0.5
        assert row["bootstrap95"][0] > 0.5
    assert prior["proportion"] == 30 / 64
    assert prior["bootstrap95"][0] < 0.5 < prior["bootstrap95"][1]
    assert "not universal" in result["interpretation"]["generality_boundary"].lower()


def test_result_is_tied_to_frozen_design_and_action_artifact():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["design_sha256"] == hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    assert result["design_sha256"] == "0ea4cc4129b2ee97a1ed1ffb2295348e0628cf0f0a1b0d0694a3b78befb4f9d0"
    assert result["workflow_run"] == 37390991122
    artifact = result["workflow_result_artifact"]
    assert artifact["artifact_id"] == 11381590034
    assert artifact["artifact_zip_sha256"] == "7c5c252cf559067f218bbd9f37b74b00c5d9c52fe30f25bb0196c9bfb9cb4872"
    assert artifact["full_result_json_sha256"] == "1951af2f2d5a8be883eae514aa84dce7d6a40407201c9a8cce501d4502773900"
    assert artifact["console_sha256"] == "7351d08f7ced7b3916428314940d86260d3f119fbd516d6ea7772d44836adb59"
