"""Read-only channel audit of the ALREADY confirmed fixed-B48 K intervention.

This analysis is POST-OUTCOME EXPLORATORY. It does not rerun biological
trajectories, refit the predeclared primary, or infer causal mediation.
Only full original 64-history / 2048-source / 114688-future admission is
allowed. Independent resampling unit is visitor history, not future cell.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_k_fixedB48_full_readout import (
    EXPECTED_SHAPE, admit, summarize,
)
from scripts.chapter2_k_fixedB48_manifest import tasks
from scripts.chapter2_k_fixedB48_prehistory import prospective_biological_design
from scripts.chapter2_order_prehistory_runner import case_key
from scripts.plan_chapter2_order_expression_identification import log_budget_weights

METRICS = (
    "restricted_persistence_updates",
    "extinct_by_update_20",
    "extinct_by_update_40",
    "extinct_by_update_60",
    "terminal_population",
    "cumulative_self_recruits",
    "cumulative_outcross_recruits",
    "cumulative_all_recruits",
    "t0_self_viable",
    "t0_outcross_viable",
    "t0_expected_pollen_export",
)
SEED = 2026100973
N_BOOTSTRAPS = 9999
ORIGINAL_VERDICT = "supported_controlled_demographic_K_moderation_at_fixed_B48"
ORIGINAL_ESTIMATE = 0.007745713876893593
ORIGINAL_INTERVAL = [0.002497158065469939, 0.013015478808429596]


def _nonnegative(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise AssertionError("Invalid numeric channel: " + name)
    v = float(value)
    if not np.isfinite(v) or v < 0:
        raise AssertionError("Invalid nonnegative channel: " + name)
    return v


def collect_verified_channels(futures_root: Path, source_admission: Path):
    """Verify complete raw archive, then extract every declared historical cell."""
    cube, design = admit(futures_root, source_admission)
    channels = {key: np.full(EXPECTED_SHAPE, np.nan, dtype=np.float64)
                for key in METRICS}
    expected_count = 0
    for shard, group in enumerate(tasks()):
        root = futures_root / f"chapter2-k48-future-shard-{shard}"
        for task in group:
            key = case_key(task)
            path = root / f"k48_{key}.json"
            chk = root / f"k48_{key}.sha256"
            if hashlib.sha256(path.read_bytes()).hexdigest() != chk.read_text().strip():
                raise AssertionError("Raw source changed after complete admission")
            record = json.loads(path.read_text())
            for row in record["futures"]:
                idx = (
                    task.visitor_history - 41110901,
                    design["reproductive_settings"].index(task.setting),
                    design["environmental_settings"].index(task.environment),
                    ("assurance_first", "investment_first").index(task.expression_order),
                    design["nested_demographic_repeats"].index(task.demographic_repeat),
                    design["postshock"]["budgets"].index(float(row["budget"])),
                    ("near", "far").index(row["visitor"]),
                    ("K8_B48", "K48_B48").index(row["arm"]),
                    ("baseline", "self_half").index(row["gate"]),
                )
                if np.isfinite(channels["terminal_population"][idx]):
                    raise AssertionError("Duplicate raw condition in posthoc channels")
                occupied = int(row["occupied"])
                end_n = _nonnegative(row["end_population"], "end_population")
                if bool(end_n) != bool(occupied):
                    raise AssertionError("Terminal population inconsistent with admitted occupancy")
                first = row["first_extinction"]
                if first is None:
                    if occupied != 1:
                        raise AssertionError("Extinct source lacks first extinction update")
                    restricted = 80
                else:
                    if type(first) is not int or not 0 <= first <= 80 or occupied != 0:
                        raise AssertionError("Invalid extinction history")
                    restricted = first
                t0_n = _nonnegative(row["t0_population"], "t0_population")
                t0 = row["t0"]
                if t0 is None:
                    if t0_n != 0:
                        raise AssertionError("t0 reproductive payoff missing for live founders")
                    a = b = c = 0.0
                else:
                    if t0_n == 0:
                        raise AssertionError("Extinct founders cannot have t0 payoff")
                    a = _nonnegative(t0["selfed_viable"], "t0 selfed")
                    b = _nonnegative(t0["outcrossed_viable"], "t0 outcross")
                    c = _nonnegative(t0["exported_pollen"], "t0 export")
                self_rec = _nonnegative(row["cumulative_selfed_recruits"], "selfed recruited")
                out_rec = _nonnegative(row["cumulative_outcrossed_recruits"], "outcross recruited")
                vals = (
                    restricted,
                    float(first is not None and first <= 20),
                    float(first is not None and first <= 40),
                    float(first is not None and first <= 60),
                    end_n, self_rec, out_rec, self_rec + out_rec, a, b, c,
                )
                for metric, val in zip(METRICS, vals):
                    channels[metric][idx] = val
                expected_count += 1
    if expected_count != 114688 or any(not np.isfinite(v).all() for v in channels.values()):
        raise AssertionError("Missing raw future channels after full admission")

    # The two K arms are identical at the beginning because B is fixed to 48.
    for name in ("t0_self_viable", "t0_outcross_viable", "t0_expected_pollen_export"):
        if not np.array_equal(channels[name][..., 0, :], channels[name][..., 1, :]):
            raise AssertionError("K changed initial reproductive payoff at fixed B48")
    # The intervention halves only viable selfed seed at the initial state.
    if not np.allclose(channels["t0_self_viable"][..., 1],
                       channels["t0_self_viable"][..., 0] * 0.5, atol=1e-9, rtol=0):
        raise AssertionError("Postzygotic manipulation did not halve t0 selfed seed")
    for name in ("t0_outcross_viable", "t0_expected_pollen_export"):
        if not np.array_equal(channels[name][..., 0], channels[name][..., 1]):
            raise AssertionError("Seed-gate intervention leaked into initial other returns")
    return cube, design, channels


def history_order_channel(values: np.ndarray, design: dict) -> np.ndarray:
    """History × K-arm × viability gate, with nested branches pooled first."""
    if values.shape != EXPECTED_SHAPE or not np.isfinite(values).all():
        raise AssertionError("Require complete raw future array")
    original = log_budget_weights(design)
    weights = np.array([original[float(b)] for b in design["postshock"]["budgets"]])
    nested = values.mean(axis=(4, 6))
    weighted = np.tensordot(nested, weights, axes=([4], [0]))
    history = (weighted[:, :, :, 0, :, :] -
               weighted[:, :, :, 1, :, :]).mean(axis=(1, 2))
    if history.shape != (64, 2, 2):
        raise AssertionError("Inconsistent independent history reduction")
    return history


def report(cube, design, channels, frozen):
    """Report exploratory *differences of assigned-order sensitivities* only."""
    registered = summarize(cube, design)
    if (frozen.get("primary_verdict") != ORIGINAL_VERDICT or
            registered["primary_verdict"] != ORIGINAL_VERDICT or
            not np.isclose(
                registered["contrasts"]["primary_K_at_fixed_B48"]["mean"],
                ORIGINAL_ESTIMATE, rtol=0, atol=1e-14) or
            not np.allclose(
                registered["contrasts"]["primary_K_at_fixed_B48"]["bootstrap95"],
                ORIGINAL_INTERVAL, rtol=0, atol=1e-14) or
            frozen["contrasts"]["primary_K_at_fixed_B48"] !=
                registered["contrasts"]["primary_K_at_fixed_B48"]):
        raise AssertionError("Original confirmed primary was altered")

    indices = np.random.default_rng(SEED).integers(0, 64, size=(N_BOOTSTRAPS, 64))

    def bootstrap(v):
        if v.shape != (64,) or not np.isfinite(v).all():
            raise AssertionError("Cluster is not the 64 independent histories")
        q = np.percentile(v[indices].mean(axis=1), [2.5, 97.5])
        return {
            "mean": float(v.mean()), "bootstrap95": [float(q[0]), float(q[1])],
            "positive_histories": int(np.count_nonzero(v > 1e-12)),
            "negative_histories": int(np.count_nonzero(v < -1e-12)),
        }

    output = {}
    for name, arr in {**channels, "terminal_occupancy": cube}.items():
        history = history_order_channel(arr, design)
        tau = history[:, :, 0] - history[:, :, 1]
        output[name] = {
            "sensitivity_K8_B48": bootstrap(tau[:, 0]),
            "sensitivity_K48_B48": bootstrap(tau[:, 1]),
            "K8_minus_K48_sensitivity": bootstrap(tau[:, 0] - tau[:, 1]),
            "order_effect_baseline_K8_B48": bootstrap(history[:, 0, 0]),
            "order_effect_baseline_K48_B48": bootstrap(history[:, 1, 0]),
            "order_effect_half_K8_B48": bootstrap(history[:, 0, 1]),
            "order_effect_half_K48_B48": bootstrap(history[:, 1, 1]),
        }

    # This exploratory refit is NEVER a substitute for the archived primary.
    return {
        "status": "POST_OUTCOME_EXPLORATORY_SOURCE_ADMITTED_CHANNEL_AUDIT",
        "source_production_run_id": 37896872795,
        "original_readout_run_id": 37900150213,
        "verified_raw_future_cells": 114688,
        "independent_bootstrap_unit": "visitor_history",
        "n_independent_histories": 64,
        "exploratory_bootstrap": {"draws": N_BOOTSTRAPS, "seed": SEED},
        "immutable_registered_primary": {
            "status": ORIGINAL_VERDICT, "mean": ORIGINAL_ESTIMATE,
            "bootstrap95": ORIGINAL_INTERVAL,
        },
        "channels": output,
        "limits": [
            "All channel analyses were selected after exposure to a positive registered primary.",
            "Initial payoff parity is a manipulation check, not an inferred causal effect.",
            "Cumulative recruits depend on survival duration and are not independent mediators.",
            "Restricted persistence updates and early extinction are alternate descriptions of demographic trajectories, not distinct replicates.",
            "No inference about natural inherited mutation-order effects, fitness or field-calibrated Izu extinction.",
            "Original predeclared primary and previous inconclusive/failed tests remain unchanged.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--futures", type=Path, required=True)
    p.add_argument("--source-admission", type=Path, required=True)
    p.add_argument("--frozen-result", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--execute-readonly-audit", action="store_true")
    args = p.parse_args()
    if not args.execute_readonly_audit:
        raise PermissionError("Explicit source-only readout permission required")
    frozen = json.loads(args.frozen_result.read_text())
    if frozen.get("status") != "INDEPENDENT_64_HISTORIES_2048_T400_114688_FIXEDB48_FUTURES_ADMITTED":
        raise AssertionError("No original independently admitted fixed-B48 result")
    cube, design, channels = collect_verified_channels(args.futures, args.source_admission)
    result = report(cube, design, channels, frozen)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "status": result["status"],
        "registered_primary": result["immutable_registered_primary"],
        "exploratory_between_K": {
            name: result["channels"][name]["K8_minus_K48_sensitivity"]
            for name in ("terminal_occupancy", "restricted_persistence_updates",
                         "extinct_by_update_20", "extinct_by_update_40",
                         "cumulative_self_recruits", "cumulative_outcross_recruits",
                         "cumulative_all_recruits", "terminal_population")
        },
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
