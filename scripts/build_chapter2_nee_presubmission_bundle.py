from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from scripts.render_chapter2_nee_v04_submission_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_4_SUBMISSION_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_4_SUBMISSION_20260915.md"
REFERENCE_LEDGER = ROOT / "docs/CHAPTER2_NEE_REFERENCE_LEDGER_20260915.md"
SOURCE_LEVERAGE_SUPPLEMENT = ROOT / "docs/CHAPTER2_NEE_SUPPLEMENTARY_SOURCE_LEVERAGE_20260915.md"
AUTHOR_PROVENANCE = ROOT / "docs/CHAPTER2_AUTHOR_METADATA_PROVENANCE_20260912.md"
AUTHOR_INTAKE = ROOT / "data/design/chapter2_nee_initial_submission_metadata.json"
ALL_SOURCE_LOO = ROOT / "data/results/chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
SOURCE_ROBUSTNESS_CLOSURE = ROOT / "data/results/chapter2_natural_regime_source_robustness_challenge_closure_20260915.json"
POSTFREEZE_CODE_REVIEW_CLOSURE = ROOT / "data/results/chapter2_postfreeze_code_review_closure_20260923.json"
DEFAULT_OUT = ROOT / "dist/chapter2_nee_presubmission"

INITIAL_SUBMISSION_BLOCKERS = [
    "peer-review model selection (single-anonymized or double-anonymized)",
    "final author list, order, affiliations and exactly one corresponding-author designation",
    "related-manuscript disclosure and prior Nature Ecology & Evolution editor discussion disclosure",
    "all-author approval",
    "acknowledgements / relevant funding / competing interests / submission declarations",
    "author confirmation of the manuscript-specific ethics statement",
    "author-reviewed LLM-use statement consistent with Nature Ecology & Evolution policy",
]
PREPUBLICATION_PENDING = [
    "corresponding-author ORCID linkage before final acceptance",
    "permanent archived code/data release DOI before publication",
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
    provenance_dir = out_dir / "provenance"
    provenance_dir.mkdir(parents=True, exist_ok=True)

    manuscript_dst = out_dir / "manuscript.md"
    cover_dst = out_dir / "cover_letter.md"
    refs_dst = out_dir / "reference_provenance.md"
    supplement_dst = out_dir / "supplementary_source_leverage.md"
    intake_dst = out_dir / "author_intake.json"
    loo_dst = provenance_dir / "all_source_leave_one_out.json"
    challenge_dst = provenance_dir / "source_robustness_challenge_closure.json"
    code_review_dst = provenance_dir / "postfreeze_code_review_closure.json"
    shutil.copy2(MANUSCRIPT, manuscript_dst)
    shutil.copy2(COVER, cover_dst)
    shutil.copy2(REFERENCE_LEDGER, refs_dst)
    shutil.copy2(SOURCE_LEVERAGE_SUPPLEMENT, supplement_dst)
    shutil.copy2(AUTHOR_INTAKE, intake_dst)
    shutil.copy2(ALL_SOURCE_LOO, loo_dst)
    shutil.copy2(SOURCE_ROBUSTNESS_CLOSURE, challenge_dst)
    shutil.copy2(POSTFREEZE_CODE_REVIEW_CLOSURE, code_review_dst)

    rendered = render_all(fig_dir)
    pdfs = sorted(path for path in rendered if path.suffix == ".pdf")
    svgs = sorted(path for path in rendered if path.suffix == ".svg")
    if len(pdfs) != 4 or len(svgs) != 4:
        raise RuntimeError(f"expected four PDF and four SVG figures, got {len(pdfs)} PDF / {len(svgs)} SVG")

    manifest = {
        "schema_version": "1.4",
        "status": "PRESUBMISSION_NOT_FINAL",
        "active_manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "active_cover_letter": str(COVER.relative_to(ROOT)),
        "reference_ledger": str(REFERENCE_LEDGER.relative_to(ROOT)),
        "source_leverage_supplement": str(SOURCE_LEVERAGE_SUPPLEMENT.relative_to(ROOT)),
        "author_metadata_provenance": str(AUTHOR_PROVENANCE.relative_to(ROOT)),
        "author_intake": str(AUTHOR_INTAKE.relative_to(ROOT)),
        "analysis_provenance": {
            "all_source_leave_one_out": str(ALL_SOURCE_LOO.relative_to(ROOT)),
            "source_robustness_challenge_closure": str(SOURCE_ROBUSTNESS_CLOSURE.relative_to(ROOT)),
            "postfreeze_code_review_closure": str(POSTFREEZE_CODE_REVIEW_CLOSURE.relative_to(ROOT)),
        },
        "files": {},
        "initial_submission_blockers": INITIAL_SUBMISSION_BLOCKERS,
        "prepublication_pending_not_initial_submission_blockers": PREPUBLICATION_PENDING,
        "finalization_rule": (
            "Do not relabel this archive as an initial-submission-ready journal bundle until the NEE author-intake "
            "metadata validates without errors. ORCID linkage and a permanent archive DOI remain tracked prepublication "
            "tasks but do not block initial editorial submission under the current NEE guidance. Scientific analyses, route "
            "metrics, natural-source membership and candidate-search closures remain frozen."
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
