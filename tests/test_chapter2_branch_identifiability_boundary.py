from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_SURFACES = (
    ROOT / "README.md",
    ROOT / "THESIS_CHAPTER_POSITIONING.md",
    ROOT / "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md",
    ROOT / "docs/CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md",
    ROOT / "docs/CHAPTER2_CANONICAL_STORY_20260927.md",
    ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md",
    ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md",
    ROOT / "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md",
    ROOT / "docs/CHAPTER2_OIKOS_SUBMISSION_CHECKLIST_20260831.md",
    ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md",
    ROOT / "docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md",
)

BANNED_OVERCLAIMS = (
    "determine how much directional branching is realized",
    "determine how much directional heterogeneity is realized",
    "determine how much heterogeneous response is realized",
    "realize/suppress branching",
)

def test_active_surfaces_do_not_promote_unidentified_latent_branch_prevalence():
    for path in ACTIVE_SURFACES:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in BANNED_OVERCLAIMS:
            assert phrase not in text, (path, phrase)

def test_canonical_surfaces_preserve_branch_identifiability_boundary():
    manuscript = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(encoding="utf-8").lower()
    story = (ROOT / "docs/CHAPTER2_CANONICAL_STORY_20260927.md").read_text(encoding="utf-8").lower()
    results = (ROOT / "docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md").read_text(encoding="utf-8").lower()
    firewall = (ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md").read_text(encoding="utf-8").lower()

    assert "stable latent branch prevalence" in manuscript
    assert "stable latent branch frequencies are not identified" in story
    assert "exact latent branch prevalence is not identified" in results
    assert "stable latent branch prevalence" in firewall
