from __future__ import annotations

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "legacy/submission-history/model3_bridge_20261004/MANUSCRIPT.md"
NEW_TITLE = "From pollination ecology to realized floral evolution in finite island populations"


def historical_provenance() -> dict:
    """Validate the immutable manuscript before using its original routing identity."""
    provenance = json.loads(SOURCE.with_name('PROVENANCE.json').read_text(encoding='utf-8'))
    if provenance.get('status') != 'historical_submission_snapshot_not_current_manuscript':
        raise ValueError('Historical manuscript provenance status is missing')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != provenance.get('sha256'):
        raise ValueError('Historical manuscript snapshot hash mismatch')
    return provenance

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
    """Reproduce the historical bridge submission; not the current process paper.

    Current manuscript delivery uses render_chapter2_process_manuscript.py.
    Keep this snapshot coupled to the legacy figure/SI builders and claim gate.
    """
    historical_provenance()
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
