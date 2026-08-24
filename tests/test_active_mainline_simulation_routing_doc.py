from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ACTIVE_DEVELOPMENT_MAINLINE_20260813.md"


def test_active_routing_doc_points_to_simulation_mainline():
    text = DOC.read_text(encoding="utf-8")
    assert "data/design/simulation_study_mainline_20260824.json" in text
    assert "field data" not in text.lower() or "not required" in text.lower()
    assert "legacy simulation complexity that does not change a comparative admission decision" not in text
    assert "They are **not required for the primary simulation study**" in text
    assert "Generate the manuscript figures" in text
