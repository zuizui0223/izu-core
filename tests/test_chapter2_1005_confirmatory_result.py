import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_1005_confirmatory_replication_20261006.json"
RESULT = ROOT / "data/results/chapter2_1005_confirmatory_replication_20261006.json"


def test_confirmatory_result_matches_frozen_design_and_primary_rule():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    assert result["status"] == "confirmed"
    assert result["workflow_run"] == 37390991122
    assert result["declared_cases"] == 4096
    assert result["independent_visitor_histories"] == 64
    assert result["nested_demographic_repeats"] == 8
    assert result["design_sha256"] == hashlib.sha256(DESIGN.read_bytes()).hexdigest()

    assert design["new_randomization"]["visitor_history_seeds"] == {
        "first": 26100601,
        "last": 26100664,
        "count": 64,
    }
    assert design["new_randomization"]["demographic_repeat_seeds"] == {
        "first": 26101601,
        "last": 26101608,
        "count": 8,
    }

    primary = result["primary_sequence"]
    assert primary["setting"] == "assurance_cost"
    assert primary["mutation_rate"] == 0.01
    assert primary["threshold"] == 0.05
    assert primary["counts"] == {"assurance_first": 51, "near_simultaneous": 13}
    assert primary["assurance_first_proportion_all_histories"] == pytest.approx(51 / 64)
    assert primary["assurance_first_bootstrap95"] == pytest.approx([0.6875, 0.890625])
    assert primary["assurance_first_bootstrap95"][0] > 0.5

    assert result["adjudication"] == {
        "status": "confirmed",
        "sequence_success": True,
        "fixed_assurance_success": True,
    }


def test_fixed_assurance_confirmation_and_scope_boundary_are_preserved():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    primary = result["fixed_assurance"][0]

    assert primary["setting"] == "assurance_cost"
    assert primary["mutation_rate"] == 0.01
    assert primary["fixed_assurance"] == 0.5
    assert primary["occupancy"] == {"near": 1, "far": 1}
    assert primary["eligible_histories_far"] == 64
    assert primary["eligible_histories_paired"] == 64
    assert primary["admissible"] is True
    assert primary["far_investment_change"]["mean"] == pytest.approx(-0.30602115590337237)
    assert primary["far_investment_change"]["bootstrap95"] == pytest.approx(
        [-0.3180538379758027, -0.2941114139044992]
    )
    assert primary["far_minus_near_investment"]["mean"] == pytest.approx(
        -0.43538938011716005
    )
    assert primary["far_minus_near_investment"]["bootstrap95"] == pytest.approx(
        [-0.4533304896960724, -0.4171906485389262]
    )

    primary_thresholds = {
        row["threshold"]: row
        for row in result["threshold_sensitivity"]
        if row["setting"] == "assurance_cost" and row["mutation_rate"] == 0.01
    }
    assert set(primary_thresholds) == {0.025, 0.05, 0.1}
    for row in primary_thresholds.values():
        assert row["proportion"] > 0.5
        assert row["bootstrap95"][0] > 0.5

    prior_positive = next(
        row
        for row in result["threshold_sensitivity"]
        if row["setting"] == "prior_selfing"
        and row["mutation_rate"] == 0.01
        and row["threshold"] == 0.05
    )
    assert prior_positive["counts"] == {
        "assurance_first": 30,
        "near_simultaneous": 34,
    }
    assert prior_positive["proportion"] == pytest.approx(30 / 64)
    assert prior_positive["bootstrap95"][0] < 0.5 < prior_positive["bootstrap95"][1]
    assert "not universal" in result["interpretation"]["generality_boundary"].lower()


def test_workflow_artifact_identity_is_frozen():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    artifact = result["workflow_result_artifact"]
    assert artifact["artifact_id"] == 11381590034
    assert artifact["artifact_zip_sha256"] == (
        "7c5c252cf559067f218bbd9f37b74b00c5d9c52fe30f25bb0196c9bfb9cb4872"
    )
    assert artifact["full_result_json_sha256"] == (
        "1951af2f2d5a8be883eae514aa84dce7d6a40407201c9a8cce501d4502773900"
    )
    assert artifact["console_sha256"] == (
        "7351d08f7ced7b3916428314940d86260d3f119fbd516d6ea7772d44836adb59"
    )
