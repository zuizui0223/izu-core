from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STATE = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md"


def test_readme_exposes_frozen_chapter2_v3_and_metadata_only_submission_gate():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "chapter 2 is scientifically complete and frozen for submission" in lower
    assert "sign(δ reproduction) = sign(δ service) = sign(δ functional opportunity)" in lower
    assert "editorial v3" in lower
    assert "scripts/build_island_ecology_manuscript_v3.py" in text
    assert "scripts/build_island_ecology_submission_metadata.py" in text
    assert "scripts/build_island_ecology_submission_bundle.py" in text
    assert "dist/island_ecology_jecology_submission_bundle.zip" in text
    assert "author-supplied identity/submission metadata" in lower


def test_submission_state_keeps_science_closed_and_builder_fail_closed():
    text = STATE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "chapter 2 science is **complete and frozen for submission**" in lower
    assert "reviewer-facing manuscript is now **editorial v3**" in lower
    assert "frozen v2 manuscript source" in lower
    assert "only **author-supplied submission metadata** remain unresolved" in lower
    assert "builder stops without creating an identity-bearing submission package" in lower
    assert "does not rerun or modify the scientific analysis" in lower
