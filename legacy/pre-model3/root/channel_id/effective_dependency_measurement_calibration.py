"""Technical recount calibration for SVD pollen counts.

This module estimates technical repeatability from independent recounts of the
same preserved SVD sample. It is intentionally narrower than direct dependency
reliability: biological flower-to-flower variation, visitor sampling, and
reproductive-treatment uncertainty remain outside this calibration layer.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Mapping, Sequence


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _count(row: Mapping[str, object], field: str) -> int:
    value = int(_text(row, field))
    if value < 0:
        raise ValueError(f"{field} must be non-negative")
    return value


def _unequal_oneway_repeatability(groups: Sequence[Sequence[float]]) -> dict[str, object]:
    usable = [tuple(values) for values in groups if len(values) >= 2]
    if len(usable) < 3:
        return {
            "status": "not_estimable",
            "reason": "At least three distinct SVD samples with two or more independent recounts each are required.",
        }

    a = len(usable)
    n_total = sum(len(values) for values in usable)
    grand = sum(sum(values) for values in usable) / n_total
    ss_between = sum(len(values) * (mean(values) - grand) ** 2 for values in usable)
    ss_within = sum(sum((value - mean(values)) ** 2 for value in values) for values in usable)
    ms_between = ss_between / (a - 1)
    ms_within = ss_within / (n_total - a)
    n0 = (n_total - sum(len(values) ** 2 for values in usable) / n_total) / (a - 1)
    between_component_raw = (ms_between - ms_within) / n0
    between_component = max(0.0, between_component_raw)
    denominator = between_component + ms_within
    repeatability = None if denominator <= 0 else between_component / denominator
    return {
        "status": "estimable",
        "distinct_svd_samples": a,
        "technical_recounts": n_total,
        "mean_recounts_per_sample": n_total / a,
        "ms_between_samples": ms_between,
        "ms_within_sample_recounts": ms_within,
        "between_sample_variance_component_raw": between_component_raw,
        "between_sample_variance_component_nonnegative": between_component,
        "technical_recount_repeatability": repeatability,
        "boundary": "This is repeatability of pollen counting on the same preserved SVD sample, not reliability of the biological direct-dependency estimand.",
    }


def build_svd_recount_calibration(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    required = {
        "calibration_id", "svd_id", "recount_id", "counter_id", "blinded_to_original",
        "total_pollen_grains", "conspecific_pollen_grains", "heterospecific_pollen_grains",
        "unclassified_pollen_grains",
    }
    seen_calibration_ids: set[str] = set()
    seen_recounts: set[tuple[str, str]] = set()
    by_svd: dict[str, list[dict[str, object]]] = defaultdict(list)

    for row in rows:
        missing = required - set(row)
        if missing:
            raise ValueError("recount calibration missing columns: " + ", ".join(sorted(missing)))
        calibration_id = _text(row, "calibration_id")
        svd_id = _text(row, "svd_id")
        recount_id = _text(row, "recount_id")
        if not calibration_id or not svd_id or not recount_id or not _text(row, "counter_id"):
            raise ValueError("calibration_id, svd_id, recount_id, and counter_id are required")
        if calibration_id in seen_calibration_ids:
            raise ValueError(f"duplicate calibration_id={calibration_id!r}")
        seen_calibration_ids.add(calibration_id)
        key = (svd_id, recount_id)
        if key in seen_recounts:
            raise ValueError(f"duplicate recount_id={recount_id!r} for svd_id={svd_id!r}")
        seen_recounts.add(key)
        if _text(row, "blinded_to_original") not in {"yes", "no"}:
            raise ValueError("blinded_to_original must be yes or no")
        counts = {
            field: _count(row, field)
            for field in (
                "total_pollen_grains", "conspecific_pollen_grains", "heterospecific_pollen_grains",
                "unclassified_pollen_grains",
            )
        }
        if counts["total_pollen_grains"] != (
            counts["conspecific_pollen_grains"]
            + counts["heterospecific_pollen_grains"]
            + counts["unclassified_pollen_grains"]
        ):
            raise ValueError(f"pollen count partition does not sum for calibration_id={calibration_id!r}")
        by_svd[svd_id].append({
            "conspecific": counts["conspecific_pollen_grains"],
            "blinded": _text(row, "blinded_to_original") == "yes",
            "counter_id": _text(row, "counter_id"),
        })

    groups = [[float(item["conspecific"]) for item in values] for values in by_svd.values()]
    repeatability = _unequal_oneway_repeatability(groups)
    blinded_fraction = None
    if rows:
        blinded_fraction = sum(_text(row, "blinded_to_original") == "yes" for row in rows) / len(rows)
    distinct_counters = sorted({_text(row, "counter_id") for row in rows if _text(row, "counter_id")})

    return {
        "schema_version": "effective_dependency_svd_recount_calibration_v1",
        "distinct_svd_samples": len(by_svd),
        "technical_recount_rows": len(rows),
        "blinded_recount_fraction": blinded_fraction,
        "distinct_counters": distinct_counters,
        "conspecific_pollen_count_repeatability": repeatability,
        "direct_dependency_reliability_identified": False,
        "direct_dependency_reliability_boundary": (
            "Technical recount repeatability can inform the pollen-count measurement-error component only. "
            "It does not absorb biological flower-to-flower variation, visitor sampling error, treatment outcome variation, "
            "or cross-taxon uncertainty and therefore must not be substituted directly for dependency_reliability in the design simulation."
        ),
    }
