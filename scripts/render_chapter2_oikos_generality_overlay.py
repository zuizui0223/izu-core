from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
NEW_TITLE = "From pollination ecology to realized floral evolution in finite island populations"

_INTERNAL_PREFIXES = (
    "**Status:**",
    "**Updated:**",
    "**Inference architecture:**",
    "**Controlling state:**",
)


def _strip_repository_metadata(text: str) -> str:
    """Remove repository-only routing metadata from the blinded journal surface."""
    lines = [line for line in text.splitlines() if not line.startswith(_INTERNAL_PREFIXES)]
    return "\n".join(lines).strip() + "\n"


def render_submission_manuscript() -> str:
    """Render the active Model 3 manuscript and fail closed on its claim boundary."""
    text = _strip_repository_metadata(SOURCE.read_text(encoding="utf-8"))
    first_line = text.splitlines()[0]
    if NEW_TITLE not in first_line:
        raise ValueError("canonical Oikos title missing from active manuscript")

    lower = text.lower()
    required = (
        "reproductive selection before demographic change",
        "conditional deterministic genotype-density propagation without demographic sampling",
        "realized evolution in finite populations",
        "24,576-case bridge",
        "128 independent visitor histories",
        "stable latent branch prevalence",
        "annual response-blind richness matching",
        "pooling eight independent visitor histories",
        "increasing plant capacity from 48 to 192",
        "conditional deterministic closure",
        "reproductive assurance",
        "principal natural-data gap",
        "ecologically explicit but system-uncalibrated",
        "0/25 full source-state",
    )
    for token in required:
        if token not in lower:
            raise ValueError(f"Oikos canonical manuscript missing claim-lock token: {token}")

    for forbidden in _INTERNAL_PREFIXES:
        if forbidden.lower() in lower:
            raise ValueError(f"repository metadata leaked into journal manuscript: {forbidden}")
    return text
