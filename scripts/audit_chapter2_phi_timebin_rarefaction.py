from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from scripts.analyze_chapter2_natural_regime_coordinates import (
    PLAN,
    _dispersion_summary,
    _hill_d1,
    _midranks,
    _nee_dispersion_pass,
    _phi,
    _stable_seed,
    load_canonical_csv,
    _matrix_for,
)

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/design/chapter2_phi_timebin_rarefaction_freeze_20260922.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_phi_timebin_rarefaction_20260922.json"


def _spearman(x: list[float], y: list[float]) -> float | None:
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)
    if len(xa) < 2 or np.std(xa) == 0 or np.std(ya) == 0:
        return None
    value = float(np.corrcoef(_midranks(xa), _midranks(ya))[0, 1])
    return value if math.isfinite(value) else None


def _coordinate_from_matrix(
    key: tuple[str, str, str],
    matrix: np.ndarray,
    *,
    breadth_override: float | None = None,
) -> dict | None:
    source, archipelago, system = key
    phi, eligible = _phi(matrix)
    if len(eligible) < 3 or not math.isfinite(phi):
        return None
    breadth = float(breadth_override) if breadth_override is not None else _hill_d1(matrix.sum(axis=0))
    if not math.isfinite(breadth) or breadth <= 0:
        return None
    m = len(eligible)
    rho_eq = float((m * phi - 1.0) / (m - 1.0)) if m > 1 else float("nan")
    return {
        "source_study_id": source,
        "archipelago_id": archipelago,
        "system_id": system,
        "breadth_D1": breadth,
        "phi": float(phi),
        "rho_eq": rho_eq,
        "eligible_synchrony_partners": m,
    }


def _load_records(paths: list[Path]) -> dict[tuple[str, str, str], dict]:
    merged: dict[tuple[str, str, str], dict] = {}
    for path in paths:
        current = load_canonical_csv(path)
        overlap = set(merged).intersection(current)
        if overlap:
            raise ValueError(f"duplicate systems across canonical inputs: {sorted(overlap)}")
        merged.update(current)
    return merged


def _quantiles(values: list[float]) -> dict:
    array = np.asarray(values, dtype=float)
    return {
        "median": float(np.median(array)),
        "q025": float(np.quantile(array, 0.025)),
        "q975": float(np.quantile(array, 0.975)),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
    }


def _loo_dispersion_pass(rows: list[dict], thresholds: dict) -> dict[str, bool]:
    sources = sorted({row["source_study_id"] for row in rows})
    return {
        source: _nee_dispersion_pass(
            _dispersion_summary([row for row in rows if row["source_study_id"] != source]),
            thresholds,
        )
        for source in sources
    }


def _loo_phi_span(rows: list[dict], thresholds: dict) -> dict[str, dict]:
    sources = sorted({row["source_study_id"] for row in rows})
    output = {}
    minimum = float(thresholds["phi_q90_q10_span_min"])
    for source in sources:
        summary = _dispersion_summary(
            [row for row in rows if row["source_study_id"] != source]
        )
        span = summary.get("phi_q90_q10_span")
        valid = span is not None and math.isfinite(float(span))
        output[source] = {
            "span": float(span) if valid else None,
            "pass": bool(valid and float(span) >= minimum),
        }
    return output


