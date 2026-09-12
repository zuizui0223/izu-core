from pathlib import Path

from scripts.build_island_ecology_submission_metadata import (
    load_metadata,
    render_cover_letter,
    render_data_archiving_statement,
    render_significance_statement,
    render_submission_statements,
    render_title_page,
    validate_metadata,
)
from scripts.render_chapter2_oikos_generality_overlay import NEW_TITLE

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
CHECKLIST = ROOT / "docs/ISLAND_ECOLOGY_SUBMISSION_METADATA_CHECKLIST_20260825.md"
OIKOS_CHECKLIST = ROOT / "docs/CHAPTER2_OIKOS_SUBMISSION_CHECKLIST_20260831.md"


def complete_metadata() -> dict:
    metadata = load_metadata(TEMPLATE)
    metadata["authors"] = [{
        "full_name": "Example Author",
        "affiliations": ["Example Institute, Example University, Example City, Example Country"],
        "email": "example@example.org",
        "postal_address": "Example Institute, Example City, Example Country",
        "orcid": "0000-0000-0000-0000",
    }]
    metadata["corresponding_author_index"] = 0
    metadata["significance_prior_work_context"] = (
        "This study extends prior work by the submitting author on plant–pollinator matching and builds on independent published work on island interaction reorganization."
    )
    metadata["acknowledgements"] = "None"
    metadata["funding"] = "None"
    metadata["inclusion_statement"] = "This study used secondary literature and simulation data and involved no new local field data collection."
    metadata["conflict_of_interest"] = "The author declares no conflict of interest."
    metadata["ethics_statement_confirmed"] = True
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    return metadata


def test_template_is_synchronized_to_oikos_mechanism_surface():
    metadata = load_metadata(TEMPLATE)
    assert metadata["journal"] == "Oikos"
    assert metadata["article_type"] == "Research Paper"
    assert metadata["schema_version"] == "1.8"
    assert metadata["manuscript_title"] == NEW_TITLE
    keywords = {value.lower() for value in metadata["keywords"]}
    assert "response geometry" in keywords
    assert "finite communities" in keywords
    assert "realized richness" in keywords
    assert "realized community" in keywords
    assert "non-additivity" in keywords
    significance = metadata["significance_statement"].lower()
    assert "exact control of realized richness" in significance
    assert "scale dependent" in significance
    assert "deterministic mean-field limit" in significance
    assert "numerical crossover is model-specific" in significance
    assert metadata["significance_prior_work_context"] is None
    assert metadata["planned_public_repository"] == "Dryad Digital Repository"
    assert "no new field sampling" in metadata["ethics_statement"].lower()
    assert metadata["ethics_statement_confirmed"] is None
    data_availability = metadata["data_availability"].lower()
    assert "exact realized-richness controls" in data_availability
    assert "finite-community system-size audits" in data_availability
    assert "anonymous reviewer archive" in data_availability
    assert "dryad digital repository" in data_availability


def test_template_fails_closed_on_initial_submission_inputs_only():
    metadata = load_metadata(TEMPLATE)
    errors = validate_metadata(metadata)
    assert errors
    assert any("authors" in error for error in errors)
    assert any("corresponding_author_index" in error for error in errors)
    assert any("significance_prior_work_context" in error for error in errors)
    assert not any("planned_public_repository" in error for error in errors)
    assert any("conflict_of_interest" in error for error in errors)
    assert any("ethics_statement_confirmed" in error for error in errors)
    assert not any("author_contributions" in error for error in errors)


