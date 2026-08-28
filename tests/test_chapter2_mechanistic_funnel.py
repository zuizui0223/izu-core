import json
from pathlib import Path

import scripts.generate_chapter2_manuscript_figures as figures


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
SUPPLEMENT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md"
MAINLINE = ROOT / "data/design/chapter2_active_manuscript_mainline_20260827.json"
MANIFEST = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
JOURNAL_AUDIT = ROOT / "docs/CHAPTER2_JOURNAL_FIT_AUDIT_20260828.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_story_uses_the_five_question_mechanistic_funnel():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert manuscript.startswith("# Response geometry under community reorganization")
    for heading in [
        "## Possibility: the same reorganization generated opposite responses",
        "## Mechanism: turnover moved the system among response regimes",
        "## Reality: the comparative universe required more than one response state",
        "## Identifiability: no entry supplied the full comparative contract",
        "## Resolution: Izu raw matching localized source-state and composition structure",
    ]:
        assert heading in manuscript
    assert "Chapter 3 ≠ validation" not in manuscript
    assert "Chapter 3 is the next measurement stage, not causal validation" in manuscript
    assert "not the result of an outcome-independent global ranking" in manuscript
    abstract = manuscript.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    assert len(abstract.split()) <= 300


def test_mainline_and_supplement_separate_evidence_roles_and_claims():
    mainline = _load(MAINLINE)
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    assert mainline["schema_version"] == "1.4"
    assert mainline["interaction_kernel"]["status"] == "exact_code_identity_verified"
    assert len(mainline["mechanistic_funnel"]["five_questions"]) == 5
    assert "not_evaluable" in mainline["next_manuscript_gate"]
    assert "# Appendix S14. Exact interaction-kernel derivation" in supplement
    assert "# Appendix S15. Evidence roles and mechanistic-resolution funnel" in supplement
    assert "not uniform scalar shrinkage" in supplement
    assert "Chapter 2 identifies that contract" in supplement


def test_new_main_figures_render_from_frozen_inputs_only(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(figures, "OUT_DIR", tmp_path)
    why = _load(figures.WHY_DIAGNOSTICS)
    phase3 = _load(figures.PHASE3)
    external = _load(figures.EXTERNAL_READINESS)
    izu = _load(figures.IZU_STRUCTURAL)
    paths = [
        figures._fig1_mechanistic_resolution_funnel(),
        figures._fig3_proximal_why_hierarchy(why, phase3),
        figures._fig4_global_to_izu_resolution(external, izu),
    ]
    assert [path.name for path in paths] == [
        "fig1_mechanistic_resolution_funnel.svg",
        "fig3_proximal_why_hierarchy.svg",
        "fig4_global_to_izu_resolution.svg",
    ]
    assert all(path.exists() and path.stat().st_size > 10_000 for path in paths)


def test_submission_routing_records_oikos_without_relabeling_the_joecology_package():
    manifest = _load(MANIFEST)
    journal_audit = JOURNAL_AUDIT.read_text(encoding="utf-8")
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["preferred_next_journal_route"] == "Oikos Research paper"
    assert "project Tier B" in journal_audit
    assert "Oikos — recommended" in journal_audit
    assert "Ecology Letters — closed" in journal_audit
