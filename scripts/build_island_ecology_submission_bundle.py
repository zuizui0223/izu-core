from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.build_island_ecology_review_archive import build_archive as build_review_archive
from scripts.build_island_ecology_submission_metadata import (
    load_metadata,
    render_cover_letter,
    render_significance_statement,
    render_submission_statements,
    render_title_page,
    validate_metadata,
)
from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_plain_text_rtf,
    render_supporting_information_rtf,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "dist/chapter2_oikos_submission_bundle.zip"
REASSESSMENT_GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
REALIZED_RICHNESS_DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
SOURCE_MANUSCRIPT = "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
SUBMISSION_MANUSCRIPT_NAME = "MANUSCRIPT.rtf"
SUBMISSION_SI_NAME = "SUPPORTING_INFORMATION.rtf"
TITLE_PAGE_NAME = "TITLE_PAGE.rtf"
COVER_LETTER_NAME = "COVER_LETTER.rtf"
SIGNIFICANCE_NAME = "SIGNIFICANCE_STATEMENT.rtf"
STATEMENTS_NAME = "SUBMISSION_STATEMENTS.rtf"
ACTIVE_SUBMISSION_MANIFEST = "data/design/chapter2_oikos_submission_manifest_20260831.json"
RELATIONAL_FIGURE_INPUTS_ARCNAME = "data/results/chapter2_manuscript_figure_inputs_relational_20260831.json"
RELATIONAL_FIGURE_INPUTS = ROOT / RELATIONAL_FIGURE_INPUTS_ARCNAME

STATIC_SUBMISSION_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md",
    "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md",
    "docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md",
    "docs/CHAPTER2_SUPPORTING_INFORMATION_S19_REALIZED_RICHNESS_20260907.md",
    "docs/CHAPTER2_SUPPORTING_TABLE_S9_REALIZED_RICHNESS_20260907.md",
    "data/design/chapter2_relational_robustness_audit_freeze_20260831.json",
    "data/design/chapter2_realized_richness_matching_freeze_20260907.json",
    "data/results/chapter2_relational_robustness_audit_frozen_20260831.json",
    "data/results/chapter2_realized_richness_matching_decision_20260907.json",
    ACTIVE_SUBMISSION_MANIFEST,
)


