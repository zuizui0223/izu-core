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
    assert manifest["paper_scope_independent_of_external_research_programmes"] is True

    main = manifest["main_files"]
    assert main["anonymous_manuscript"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"
    assert main["anonymous_manuscript_source"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"
    assert main["anonymous_manuscript_builder"] == "scripts/build_island_ecology_manuscript_v3.py"
    assert main["anonymous_manuscript_status"] == "editorial_v3_rendered_deterministically_from_frozen_v2_source"
    assert main["supporting_information"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md"
    assert main["h2_analytical_sign_decomposition"] == "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md"
    assert "frozen_scientific_manuscript" not in main

    assert [row["figure"] for row in manifest["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert manifest["supplement"]["manuscript"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md"
    h2 = manifest["supplement"]["h2_analytical_sign_decomposition"]
    assert h2["file"] == "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md"
    assert h2["role"] == "algebraic_unpacking_of_frozen_v12_endpoint_not_new_scientific_result"
    assert h2["exact_identity"] == "sign_delta_reproduction_equals_sign_delta_service_equals_sign_delta_functional_opportunity"
    assert manifest["supplement"]["state_separability_figure"]["figure"] == "FigS1"
    assert manifest["supplement"]["state_separability_figure"]["role"] == "supporting_inference_guard_not_primary_biological_result"
    assert manifest["supplement"]["tables"] == ["TableS1_frozen_simulation_blocks", "TableS2_state_separability", "TableS3_external_systems"]

    review = manifest["review_archive"]
    assert review["anonymous"] is True
    assert review["builder"] == "scripts/build_island_ecology_review_archive.py"
    assert review["manuscript"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"
    assert review["identity_scan_required"] is True
    assert review["new_unpublished_field_data_required"] is False
    assert review["external_research_programmes_included"] is False

    separate = manifest["separate_submission_files"]
    assert separate["title_page_template"] == "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md"
    assert separate["submission_metadata_template"] == "data/design/island_ecology_submission_metadata_template.json"
    assert separate["submission_metadata_checklist"] == "docs/ISLAND_ECOLOGY_SUBMISSION_METADATA_CHECKLIST_20260825.md"
    assert separate["submission_metadata_builder"] == "scripts/build_island_ecology_submission_metadata.py"
    assert separate["submission_bundle_builder"] == "scripts/build_island_ecology_submission_bundle.py"
    assert separate["title_page_status"] == "builder_ready_pending_author_supplied_metadata"
    assert separate["cover_letter"] == "docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md"
    assert separate["cover_letter_status"] == "builder_ready_pending_author_supplied_metadata"
    assert separate["anonymous_review_manuscript"] == "editorial_v3_ready_via_deterministic_builder"
    assert separate["supplement"] == "assembled_with_h2_analytical_sign_decomposition"

    assert "future_empirical_tracks_excluded_from_submission_gate" not in manifest
    assert manifest["archived_provenance"]["pre_editorial_submission_source"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"
    assert manifest["archived_provenance"]["pre_submission_scientific_draft"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
    assert "editorial_v3_does_not_rerun_or_change_scientific_analysis" in manifest["protected_boundaries"]
    assert "author_identity_metadata_must_be_explicitly_supplied_not_inferred" in manifest["protected_boundaries"]
    assert manifest["next_executable_task"].startswith("fill_author_supplied_submission_metadata_json")


def test_data_code_statement_preserves_anonymous_review_and_paper_scope():
    text = DATA_CODE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "anonymized review archive" in lower
    assert "no new unpublished field dataset" in lower
    assert "immutable versioned archive" in lower
    assert "persistent doi" in lower
    assert "independent research programmes" in lower
    assert "neither dependencies nor validation requirements" in lower
    assert "issue #91" not in lower
    assert "real-world signed functional-position" not in lower
