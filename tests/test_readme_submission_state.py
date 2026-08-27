from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STATE = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
AUDIT = ROOT / "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"


def test_readme_exposes_closed_science_and_active_metadata_gate():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    unresolved = lower.split("## what is actually unresolved now", 1)[1].split("## current manuscript status", 1)[0]
    assert "response-geometry gate and the conditional-why diagnostics are complete" in unresolved
    assert "author-supplied identity metadata and declarations" in unresolved
    assert "ultimate why" in unresolved


def test_submission_state_closes_science_and_blocks_on_metadata():
    text = STATE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "scientifically assembled but not yet submission-ready" in lower
    assert "conditional-why diagnostics" in lower
    assert "author-supplied identity metadata and declarations" in lower
    assert "**how:**" in lower
    assert "**proximal why:**" in lower
    assert "**ultimate why:** not answered here" in lower
    assert "continues to **fail closed**" in lower


def test_reassessment_gate_and_audit_are_present():
    assert GATE.exists()
    assert AUDIT.exists()
    gate = GATE.read_text(encoding="utf-8")
    assert '"current_research_article_submission_ready": false' in gate
    assert "response_geometry_analysis_identifying_sign_switch_conditions" in gate
    audit = AUDIT.read_text(encoding="utf-8")
    assert "H2: not a pure tautology, but oversold" in audit
    assert "H5: qualitative coverage is not strong validation" in audit