def validate_scientific_gate() -> dict:
    if not REASSESSMENT_GATE.exists():
        raise ValueError("scientific reassessment gate is missing; refuse to build a submission bundle")
    try:
        gate = json.loads(REASSESSMENT_GATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("scientific reassessment gate is unreadable; refuse to build a submission bundle") from exc
    if gate.get("scientific_model_gate_complete") is not True:
        raise ValueError("Chapter 2 scientific model gate is not complete")
    if gate.get("research_article_route") != "candidate_conditional_response_geometry":
        raise ValueError("Chapter 2 is not currently routed to the conditional-response-geometry Research Article candidate")
    if gate.get("realized_richness_reframe_complete") is not True:
        raise ValueError("Chapter 2 realized-richness reframe is not complete")
    if not REALIZED_RICHNESS_DECISION.exists():
        raise ValueError("realized-richness decision is missing")
    decision = json.loads(REALIZED_RICHNESS_DECISION.read_text(encoding="utf-8"))
    if decision.get("prespecified_gate", {}).get("decision") != "blocker_failed_reframe_before_author_metadata":
        raise ValueError("realized-richness decision no longer matches the frozen reframe")
    if gate.get("realized_richness_decision") != REALIZED_RICHNESS_DECISION.relative_to(ROOT).as_posix():
        raise ValueError("scientific gate is not linked to the frozen realized-richness decision")
    return gate


def _write_rtf(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    rendered = path.read_text(encoding="utf-8")
    if not rendered.startswith("{\\rtf1"):
        raise ValueError(f"Oikos upload file is not RTF: {path.name}")


def build_submission_bundle(metadata_path: Path, output: Path) -> Path:
    gate = validate_scientific_gate()

    metadata = load_metadata(metadata_path)
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    if metadata.get("journal") != "Oikos" or metadata.get("article_type") != "Research Paper":
        raise ValueError("active submission metadata must route to Oikos Research Paper")

    if not (ROOT / SOURCE_MANUSCRIPT).exists():
        raise FileNotFoundError(SOURCE_MANUSCRIPT)
    for rel in STATIC_SUBMISSION_FILES:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)

    figure_payload = build_figures()
    figure_files = tuple(figure_payload["figure_outputs"])
    for rel in figure_files:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)
    if not RELATIONAL_FIGURE_INPUTS.exists():
        raise FileNotFoundError(RELATIONAL_FIGURE_INPUTS)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        manuscript = tmp / SUBMISSION_MANUSCRIPT_NAME
        supporting_information = tmp / SUBMISSION_SI_NAME
        title_page = tmp / TITLE_PAGE_NAME
        cover_letter = tmp / COVER_LETTER_NAME
        significance = tmp / SIGNIFICANCE_NAME
        statements = tmp / STATEMENTS_NAME
        review_archive = tmp / "anonymous_review_archive.zip"

        _write_rtf(manuscript, render_manuscript_rtf())
        _write_rtf(supporting_information, render_supporting_information_rtf())
        _write_rtf(title_page, render_plain_text_rtf(render_title_page(metadata)))
        _write_rtf(cover_letter, render_plain_text_rtf(render_cover_letter(metadata)))
        _write_rtf(significance, render_plain_text_rtf(render_significance_statement(metadata)))
        _write_rtf(statements, render_plain_text_rtf(render_submission_statements(metadata)))
        build_review_archive(review_archive)

        main_rtf = manuscript.read_text(encoding="utf-8")
        lower_main = main_rtf.lower()
        for control in ("\\sl480\\slmult1", "\\linemod1", "\\linecont", "fldinst PAGE", "\\page"):
            if control not in main_rtf:
                raise ValueError(f"Oikos manuscript formatting control missing: {control}")
        required_story = (
            "conditional response geometry",
            "realized richness differences therefore help position the ensemble mean regime",
            "ordering of response determinants is itself regime dependent",
            "deterministic mean-field kernel contrast was all-positive",
            "optional future validation programme",
        )
        missing_story = [token for token in required_story if token not in lower_main]
        if missing_story:
            raise ValueError(f"Oikos manuscript lost the mechanism-mainline narrative: {missing_story}")
        stale_story = (
            "result 1—mechanistic prediction",
            "result 2—real-world exposure",
            "result 3—biological consequence",
            "figure 1. three-result inference chain",
        )
        leaked = [token for token in stale_story if token in lower_main]
        if leaked:
            raise ValueError(f"historical three-result narrative leaked into active manuscript: {leaked}")

        bundle_manifest = {
            "journal": metadata["journal"],
            "article_type": metadata["article_type"],
            "scientific_state": "synthetic_conditional_response_geometry_with_regime_dependent_determinant_ordering",
            "manuscript_state": "active_20260911_mechanism_mainline_rendered_to_oikos_rtf_submission",
            "mechanism_mainline_narrative": True,
            "three_result_narrative": False,
            "identifiability_coequal_study_objective": False,
            "field_e3_e4_required_for_submission": False,
            "source_manuscript": SOURCE_MANUSCRIPT,
            "submission_manuscript": SUBMISSION_MANUSCRIPT_NAME,
            "submission_supporting_information": SUBMISSION_SI_NAME,
            "active_submission_manifest": ACTIVE_SUBMISSION_MANIFEST,
            "author_metadata_source": metadata_path.name,
            "review_archive_anonymous": True,
            "oikos_upload_format": "RTF",
            "main_text_single_column": True,
            "main_text_double_spaced": True,
            "main_text_continuous_line_numbers": True,
            "main_text_page_numbers": True,
            "introduction_forced_to_page_two": True,
            "main_text_reference_list_included": True,
            "main_text_reference_scope": "active_references_for_mechanism_mainline_and_empirical_claim_boundary",
            "main_text_reference_audit_metadata_excluded": True,
            "world_descriptive_research_entries": 42,
            "world_descriptive_exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "realized_richness_reframe_complete": True,
            "realized_richness_mean_geometry": "all_positive_in_6_of_6_matching_seeds",
            "realized_richness_mixed_individual_realizations": "51_to_65_of_96",
            "realized_richness_nonadditivity_fraction": "0.4272_to_0.4851",
            "system_size_rank_crossover": {
                "k_values": [1, 2, 4, 8, 16],
                "median_starting_share_percent": [2.55, 10.33, 27.33, 42.52, 55.84],
                "median_community_share_percent": [72.98, 48.03, 23.52, 18.26, 12.72],
                "starting_exceeds_community_from_k4": "6_of_6_seeds",
                "mixed_at_k16": "28_to_42_of_96",
                "natural_threshold_claimed": False,
            },
            "izu_e3_e4_status": "future_optional_validation_not_completion_gate",
            "chapter3_direct_phenotype_used_as_validation": False,
            "corresponding_author_orcid_required": True,
            "planned_public_repository_named": True,
            "significance_prior_work_context_included": True,
            "submission_manuscript_internal_thesis_language_removed_fail_closed": True,
            "supporting_information_superseded_nonadditivity_wording_removed_fail_closed": True,
            "oikos_significance_statement_included": True,
            "oikos_submission_statements_included": True,
            "oikos_data_code_ready_for_first_submission": True,
            "figures_regenerated_from_frozen_gate": True,
            "model_gate": gate.get("status"),
            "files": [
                SUBMISSION_MANUSCRIPT_NAME,
                SUBMISSION_SI_NAME,
                *STATIC_SUBMISSION_FILES,
                *figure_files,
                RELATIONAL_FIGURE_INPUTS_ARCNAME,
                TITLE_PAGE_NAME,
                COVER_LETTER_NAME,
                SIGNIFICANCE_NAME,
                STATEMENTS_NAME,
                "anonymous_review_archive.zip",
            ],
            "boundary": (
                "The submission is organized around synthetic conditional response geometry, exact realized-richness control, and a prespecified system-size determinant-rank crossover. "
                "Exact realized-richness matching shifts the ensemble mean geometry to all-positive in all six matching seeds while individual branching and state-by-community nonadditivity remain. "
                "Under active plant adjustment the additive determinant ordering reverses across the declared k sequence, but the numerical crossover is model-specific and is not transferred to nature. "
                "World and Izu evidence bound biological plausibility and historical identifiability; field E3/E4 remains optional future validation rather than a submission gate."
            ),
        }

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for generated in (manuscript, supporting_information, title_page, cover_letter, significance, statements, review_archive):
                archive.write(generated, arcname=generated.name)
            for rel in STATIC_SUBMISSION_FILES:
                archive.write(ROOT / rel, arcname=rel)
            for rel in figure_files:
                archive.write(ROOT / rel, arcname=rel)
            archive.write(RELATIONAL_FIGURE_INPUTS, arcname=RELATIONAL_FIGURE_INPUTS_ARCNAME)
            archive.writestr(
                "SUBMISSION_BUNDLE_MANIFEST.json",
                json.dumps(bundle_manifest, indent=2, ensure_ascii=False) + "\n",
            )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = build_submission_bundle(args.metadata, args.output)
    print(path)


if __name__ == "__main__":
    main()
