"""R2 source-only maternal payoff diagnostic on the original frozen pollen factorial.

This constructs homogeneous artificial plant reporters and evaluates ONE expected
reproduction ledger per condition, plus two finite-difference ledgers. It never
advances a population, resamples the 384 trajectories, estimates new p-values,
or isolates causal mediation in the original evolutionary experiment.
"""
from __future__ import annotations

import json
from math import log, isfinite
from pathlib import Path

import numpy as np

from scripts.chapter2_pollen_baseline_factorial_20261019 import (
    admit, config, visitors,
)
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState

ROOT = Path(__file__).resolve().parents[1]
STATUS = "EXPLORATORY_EXACT_NATIVE_STATIC_MATERNAL_ASSAY_NO_EVOLUTION"
PREFIX_A_VALUES = (0.3, 0.5)
EFFECTIVENESS_STRATA = ("strong_baseline_limitation", "weak_baseline_limitation")
ARMS = (("control", 0.4), ("decline", 0.04))


def _reporter(a: float, n: int = 48) -> PlantState:
    if not (0 < a < 1 and isinstance(n, int) and n > 1):
        raise ValueError("maternal gradient requires an interior reporter A and n > 1")
    alleles = np.full((n, 3, 2), 0.5, dtype=np.float64)
    alleles[:, 2, :] = a
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def _ledger(a: float, d: dict, baseline: str, activity: float):
    return reproduce(_reporter(a), visitors(d, baseline),
                     config(d, baseline, activity))


def _relative_q(ledger) -> float:
    o = float(ledger.ovules.sum())
    return float(ledger.outcross.sum() / o)


def maternal_grad_and_threshold(a: float, q: float, viable_self: float,
                                direct_assurance_cost: float) -> tuple[float, float]:
    """Exact static derivative of log viable maternal return at fixed q, M, I.

    For the original delayed selfing operator without pollen discount:
       Y = O0 exp(-cA*A^2) [q + (1-q)*v*A].
    The threshold is in q, NOT a resource budget, historical colonisation age,
    or proven threshold in population evolution.
    """
    if not (0 < a < 1 and 0 <= q <= 1 and
            0 < viable_self <= 1 and direct_assurance_cost > 0):
        raise ValueError("invalid interior maternal-payoff condition")
    z = q + (1 - q) * viable_self * a
    if z <= 0:
        raise ArithmeticError("zero viable maternal return")
    grad = viable_self * (1 - q) / z - 2 * direct_assurance_cost * a
    upper = viable_self * (1 - 2 * direct_assurance_cost * a * a)
    threshold = (upper / (upper + 2 * direct_assurance_cost * a)
                 if upper > 0 else None)
    return grad, threshold


def analyze() -> dict:
    # Original frozen protocol and full native operator source hashes are checked
    # by admit(); do not weaken these checks when original source changes.
    d = admit()
    f, m = d["factorial"], d["model"]
    if (d["status"] != "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
            or tuple(f["initial_A_means"]) != PREFIX_A_VALUES
            or m["assurance_timing"] != "delayed"
            or m["assurance_mode"] != "evolving"
            or m["pollen_discount"] != 0
            or m["capacity"] != 48
            or m["mutation_rate"] != 0
            or m["inbreeding_depression"] != 0.5
            or m["assurance_cost"] != 0.5
            or m["pollen_scale"] != 0.15
            or f["freeze_prefix_updates"] != 30
            or f["future_updates"] != 50):
        raise AssertionError("the source-locked 384 pilot context changed")
    v = 1.0 - m["inbreeding_depression"]
    c_a = m["assurance_cost"]
    result = []
    for a in PREFIX_A_VALUES:
        for level in EFFECTIVENESS_STRATA:
            if level not in f["effectiveness"]:
                raise AssertionError("missing original pollen limitation regime")
            for name, activity in ARMS:
                if activity != f["pollinator_activity"][("control_future" if name == "control" else "decline_future")]:
                    raise AssertionError("original activity allocation changed")
                native = _ledger(a, d, level, activity)
                q = _relative_q(native)
                o = float(native.ovules.sum())
                viable = float(native.maternal.sum())
                expected = o * (q + (1 - q) * v * a)
                if not np.isclose(viable, expected, rtol=0, atol=1e-10):
                    raise AssertionError("maternal source kernel mismatches the frozen identity")
                gradient, threshold = maternal_grad_and_threshold(a, q, v, c_a)
                h = 1e-6
                lp = log(float(_ledger(a+h, d, level, activity).maternal.sum()))
                lm = log(float(_ledger(a-h, d, level, activity).maternal.sum()))
                numerical = (lp - lm) / (2 * h)
                if not (isfinite(numerical) and abs(numerical-gradient) < 2e-7):
                    raise AssertionError("native source maternal A-gradient finite difference failed")
                if threshold is None or not (0 < threshold < 1):
                    raise AssertionError("expected interior maternal q threshold missing")
                if (gradient > 0) != (q < threshold):
                    raise AssertionError("maternal gradient and conditional threshold disagree")
                # Frozen homogeneous diagnostic uses A=.5 and zero A pollen discount.
                if a == 0.5:
                    key = level.replace("_limitation", "_limit")
                    key += ("_control_initial_outcross_fraction" if name == "control"
                            else "_after_decline_initial_outcross_fraction")
                    if abs(q - d["native_preexecution_homogeneous_q_diagnostic"][key]) > 1e-4:
                        raise AssertionError("static reporter pollen fraction does not match original admission")
                result.append({
                    "initial_reporter_A": a,
                    "baseline": level,
                    "future_arm": name,
                    "activity": activity,
                    "outcross_ovule_fraction_q": q,
                    "viable_maternal_seed_expected": viable,
                    "analytic_log_maternal_return_gradient_A": gradient,
                    "finite_difference_gradient_A": numerical,
                    "conditional_q_sign_switch_for_this_A": threshold,
                    "within_source_maternal_gradient_positive": gradient > 0,
                    "no_evolution_trajectory": True,
                })
    return {
        "status": STATUS,
        "original_source_protocol_sha256": "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849",
        "design": "48 identical source-model reporter plants at I=M=.5, A=.3/.5; four visitor treatments",
        "rows": result,
        "comparison": (
            "This is an instantaneous MATERNAL genetic-return accounting result "
            "conditional on identical synthetic resident states. It does not "
            "estimate the full paternal-inclusive A selection gradient, population "
            "fixation probability, or mediate archived R2 evolutionary endpoints."
        ),
        "observed_R2_384_results_reused_as_outcomes": False,
        "new_biological_population_updates": 0,
        "new_statistical_tests": 0,
        "registration_claim": "EXPLORATORY_PREVIOUSLY_EXPOSED_SOURCE_NOT_INDEPENDENT_CONFIRMATION",
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2, ensure_ascii=False))
