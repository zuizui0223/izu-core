"""Render a source-locked NEE Article *author preview* from the admitted master.

Formatting only: no biological simulation, changed figures, claims, references,
post-hoc inference, licence, journal submission or DOI. No files overwritten.
The original source master remains the canonical scientific record.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MASTER = "docs/CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md"
TITLE = "Founding constraints and the predictability of reproductive evolution in an island plant model"
STATUS = "NEE_ARTICLE_FORMAT_PREVIEW_NOT_AUTHOR_APPROVED_NOT_SUBMITTED"
HEADINGS = (
    "## Abstract\n",
    "## Introduction\n",
    "## Results\n",
    "## Discussion\n",
    "## Online Methods",
    "## Figure legends",
    "## Data availability\n",
    "## References",
)
ABSTRACT_LIMIT = 200
MAIN_LIMIT = 3500
DISCUSSION_SUBHEADS = (
    "Arrival:", "After arrival:", "Assurance changes floral evolution",
    "Finite populations", "Persistence and retained options",
    "Subsequent environments:", "Scope and limitations",
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError("NEE Article author-review preflight: " + message)


def words(text: str) -> int:
    return len(text.split())


def render(master: str, source_sha: str = "UNKNOWN") -> tuple[str, dict]:
    require(master.startswith("# " + TITLE + "\n"), "unexpected master title")
    require(len(source_sha) == 40 or source_sha == "UNKNOWN", "invalid source commit")
    starts = [master.find(h) for h in HEADINGS]
    require(all(p >= 0 and master.count(h) == 1 for p, h in zip(starts, HEADINGS)),
            "master section heading mismatch")
    require(starts == sorted(starts), "master section order mismatch")
    require("## Planned new decisive Results" not in master,
            "historical unexecuted results included")
    lead = master[:starts[0]]
    require(lead.startswith("# " + TITLE + "\n")
            and "Completed-evidence editorial extract" in lead,
            "expected historical editorial lead not identified")
    abstract = master[starts[0] + len(HEADINGS[0]):starts[1]]
    introduction = master[starts[1] + len(HEADINGS[1]):starts[2]]
    results = master[starts[2] + len(HEADINGS[2]):starts[3]]
    discussion = master[starts[3] + len(HEADINGS[3]):starts[4]]
    methods_to_end = master[starts[4]:]

    headings = re.findall(r"(?m)^### (.+)$", discussion)
    require(len(headings) == len(DISCUSSION_SUBHEADS)
            and all(h.startswith(needle) for h, needle in
                    zip(headings, DISCUSSION_SUBHEADS)),
            "expected seven Discussion editorial navigation subheads changed")
    discussion_prose = re.sub(r"(?m)^### .+\n(?:\n)?", "", discussion)
    require(not re.search(r"(?m)^#{1,6} ", discussion_prose),
            "Discussion remains subdivided")
    assert "### R1" in results and "### R5" in results
    result_labels = re.findall(r"(?m)^### R([1-5]) — ", results)
    require(result_labels == ["1", "2", "3", "4", "5"],
            "five current result sections changed")
    require("post-outcome joint analysis" in discussion_prose,
            "post-outcome result not visibly qualified")
    require("registered" in results.lower() and "post-outcome" in results,
            "source inferential-rank labels absent")
    require("## Online Methods — completed studies\n" in methods_to_end
            and "## Figure legends — source-linked vector drafts\n" in methods_to_end
            and "## References — preliminary\n" in methods_to_end,
            "status-bounded master format changed")

    methods_to_end = methods_to_end.replace(
        "## Online Methods — completed studies\n", "## Online Methods\n", 1)
    methods_to_end = methods_to_end.replace(
        "## Figure legends — source-linked vector drafts\n", "## Figure legends\n", 1)
    methods_to_end = methods_to_end.replace(
        "## References — preliminary\n", "## References\n", 1)

    formatted = ("# " + TITLE + "\n\n## Abstract\n" + abstract
                 + "\n" + introduction + "## Results\n" + results
                 + "## Discussion\n" + discussion_prose + methods_to_end)
    # No hidden editorial claims: all surviving Introduction/Results/Discussion
    # prose must match exactly after just deleting the seven subheading labels.
    result_in = results
    result_out = formatted.split("## Results\n", 1)[1].split("## Discussion\n", 1)[0]
    require(result_in == result_out, "scientific Results altered")
    discussion_out = formatted.split("## Discussion\n", 1)[1].split(
        "## Online Methods\n", 1)[0]
    require(discussion_out == discussion_prose, "scientific Discussion prose altered")
    require(formatted.count("## Introduction") == 0
            and formatted.count("## Discussion\n") == 1,
            "NEE Article section titles")
    require(not re.search(r"(?m)^### ", discussion_out),
            "NEE Article Discussion must be unheaded")

    aw = words(abstract)
    iw = words(introduction)
    mw = words(introduction + results + discussion_prose)
    figure_legends = formatted.split("## Figure legends\n", 1)[1].split(
        "## Data availability\n", 1)[0]
    legend_numbers = [int(x) for x in re.findall(
        r"(?m)^\d+\.\s+\*\*Figure\s+(\d+)", figure_legends)]
    require(100 <= aw <= ABSTRACT_LIMIT, "NEE 200-word abstract bound")
    require(400 <= iw <= 650, "NEE circa-500 Introduction guide")
    require(2500 <= mw <= MAIN_LIMIT, "NEE 3500-word main-text bound")
    require(legend_numbers == [1, 2, 3, 4, 5, 6],
            "NEE six-display maximum or figure sequence changed")
    require("0.08328125" not in abstract, "accidental p-value insertion")
    require("not an Ecology Letters submission" in formatted
            and "a deposited raw-data DOI" in formatted,
            "data-availability DOI limitation omitted")
    require("#### #" not in formatted and "## Planned new" not in formatted,
            "unexecuted/presentation content")

    report = {
        "status": STATUS, "original_article_master": MASTER,
        "source_commit": source_sha,
        "master_sha256": sha256(master.encode("utf8")).hexdigest(),
        "formatted_sha256": sha256(formatted.encode("utf8")).hexdigest(),
        "format_changes_only": [
            "Remove repository-internal editorial title-page note",
            "Remove Introduction heading, retain all five original paragraphs",
            "Remove seven Discussion navigation subheadings, retain all prose",
            "Normalize display-only Online Methods, Figure legends and References headings",
        ],
        "abstract_words": aw,
        "intro_words": iw,
        "main_words": mw,
        "results_topical_headings": 5,
        "discussion_subheadings": 0,
        "figure_legends": 6,
        "new_biological_simulations": 0,
        "new_scientific_inference": False,
        "registered_G_S_unchanged": True,
        "posthoc_joint_access_remains_explicitly_descriptive": True,
        "references_formatted_and_verified_by_author": False,
        "author_order_and_approval_complete": False,
        "data_code_external_deposit_doi_verified": False,
        "final_journal_artwork_approved": False,
        "article_formally_submitted": False,
        "original_relative_markdown_source_links_require_repository": True,
    }
    return formatted, report


def publish(root: Path, out: Path, report_path: Path,
            source_sha: str = "UNKNOWN") -> dict:
    root, out, report_path = Path(root), Path(out), Path(report_path)
    require(out.resolve() != report_path.resolve(), "output/report locations collide")
    require(not out.exists() and not report_path.exists(), "refuse overwriting outputs")
    raw = (root / MASTER).read_text(encoding="utf8")
    output, report = render(raw, source_sha)
    out.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf8") as f:
        f.write(output)
    with report_path.open("x", encoding="utf8") as f:
        json.dump(report, f, indent=2, sort_keys=True, ensure_ascii=False,
                  allow_nan=False)
        f.write("\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--source-commit", default="UNKNOWN")
    args = parser.parse_args()
    d = publish(args.root, args.out, args.report, args.source_commit)
    print(json.dumps({"status": STATUS, "abstract": d["abstract_words"],
                      "main": d["main_words"], "new_simulations": 0}))


if __name__ == "__main__":
    main()
