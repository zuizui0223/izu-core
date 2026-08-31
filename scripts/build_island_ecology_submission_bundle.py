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
    render_title_page,
    validate_metadata,
)
from scripts.generate_chapter2_manuscript_figures_relational import build_figures
from scripts.render_chapter2_supporting_information import render_to_path as render_si_to_path
from scripts.render_island_ecology_submission_manuscript import render_to_path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "dist/chapter2_oikos_submission_bundle.zip"
REASSESSMENT_GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
SOURCE_MANUSCRIPT = "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
SUBMISSION_MANUSCRIPT_NAME = "MANUSCRIPT.md"
SUBMISSION_SI_NAME = "SUPPORTING_INFORMATION.md"
ACTIVE_SUBMISSION_MANIFEST = "data/design/chapter2_oikos_submission_manifest_20260831.json"
RELATIONAL_FIGURE_INPUTS_ARCNAME = "data/results/chapter2_manuscript_figure_inputs_relational_20260831.json"
RELATIONAL_FIGURE_INPUTS = ROOT / RELATIONAL_FIGURE_INPUTS_ARCNAME

STATIC_SUBMISSION_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md",
    "data/design/chapter2_relational_robustness_audit_freeze_20260831.json",
    "data/results/chapter2_relational_robustness_audit_frozen_20260831.json",
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
    return gate


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
        title_page = tmp / "TITLE_PAGE.md"
        cover_letter = tmp / "COVER_LETTER.md"
        significance = tmp / "SIGNIFICANCE_STATEMENT.md"
        review_archive = tmp / "anonymous_review_archive.zip"
        render_to_path(manuscript)
        render_si_to_path(supporting_information)
        title_page.write_text(render_title_page(metadata), encoding="utf-8")
        cover_letter.write_text(render_cover_letter(metadata), encoding="utf-8")
        significance.write_text(render_significance_statement(metadata), encoding="utf-8")
        build_review_archive(review_archive)

        bundle_manifest = {
            "journal": metadata["journal"],
            "article_type": metadata["article_type"],
            "scientific_state": "relational_response_geometry_with_structural_robustness_and_bounded_empirical_resolution",
            "manuscript_state": "active_20260831_relational_source_rendered_to_oikos_clean_submission",
            "source_manuscript": SOURCE_MANUSCRIPT,
            "submission_manuscript": SUBMISSION_MANUSCRIPT_NAME,
            "submission_supporting_information": SUBMISSION_SI_NAME,
            "active_submission_manifest": ACTIVE_SUBMISSION_MANIFEST,
            "author_metadata_source": metadata_path.name,
            "review_archive_anonymous": True,
            "submission_manuscript_internal_thesis_language_removed_fail_closed": True,
            "supporting_information_superseded_nonadditivity_wording_removed_fail_closed": True,
            "oikos_significance_statement_included": True,
            "oikos_data_code_ready_for_first_submission": True,
            "figures_regenerated_from_frozen_gate_then_relational_overlay": True,
            "model_gate": gate.get("status"),
            "files": [
                SUBMISSION_MANUSCRIPT_NAME,
                SUBMISSION_SI_NAME,
                *STATIC_SUBMISSION_FILES,
                *figure_files,
                RELATIONAL_FIGURE_INPUTS_ARCNAME,
                "TITLE_PAGE.md",
                "COVER_LETTER.md",
                "SIGNIFICANCE_STATEMENT.md",
                "anonymous_review_archive.zip",
            ],
            "boundary": (
                "The historical Chapter 2 freeze chain remains unchanged. Packaging renders the 2026-08-31 relational manuscript and a corrected "
                "Supporting Information surface that supersedes the old within-cell-noise interpretation without rewriting historical frozen inputs. "
                "The exact 80.17/17.64/2.18% baseline decomposition remains one frozen example; structural inference is based on component ordering, "
                "state-by-community nonadditivity and prespecified seed/horizon/trait-adjustment/equal-richness sensitivities. World confrontation is "
                "reported as an outcome-rich/process-poor measurement audit, and Izu remains a mechanistic-resolution analysis rather than validation."
            ),
        }

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(manuscript, arcname=SUBMISSION_MANUSCRIPT_NAME)
            archive.write(supporting_information, arcname=SUBMISSION_SI_NAME)
            for rel in STATIC_SUBMISSION_FILES:
                archive.write(ROOT / rel, arcname=rel)
            for rel in figure_files:
                archive.write(ROOT / rel, arcname=rel)
            archive.write(RELATIONAL_FIGURE_INPUTS, arcname=RELATIONAL_FIGURE_INPUTS_ARCNAME)
            archive.write(title_page, arcname=title_page.name)
            archive.write(cover_letter, arcname=cover_letter.name)
            archive.write(significance, arcname=significance.name)
            archive.write(review_archive, arcname=review_archive.name)
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
