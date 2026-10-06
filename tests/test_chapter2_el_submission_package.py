from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/chapter2_evolution_letters_submission_manifest_20261004.json"
COVER = ROOT / "docs/CHAPTER2_EVOLUTION_LETTERS_COVER_LETTER_20261004.md"
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"


def test_evolution_letters_submission_manifest_is_fail_closed_on_human_fields():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["journal_target"] == "Evolution Letters"
    assert m["article_type"] == "Letter"
    assert m["submission_ready"] is False
    assert m["verification"]["scientific_gate"]["status"] == "success"
    assert m["verification"]["full_ci"]["status"] == "success"
    assert m["verification"]["oikos_path_changes_vs_main"] == 0
    blockers = set(m["human_blockers"])
    assert "exact_AI_use_disclosure_scope_and_tool_version_details" in blockers
    assert "Oikos_current_submission_status_and_related_manuscript_difference_statement" in blockers
    assert "conflict_of_interest_confirmation" in blockers


def test_cover_letter_keeps_ai_and_related_manuscript_disclosures_open():
    cover = COVER.read_text(encoding="utf-8")
    assert "Related or similar manuscripts — REQUIRES AUTHOR CONFIRMATION" in cover
    assert "AI-use disclosure — REQUIRES AUTHOR CONFIRMATION" in cover
    assert "Do not infer or minimize the scope." in cover
    assert "[CORRESPONDING AUTHOR NAME]" in cover
    assert "[EMAIL]" in cover


def test_cover_letter_preserves_structural_control_interpretation():
    cover = COVER.read_text(encoding="utf-8")
    assert "structural delayed-selfing control itself reached a 16.4%" in cover
    assert "prior selfing reached 10.2%" in cover
    assert "pollen discounting 21.3%" in cover
    assert "assurance cost 43.0%" in cover
    assert "clearest trade-off-specific amplification under assurance cost" in cover


def test_manuscript_endmatter_present_before_references():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    refs = manuscript.index("# Core references for framing")
    for heading in (
        "# Data and code availability",
        "# Author contributions",
        "# Funding",
        "# Conflict of interest",
        "# Acknowledgements",
    ):
        assert 0 <= manuscript.index(heading) < refs
