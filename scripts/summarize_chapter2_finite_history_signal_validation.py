"""Summarize prospectively frozen new-demographic-seed history-signal validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

INTERVENTIONS = ("natural", "visitor_pooled", "large_plant_capacity")


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b) or len(a) < 3 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("correlation requires complete finite support")
    if np.std(a) <= 1e-15 or np.std(b) <= 1e-15:
        raise ValueError("zero-variance history vector")
    return float(np.corrcoef(a, b)[0, 1])


def _label(v: np.ndarray, eps: float) -> str:
    pos = bool(np.any(v > eps))
    neg = bool(np.any(v < -eps))
    return "mixed" if pos and neg else "positive" if pos else "negative" if neg else "neutral"


def _counts(labels: list[str]) -> dict:
    return {k: labels.count(k) for k in ("negative", "mixed", "positive", "neutral")}


def _varcomp(x: np.ndarray) -> dict:
    # x: starts x histories x repeats
    a, b, n = x.shape
    grand = float(x.mean())
    mean_s = x.mean(axis=(1, 2))
    mean_h = x.mean(axis=(0, 2))
    mean_sh = x.mean(axis=2)
    ss_h = a * n * np.sum((mean_h - grand) ** 2)
    ss_sh = n * np.sum((mean_sh - mean_s[:, None] - mean_h[None, :] + grand) ** 2)
    ss_e = np.sum((x - mean_sh[:, :, None]) ** 2)
    ms_h = ss_h / (b - 1)
    ms_sh = ss_sh / ((a - 1) * (b - 1))
    ms_e = ss_e / (a * b * (n - 1))
    raw_h = float((ms_h - ms_sh) / (a * n))
    raw_sh = float((ms_sh - ms_e) / n)
    h = max(0.0, raw_h)
    sh = max(0.0, raw_sh)
    structured = h + sh
    rel = structured / (structured + ms_e / n) if structured + ms_e / n > 0 else None
    return {
        "history_raw": raw_h,
        "history_by_start_raw": raw_sh,
        "history_nonnegative": h,
        "history_by_start_nonnegative": sh,
        "demographic_residual": float(ms_e),
        "four_repeat_mean_reliability": None if rel is None else float(rel),
    }


def summarize(validation: dict, predictions: dict, input_dir: Path) -> dict:
    files = sorted(input_dir.glob("validation-shard-*.json"))
    if len(files) != 16:
        raise ValueError(f"expected 16 validation shards, got {len(files)}")

    rows = []
    histories = []
    source_roots = set()
    total_arm_trajectories = 0
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc["status"] != "complete_finite_history_signal_validation_shard":
            raise ValueError(f"incomplete validation shard: {path}")
        rows.extend(doc["rows"])
        histories.extend(doc["history_seeds"])
        source_roots.add(doc["source_hash_root"])
        total_arm_trajectories += int(doc["simulated_arm_trajectories"])

    history_seeds = sorted(set(histories))
    if len(histories) != len(history_seeds) or len(history_seeds) != 128:
        raise ValueError("validation history denominator mismatch")
    if history_seeds != predictions["history_seeds"]:
        raise ValueError("validation histories differ from frozen prediction histories")
    if len(source_roots) != 1:
        raise ValueError("validation shards used different source roots")
    if total_arm_trajectories != int(validation["validation_source"]["expected_arm_trajectories"]):
        raise ValueError("validation arm-trajectory denominator mismatch")

    starts = [float(x) for x in validation["validation_source"]["starts"]]
    demos = [int(x) for x in validation["validation_source"]["new_demographic_seeds"]]
    hindex = {h: i for i, h in enumerate(history_seeds)}
    sindex = {s: i for i, s in enumerate(starts)}
    dindex = {d: i for i, d in enumerate(demos)}

    reports = {}
    validation_history_vectors = {}
    for intervention in INTERVENTIONS:
        x = np.full((len(starts), len(history_seeds), len(demos)), np.nan)
        near_occ = []
        far_occ = []
        for row in rows:
            if row["intervention"] != intervention:
                continue
            si = sindex[float(row["start"])]
            hi = hindex[int(row["history_seed"])]
            di = dindex[int(row["demographic_seed"])]
            effect = row["effect_far_minus_near"]
            if effect is not None:
                x[si, hi, di] = float(effect)
            near_occ.append(int(row["near_terminal_population"] > 0))
            far_occ.append(int(row["far_terminal_population"] > 0))
        if not np.isfinite(x).all():
            raise ValueError(f"primary validation has missing/extinct paired effect: {intervention}")

        validation_history = x.mean(axis=(0, 2))
        discovery_history = np.asarray(predictions["predictions"][intervention], float)
        if len(discovery_history) != 128:
            raise ValueError("frozen discovery prediction length changed")
        observed = _corr(discovery_history, validation_history)
        validation_history_vectors[intervention] = validation_history

        labels = {}
        for eps in (0.0, 0.01):
            labs = [_label(x[:, hi, :].mean(axis=1), eps) for hi in range(len(history_seeds))]
            labels[str(eps)] = _counts(labs)

        slope = float(np.polyfit(discovery_history, validation_history, 1)[0])
        rmse = float(np.sqrt(np.mean((validation_history - discovery_history) ** 2)))
        reports[intervention] = {
            "discovery_validation_history_correlation": observed,
            "discovery_validation_rmse": rmse,
            "discovery_validation_slope": slope,
            "near_terminal_occupancy": float(np.mean(near_occ)),
            "far_terminal_occupancy": float(np.mean(far_occ)),
            "history_labels": labels,
            "validation_variance_components": _varcomp(x),
            "validation_history_mean": validation_history.tolist(),
        }

    rng = np.random.default_rng(int(validation["primary_validation"]["inference"].split("seed ")[-1]))
    nres = 1999
    boot_corr = {k: [] for k in INTERVENTIONS}
    boot_diff_large = []
    boot_diff_pool = []
    pred_arrays = {k: np.asarray(predictions["predictions"][k], float) for k in INTERVENTIONS}
    for _ in range(nres):
        ix = rng.integers(0, 128, 128)
        vals = {
            k: _corr(pred_arrays[k][ix], validation_history_vectors[k][ix])
            for k in INTERVENTIONS
        }
        for k in INTERVENTIONS:
            boot_corr[k].append(vals[k])
        boot_diff_large.append(vals["large_plant_capacity"] - vals["natural"])
        boot_diff_pool.append(vals["visitor_pooled"] - vals["natural"])

    for k in INTERVENTIONS:
        reports[k]["correlation_bootstrap95"] = np.quantile(boot_corr[k], [0.025, 0.975]).tolist()

    large_diff = float(reports["large_plant_capacity"]["discovery_validation_history_correlation"] - reports["natural"]["discovery_validation_history_correlation"])
    pool_diff = float(reports["visitor_pooled"]["discovery_validation_history_correlation"] - reports["natural"]["discovery_validation_history_correlation"])
    large_ci = np.quantile(boot_diff_large, [0.025, 0.975]).tolist()
    pool_ci = np.quantile(boot_diff_pool, [0.025, 0.975]).tolist()

    observed_order = (
        reports["large_plant_capacity"]["discovery_validation_history_correlation"]
        > reports["natural"]["discovery_validation_history_correlation"]
        > reports["visitor_pooled"]["discovery_validation_history_correlation"]
    )
    strong = bool(observed_order and large_ci[0] > 0 and pool_ci[1] < 0)
    weak = bool(observed_order and not strong)
    decision = "strong_success" if strong else "weak_success" if weak else "failure"

    return {
        "schema_version": "1.0",
        "status": "complete_prospective_new_demographic_history_signal_validation",
        "validation_design_status": validation["status"],
        "discovery_prediction_status": predictions["status"],
        "source_hash_root": next(iter(source_roots)),
        "simulated_arm_trajectories": total_arm_trajectories,
        "histories": len(history_seeds),
        "starts": len(starts),
        "new_demographic_repeats": len(demos),
        "reports": reports,
        "primary_validation": {
            "observed_order_large_gt_natural_gt_pooled": observed_order,
            "large_minus_natural_correlation": large_diff,
            "large_minus_natural_bootstrap95": large_ci,
            "pooled_minus_natural_correlation": pool_diff,
            "pooled_minus_natural_bootstrap95": pool_ci,
            "decision": decision,
            "strong_success_rule": validation["primary_validation"]["strong_success_rule"],
            "weak_success_rule": validation["primary_validation"]["weak_success_rule"],
            "failure_rule": validation["primary_validation"]["failure_rule"],
        },
        "claim_boundary": validation["claim_boundary"],
        "source_shards": [p.name for p in files],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--validation-design", required=True)
    p.add_argument("--predictions", required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    validation = json.loads(Path(a.validation_design).read_text(encoding="utf-8"))
    predictions = json.loads(Path(a.predictions).read_text(encoding="utf-8"))
    if predictions["status"] != "frozen_discovery_history_predictions_before_new_demographic_validation":
        raise ValueError("discovery predictions are not frozen")
    result = summarize(validation, predictions, Path(a.input_dir))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
