from __future__ import annotations

import json
from pathlib import Path

from scripts.run_chapter2_conditional_why_diagnostics import (
    BASE,
    BASELINE_REPLICATES,
    OUT,
    SEED,
    realization_class_counts,
    response_matrix,
    two_way_decomposition,
)

CORRECTED_RECEIPT = Path("data/results/chapter2_rng_stream_correction_20260922.json")


def recompute_headline() -> dict:
    matrix = response_matrix(BASE, BASELINE_REPLICATES, SEED)
    fractions = two_way_decomposition(matrix)["sum_of_squares_fraction"]
    return {
        "baseline_realization_class_counts": realization_class_counts(matrix),
        "baseline_sum_of_squares_fraction": fractions,
    }


def frozen_headline() -> dict:
    """Return the corrected deterministic primary draw used for regression tests."""
    payload = json.loads(CORRECTED_RECEIPT.read_text(encoding="utf-8"))
    row = next(
        row
        for row in payload["baseline_ensemble"]["rows"]
        if int(row["seed"]) == int(SEED)
    )
    return {
        "baseline_realization_class_counts": row["realization_class_counts"],
        "baseline_sum_of_squares_fraction": row["sum_of_squares_fraction"],
    }


def historical_headline() -> dict:
    """Return the superseded offset-stream draw for provenance only."""
    payload = json.loads(OUT.read_text(encoding="utf-8"))
    block = payload["starting_position_by_community_realization"]
    return {
        "baseline_realization_class_counts": block["baseline_realization_class_counts"],
        "baseline_sum_of_squares_fraction": block["baseline"]["sum_of_squares_fraction"],
    }


def main() -> None:
    observed = recompute_headline()
    frozen = frozen_headline()
    print(json.dumps({"observed": observed, "frozen": frozen}, indent=2))


if __name__ == "__main__":
    main()
