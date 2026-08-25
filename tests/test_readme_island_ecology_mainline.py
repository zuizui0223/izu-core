from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_current_island_ecology_manuscript():
    text = README.read_text(encoding="utf-8")
    assert text.startswith("# Izu Core — state-dependent island plant responses")
    assert "Why does island-associated simplification or reorganization of pollinator function" in text
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" in text
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md" in text
    assert "data/design/simulation_study_mainline_20260824.json" in text
    assert "Journal of Ecology" in text


def test_readme_preserves_island_syndrome_three_layer_framing():
    text = README.read_text(encoding="utf-8")
    for token in [
        "Colonization / assembly filtering",
        "In-situ evolutionary change",
        "Post-establishment interaction response",
        "aggregate island syndromes can coexist with lineage-level branching",
    ]:
        assert token.lower() in text.lower()
    assert "docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md" in text
    assert "data/design/island_syndrome_literature_claim_matrix_20260824.json" in text


def test_readme_preserves_frozen_scientific_boundaries():
    text = README.read_text(encoding="utf-8")
    for token in ["0.4167", "105/288", "16/96", "11/96", "207/216", "0/525"]:
        assert token in text
    assert "strict challenge set, not a prevalence sample" in text
    assert "Dominica" in text
    assert "was not retuned" in text
    assert "not submission blockers" in text


def test_readme_does_not_route_issue_91_as_current_mainline():
    text = README.read_text(encoding="utf-8")
    assert "Issue #91 field work is a future empirical-translation programme" in text
    assert "The current development target is Issue #91" not in text
    assert "method-first MEE drafts are archived alternative framings" in text
