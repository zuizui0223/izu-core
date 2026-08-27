from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

FINAL_TITLE = (
    "Conditional response geometry under island pollinator reorganization: "
    "from synthetic regime structure to source-state matching in the Izu Islands"
)

INTRO_THESIS_PARAGRAPH = (
    "At the dissertation scale, the preceding comparative chapter supplies the when/where handoff: "
    "isolation-associated floral and reproductive filtering is detectable in multiple biogeographic contexts, "
    "but the observed multivariate response vectors differ. That result does not by itself identify why the vectors differ. "
    "It motivates a narrower post-establishment question: **when pollinator functional environments are reorganized in a "
    "broadly island-like direction, what determines whether an already-established plant lineage benefits or declines?**"
)

INTRO_STANDALONE_PARAGRAPH = (
    "The coexistence of recurrent island-associated floral and reproductive syndromes with heterogeneous responses among "
    "lineages and biogeographic contexts does not by itself identify why response vectors differ. It motivates a narrower "
    "post-establishment question: **when pollinator functional environments are reorganized in a broadly island-like direction, "
    "what determines whether an already-established plant lineage benefits or declines?**"
)

THESIS_SECTION_RE = re.compile(
    r"\n## From Chapter 1 to Chapter 3\n.*?(?=\n## Limitations and decisive next test\n)",
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
        "# Conditional response geometry under island pollinator reorganization\n\n"
        "**Status:** active working manuscript v2 — not submission-ready  \n"
        "**Updated:** 2026-08-27  \n"
        "**Inference architecture:** synthetic primary analysis + comparative reality boundary + focal Izu empirical triangulation  \n"
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

    # One Discussion sentence refers to the framework by chapter number; make it article-internal.
    text = text.replace(
        "This is not a failure of the Chapter 2 framework.",
        "This does not undermine the conditional-response framework.",
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