def run(
    inputs: list[Path],
    *,
    freeze_path: Path = FREEZE,
    plan_path: Path = PLAN,
) -> dict:
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if freeze.get("status") != "frozen_before_execution":
        raise ValueError("phi rarefaction design is not frozen before execution")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    thresholds = plan["route_thresholds"]["nee_candidate"]
    target = int(freeze["target_time_bins"])
    replicates = int(freeze["rarefaction_replicates"])
    base_seed = int(freeze["seed"])

    records = _load_records(inputs)
    if len(records) != int(freeze["expected_systems"]):
        raise ValueError(
            f"expected {freeze['expected_systems']} admitted systems, got {len(records)}"
        )
    observed_sources = {key[0] for key in records}
    if observed_sources != set(freeze["admitted_sources"]):
        raise ValueError(
            f"source set differs from freeze: {sorted(observed_sources)}"
        )

    matrices: dict[tuple[str, str, str], np.ndarray] = {}
    original_rows: list[dict] = []
    original_time_bins: dict[tuple[str, str, str], int] = {}
    rngs: dict[tuple[str, str, str], np.random.Generator] = {}
    for key in sorted(records):
        time_bins, _, matrix = _matrix_for(records[key])
        if len(time_bins) < target:
            raise ValueError(f"{key}: fewer than target {target} time bins")
        row = _coordinate_from_matrix(key, matrix)
        if row is None:
            raise ValueError(f"{key}: full matrix has invalid coordinate")
        row["time_bins"] = len(time_bins)
        original_rows.append(row)
        original_time_bins[key] = len(time_bins)
        matrices[key] = matrix
        rngs[key] = np.random.default_rng(
            _stable_seed(base_seed, "|".join(key) + "|six-bin-rarefaction")
        )

    original_phi_time_spearman = _spearman(
        [float(row["phi"]) for row in original_rows],
        [float(row["time_bins"]) for row in original_rows],
    )
    original_rho_time_spearman = _spearman(
        [float(row["rho_eq"]) for row in original_rows],
        [float(row["time_bins"]) for row in original_rows],
    )
    original_by_key = {
        (row["source_study_id"], row["archipelago_id"], row["system_id"]): row
        for row in original_rows
    }

    per_system_phi: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    phi_only_pass: list[bool] = []
    joint_pass: list[bool] = []
    phi_only_loo: dict[str, list[bool]] = defaultdict(list)
    joint_loo: dict[str, list[bool]] = defaultdict(list)
    phi_only_loo_span_pass: dict[str, list[bool]] = defaultdict(list)
    joint_loo_span_pass: dict[str, list[bool]] = defaultdict(list)
    phi_only_loo_spans: dict[str, list[float]] = defaultdict(list)
    joint_loo_spans: dict[str, list[float]] = defaultdict(list)
    phi_only_span: list[float] = []
    joint_span: list[float] = []
    invalid_iterations = 0

    for _ in range(replicates):
        phi_only_rows: list[dict] = []
        joint_rows: list[dict] = []
        iteration_phi: dict[tuple[str, str, str], float] = {}
        iteration_valid = True
        for key in sorted(matrices):
            matrix = matrices[key]
            indices = np.sort(rngs[key].choice(matrix.shape[0], size=target, replace=False))
            sample = matrix[indices]
            full_d1 = float(original_by_key[key]["breadth_D1"])
            phi_row = _coordinate_from_matrix(key, sample, breadth_override=full_d1)
            joint_row = _coordinate_from_matrix(key, sample)
            if phi_row is None or joint_row is None:
                iteration_valid = False
                continue
            iteration_phi[key] = float(phi_row["phi"])
            phi_only_rows.append(phi_row)
            joint_rows.append(joint_row)

        if not iteration_valid or len(iteration_phi) != len(matrices):
            invalid_iterations += 1
            continue

        for key, value in iteration_phi.items():
            per_system_phi[key].append(value)

        phi_summary = _dispersion_summary(phi_only_rows)
        joint_summary = _dispersion_summary(joint_rows)
        phi_only_pass.append(_nee_dispersion_pass(phi_summary, thresholds))
        joint_pass.append(_nee_dispersion_pass(joint_summary, thresholds))
        phi_only_span.append(float(phi_summary["phi_q90_q10_span"]))
        joint_span.append(float(joint_summary["phi_q90_q10_span"]))

        for source, passed in _loo_dispersion_pass(phi_only_rows, thresholds).items():
            phi_only_loo[source].append(passed)
        for source, passed in _loo_dispersion_pass(joint_rows, thresholds).items():
            joint_loo[source].append(passed)

        for source, row in _loo_phi_span(phi_only_rows, thresholds).items():
            phi_only_loo_span_pass[source].append(bool(row["pass"]))
            if row["span"] is not None:
                phi_only_loo_spans[source].append(float(row["span"]))
        for source, row in _loo_phi_span(joint_rows, thresholds).items():
            joint_loo_span_pass[source].append(bool(row["pass"]))
            if row["span"] is not None:
                joint_loo_spans[source].append(float(row["span"]))

    valid = len(phi_only_pass)
    if valid == 0:
        raise RuntimeError("no valid rarefaction iterations")

    per_system = []
    for key in sorted(matrices):
        values = per_system_phi[key]
        if len(values) != valid:
            raise RuntimeError(f"{key}: rarefaction result count drift")
        original = original_by_key[key]
        q = _quantiles(values)
        per_system.append({
            "source_study_id": key[0],
            "archipelago_id": key[1],
            "system_id": key[2],
            "original_time_bins": original_time_bins[key],
            "original_phi": float(original["phi"]),
            "rarefied_phi": q,
            "median_delta_phi": q["median"] - float(original["phi"]),
        })

    source_summary = []
    for source in sorted(observed_sources):
        rows = [row for row in per_system if row["source_study_id"] == source]
        source_summary.append({
            "source_study_id": source,
            "systems": len(rows),
            "original_time_bins_median": float(np.median([row["original_time_bins"] for row in rows])),
            "original_phi_median": float(np.median([row["original_phi"] for row in rows])),
            "rarefied_phi_median_of_system_medians": float(
                np.median([row["rarefied_phi"]["median"] for row in rows])
            ),
        })

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_phi_timebin_rarefaction",
        "status": "complete",
        "freeze": str(freeze_path),
        "inputs": [str(path) for path in inputs],
        "systems": len(records),
        "sources": len(observed_sources),
        "target_time_bins": target,
        "requested_iterations": replicates,
        "valid_iterations": valid,
        "invalid_iterations": invalid_iterations,
        "full_data_diagnostics": {
            "spearman_phi_vs_time_bins": original_phi_time_spearman,
            "spearman_rho_eq_vs_time_bins": original_rho_time_spearman,
            "dispersion_summary": _dispersion_summary(original_rows),
            "dispersion_criteria_pass": _nee_dispersion_pass(
                _dispersion_summary(original_rows), thresholds
            ),
        },
        "phi_only_primary": {
            "dispersion_criteria_pass_fraction": float(np.mean(phi_only_pass)),
            "phi_q90_q10_span": _quantiles(phi_only_span),
            "leave_one_source_out_pass_fraction": {
                source: float(np.mean(values))
                for source, values in sorted(phi_only_loo.items())
            },
            "leave_one_source_out_phi_span_pass_fraction": {
                source: float(np.mean(values))
                for source, values in sorted(phi_only_loo_span_pass.items())
            },
            "leave_one_source_out_phi_span": {
                source: _quantiles(values)
                for source, values in sorted(phi_only_loo_spans.items())
            },
        },
        "joint_coordinate_secondary": {
            "dispersion_criteria_pass_fraction": float(np.mean(joint_pass)),
            "phi_q90_q10_span": _quantiles(joint_span),
            "leave_one_source_out_pass_fraction": {
                source: float(np.mean(values))
                for source, values in sorted(joint_loo.items())
            },
            "leave_one_source_out_phi_span_pass_fraction": {
                source: float(np.mean(values))
                for source, values in sorted(joint_loo_span_pass.items())
            },
            "leave_one_source_out_phi_span": {
                source: _quantiles(values)
                for source, values in sorted(joint_loo_spans.items())
            },
        },
        "per_system": per_system,
        "source_summary": source_summary,
        "claim_boundary": freeze["interpretation_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--freeze", type=Path, default=FREEZE)
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = run(args.inputs, freeze_path=args.freeze, plan_path=args.plan)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "valid_iterations": result["valid_iterations"],
        "phi_only_pass_fraction": result["phi_only_primary"]["dispersion_criteria_pass_fraction"],
        "joint_pass_fraction": result["joint_coordinate_secondary"]["dispersion_criteria_pass_fraction"],
    }, indent=2))


if __name__ == "__main__":
    main()
