"""Pure prospective Chapter 2 fixed-founder capacity readout algebra.

This module does NOT generate biological data and does NOT admit raw archives.
Full 2048-source/172032-future cryptographic admission MUST precede its use
for a scientific verdict. The new source and raw-admission runner are pending.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    load_protocol, log_budget_weights,
)
from scripts.plan_chapter2_orthogonal_founder_capacity import (
    PROTOCOL, validate_protocol,
)


EXPECTED_SHAPE = (64, 4, 2, 2, 2, 7, 2, 3, 2)
ARM_NAMES = (
    "eight_founders_capacity8",
    "eight_founders_capacity48",
    "all_available_founders_capacity48",
)
GATE_NAMES = ("baseline", "self_half")


def history_order_effects(occupied: np.ndarray, *, design: dict) -> np.ndarray:
    """From complete binary grid to 64 histories x 3 arms x 2 gates.

    Axes: history, setting, past visitor, expression assignment,
    demographic repeat, budget, future visitor, arm, viability gate.
    """
    z = np.asarray(occupied)
    if z.shape != EXPECTED_SHAPE or not np.isfinite(z).all():
        raise ValueError("Require the entire 172032-binary-future grid")
    if np.any((z != 0) & (z != 1)):
        raise ValueError("Occupancy must be binary with pre-extinct sources retained")
    if tuple(design["postshock"]["budgets"]) != (0.5, 1, 2, 3, 4, 5, 8):
        raise AssertionError("Unexpected log-weight budget support")

    log_weights = log_budget_weights(design)
    weights = np.array(
        [log_weights[float(b)] for b in design["postshock"]["budgets"]],
        dtype=float,
    )
    if not np.isfinite(weights).all() or abs(float(weights.sum()) - 1) > 1e-12:
        raise AssertionError("Invalid preregistered log-budget weights")

    pooled_repeats = z.mean(axis=(4, 6))
    if pooled_repeats.shape != (64, 4, 2, 2, 7, 3, 2):
        raise AssertionError("Unexpected future pairing axes")
    weighted = np.tensordot(pooled_repeats, weights, axes=([4], [0]))
    if weighted.shape != (64, 4, 2, 2, 3, 2):
        raise AssertionError("Unexpected weighted axes")
    assignment = weighted[:, :, :, 0, :, :] - weighted[:, :, :, 1, :, :]
    result = assignment.mean(axis=(1, 2))
    if result.shape != (64, 3, 2) or not np.isfinite(result).all():
        raise AssertionError("Invalid visitor-history cluster reduction")
    return result


def summarize_history_effects(
    history_effects: np.ndarray, *,
    draws: int = 9999, seed: int = 2026100943,
) -> dict:
    """Joint cluster bootstrap, never resampling separate future branches."""
    a = np.asarray(history_effects, dtype=float)
    if a.shape != (64, 3, 2) or not np.isfinite(a).all():
        raise ValueError("Required: 64 paired-history x 3 arms x 2 gates")
    if np.any(np.abs(a) > 1 + 1e-12):
        raise ValueError("Invalid mean occupancy assignment contrast")
    if draws != 9999 or seed != 2026100943:
        raise ValueError("Frozen bootstrap draw count and seed changed")

    tau = a[:, :, 0] - a[:, :, 1]
    contrasts = {
        "primary_capacity_conditional_fixed_eight": tau[:, 0] - tau[:, 1],
        "secondary_founder_abundance_and_sampling": tau[:, 1] - tau[:, 2],
    }
    indices = np.random.default_rng(seed).integers(0, 64, size=(draws, 64))

    def summary(v: np.ndarray) -> dict:
        mean = float(v.mean())
        interval = np.percentile(v[indices].mean(axis=1), [2.5, 97.5])
        return {
            "mean": mean,
            "history_bootstrap95": interval.tolist(),
            "positive_histories": int(np.count_nonzero(v > 1e-12)),
            "negative_histories": int(np.count_nonzero(v < -1e-12)),
            "zero_histories": int(np.count_nonzero(abs(v) <= 1e-12)),
        }

    estimates = {name: summary(v) for name, v in contrasts.items()}
    estimates_by_arm = {name: summary(tau[:, i]) for i, name in enumerate(ARM_NAMES)}
    primary = estimates["primary_capacity_conditional_fixed_eight"]
    lo, hi = primary["history_bootstrap95"]
    if abs(primary["mean"]) >= 0.005 and (lo > 0 or hi < 0):
        decision = "supported_conditional_capacity_moderation"
    elif lo > -0.005 and hi < 0.005:
        decision = "practically_equivalent_within_0p005"
    else:
        decision = "inconclusive"

    return {
        "status": "ALGEBRA_ONLY_NOT_AN_ADMITTED_SCIENTIFIC_RESULT",
        "planned_histories": 64,
        "planned_full_futures": 172032,
        "independent_inference_unit": "visitor_history",
        "bootstrap": {
            "draws": draws, "seed": seed, "unit": "paired_visitor_history",
        },
        "by_arm_self_viability_sensitivity": estimates_by_arm,
        "contrasts": estimates,
        "primary_decision_if_and_only_if_complete_raw_archive_admitted": decision,
        "critical_interpretation": (
            "The fixed-eight capacity contrast is model-conditional; "
            "the secondary fixed-capacity contrast combines founder number "
            "and sampled genotypes. This arithmetic is not confirmation "
            "without a complete independently authenticated future archive."
        ),
    }


def validate_readout_contract() -> dict:
    """Safe preflight only; neither simulates nor examines future outcomes."""
    plan = validate_protocol()
    frozen = json.loads(Path(PROTOCOL).read_text(encoding="utf-8"))
    biology = load_protocol()
    if tuple(x["name"] for x in frozen["experimental_arms"]) != ARM_NAMES:
        raise AssertionError("Unexpected arm order")
    if tuple(x["name"] for x in frozen["postzygotic_gates"]) != GATE_NAMES:
        raise AssertionError("Unexpected gate order")
    if tuple(biology["postshock"]["budgets"]) != tuple(
        frozen["complete_future_grid"]["budgets"]
    ):
        raise AssertionError("Budget definition drift")
    if plan["planned_futures"] != int(np.prod(EXPECTED_SHAPE)):
        raise AssertionError("Full-grid shape not aligned to frozen design")
    return {"status": "READOUT_ALGEBRA_PREFLIGHT_ONLY",
            "expected_shape": list(EXPECTED_SHAPE),
            "science_executed": False}


if __name__ == "__main__":
    print(json.dumps(validate_readout_contract(), sort_keys=True))
