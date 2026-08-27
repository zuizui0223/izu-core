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
    render_title_page,
    validate_metadata,
)
from scripts.generate_chapter2_manuscript_figures import build_figures

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "dist/island_ecology_jecology_submission_bundle.zip"
REASSESSMENT_GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
MANUSCRIPT = "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"

STATIC_SUBMISSION_FILES = (
    MANUSCRIPT,
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "data/design/island_ecology_jecology_submission_manifest.json",
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

    for rel in STATIC_SUBMISSION_FILES:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)

    figure_payload = build_figures()
    figure_files = tuple(figure_payload["figure_outputs"])
    for rel in figure_files:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        title_page = tmp / "ISLAND_ECOLOGY_TITLE_PAGE.md"
        cover_letter = tmp / "ISLAND_ECOLOGY_COVER_LETTER.md"
        review_archive = tmp / "island_ecology_anonymous_review_archive.zip"
        title_page.write_text(render_title_page(metadata), encoding="utf-8")
        cover_letter.write_text(render_cover_letter(metadata), encoding="utf-8")
        build_review_archive(review_archive)

        bundle_manifest = {
            "journal": metadata["journal"],
            "article_type": metadata["article_type"],
            "scientific_state": "model_gate_closed_conditional_response_geometry_with_focal_izu_triangulation",
            "manuscript_state": "active_v2_20260827",
            "author_metadata_source": metadata_path.name,
            "review_archive_anonymous": True,
            "figures_regenerated_fail_closed": True,
            "model_gate": gate.get("status"),
            "files": [
                *STATIC_SUBMISSION_FILES,
                *figure_files,
                "ISLAND_ECOLOGY_TITLE_PAGE.md",
                "ISLAND_ECOLOGY_COVER_LETTER.md",
                "island_ecology_anonymous_review_archive.zip",
            ],
            "boundary": (
                "Packaging uses the Chapter 2 v2 active manuscript: synthetic response geometry is the primary analysis; "
                "Izu is focal empirical triangulation at the source-state/community-composition level and is not treated as "
                "validation of synthetic thresholds or as evidence for non-random partner sorting beyond background composition. "
                "Figure regeneration must match the frozen Chapter 2 scientific gate. Metadata validation remains fail-closed."
            ),
        }

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for rel in STATIC_SUBMISSION_FILES:
                archive.write(ROOT / rel, arcname=rel)
            for rel in figure_files:
                archive.write(ROOT / rel, arcname=rel)
            archive.write(title_page, arcname=title_page.name)
            archive.write(cover_letter, arcname=cover_letter.name)
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
