from __future__ import annotations

import argparse
from pathlib import Path

from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript as render_canonical_manuscript

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

FINAL_TITLE = "Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching"

# Retained for downstream imports. The active submission path is now owned by
# render_chapter2_oikos_generality_overlay.py; this compatibility layer must not
# reintroduce the historical world-saturation / Izu-continuity narrative.
FORBIDDEN_SUBMISSION_TOKENS = (
    "three-result inference chain",
    "result 1—mechanistic prediction",
    "result 2—real-world exposure",
    "result 3—biological consequence",
)


def render_submission_manuscript(source: Path = SOURCE) -> str:
    if source != SOURCE:
        text = source.read_text(encoding="utf-8")
        required = (
            FINAL_TITLE,
            "Realized richness differences therefore help position the ensemble mean regime",
            "The ordering of response determinants is itself regime dependent",
        )
        missing = [token for token in required if token.lower() not in text.lower()]
        if missing:
            raise ValueError(f"canonical mechanism-mainline contract changed: {missing}")
        return text
    text = render_canonical_manuscript()
    lower = text.lower()
    for token in FORBIDDEN_SUBMISSION_TOKENS:
        if token.lower() in lower:
            raise ValueError(f"historical empirical-cascade token survived canonical render: {token}")
    return text


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_submission_manuscript(), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(render_to_path(args.output))


if __name__ == "__main__":
    main()
