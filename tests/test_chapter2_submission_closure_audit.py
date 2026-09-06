import json
from pathlib import Path

from scripts.audit_chapter2_submission_closure import build_audit

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/chapter2_submission_closure_audit_20260906.json"


def test_submission_closure_audit_matches_frozen_preflight():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    current = build_audit()
    assert current == frozen


def test_submission_closure_is_author_metadata_only_not_science_or_renderer_work():
    audit = build_audit()
    assert audit["scientific_gate_complete"] is True
    assert audit["nonmetadata_submission_preflight_ready"] is True
    assert audit["nonmetadata_submission_errors"] == []
    assert audit["only_author_supplied_metadata_and_confirmations_remain"] is True
    assert audit["metadata_template_validation_error_count"] == 14
    assert audit["unexpected_metadata_errors"] == []
    assert audit["submission_ready"] is False


def test_submission_closure_requires_explicit_ethics_confirmation_and_preserves_optional_items():
    audit = build_audit()
    assert audit["ethics_statement_prefilled"] is True
    assert audit["ethics_statement_author_confirmation_required"] is True
    assert "ethics_statement_author_confirmation" in audit["required_human_input_categories"]
    assert set(audit["optional_not_initial_submission_blockers"]) == {
        "coauthor_orcids",
        "author_contributions_credit_roles",
    }
    assert audit["planned_public_repository_already_fixed"] == "Dryad Digital Repository"
