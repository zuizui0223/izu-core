from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from scripts.render_chapter2_nee_v03_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_4_SUBMISSION_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_4_SUBMISSION_20260915.md"
REFERENCE_LEDGER = ROOT / "docs/CHAPTER2_NEE_REFERENCE_LEDGER_20260915.md"
AUTHOR_PROVENANCE = ROOT / "docs/CHAPTER2_AUTHOR_METADATA_PROVENANCE_20260912.md"
DEFAULT_OUT = ROOT / "dist/chapter2_nee_presubmission"

UNRESOLVED_AUTHOR_CONTROLLED = [
    "final author list and order",
    "corresponding-author designation",
    "ORCID(s)",
    "all-author approval",
    "funding / acknowledgements / competing interests / submission declarations",
]
UNRESOLVED_ARCHIVE = [
    "permanent archived code/data release DOI",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build(out_dir: Path = DEFAULT_OUT) -> Path:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    manuscript_dst = out_dir / "manuscript.md"
    cover_dst = out_dir / "cover_letter.md"
    refs_dst = out_dir / "reference_provenance.md"
    shutil.copy2(MANUSCRIPT, manuscript_dst)
    shutil.copy2(COVER, cover_dst)
    shutil.copy2(REFERENCE_LEDGER, refs_dst)

    rendered = render_all(fig_dir)
    pdfs = sorted(path for path in rendered if path.suffix == ".pdf")
    svgs = sorted(path for path in rendered if path.suffix == ".svg")
    if len(pdfs) != 4 or len(svgs) != 4:
        raise RuntimeError(f"expected four PDF and four SVG figures, got {len(pdfs)} PDF / {len(svgs)} SVG")

    manifest = {
        "schema_version": "1.0",
        "status": "PRESUBMISSION_NOT_FINAL",
        "active_manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "active_cover_letter": str(COVER.relative_to(ROOT)),
        "reference_ledger": str(REFERENCE_LEDGER.relative_to(ROOT)),
        "author_metadata_provenance": str(AUTHOR_PROVENANCE.relative_to(ROOT)),
        "files": {},
        "blocking_author_controlled_fields": UNRESOLVED_AUTHOR_CONTROLLED,
        "blocking_archive_field": UNRESOLVED_ARCHIVE,
        "finalization_rule": (
            "Do not relabel this archive as a final journal submission bundle until the author-controlled fields "
            "and permanent archive DOI are explicitly supplied and validated. Scientific analyses, route metrics, "
            "natural-source membership and candidate search remain frozen."
        ),
    }
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
        rel = str(path.relative_to(out_dir))
        manifest["files"][rel] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    manifest_path = out_dir / "PRESUBMISSION_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    zip_path = out_dir.parent / "chapter2_nee_presubmission_bundle.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
            zf.write(path, arcname=str(path.relative_to(out_dir)))
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    print(build(args.out_dir))


if __name__ == "__main__":
    main()
