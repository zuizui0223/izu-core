import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/results/model3_full_clean_rerun_receipt_20261003.json"
LOCK = ROOT / "data/design/chapter2_vnext_syndrome_integration_lock_20261002.json"
WORKFLOW = ROOT / ".github/workflows/model3_full_clean_rerun.yml"


def test_full_clean_rerun_receipt_closes_both_frozen_campaigns() -> None:
    r = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert r["status"] == "complete_full_model3_clean_rerun_verified"
    assert r["fresh_cases"] == {
        "base_model3": 19968,
        "chapter2_bridge": 24576,
        "total": 44544,
    }
    assert r["base_model3_reproduction"]["numeric_differences_gt_1e_12"] == 0
    assert r["base_model3_reproduction"]["structural_mismatch_classification"] == {
        "crossed_extra_histories_field": 4,
        "paired_contrasts_extra_eligible_pairs_field": 156,
        "scientific_schema_mismatch_after_ignoring_these_added_audit_fields": 0,
    }
    assert r["bridge_reproduction"]["numeric_differences_gt_1e_12"] == 0
    assert r["bridge_reproduction"]["structural_mismatch_count"] == 0


def test_vnext_lock_points_to_clean_rerun_receipt() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["evidence_promoted_into_vnext"]["full_clean_model3_reproduction"] == (
        "data/results/model3_full_clean_rerun_receipt_20261003.json"
    )
    repro = lock["computational_reproducibility"]
    assert repro["status"] == "closed"
    assert repro["total_fresh_cases"] == 44544
    assert repro["base_schema_only_additions"]["scientific_schema_mismatches_after_normalization"] == 0


def test_clean_rerun_workflow_is_manual_only() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
