from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STATE = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
AUDIT = ROOT / "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"


def test_readme_exposes_reassessment_as_active_gate():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "reopened for scientific reassessment" in lower
    assert "response geometry / parameter robustness" in text
    assert "metadata" not in lower.split("## what is actually unresolved now", 1)[1].split("## current manuscript status", 1)[0]


def test_submission_state_reopens_science_and_blocks_packaging():
    text = STATE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "not currently submission-ready" in lower
    assert "scientific reassessment" in lower
    assert "response-geometry and parameter-robustness analysis" in lower
    assert "author metadata are **not** the active blocker now" in lower
    assert "submission bundle machinery is retained but must fail closed" in lower


def test_reassessment_gate_and_audit_are_present():
    assert GATE.exists()
    assert AUDIT.exists()
    gate = GATE.read_text(encoding="utf-8")
    assert '"current_research_article_submission_ready": false' in gate
    assert "response_geometry_analysis_identifying_sign_switch_conditions" in gate
    audit = AUDIT.read_text(encoding="utf-8")
    assert "H2: not a pure tautology, but oversold" in audit
    assert "H5: qualitative coverage is not strong validation" in audit
