#!/usr/bin/env python3
"""Sensitivity of Southwest Pacific starting-size slopes to denominator coupling.

The analysed response is LR = log10(FI/FM) and the predictor is log10(FM).
Because the observed mainland value appears in both variables, classical
measurement error in log10(FM) induces a negative LR slope even when the true
island/mainland response is independent of true mainland size.

Let X = true log mainland flower size and X* = X + e be the observed value.
Let Z = true log island flower size with true slope lambda_true against X.
Under independent classical error in X and no correlated measurement error,

    lambda_observed = reliability_X * lambda_true
    beta_LR_observed = lambda_observed - 1

so

    beta_LR_true = (beta_LR_observed + 1) / reliability_X - 1.

This script does not estimate reliability. It reports the reliability threshold
needed for the source-coded negative slope, and its cluster-bootstrap interval,
to remain negative. It is a sensitivity/adversary, not a measurement-error
correction.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_RELIABILITIES = (1.0, 0.975, 0.95, 0.925, 0.9, 0.85, 0.8)
MODEL_PATHS = {
    "animal_source_coded": ("primary_models", "animal_source_coded"),
    "wind_source_coded": ("primary_models", "wind_source_coded"),
    "phylogenetic_animal": ("key_sensitivities", "phylogenetic_animal"),
    "actinomorphic_fused_petals": ("key_sensitivities", "actinomorphic_fused_petals"),
    "actinomorphic_free_petals": ("key_sensitivities", "actinomorphic_free_petals"),
}
COLUMNS = (
    "model",
    "n",
    "observed_lr_slope",
    "observed_log_island_on_log_mainland_slope",
    "observed_coupling_ci_low",
    "observed_coupling_ci_high",
    "point_negative_requires_reliability_gt",
    "ci_entirely_negative_requires_reliability_gt",
    "assumed_mainland_log_size_reliability",
    "implied_true_lr_slope",
    "implied_true_lr_ci_low",
    "implied_true_lr_ci_high",
    "point_remains_negative",
    "interval_entirely_negative",
    "row_role",
    "causal_claim_allowed",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def nested(document: Mapping[str, Any], path: Sequence[str]) -> Mapping[str, Any]:
    value: Any = document
    for key in path:
        if not isinstance(value, Mapping) or key not in value:
            raise KeyError("/".join(path))
        value = value[key]
    if not isinstance(value, Mapping):
        raise TypeError(f"expected mapping at {'/'.join(path)}")
    return value


def corrected_lr_slope(observed_coupling_slope: float, reliability: float) -> float:
    if not 0 < reliability <= 1:
        raise ValueError("reliability must be in (0, 1]")
    if not math.isfinite(observed_coupling_slope):
        raise ValueError("observed coupling slope must be finite")
    return observed_coupling_slope / reliability - 1.0


def model_record(model: str, result: Mapping[str, Any]) -> dict[str, object]:
    if result.get("status") != "estimated":
        raise ValueError(f"model {model} is not estimated")
    observed_lr = float(result["ols_slope"])
    coupling = float(result["coupling_slope"])
    ci = [float(value) for value in result["coupling_island_ci_95"]]
    if len(ci) != 2 or ci[0] > ci[1]:
        raise ValueError(f"invalid coupling interval for {model}: {ci}")
    if not math.isclose(coupling, observed_lr + 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError(
            f"model {model} violates LR/log-island algebra: "
            f"coupling={coupling}, 1+LR={observed_lr + 1.0}"
        )
    return {
        "model": model,
        "n": int(result["n"]),
        "observed_lr_slope": observed_lr,
        "observed_log_island_on_log_mainland_slope": coupling,
        "observed_coupling_ci_low": ci[0],
        "observed_coupling_ci_high": ci[1],
        "point_negative_requires_reliability_gt": coupling,
        "ci_entirely_negative_requires_reliability_gt": ci[1],
    }


def sensitivity_rows(
    model: str,
    record: Mapping[str, object],
    reliabilities: Sequence[float],
) -> list[dict[str, object]]:
    coupling = float(record["observed_log_island_on_log_mainland_slope"])
    ci_low = float(record["observed_coupling_ci_low"])
    ci_high = float(record["observed_coupling_ci_high"])
    output = []
    for reliability in reliabilities:
        beta = corrected_lr_slope(coupling, reliability)
        lower = corrected_lr_slope(ci_low, reliability)
        upper = corrected_lr_slope(ci_high, reliability)
        output.append(
            {
                **record,
                "assumed_mainland_log_size_reliability": reliability,
                "implied_true_lr_slope": beta,
                "implied_true_lr_ci_low": lower,
                "implied_true_lr_ci_high": upper,
                "point_remains_negative": beta < 0,
                "interval_entirely_negative": upper < 0,
                "row_role": "classical_measurement_error_sensitivity_not_correction",
                "causal_claim_allowed": "no",
            }
        )
    return output


def analyse(
    document: Mapping[str, Any],
    *,
    reliabilities: Sequence[float] = DEFAULT_RELIABILITIES,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    if any(not 0 < value <= 1 for value in reliabilities):
        raise ValueError("all reliabilities must be in (0, 1]")
    models = {
        name: model_record(name, nested(document, path))
        for name, path in MODEL_PATHS.items()
    }
    rows = [
        row
        for model, record in models.items()
        for row in sensitivity_rows(model, record, reliabilities)
    ]
    animal = models["animal_source_coded"]
    wind = models["wind_source_coded"]
    summary = {
        "schema_version": "1.0",
        "status": "classical_measurement_error_coupling_sensitivity_complete",
        "source_id": document.get("source_id"),
        "article_doi": document.get("article_doi"),
        "response": "log10(FI/FM) against log10(FM)",
        "assumption": (
            "Classical independent measurement error in observed log10 mainland flower size; "
            "island-side error is independent and contributes residual variance rather than predictor coupling."
        ),
        "reliability_is_empirically_estimated_here": False,
        "animal_point_negative_reliability_threshold": animal[
            "point_negative_requires_reliability_gt"
        ],
        "animal_ci_negative_reliability_threshold": animal[
            "ci_entirely_negative_requires_reliability_gt"
        ],
        "wind_point_negative_reliability_threshold": wind[
            "point_negative_requires_reliability_gt"
        ],
        "wind_ci_negative_reliability_threshold": wind[
            "ci_entirely_negative_requires_reliability_gt"
        ],
        "interpretation": (
            "For the source-coded animal subset, the observed point slope remains negative under the declared "
            "classical-error model only when mainland log-flower-size reliability exceeds the observed "
            "log-island-on-log-mainland slope (~0.849). To keep the island-cluster interval entirely below zero, "
            "reliability must exceed its upper coupling bound (~0.926). The source does not provide a reliability "
            "estimate that closes this sensitivity."
        ),
        "claim_boundary": (
            "This is a partial-identification sensitivity, not evidence that measurement error caused the observed "
            "pattern and not a correction of the source estimate. Nonclassical, correlated, phylogenetic, or "
            "source-specific errors can behave differently. Pollination mode remains distinct from effective dependency."
        ),
        "effect_registry_eligible": False,
        "causal_claim_allowed": False,
    }
    return rows, summary


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analysis-summary",
        type=Path,
        default=Path("data/results/southwest_pacific_pairs/analysis_summary.json"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/results/southwest_pacific_pairs/measurement_error_coupling_sensitivity.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("data/results/southwest_pacific_pairs/measurement_error_coupling_sensitivity_summary.json"),
    )
    args = parser.parse_args()
    document = load_json(args.analysis_summary)
    rows, summary = analyse(document)
    write_csv(args.output_csv, rows)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(summary["animal_point_negative_reliability_threshold"])
    print(summary["animal_ci_negative_reliability_threshold"])


if __name__ == "__main__":
    main()
