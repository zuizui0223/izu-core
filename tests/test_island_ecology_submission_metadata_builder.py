import json
from pathlib import Path

from scripts.build_island_ecology_submission_metadata import (
    load_metadata,
    render_cover_letter,
    render_title_page,
    validate_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
CHECKLIST = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_METADATA_CHECKLIST_20260825.md"


def complete_metadata() -> dict:
    metadata = load_metadata(TEMPLATE)
    metadata["authors"] = [
        {
            "full_name": "Example Author",
            "affiliations": ["Example Institute, Example University, Example City, Example Country"],
            "email": "example@example.org",
            "postal_address": "Example Institute, Example City, Example Country",
            "orcid": "0000-0000-0000-0000",
        }
    ]
    metadata["corresponding_author_index"] = 0
    metadata["acknowledgements"] = "None"
    metadata["funding"] = "None"
    metadata["author_contributions"] = "Example Author conceived the study, performed the analyses and wrote the manuscript."
    metadata["inclusion_statement"] = "This study used secondary literature and simulation data and involved no new local field data collection."
    metadata["conflict_of_interest"] = "The author declares no conflict of interest."
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    return metadata


def test_template_fails_closed_without_author_supplied_metadata():
    metadata = load_metadata(TEMPLATE)
    errors = validate_metadata(metadata)
    assert errors
    assert any("authors" in error for error in errors)
    assert any("corresponding_author_index" in error for error in errors)
    assert any("author_contributions" in error for error in errors)
    assert any("conflict_of_interest" in error for error in errors)


def test_complete_metadata_can_still_render_identity_files_for_later_use():
    metadata = complete_metadata()
    assert validate_metadata(metadata) == []
    title_page = render_title_page(metadata)
    cover_letter = render_cover_letter(metadata)
    assert "Example Author" in title_page
    assert "Example Institute" in title_page
    assert "## Author contributions" in title_page
    assert "## Inclusion statement" in title_page
    assert "## Conflict of interest" in title_page
    assert "## Data availability" in title_page
    assert "Example Author" in cover_letter
    assert "not under consideration elsewhere" in cover_letter


def test_builder_requires_explicit_submission_declarations():
    metadata = complete_metadata()
    metadata["submission_declarations"]["all_authors_approve_submission"] = False
    errors = validate_metadata(metadata)
    assert "submission_declarations.all_authors_approve_submission must be explicitly true" in errors


def test_builder_does_not_silently_infer_optional_identity_metadata():
    metadata = complete_metadata()
    metadata["authors"][0].pop("orcid")
    assert validate_metadata(metadata) == []
    title_page = render_title_page(metadata)
    assert "ORCID: not supplied" in title_page


def test_checklist_places_scientific_reassessment_before_author_metadata():
    text = CHECKLIST.read_text(encoding="utf-8")
    lower = text.lower()
    assert "submission paused pending scientific reassessment" in lower
    assert "author-metadata workflow remains prepared, but it is not the active gate" in lower
    assert "response-geometry and parameter-robustness" in lower
    assert "final author order and affiliations" in lower
    assert "final bundle" in lower
    assert "will raise an error while the scientific reassessment gate remains open" in lower
