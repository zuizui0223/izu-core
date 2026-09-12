from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_closed_science_and_current_active_surface():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — conditional island plant response geometry")
    assert "chapter 2 is scientifically closed without new focal field data" in lower
    assert "simulation + source-audited metadata/secondary-data confrontation" in lower
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md" in text
    assert "data/design/chapter2_simulation_metadata_completion_lock_20260912.json" in text
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


def test_readme_records_rank_crossover_without_universal_community_dominance():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "conditional response geometry" in lower
    assert "hierarchy of response determinants is **not fixed**" in lower
    assert "55.84%" in text and "12.72%" in text
    assert "28–42/96" in text
    assert "numerical crossover is model-specific" in lower
    assert "not natural frequencies or calibrated ecological thresholds" in lower
    assert "formal external prediction: **`not_evaluable`**" in text


def test_readme_routes_implementation_detail_to_active_surfaces():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "active scientific and submission surfaces" in lower
    assert "docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md" in text
    assert "scripts/render_island_ecology_submission_manuscript.py" in text
    assert "scripts/build_island_ecology_review_archive.py" in text


def test_readme_preserves_bounded_metadata_role_and_post_chapter2_field_role():
    lower = README.read_text(encoding="utf-8").lower()
    assert "biological plausibility, adversarial stress testing and empirical identifiability" in lower
    assert "not full validation" in lower
    assert "21/25" in lower and "2/25" in lower and "0/25" in lower
    assert "post-chapter-2 transport/falsification" in lower
    assert "not a submission gate or completion criterion" in lower


def test_readme_blocks_retroactive_chapter3_validation():
    lower = README.read_text(encoding="utf-8").lower()
    assert "chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove" in lower
    assert "chapter 3 phenotype validates chapter 2" in lower
    assert "prospective izu e3/e4 chain is required for chapter 2 completion" in lower
