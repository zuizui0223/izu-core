"""Versioned manuscript length, anonymity and ecological-claim admission.

Does not change the 2026-10-10 route, original manuscript, figures, underlying
simulation readouts or source-pinned submission builder. Not a DOI deposit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_RECONCILED_20261017.md"
REQUIRED_SECTIONS = (
    "## Abstract", "## Keywords", "# Introduction", "# Materials and Methods",
    "# Results", "# Discussion", "# Conclusion",
    "# Primary figure assembly and captions", "# Data accessibility",
    "## Evidence hierarchy and study-origin record", "# References",
)
REQUIRED_CLAIMS = (
    "fixed at 0.5", "Both co-primary intervals included zero",
    "703/2,304", "3/32", "2/32", "A evolvability **continued during the future**",
    "not a natural mediation analysis",
    "but in only three of four new crossed-founder settings",
)
DENIED = ("zuizui0223", "github.com/", "/workspace/", "/home/", "/root/",
          "issue #436", "pr #452", "pr #455")


def lengths(source: str) -> dict[str, int]:
    return {
        "abstract": len(source.split("## Abstract", 1)[1].split("## Keywords", 1)[0].split()),
        "main_text": len(source.split("# Introduction", 1)[1].split(
            "# Primary figure assembly and captions", 1)[0].split()),
    }


def verify_source(source: str) -> dict[str, int]:
    lines = source.splitlines()
    if not lines or not lines[0].startswith(
        "# Temporal precedence is not evolutionary necessity:"
    ):
        raise ValueError("Reconciled manuscript title differs")
    if any(lines.count(section) != 1 for section in REQUIRED_SECTIONS):
        raise ValueError("Missing/duplicated manuscript section")
    if any(lines.index(a) >= lines.index(b) for a, b in zip(
        REQUIRED_SECTIONS, REQUIRED_SECTIONS[1:]
    )):
        raise ValueError("Manuscript section order differs")
    for claim in REQUIRED_CLAIMS:
        if claim not in source:
            raise ValueError("Critical ecological claim or null boundary missing: " + claim)
    if "The original four-setting test passed" not in source:
        raise ValueError("Original Q1 confirmatory result missing")
    if "assurance-cost interval crossed zero" not in source:
        raise ValueError("Fresh-founder Q1 uncertainty missing")
    if "Density is **not** the ABM stochastic expectation" not in source:
        raise ValueError("Approximate deterministic counterfactual overstated")
    n = lengths(source)
    if not 100 <= n["abstract"] <= 150 or not 2000 <= n["main_text"] <= 5000:
        raise ValueError("Reconciled manuscript exceeds EL letter limits or is truncated")
    return n


def anonymous_review_text(source: str) -> str:
    """Make a derivative, following the existing single-paper reviewer redaction.

    Source manuscript and historical SI are never overwritten. The return
    is a preview for author/editor review; it is not a submission packet.
    """
    verify_source(source)
    title = source.splitlines()[0]
    manuscript = title + "\n\n## Abstract" + source.split("## Abstract", 1)[1]
    before, after = manuscript.split("## Evidence hierarchy and study-origin record", 1)
    if "# References" not in after:
        raise ValueError("Original references missing after provenance section")
    manuscript = before + "# References" + after.split("# References", 1)[1]
    start, end = manuscript.index("# Data accessibility"), manuscript.index("# References")
    disclosure = (
        "# Data accessibility\n\n"
        "Frozen source, model designs and the distinct evidence cohorts are retained "
        "with verification receipts. Permanent, independently downloadable DOI-backed "
        "raw-data deposition has not yet been completed. Editorial approval and a "
        "versioned, anonymized data-access plan are required before submission.\n\n"
    )
    manuscript = manuscript[:start] + disclosure + manuscript[end:]
    figure_path = "figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg"
    manuscript = manuscript.replace("../" + figure_path, "Figure4.svg")
    manuscript = manuscript.replace(figure_path, "Figure4.svg")
    manuscript = manuscript.replace(
        "generated without refitting by " +
        chr(96) + "scripts/render_chapter2_capacity_companion_evidence_figure.py" + chr(96),
        "generated without refitting from the original cohort readouts",
    )
    manuscript = manuscript.replace(
        chr(96) + "docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md" + chr(96),
        "Supporting Information S3",
    )
    if re.search(
        r"(?<!\w)(?:docs|figures|data/design|data/results|scripts)/[A-Za-z0-9_./-]+",
        manuscript,
    ):
        raise ValueError("Unmapped project path remains in anonymous review manuscript")
    if any(term in manuscript.lower() for term in DENIED):
        raise ValueError("Identifying internal token in anonymous manuscript")
    result = lengths(manuscript)
    if result["abstract"] > 150 or result["main_text"] > 5000:
        raise ValueError("Anonymous reviewer manuscript word limit exceeded")
    return manuscript.rstrip() + "\n"


def audit(root: Path = ROOT) -> dict:
    original = (root / SOURCE.relative_to(ROOT)).read_bytes()
    source = original.decode("utf-8")
    source_n = verify_source(source)
    anonymous = anonymous_review_text(source)
    return {
        "schema": "chapter2_reconciled_manuscript_review_v1",
        "status": "WORD_COUNT_AND_ANONYMITY_PASS_NOT_SUBMITTED",
        "source_sha256": hashlib.sha256(original).hexdigest(),
        "anonymous_sha256": hashlib.sha256(anonymous.encode("utf-8")).hexdigest(),
        "source_word_counts": source_n,
        "anonymous_word_counts": lengths(anonymous),
        "figure_roster": ["Figure1.pdf", "Figure2.pdf", "Figure3.pdf", "Figure4.svg",
                          "SupplementaryFigureS1.pdf", "SupplementaryFigureS2.svg",
                          "SupplementaryFigureS3.pdf"],
        "figure_bytes_reverified_in_this_audit": False,
        "registered_results_modified": False,
        "external_doi_deposited": False,
        "original_manuscript_overwritten": False,
        "not_claimed": [
            "Independent biological regeneration",
            "Journal submission or editorial acceptance",
            "External DOI-backed raw archive",
            "S1-S33 source SI rewrite",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=ROOT)
    p.add_argument("--anonymous-out", type=Path,
                   help="Optional versioned reviewer-only Markdown output; refuses overwrite.")
    options = p.parse_args()
    report = audit(options.repo_root)
    if options.anonymous_out:
        if options.anonymous_out.exists():
            p.error("Refusing to overwrite existing reviewer draft")
        text = (options.repo_root / SOURCE.relative_to(ROOT)).read_text(encoding="utf-8")
        options.anonymous_out.parent.mkdir(parents=True, exist_ok=True)
        options.anonymous_out.write_text(anonymous_review_text(text), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
