"""Approval admission tests only: NEVER dispatch or execute 200-update biology."""
from __future__ import annotations

import json
from pathlib import Path
import re

import pytest

from scripts.chapter2_q2_i_support_order_20261016 import (
    DEFAULT_DESIGN, PIN_PATH, ROOT, sha,
)
from scripts.run_chapter2_q2_i_support_production_20261016 import admission


ACTIVATION = ROOT / "docs/protocols/chapter2_q2_i_support_order_20261016_activation.json"
WORKFLOW = ROOT / ".github/workflows/chapter2-q2-i-support-registered-20261016.yml"


def test_explicit_approval_is_admitted_by_actual_production_preflight():
    """Positive source-bound entrypoint check; no execute_shard or simulate call."""
    data = json.loads(ACTIVATION.read_text(encoding="utf-8"))
    design, sources = admission(ACTIVATION, DEFAULT_DESIGN)
    assert data["status"] == "author_reviewed_scientific_execution_approved"
    assert data["owner_explicit_approval"] is True
    assert data["approval_is_new_not_reused"] is True
    assert data["study"] == "ch2_q2_I_support_order_20261016"
    assert data["declared_full_cases"] == design["design_matrix"]["total_full_trajectories"] == 384
    assert data["total_registered_updates"] == 76800
    assert data["design_sha256"] == sha(DEFAULT_DESIGN.read_bytes())
    assert data["source_pin_receipt_sha256"] == sha(PIN_PATH.read_bytes())
    assert data["source_manifest_sha256"] == sha(
        json.dumps(sources, sort_keys=True).encode("utf-8"))
    assert data["model_baseline_sha"] == design["source_baseline_commit"]
    assert data["original_model_source_files_pinned"] == 25
    assert data["scientific_conditions"]["horizon"] == 200
    assert data["scientific_conditions"]["mutation_traits"] == {
        "match": True, "investment": False, "assurance": True,
    }


@pytest.mark.parametrize(("key", "tampered"), [
    ("status", "PENDING_AUTHOR_REVIEW_NOT_APPROVED"),
    ("owner_explicit_approval", False),
    ("approval_is_new_not_reused", False),
    ("declared_full_cases", 383),
    ("study", "different_study"),
    ("design_sha256", "0"*64),
    ("source_manifest_sha256", "0"*64),
])
def test_production_refuses_altered_core_approval_contract(tmp_path, key, tampered):
    data = json.loads(ACTIVATION.read_text(encoding="utf-8"))
    data[key] = tampered
    altered = tmp_path / "altered_approval.json"
    altered.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="Production HOLD"):
        admission(altered, DEFAULT_DESIGN)


def test_approved_campaign_still_uses_manual_only_workflow():
    contents = WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"^on:\s*\n\s+workflow_dispatch:", contents, re.M)
    assert not re.search(r"^\s*(?:push|pull_request):", contents, re.M)
    assert "needs: preflight" in contents
    assert "author-authorized" not in contents  # approval is verified by the source-bound gate
    assert "chapter2_q2_i_support_order_20261016_activation.json" in contents
    # This test cannot launch an Actions workflow and does not synthesize results.
