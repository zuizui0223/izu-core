from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"


def render_submission_manuscript() -> str:
    """Return the canonical active manuscript.

    The realized-richness reframe and simulation-metadata completion state are
    integrated directly into the active manuscript. Keeping this historical
    renderer as an identity layer preserves downstream imports without obsolete
    string-replacement anchors.
    """
    text = SOURCE.read_text(encoding="utf-8")
    required = (
        "Realized richness differences therefore help position the ensemble mean regime",
        "The ordering of response determinants is itself regime dependent",
        "Metadata confrontation supports biological ingredients while bounding attribution",
        "post-Chapter-2 transport/falsification",
    )
    lower = text.lower()
    for token in required:
        if token.lower() not in lower:
            raise ValueError(f"canonical Chapter 2 manuscript missing required claim: {token}")
    return text


def build(output: Path = DEFAULT_OUTPUT) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_submission_manuscript(), encoding="utf-8")
    return output


if __name__ == "__main__":
    print(build())
