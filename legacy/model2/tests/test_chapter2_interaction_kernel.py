from pathlib import Path

from scripts.audit_chapter2_interaction_kernel import build


ROOT = Path(__file__).resolve().parents[1]


def test_interaction_kernel_is_exact_code_identity_not_a_new_simulation():
    payload = build()
    assert payload["status"] == "exact_code_identity_verified"
    assert payload["audit_kind"] == "deterministic_algebraic_identity_no_new_simulation"
    assert all(payload["checks"].values())
    assert payload["maximum_direct_identity_error"] <= 1e-12
    assert payload["maximum_trajectory_composite_identity_error"] <= 1e-12
    assert len(payload["source_canonical_text_sha256"]) == 3


def test_interaction_kernel_audit_rejects_overclaiming_shortcuts():
    payload = build()
    assert "not the exact endpoint response coordinate" in payload["rejected_shortcut"]
    assert "nonlinear" in payload["aggregation_boundary"]
    assert "not a scalar shrinkage" in payload["local_filtering_boundary"]
    assert "not covered by that theorem" in payload["assurance_boundary"]
    assert "natural-frequency" in payload["claim_boundary"]


def test_interaction_kernel_audit_is_provenance_not_current_automatic_gate():
    workflow = (ROOT / ".github/workflows/chapter2-scientific-gate.yml").read_text(
        encoding="utf-8"
    )
    assert "python -m scripts.audit_chapter2_interaction_kernel" not in workflow
    assert "chapter2_interaction_kernel_audit_ci.json" not in workflow
