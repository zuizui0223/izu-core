"""Output guards for direct effective-pollinator dependency audits."""

from __future__ import annotations

from collections import defaultdict

from channel_id.effective_pollinator_dependency import EffectiveDependencyAudit


def mask_uncontrolled_effective_service(audit: EffectiveDependencyAudit) -> EffectiveDependencyAudit:
    """Withhold adjusted service values when no SVD background control exists.

    Raw SVD rows remain available for troubleshooting.  Official effective-service
    output, however, must not imply a background-adjusted estimate for a visitor
    group with neither an exposed-no-visit nor a bagged-unvisited control.  Shares
    are recomputed only among visitor groups with controlled SVD estimates.
    """
    uncontrolled = {
        (row["population_id"], row["visitor_group"])
        for row in audit.svd_group_rows
        if row["background_control_basis"] == "missing_no_visit_control"
    }

    rows = [dict(row) for row in audit.effective_service_rows]
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        key = (row["population_id"], row["visitor_group"])
        if key in uncontrolled:
            row["mean_background_adjusted_svd"] = ""
            row["effective_pollen_delivery_per_flower_hour"] = ""
            row["effective_service_share"] = ""
            row["boundary"] = (
                "Effective service withheld because this visitor group lacks a no-visit SVD background control. "
                "Raw visit rate and raw SVD remain audit information only."
            )
            continue
        value = row["effective_pollen_delivery_per_flower_hour"].strip()
        if value:
            totals[row["population_id"]] += float(value)

    for row in rows:
        key = (row["population_id"], row["visitor_group"])
        if key in uncontrolled:
            continue
        value = row["effective_pollen_delivery_per_flower_hour"].strip()
        total = totals.get(row["population_id"], 0.0)
        row["effective_service_share"] = f"{float(value) / total:.8f}" if value and total > 0 else ""

    return EffectiveDependencyAudit(
        svd_group_rows=audit.svd_group_rows,
        effective_service_rows=tuple(rows),
        treatment_rows=audit.treatment_rows,
        population_readiness_rows=audit.population_readiness_rows,
        summary=audit.summary,
    )
