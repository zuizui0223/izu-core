from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

FINAL_TITLE = (
    "Response geometry under community reorganization: from ecological possibility "
    "to mechanistic resolution in island plant–pollinator systems"
)

INTRO_THESIS_PARAGRAPH = (
    "That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent "
    "winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, "
    "numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher "
    "resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background "
    "community-composition structure versus additional within-community non-random partner sorting. Chapter 2 ends at this "
    "distinction and at the measurements still required to connect matching to reproduction; Chapter 3 is the next measurement "
    "stage, not causal validation of the present model."
)

INTRO_STANDALONE_PARAGRAPH = (
    "That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent "
    "winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, "
    "numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher "
    "resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background "
    "community-composition structure versus additional within-community non-random partner sorting. The analysis ends at this "
    "distinction and at the prospective measurements still required to connect matching to reproductive propagation."
)

THESIS_SECTION_RE = re.compile(
    r"\n## Chapter 2 hands a measurement contract to Chapter 3\n.*?(?=\n## Limits and decisive next measurement\n)",
    flags=re.DOTALL,
)

FORBIDDEN_SUBMISSION_TOKENS = (
    "At the dissertation scale",
    "preceding comparative chapter",
    "## From Chapter 1 to Chapter 3",
    "Chapter 1",
    "Chapter 2",
    "Chapter 3",
    "Campanula microdonta",
    "**Status:** active working manuscript",
    "**Inference architecture:**",
    "**Controlling state:**",
    "## Working title",
)


def render_submission_manuscript(source: Path = SOURCE) -> str:
    text = source.read_text(encoding="utf-8")

    working_title_block = (
        "# Response geometry under community reorganization\n\n"
        "**Status:** active working manuscript v2 — mechanistic-funnel reconstruction; not submission-ready\n"
        "**Updated:** 2026-08-28\n"
        "**Inference architecture:** model possibilities → world confrontation → identifiability bottleneck → focal Izu mechanistic-resolution zoom\n"
        "**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `data/design/chapter2_active_manuscript_mainline_20260827.json`, `data/results/chapter2_scientific_gate_final_20260827.json`\n\n"
        "## Working title\n\n"
        f"**{FINAL_TITLE}**"
    )
    if working_title_block not in text:
        raise ValueError("active manuscript header changed; refuse to render submission manuscript silently")
    text = text.replace(working_title_block, f"# {FINAL_TITLE}", 1)

    if INTRO_THESIS_PARAGRAPH not in text:
        raise ValueError("thesis-specific Introduction bridge changed; refuse silent submission rendering")
    text = text.replace(INTRO_THESIS_PARAGRAPH, INTRO_STANDALONE_PARAGRAPH, 1)

    text, n_removed = THESIS_SECTION_RE.subn("\n", text, count=1)
    if n_removed != 1:
        raise ValueError("thesis Chapter 1-to-3 section not found exactly once")

    text = text.replace(
        "the remaining effectiveness-to-reproduction contract is handed to Chapter 3 without validation claims.",
        "the remaining effectiveness-to-reproduction contract is retained as a prospective measurement target.",
        1,
    )

    # Submission source should not expose repository-internal reference routing instructions.
    text = re.sub(
        r"\n## References\n\nUse the source-audited active reference ledger in `[^`]+`\. "
        r"Hiraiwa & Ushimaru \(2017, 2024\) are the empirical sources for the Izu triangulation\. "
        r"External-system references remain in the comparative-grounding supplement and are not presented as validation coverage\.\s*$",
        "\n## References\n\nReferences are supplied in the accompanying reference list.\n",
        text,
        flags=re.DOTALL,
    )

    for token in FORBIDDEN_SUBMISSION_TOKENS:
        if token.lower() in text.lower():
            raise ValueError(f"submission manuscript still contains internal token: {token}")

    if "null-corrected matching" not in text.lower():
        raise ValueError("Izu structural negative control disappeared from submission manuscript")
    if "80.17%" not in text:
        raise ValueError("community-realization diagnostic disappeared from submission manuscript")
    if "41" not in text or "96" not in text:
        raise ValueError("baseline response-geometry counts disappeared from submission manuscript")

    return text.rstrip() + "\n"


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    text = render_submission_manuscript()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(render_to_path(args.output))


if __name__ == "__main__":
    main()
