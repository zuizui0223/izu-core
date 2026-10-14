"""Freeze the admitted negative independent Chapter 2 budget-window result.

Archive provenance and original full-grid decision must remain stable. No new
visitor histories, postshock futures, or external downloads are run in CI.
"""
from pathlib import Path
import hashlib
import json

RESULT = Path("results/chapter2/independent_window_confirmation_20261009.json")
OLD_RESULT = Path("results/chapter2/order_expression_full_cohort_20261009.json")
EXPECTED_SHA256 = "fa3d4103b3f3a84781c052907012a0dfed13caebb247c80f4c34b760a536cc58"


def test_exact_archived_readout_checksum_and_full_admission():
    raw = RESULT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    data = json.loads(raw)
    assert data["status"] == "all_2048_new_sources_57344_futures_admitted"
    assert (data["independent_visitor_histories"],
            data["prehistories"], data["future_branches"]) == (64, 2048, 57344)
    assert data["new_protocol_sha256"] == (
        "39918e4fe6650f99b0eac4372449509bdef45e58318dc760906d7a8ca3d9fe30")


def test_predeclared_negative_not_promoted_from_single_budget():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    primary = data["primary"]
    assert primary["predeclared_joint_decision"] == "window_residual_practically_equivalent"
    assert primary["window_gate_passed"] is False
    assert primary["smooth_gate_passed"] is False
    assert primary["history_bootstrap95"][0] < 0 < primary["history_bootstrap95"][1]
    assert all(-0.05 < x < 0.05 for x in primary["history_bootstrap95"])
    assert data["by_regime"]["unbottlenecked_capacity48"][
        "fixed_window_diagnostic"]["predeclared_joint_decision"] == (
            "window_residual_practically_equivalent"
        )
    prev = json.loads(OLD_RESULT.read_text(encoding="utf-8"))
    assert prev["main_order_history_DID"]["decision"] == (
        "equivalent_within_predeclared_ROPE"
    )


def test_exploratory_budget_peak_is_not_new_primary_gate():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    primary = data["by_regime"]["eight_founders_capacity8"][
        "history_average_DID_by_budget"]
    assert primary["3"] == 0.0029296875
    assert primary["4"] == -0.0625
    assert data["primary"]["window_gate_passed"] is False
