from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_closed_science_and_current_active_surface():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — conditional island plant response geometry")
    assert "chapter 2 is scientifically closed" in lower
    assert "synthetic gate is closed" in lower
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in text
    assert "historical v2 manuscripts" in lower
    assert "must not be treated as the current manuscript surface" in lower


def test_readme_preserves_three_layer_island_syndrome_core():
    text = README.read_text(encoding="utf-8")
    for token in [
        "Colonization / assembly filtering",
        "In-situ evolutionary change",
        "Post-establishment interaction response",
    ]:
        assert token in text
    assert "three distinct processes" in text.lower()


def test_readme_preserves_current_claim_ceiling_without_old_hypothesis_headings():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "conditional response geometry" in lower
    assert "community realization is the largest additive component" in lower
    assert "not natural frequencies or calibrated ecological thresholds" in lower
    assert "the frozen 25 systems validate one universal mechanism" in lower
    assert "formal external prediction: **`not_evaluable`**" in text
    assert "h2 — reassigned" not in lower
    assert "h4 — retained" not in lower
    assert "h5 — demoted" not in lower


def test_readme_routes_implementation_detail_to_active_surfaces_not_entrypoint_history():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "active scientific and submission surfaces" in lower
    assert "scripts/render_island_ecology_submission_manuscript.py" in text
    assert "scripts/build_island_ecology_review_archive.py" in text
    assert "support_strength" not in text
    assert "0.4167" not in text
    assert "replicated_minimal_generator" not in text


def test_readme_registers_current_izu_claim_ceiling_and_selection_logic():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "why izu is the focal depth system" in lower
    assert "measurement continuity across the unresolved chain" in lower
    assert "not focal because it is in japan" in lower
    assert "null-corrected matching" in lower
    assert "leave-one-island sign stability" in lower
    assert "matching-to-pollen propagation is positive on average but not leave-one-island sign stable" in lower
    assert "does not infer historical *bombus* loss" in lower


def test_readme_allows_focal_lineage_context_but_blocks_retroactive_validation():
    lower = README.read_text(encoding="utf-8").lower()
    assert "microdonta" in lower
    assert "chapter 3" in lower
    assert "not** used to tune, validate or retroactively prove" in lower
    assert "chapter 3 phenotype validates chapter 2" in lower
    assert "present functional structure identifies the historical cause" in lower
