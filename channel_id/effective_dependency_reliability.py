"""Reliability gate for the final direct reproductive-dependency estimand.

This module is intentionally downstream of the ordinary Campanula pilot and of
technical SVD recount calibration.  The focal pilot can estimate plant-level
dispersion, coverage and attrition; recounts of one preserved stigma can estimate
pollen-count repeatability.  Neither identifies the reliability ratio of the
final dependency predictor used by the dependency x FDQ design simulation.

A reliability ratio becomes estimable here only when the *same final estimand*
is independently re-estimated for several target taxon x site x season units
using non-overlapping plant panels and distinct frozen source bundles.  Even an
estimable calibration-scope reliability is not automatically transportable to a
cross-lineage design simulation.
"""

from __future__ import annotations

from collections import defaultdict
from math import isfinite
from statistics import mean
from typing import Mapping, Sequence

EXPECTED_ESTIMAND = "direct_reproductive_dependency_0_1"
REQUIRED_COLUMNS = frozenset(
    {
        "calibration_id",
        "target_unit_id",
        "taxon",
        "site_id",
        "season_id",
        "repeat_block_id",
        "estimand_name",
        "dependency_estimate",
        "independent_plants",
        "nonoverlapping_plant_panel",
        "protocol_id",
        "source_bundle_sha256",
    }
)


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _positive_int(row: Mapping[str, object], field: str) -> int:
    try:
        value = int(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be an integer") from error
    if value < 1:
        raise ValueError(f"{field} must be positive")
    return value


def _unit_value(row: Mapping[str, object], field: str) -> float:
    try:
        value = float(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric") from error
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{field} must be finite and lie in [0, 1]")
    return value


def _sha256(value: str) -> str:
    lowered = value.lower()
    if len(lowered) != 64 or any(character not in "0123456789abcdef" for character in lowered):
        raise ValueError("source_bundle_sha256 must be a 64-character hexadecimal SHA-256")
    return lowered


def _unequal_oneway_reliability(groups: Sequence[Sequence[float]]) -> dict[str, object]:
    """Variance-component reliability for repeated estimates of target units."""
    usable = [tuple(values) for values in groups if len(values) >= 2]
    if len(usable) < 3:
        return {
            "status": "not_estimable",
            "reason": "At least three target units with two or more eligible independent repeat blocks each are required.",
        }

    a = len(usable)
    n_total = sum(len(values) for values in usable)
    grand = sum(sum(values) for values in usable) / n_total
    ss_between = sum(len(values) * (mean(values) - grand) ** 2 for values in usable)
    ss_within = sum(sum((value - mean(values)) ** 2 for value in values) for values in usable)
    ms_between = ss_between / (a - 1)
    ms_within = ss_within / (n_total - a)
    n0 = (n_total - sum(len(values) ** 2 for values in usable) / n_total) / (a - 1)
    between_raw = (ms_between - ms_within) / n0
    between = max(0.0, between_raw)
    denominator = between + ms_within
    reliability = None if denominator <= 0.0 else between / denominator
    return {
        "status": "estimable",
        "target_units": a,
        "repeat_blocks": n_total,
        "mean_repeat_blocks_per_target": n_total / a,
        "ms_between_targets": ms_between,
        "ms_within_target_repeats": ms_within,
        "between_target_variance_component_raw": between_raw,
        "between_target_variance_component_nonnegative": between,
        "direct_dependency_repeat_reliability": reliability,
    }


def build_dependency_reliability_audit(
    rows: Sequence[Mapping[str, object]],
    *,
    expected_estimand: str = EXPECTED_ESTIMAND,
) -> dict[str, object]:
    """Audit whether repeated final dependency estimates identify reliability.

    A row is eligible only when its dependency estimate was built from at least
    two independent plants and the repeat explicitly uses a non-overlapping plant
    panel.  Within one target unit, frozen source-bundle checksums and repeat IDs
    must be distinct.  Repeats must also share one estimand and one analysis
    protocol before they can enter a pooled variance-component calculation.
    """

    seen_calibration_ids: set[str] = set()
    seen_repeat_ids: set[tuple[str, str]] = set()
    seen_bundle_by_target: set[tuple[str, str]] = set()
    target_metadata: dict[str, tuple[str, str, str]] = {}
    eligible: dict[str, list[dict[str, object]]] = defaultdict(list)
    ineligible_rows: list[dict[str, str]] = []

    for index, row in enumerate(rows, start=1):
        missing = REQUIRED_COLUMNS - set(row)
        if missing:
            raise ValueError("dependency reliability calibration missing columns: " + ", ".join(sorted(missing)))

        calibration_id = _text(row, "calibration_id")
        target = _text(row, "target_unit_id")
        taxon = _text(row, "taxon")
        site = _text(row, "site_id")
        season = _text(row, "season_id")
        repeat = _text(row, "repeat_block_id")
        estimand = _text(row, "estimand_name")
        protocol = _text(row, "protocol_id")
        if not all((calibration_id, target, taxon, site, season, repeat, estimand, protocol)):
            raise ValueError(f"blank required identifier in reliability row {index}")
        if calibration_id in seen_calibration_ids:
            raise ValueError(f"duplicate calibration_id={calibration_id!r}")
        seen_calibration_ids.add(calibration_id)
        repeat_key = (target, repeat)
        if repeat_key in seen_repeat_ids:
            raise ValueError(f"duplicate repeat_block_id={repeat!r} for target_unit_id={target!r}")
        seen_repeat_ids.add(repeat_key)

        bundle = _sha256(_text(row, "source_bundle_sha256"))
        bundle_key = (target, bundle)
        if bundle_key in seen_bundle_by_target:
            raise ValueError(f"source bundle reused as an independent repeat for target_unit_id={target!r}")
        seen_bundle_by_target.add(bundle_key)

        metadata = (taxon, site, season)
        if target in target_metadata and target_metadata[target] != metadata:
            raise ValueError(f"target_unit_id={target!r} maps to inconsistent taxon/site/season metadata")
        target_metadata[target] = metadata

        estimate = _unit_value(row, "dependency_estimate")
        independent_plants = _positive_int(row, "independent_plants")
        nonoverlap = _text(row, "nonoverlapping_plant_panel")
        if nonoverlap not in {"yes", "no"}:
            raise ValueError("nonoverlapping_plant_panel must be yes or no")

        reasons: list[str] = []
        if estimand != expected_estimand:
            reasons.append("estimand_mismatch")
        if independent_plants < 2:
            reasons.append("fewer_than_two_independent_plants")
        if nonoverlap != "yes":
            reasons.append("plant_panel_not_independent")
        if reasons:
            ineligible_rows.append({"calibration_id": calibration_id, "target_unit_id": target, "reason": ";".join(reasons)})
            continue
        eligible[target].append(
            {
                "estimate": estimate,
                "protocol_id": protocol,
                "taxon": taxon,
            }
        )

    repeated_targets = {target: values for target, values in eligible.items() if len(values) >= 2}
    protocols = sorted({str(item["protocol_id"]) for values in repeated_targets.values() for item in values})
    taxa = sorted({str(item["taxon"]) for values in repeated_targets.values() for item in values})
    target_means = [mean(float(item["estimate"]) for item in values) for values in repeated_targets.values()]

    if len(protocols) > 1:
        reliability = {
            "status": "not_estimable",
            "reason": "Eligible repeats use multiple protocol_id values; reliability is not pooled across incomparable final-estimand pipelines.",
        }
    else:
        reliability = _unequal_oneway_reliability(
            [[float(item["estimate"]) for item in values] for values in repeated_targets.values()]
        )

    identified = reliability.get("status") == "estimable" and reliability.get("direct_dependency_repeat_reliability") is not None
    return {
        "schema_version": "effective_dependency_reliability_audit_v1",
        "target_estimand": expected_estimand,
        "calibration_rows": len(rows),
        "eligible_repeat_rows": sum(len(values) for values in eligible.values()),
        "target_units_with_two_or_more_eligible_repeats": len(repeated_targets),
        "distinct_taxa_in_repeated_targets": len(taxa),
        "taxa_in_repeated_targets": taxa,
        "protocol_ids_in_repeated_targets": protocols,
        "target_mean_dependency_span": None if not target_means else max(target_means) - min(target_means),
        "ineligible_rows": ineligible_rows,
        "calibration_scope_reliability": reliability,
        "direct_dependency_reliability_identified_for_calibration_scope": identified,
        "dependency_fdq_design_reliability_admitted": False,
        "automatic_design_simulation_injection_allowed": False,
        "design_admission_next_gate": (
            "If calibration-scope reliability is estimable, separately review transportability to the prespecified cross-lineage taxon x site x season dependency predictor. "
            "Do not inject the value automatically."
            if identified
            else "Collect independent repeat blocks of the final dependency estimand across multiple target units before attempting a reliability ratio."
        ),
        "forbidden_substitutions": [
            "technical SVD recount repeatability",
            "repeated flowers within one plant",
            "repeated visits within one plant",
            "between-plant biological dispersion from one unrepeated target panel",
            "floral syndrome or visitor identity",
            "synthetic dependency reliability used in prospective design simulations",
        ],
        "claim_boundary": (
            "This gate can identify repeat reliability for the declared final dependency estimand within the calibration scope when independent repeated target panels exist. "
            "It does not by itself establish transportability to cross-lineage FDQ moderation, empirical power, historical Bombus causation, or a causal geographic boundary."
        ),
    }
