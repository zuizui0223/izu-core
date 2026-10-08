"""Frozen time window -> transient A/I phenotype offsets, with no outcomes.

Keep this scheduling module separate from Model 3 core and its source archive.
"""
from __future__ import annotations

from scripts.plan_chapter2_order_expression_identification import validate_protocol


def assigned_offsets(protocol: dict, arm: str, year: int) -> tuple[float, float]:
    """Return (assurance_logit_shift, investment_logit_shift) at update year.

    The t=400 genotype census is an endpoint and has no reproductive update.
    """
    if isinstance(year, bool) or not isinstance(year, int) or not 0 <= year < 400:
        raise ValueError("year must be one of the 400 declared prehistory updates")
    try:
        phases = protocol["path_perturbation"]["arms"][arm]
    except (KeyError, TypeError) as exc:
        raise ValueError("unknown expression-order treatment") from exc
    for phase in phases:
        if phase["from"] <= year < phase["to"]:
            return float(phase["A"]), float(phase["I"])
    raise AssertionError("noncontiguous assigned expression schedule")


def validate_scheduled_interventions(protocol: dict) -> dict:
    """Reconcile all yearwise offsets against the prospectively frozen doses."""
    validate_protocol(protocol)
    report = {}
    for arm in protocol["path_perturbation"]["arms"]:
        yearly = [assigned_offsets(protocol, arm, t) for t in range(400)]
        positive_a = sum(a == 0.45 for a, _ in yearly)
        negative_i = sum(i == -0.45 for _, i in yearly)
        no_offset_tail = all(v == (0.0, 0.0) for v in yearly[300:])
        if positive_a != 200 or negative_i != 200 or not no_offset_tail:
            raise AssertionError("wrong dosage or missing common release")
        report[arm] = {
            "A_offset_years": positive_a,
            "I_offset_years": negative_i,
            "common_release_updates": 100,
        }
    return report
