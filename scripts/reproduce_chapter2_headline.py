from __future__ import annotations

import json

from scripts.run_chapter2_conditional_why_diagnostics import (
    BASE,
    BASELINE_REPLICATES,
    OUT,
    SEED,
    realization_class_counts,
    response_matrix,
    two_way_decomposition,
)


def recompute_headline() -> dict:
    matrix = response_matrix(BASE, BASELINE_REPLICATES, SEED)
    fractions = two_way_decomposition(matrix)["sum_of_squares_fraction"]
    return {
        "baseline_realization_class_counts": realization_class_counts(matrix),
        "baseline_sum_of_squares_fraction": fractions,
    }


def frozen_headline() -> dict:
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
