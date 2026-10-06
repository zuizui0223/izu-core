"""Render the submission-focused Chapter 2 manuscript.

The active manuscript remains the full scientific record. This renderer keeps the
confirmed 2026-10-05 process spine in the journal-facing main text and routes
supporting diagnostics to SI without deleting them from the source manuscript.
"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
TITLE = "How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization"

METHODS = [
    "## Ecological scope and claim boundary",
    "## Replenishment is distinct from island area and plant population size",
    "## Current primary experiments and their causal contrasts",
    "## Prospectively frozen independent confirmation",
    "## Ecologically explicit reproductive and inheritance pathway",
    "## Local selection, isolation gradients and parameter sensitivity",
]

RESULTS = [
    "## Visitor limitation lowers the return on attraction before plant traits evolve",
    "## Reproductive assurance often changes first under sustained isolation",
    "## Assurance evolution is not required for investment decline",
    "## Local conditions for syndrome-direction selection",
    "## Lower pollen deficit does not necessarily mean greater viable reproduction",
]

DISCUSSION = [
    "## Sequence does not identify a selfing-mediated causal pathway",
    "## Pollination ecology and realized evolution are distinct biological stages",
    "## Reproductive assurance preserves trajectories rather than prescribing phenotypes",
    "## Natural systems contain the ecological ingredients but not yet the full transition",
    "## Ecological validity and limits",
]


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.index(heading)
    end = len(text) if next_heading is None else text.index(next_heading, start + len(heading))
    return text[start:end].rstrip()


def filter_h2(block: str, keep: list[str]) -> str:
    chunks = re.split(r"(?=^## )", block, flags=re.MULTILINE)
    prefix = chunks[0].rstrip()
    by_heading = {}
    for chunk in chunks[1:]:
        heading = chunk.splitlines()[0].strip()
        by_heading[heading] = chunk.rstrip()
    missing = [h for h in keep if h not in by_heading]
    if missing:
        raise ValueError(f"missing requested subsection(s): {missing}")
    kept = [by_heading[h] for h in keep]
    return prefix + "\n\n" + "\n\n".join(kept)


def render_manuscript(source: Path | None = None) -> str:
    text = (SOURCE if source is None else source).read_text(encoding="utf-8")
    if text.splitlines()[0] != "# " + TITLE:
        raise ValueError("active manuscript title does not match submission route")

    required = [
        "## Abstract",
        "## Keywords",
        "# Introduction",
        "# Materials and Methods",
        "# Results",
        "# Discussion",
        "# Conclusion",
        "# Primary figure assembly and captions",
        "# References",
    ]
    for heading in required:
        if text.splitlines().count(heading) != 1:
            raise ValueError(f"missing required section or duplicate: {heading}")

    front = section(text, "## Abstract", "# Introduction")
    intro = section(text, "# Introduction", "# Materials and Methods")
    methods = filter_h2(section(text, "# Materials and Methods", "# Results"), METHODS)
    results = filter_h2(section(text, "# Results", "# Discussion"), RESULTS)
    discussion = filter_h2(section(text, "# Discussion", "# Conclusion"), DISCUSSION)
    conclusion = section(text, "# Conclusion", "# Primary figure assembly and captions")
    figures = section(text, "# Primary figure assembly and captions", "# References")
    references = section(text, "# References", None)

    out = "\n\n".join([
        "# " + TITLE,
        front,
        intro,
        methods,
        results,
        discussion,
        conclusion,
        figures,
        references,
    ]).strip() + "\n"

    forbidden = [
        "## Continuous replenishment extension: completed finite-population gradient",
        "## Prospective isolation-bridge controls",
        "## Current flowers do not uniquely determine inherited response",
        "## Reciprocal coupling of selection on capacity and investment",
        "## Reproductive assumptions delimit reciprocal selection",
        "## Genetic diversity, fitness and model scope",
        "## Realized evolution across continuous replenishment",
        "## Numerical sensitivity and branch-identifiability limits",
        "## Independent connection to Q1",
    ]
    for heading in forbidden:
        if heading in out:
            raise ValueError(f"supporting subsection leaked into submission main text: {heading}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "outputs/chapter2_process_delivery/MANUSCRIPT.md",
    )
    args = parser.parse_args()
    rendered = render_manuscript()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
