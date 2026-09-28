import json
from pathlib import Path

from scripts.build_island_ecology_review_archive import CORE_REVIEW_FILES
from scripts.build_island_ecology_submission_bundle import STATIC_SUBMISSION_FILES
from scripts.render_oikos_submission_rtf import render_supporting_information_markdown

ROOT = Path(__file__).resolve().parents[1]


def test_model2_is_excluded_from_current_supporting_information() -> None:
    text = render_supporting_information_markdown().lower()
    assert "unified model 3" in text
    for legacy in (
        "appendix s19",
        "finite-community system-size audit",
        "gaussian mean-field limit",
        "regime-dependent response hierarchy under active plant adjustment",
        "supporting table s9. exact realized-richness matching sensitivity",
    ):
        assert legacy not in text


def test_model2_is_excluded_from_submission_and_review_file_lists() -> None:
    joined = "\n".join((*STATIC_SUBMISSION_FILES, *CORE_REVIEW_FILES)).lower()
    for legacy_path in (
        "chapter2_supporting_information_s19",
        "chapter2_supporting_information_s20",
        "chapter2_supporting_information_s21",
        "chapter2_supporting_information_s22",
        "chapter2_supporting_table_s9",
        "run_response_geometry_realization_stability",
        "audit_chapter2_finite_community_system_size",
        "audit_finite_n_gaussian_mean_field",
    ):
        assert legacy_path not in joined


def test_active_manifests_lock_model2_to_legacy_archive() -> None:
    oikos = json.loads((ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json").read_text())
    lock = json.loads((ROOT / "data/design/chapter2_unified_model3_lock_20260927.json").read_text())
    for payload in (oikos["legacy_model2"], lock["legacy_model2_disposition"]):
        assert payload.get("archive_index") == "legacy/model2/README.md"
        assert payload.get("included_in_current_supporting_information") is False
        assert payload.get("included_in_current_review_archive") is False
    assert (ROOT / "legacy/model2/README.md").is_file()
