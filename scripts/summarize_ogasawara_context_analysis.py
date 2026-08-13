#!/usr/bin/env python3
"""Create a compact, checked summary from the full Ogasawara context analysis."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping


def compact_summary(analysis: Mapping[str, object]) -> dict[str, object]:
    contrast = analysis.get("anijima_anole_contrast")
    if not isinstance(contrast, dict):
        raise ValueError("analysis lacks anijima_anole_contrast")
    effect_document = contrast.get("effect_level_uncertainty")
    if not isinstance(effect_document, dict):
        raise ValueError("contrast lacks effect_level_uncertainty")
    effects = effect_document.get("effects")
    if not isinstance(effects, list) or not effects:
        raise ValueError("effect_level_uncertainty lacks effects")

    return {
        "schema_version": "1.0",
        "status": analysis.get("status"),
        "source_id": analysis.get("source_id"),
        "dataset_doi": analysis.get("dataset_doi"),
        "license": analysis.get("license"),
        "source_workbook": analysis.get("source_workbook"),
        "source_sha256": analysis.get("source_sha256"),
        "n_source_rows": analysis.get("n_source_rows"),
        "n_zero_marker_rows": analysis.get("n_zero_marker_rows"),
        "n_contexts": analysis.get("n_contexts"),
        "n_context_season_networks": analysis.get("n_context_season_networks"),
        "context_metadata": analysis.get("context_metadata"),
        "anijima_anole_contrast_summary": {
            "absence_context": contrast.get("absence_context"),
            "presence_context": contrast.get("presence_context"),
            "shared_seasons": contrast.get("shared_seasons"),
            "n_plant_season_contrasts": contrast.get("n_plant_season_contrasts"),
            "n_unique_shared_plants": contrast.get("n_unique_shared_plants"),
            "visitation_direction": contrast.get("visitation_direction"),
            "pollinator_richness_direction": contrast.get(
                "pollinator_richness_direction"
            ),
            "effects": effects,
        },
        "methods": analysis.get("methods"),
        "formal_cross_system_fit_ready": bool(
            effect_document.get("formal_cross_system_fit_ready")
        ),
        "claim_boundary": analysis.get("claim_boundary"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analysis",
        type=Path,
        default=Path("artifacts/ogasawara_context_analysis/analysis.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/ogasawara_context_analysis/analysis_summary.json"),
    )
    args = parser.parse_args()

    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    summary = compact_summary(analysis)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
