from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ACTIVE_DEVELOPMENT_MAINLINE_20260813.md"


def test_active_routing_doc_points_to_island_ecology_mainline():
    text = DOC.read_text(encoding="utf-8")
    assert "data/design/simulation_study_mainline_20260824.json" in text
    assert "data/design/island_ecology_hypothesis_recovery_20260824.json" in text
    assert "docs/ISLAND_ECOLOGY_MANUSCRIPT_REASSEMBLY_SPEC_20260824.md" in text
    assert "H1–H5 recovery state" in text
    assert "The 13-system set is a strict **challenge set**, not a prevalence sample." in text
    assert "supporting inference guard" in text
    assert "must not survive in the primary island-ecology Discussion" in text
    assert "Unresolved sidelines — preserved but non-blocking" in text
    assert "do not require new simulation, field data or external-system search before submission" in text
    assert "Apply the frozen H1–H5 order to the primary manuscript and figure captions" in text