def test_complete_metadata_renders_oikos_identity_significance_and_statement_files():
    metadata = complete_metadata()
    assert validate_metadata(metadata) == []
    title_page = render_title_page(metadata)
    cover_letter = render_cover_letter(metadata)
    significance = render_significance_statement(metadata)
    archiving = render_data_archiving_statement(metadata)
    statements = render_submission_statements(metadata)
    assert "Title page — Oikos" in title_page
    assert "Example Author" in title_page
    assert "ORCID: 0000-0000-0000-0000" in title_page
    assert NEW_TITLE in title_page
    assert NEW_TITLE in cover_letter
    assert "publication in *Oikos*" in cover_letter
    lower_cover = cover_letter.lower()
    assert "coarse placement of the ensemble response regime" in lower_cover
    assert "exact stepwise control of realized pollinator richness" in lower_cover
    assert "dominant source of response variation is not fixed" in lower_cover
    assert "deterministic mean-field limit" in lower_cover
    assert "numerical crossover is explicitly model-specific" in lower_cover
    assert "optional future falsification" in lower_cover
    assert "dryad digital repository" in lower_cover
    assert "Significance statement — Oikos" in significance
    assert metadata["significance_statement"] in significance
    assert metadata["significance_prior_work_context"] in significance
    assert "Dryad Digital Repository" in archiving
    assert "## Ethics statement" in statements
    assert "## Data archiving statement" in statements
    assert "CRediT roles will be supplied if a revised submission is invited" in statements


def test_author_contributions_are_optional_at_initial_submission():
    metadata = complete_metadata()
    metadata["author_contributions"] = None
    assert validate_metadata(metadata) == []
    statements = render_submission_statements(metadata)
    assert "CRediT roles will be supplied if a revised submission is invited" in statements


def test_builder_requires_explicit_submission_declarations():
    metadata = complete_metadata()
    metadata["submission_declarations"]["all_authors_approve_submission"] = False
    errors = validate_metadata(metadata)
    assert "submission_declarations.all_authors_approve_submission must be explicitly true" in errors


def test_builder_requires_explicit_author_confirmation_of_prefilled_ethics_statement():
    metadata = complete_metadata()
    metadata["ethics_statement_confirmed"] = False
    errors = validate_metadata(metadata)
    assert "ethics_statement_confirmed must be explicitly true after author review" in errors


def test_builder_requires_significance_prior_work_context_and_rejects_blank_repository():
    metadata = complete_metadata()
    metadata["significance_prior_work_context"] = ""
    metadata["planned_public_repository"] = ""
    errors = validate_metadata(metadata)
    assert "significance_prior_work_context requires an explicit statement" in errors
    assert "planned_public_repository requires an explicit statement" in errors


def test_corresponding_author_orcid_is_required_but_coauthor_orcid_is_optional():
    metadata = complete_metadata()
    metadata["authors"][0].pop("orcid")
    errors = validate_metadata(metadata)
    assert "corresponding author orcid is required by Oikos at submission" in errors

    metadata = complete_metadata()
    metadata["authors"].append({"full_name": "Example Coauthor", "affiliations": ["Example Institute"]})
    assert validate_metadata(metadata) == []
    title_page = render_title_page(metadata)
    assert "Example Coauthor" in title_page
    assert "ORCID: not supplied" in title_page


def test_checklist_places_author_metadata_after_closed_scientific_gate():
    text = CHECKLIST.read_text(encoding="utf-8")
    lower = text.lower()
    assert "scientific and manuscript-integration gates are closed" in lower
    assert "author-supplied metadata and declarations are the active blocker" in lower
    assert "final author order and affiliations" in lower
    assert "final bundle" in lower


def test_oikos_checklist_uses_mechanism_mainline_and_current_submission_contract():
    text = OIKOS_CHECKLIST.read_text(encoding="utf-8")
    lower = text.lower()
    assert "conditional response geometry → exact realized-richness control → scale-dependent determinant ordering → downstream modifiers → metadata confrontation / empirical claim ceiling" in lower
    assert "post-chapter-2 future transport/falsification, not a submission gate" in lower
    assert "mean all-positive in **6/6**" in lower
    assert "51–65/96" in text
    assert "70/96" in text and "65.61%" in text
    assert "55.84%" in text and "12.72%" in text
    assert "numerical crossover near `k=4` is model-specific" in lower
    assert "21/25" in text and "2/25" in text and "0/25" in text
    assert "manuscript.rtf" in lower
    assert "continuous line numbering" in lower
    assert "introduction forced to begin on page two" in lower
    assert "orcid" in lower
    assert "dryad digital repository" in lower
    assert "significance prior-work context" in lower
    assert "ethics_statement_confirmed" in text
    assert "credit / author-contribution roles are not an initial-submission blocker" in lower
