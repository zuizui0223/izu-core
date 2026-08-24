import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_submission_manifest_routes_ecology_files_only():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["primary_scientific_state"] == "H1_H5_closed_for_submission"
    assert manifest["scientific_reopening_required"] is False
    assert manifest["main_files"]["anonymous_manuscript"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_20260824.md"
    assert manifest["main_files"]["frozen_scientific_manuscript"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
    assert [row["figure"] for row in manifest["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert manifest["supplement"]["state_separability_figure"]["figure"] == "FigS1"
    assert manifest["supplement"]["state_separability_figure"]["role"] == "supporting_inference_guard_not_primary_biological_result"
    assert manifest["review_archive"]["anonymous"] is True
    assert manifest["review_archive"]["builder"] == "scripts/build_island_ecology_review_archive.py"
    assert manifest["review_archive"]["identity_scan_required"] is True
    assert manifest["review_archive"]["new_unpublished_field_data_required"] is False
    assert manifest["separate_submission_files"]["title_page_template"] == "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md"
    assert manifest["separate_submission_files"]["title_page_status"] == "pending_author_and_affiliation_metadata"
    assert manifest["separate_submission_files"]["anonymous_review_manuscript"] == "assembled_pending_ci_validation"
    assert len(manifest["future_empirical_tracks_excluded_from_submission_gate"]) == 3


def test_data_code_statement_preserves_anonymous_review_and_no_field_blocker():
    text = DATA_CODE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "anonymized review archive" in lower
    assert "no new unpublished field dataset" in lower
    assert "immutable versioned archive" in lower
    assert "persistent doi" in lower
    assert "real-world signed functional-position" in lower
    assert "issue #91" in lower
    assert "not required" in lower
