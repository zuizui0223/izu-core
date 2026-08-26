from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.build_island_ecology_manuscript_v3 import build_manuscript
from scripts.build_island_ecology_review_archive import build_archive as build_review_archive
from scripts.build_island_ecology_submission_metadata import (
    load_metadata,
    render_cover_letter,
    render_title_page,
    validate_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "dist/island_ecology_jecology_submission_bundle.zip"
REASSESSMENT_GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"
MANUSCRIPT_ARCNAME = "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"

STATIC_SUBMISSION_FILES = (
    "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md",
    "docs/ISLAND_ECOLOGY_FIGURE_CAPTIONS_20260824.md",
    "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md",
    "data/design/island_ecology_jecology_submission_manifest.json",
)


def validate_scientific_gate() -> None:
    if not REASSESSMENT_GATE.exists():
        return
    gate = json.loads(REASSESSMENT_GATE.read_text(encoding="utf-8"))
    if gate.get("current_research_article_submission_ready") is not True:
        raise ValueError(
            "scientific reassessment gate is open; complete the response-geometry / "
            "parameter-robustness gate before building a submission bundle"
        )


def build_submission_bundle(metadata_path: Path, output: Path) -> Path:
    validate_scientific_gate()

    metadata = load_metadata(metadata_path)
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))

    for rel in STATIC_SUBMISSION_FILES:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        title_page = tmp / "ISLAND_ECOLOGY_TITLE_PAGE.md"
        cover_letter = tmp / "ISLAND_ECOLOGY_COVER_LETTER.md"
        review_archive = tmp / "island_ecology_anonymous_review_archive.zip"
        manuscript = tmp / "ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"
        title_page.write_text(render_title_page(metadata), encoding="utf-8")
        cover_letter.write_text(render_cover_letter(metadata), encoding="utf-8")
        build_manuscript(manuscript)
        build_review_archive(review_archive)

        bundle_manifest = {
            "journal": metadata["journal"],
            "article_type": metadata["article_type"],
            "scientific_state": "submission_ready_after_reassessment",
            "manuscript_state": "editorial_v3_rendered_from_frozen_v2_source",
            "author_metadata_source": metadata_path.name,
            "review_archive_anonymous": True,
            "files": [
                MANUSCRIPT_ARCNAME,
                *STATIC_SUBMISSION_FILES,
                "ISLAND_ECOLOGY_TITLE_PAGE.md",
                "ISLAND_ECOLOGY_COVER_LETTER.md",
                "island_ecology_anonymous_review_archive.zip",
            ],
            "boundary": "Packaging does not rerun scientific analysis and is blocked while the reassessment gate is open.",
        }

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(manuscript, arcname=MANUSCRIPT_ARCNAME)
            for rel in STATIC_SUBMISSION_FILES:
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
