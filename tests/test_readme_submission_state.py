from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STATE = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
AUDIT = ROOT / "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"


def test_readme_exposes_bridge_complete_model3_and_package_qa_state():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    submission = lower.split("## submission status", 1)[1].split("## claim boundary", 1)[0]
    assert "biological mechanism and the original chapter 2 control suite are now resolved inside model 3" in submission
    assert "oikos package is still not submission-ready only because figures" in submission
    assert "no new focal field data are required" in submission
    assert "post-chapter-2 nee/field lane remains optional" in submission
    assert "present-day izu associations do not identify historical *bombus* loss" in lower

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
