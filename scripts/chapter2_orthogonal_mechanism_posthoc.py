"""Read-only, post-outcome mechanism-channel audit of ALL orthogonal futures.

This is an exploratory channel decomposition, NOT a new registered causal
mediator test and NOT a new biological simulation. All 172032 futures must
pass the existing whole-cohort cryptographic admission first.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np

from scripts.chapter2_orthogonal_full_adjudication import audit_and_collect
from scripts.chapter2_orthogonal_capacity_readout import (
    ARM_NAMES, EXPECTED_SHAPE, history_order_effects, summarize_history_effects
)
from scripts.chapter2_orthogonal_cohort_manifest import tasks
from scripts.chapter2_orthogonal_prehistory_source_runner import prospective_biological_design
from scripts.chapter2_order_prehistory_runner import case_key
from scripts.plan_chapter2_order_expression_identification import log_budget_weights

SEED = 2026100951
DRAWS = 9999
METRICS = (
    "initial_population", "t0_self_viable", "t0_outcross_viable",
    "t0_expected_pollen_export", "cumulative_selfed_recruits",
    "cumulative_outcross_recruits", "cumulative_total_recruits",
    "terminal_population", "extinct_by_20",
)


def _as_float(x, field):
    if isinstance(x, bool) or not isinstance(x, (float, int)):
        raise AssertionError("Invalid numeric " + field)
    value = float(x)
    if not np.isfinite(value) or value < 0:
        raise AssertionError("Non-finite or negative " + field)
    return value


def load_channels(futures_root: Path, admission_path: Path):
    """Full raw audit FIRST; thereafter admit all and only registered channels."""
    occupied = audit_and_collect(futures_root, admission_path)
    if occupied.shape != EXPECTED_SHAPE:
        raise AssertionError("Full binary occupancy cube absent")
    d = prospective_biological_design()
    z = {name: np.full(EXPECTED_SHAPE, np.nan, dtype=float)
         for name in METRICS}
    for shard, group in enumerate(tasks()):
        folder = (futures_root /
                  f"chapter2-orthogonal-future-shard-{shard}")
        for task in group:
            key = case_key(task)
            path = folder / f"orthogonal_{key}.json"
            checksum = folder / f"orthogonal_{key}.sha256"
            if hashlib.sha256(path.read_bytes()).hexdigest() != checksum.read_text().strip():
                raise AssertionError("Archive changed since full-cohort admission")
            case = json.loads(path.read_text(encoding="utf-8"))
            source_keys = set()
            for row in case["futures"]:
                condition = (row["regime"], row["gate"],
                             float(row["budget"]), row["future_visitor"])
                if condition in source_keys:
                    raise AssertionError("Duplicate science condition")
                source_keys.add(condition)
                index = (
                    task.visitor_history - 39110901,
                    d["reproductive_settings"].index(task.setting),
                    d["environmental_settings"].index(task.environment),
                    ("assurance_first", "investment_first").index(task.expression_order),
                    d["nested_demographic_repeats"].index(task.demographic_repeat),
                    d["postshock"]["budgets"].index(float(row["budget"])),
                    ("near", "far").index(row["future_visitor"]),
                    ARM_NAMES.index(row["regime"]),
                    ("baseline", "self_half").index(row["gate"]),
                )
                if np.isfinite(z["initial_population"][index]):
                    raise AssertionError("Duplicate source/stratum index")
                n = _as_float(row["t0_population"], "t0_population")
                payoff = row["t0_payoff"]
                if (n == 0) != (payoff is None):
                    raise AssertionError("Pre-extinct t0 source misclassified")
                if payoff is None:
                    selfed = outcross = pollen = 0.0
                else:
                    selfed = _as_float(payoff["viable_selfed"], "viable_selfed")
                    outcross = _as_float(payoff["viable_outcross"], "viable_outcross")
                    pollen = _as_float(payoff["expected_pollen_export"], "pollen_export")
                sr = _as_float(row["selfed_recruits"], "selfed_recruits")
                oc = _as_float(row["outcrossed_recruits"], "outcrossed_recruits")
                pop = _as_float(row["terminal_population"], "terminal_population")
                t = row["first_extinction"]
                if t is not None and (type(t) is not int or not 0 <= t <= 80):
                    raise AssertionError("Invalid extinction time")
                numbers = (n, selfed, outcross, pollen, sr, oc, sr + oc,
                           pop, float(t is not None and t <= 20))
                for metric, v in zip(METRICS, numbers):
                    z[metric][index] = v
                if int(pop > 0) != int(occupied[index]):
                    raise AssertionError("Terminal population disagrees with admitted occupancy")
            if len(source_keys) != 84:
                raise AssertionError("Incomplete source condition count")

    if any(not np.isfinite(v).all() for v in z.values()):
        raise AssertionError("Incomplete mechanism channels")
    # The treatment is postzygotic. Both gates use the same t0 source;
    # outcross and pollen export must be identical, viable selfed seeds halved.
    initial = z["initial_population"]
    if not np.array_equal(initial[..., 0], initial[..., 1]):
        raise AssertionError("Same source not preserved between seed gates")
    for name in ("t0_outcross_viable", "t0_expected_pollen_export"):
        if not np.allclose(z[name][..., 0], z[name][..., 1], atol=1e-9, rtol=0):
            raise AssertionError("Postzygotic gate altered prezygotic outcome")
    if not np.allclose(
        z["t0_self_viable"][..., 1],
        z["t0_self_viable"][..., 0] * 0.5, atol=1e-9, rtol=0
    ):
        raise AssertionError("Self-viability intervention differs from 50%")

    # Same F8 founder IDs under capacity 8 and 48; audit their immediate
    # outputs rather than assume capacity has no direct effect on reproduction.
    identical_founders = bool(np.array_equal(initial[..., 0, :],
                                              initial[..., 1, :]))
    initial_differences = {
        name: float(np.max(np.abs(z[name][..., 0, :] - z[name][..., 1, :])))
        for name in ("t0_self_viable", "t0_outcross_viable",
                     "t0_expected_pollen_export")
    }
    return d, z, occupied, {
        "identical_F8_starting_counts": identical_founders,
        "F8_max_initial_payoff_abs_difference_capacity8_vs_capacity48": initial_differences,
        "viability_gate_preserves_outcross_and_pollen": True,
        "viability_gate_halves_selfed_viable_seed": True,
    }


def history_schedule_effect(array, d):
    if array.shape != EXPECTED_SHAPE:
        raise AssertionError("Unexpected mechanism-channel grid")
    weights = log_budget_weights(d)
    w = np.array([weights[float(b)] for b in d["postshock"]["budgets"]])
    collapsed = array.mean(axis=(4, 6))
    pooled = np.tensordot(collapsed, w, axes=([4], [0]))
    by_order = pooled[:, :, :, 0, :, :] - pooled[:, :, :, 1, :, :]
    return by_order.mean(axis=(1, 2))  # histories(64), arms(3), gates(2)


def summarize(d, z, occupied, checks, original_result):
    # Confirm exact agreement with immutable full-cohort registered endpoint,
    # rather than independently promoting an exploratory analysis.
    base_h = history_order_effects(occupied, design=d)
    baseline = summarize_history_effects(base_h)
    primary = baseline["contrasts"]["primary_capacity_conditional_fixed_eight"]
    frozen = original_result["inference"]["contrasts"]["primary_capacity_conditional_fixed_eight"]
    if (baseline["primary_decision_if_and_only_if_complete_raw_archive_admitted"]
            != "inconclusive"
            or not np.isclose(primary["mean"], frozen["mean"], atol=1e-12, rtol=0)
            or not np.allclose(primary["history_bootstrap95"],
                               frozen["history_bootstrap95"], atol=1e-12, rtol=0)):
        raise AssertionError("Archived primary scientific result was altered")

    draws = np.random.default_rng(SEED).integers(0, 64, size=(DRAWS, 64))
    def effect(v):
        if v.shape != (64,) or not np.isfinite(v).all():
            raise AssertionError("Not 64 complete history-level pairs")
        lo, hi = np.percentile(v[draws].mean(axis=1), [2.5, 97.5])
        return {"mean": float(v.mean()), "history_bootstrap95": [float(lo), float(hi)],
                "n_positive": int(np.sum(v > 1e-12)),
                "n_negative": int(np.sum(v < -1e-12)),
                "n_zero": int(np.sum(abs(v) <= 1e-12))}
    by_metric = {}
    for name, array in {**z, "terminal_occupancy": occupied}.items():
        h = history_schedule_effect(array, d)
        sensitivities = h[:, :, 0] - h[:, :, 1]
        by_metric[name] = {
            "A_first_minus_I_first": {
                ARM_NAMES[i]: {
                    "baseline": effect(h[:, i, 0]),
                    "self_half": effect(h[:, i, 1]),
                } for i in range(3)
            },
            "viability_sensitivity_baseline_minus_self_half": {
                ARM_NAMES[i]: effect(sensitivities[:, i]) for i in range(3)
            },
            "between_capacity_sensitivity_fixed_F8": effect(
                sensitivities[:, 0] - sensitivities[:, 1]
            ),
            "founder_dose_sensitivity_fixed_C48": effect(
                sensitivities[:, 1] - sensitivities[:, 2]
            ),
        }
    return {
        "status": "POST_OUTCOME_EXPLORATORY_RAW_AUTHENTICATED_CHANNEL_AUDIT",
        "source_run": 37887039116,
        "future_run": 37887290489,
        "full_future_count": 172032,
        "history_bootstrap": {"unit": "visitor_history", "n": 64,
                              "draws": DRAWS, "seed": SEED},
        "frozen_primary_unchanged": {
            "decision": "inconclusive",
            "estimate": primary["mean"],
            "bootstrap95": primary["history_bootstrap95"],
        },
        "initial_mechanical_checks": checks,
        "outcomes": by_metric,
        "interpretation_limits": [
            "Selected after seeing the independent primary inconclusive result: exploratory only.",
            "Cumulative selfed and outcross recruits depend on duration of population persistence.",
            "A correlation of cumulative recruitment with terminal occupancy is not causal mediation.",
            "The initial self-half seed-viability gate difference is engineered by design, not newly inferred.",
            "Terminal occupancy is not lifetime plant fitness or empirically calibrated Izu extinction.",
            "Founder abundance and genotype sampling remain inseparable in the fixed-capacity founder-dose comparator.",
            "No selective seed reruns, missing histories, new biological simulations, or redefinition of the frozen primary.",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--futures", type=Path, required=True)
    ap.add_argument("--source-admission", type=Path, required=True)
    ap.add_argument("--original-result", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--execute-readonly-audit", action="store_true")
    args = ap.parse_args()
    if not args.execute_readonly_audit:
        raise PermissionError("Explicit read-only analysis mode required")
    original = json.loads(args.original_result.read_text(encoding="utf-8"))
    if (original.get("status") !=
            "ALL_64_NEW_HISTORIES_2048_SOURCES_172032_FUTURES_AUTHENTICATED"
            or original.get("primary_decision") != "inconclusive"):
        raise AssertionError("Frozen original orthogonal readout missing")
    d, z, occupied, checks = load_channels(args.futures, args.source_admission)
    result = summarize(d, z, occupied, checks, original)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "frozen_primary": result["frozen_primary_unchanged"],
        "initial_checks": checks,
        "channels": {
            key: {arm: row["mean"] for arm, row in
                  val["viability_sensitivity_baseline_minus_self_half"].items()}
            for key, val in result["outcomes"].items()
            if key in ("cumulative_selfed_recruits", "cumulative_outcross_recruits",
                       "cumulative_total_recruits", "terminal_population",
                       "extinct_by_20", "terminal_occupancy")
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
