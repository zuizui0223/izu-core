"""Build a guarded register comparing the two Izu model families.

The source-level multichannel analysis and the island-stage pattern check reuse
some biological channels but answer different mathematical questions. This module
makes that non-equivalence explicit. It never pools their scores or selects a
single historical mechanism from their rank values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence


CLAIM_COLUMNS = (
    "claim_id",
    "status",
    "claim",
    "source_level_evidence",
    "stage_pattern_evidence",
    "current_safe_wording",
    "what_would_change_this",
)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _records(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    rows = payload.get(key)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"payload lacks a list of objects at {key!r}")
    return rows


def _rank(rows: Iterable[dict[str, Any]], metric: str, *, descending: bool) -> list[dict[str, Any]]:
    result = list(rows)
    if not result or any(metric not in row for row in result):
        raise ValueError(f"cannot rank empty rows or rows missing {metric!r}")
    return sorted(result, key=lambda row: float(row[metric]), reverse=descending)


def _rank_number(rows: Sequence[dict[str, Any]], label_field: str, label: str) -> int | None:
    for index, row in enumerate(rows, start=1):
        if str(row.get(label_field, "")) == label:
            return index
    return None


def _by_label(rows: Iterable[dict[str, Any]], label_field: str, label: str) -> dict[str, Any] | None:
    for row in rows:
        if str(row.get(label_field, "")) == label:
            return row
    return None


def _all_ablation_winners(source: dict[str, Any], scenario: str) -> bool:
    ablations = source.get("leave_one_channel_out")
    if not isinstance(ablations, dict) or not ablations:
        return False
    for rows in ablations.values():
        if not isinstance(rows, list) or not rows:
            return False
        ranked = _rank(rows, "log_marginal_compatibility", descending=True)
        if str(ranked[0].get("scenario", "")) != scenario:
            return False
    return True


def _retained_rows(source: dict[str, Any]) -> dict[str, Any]:
    retained = source.get("retained_rows")
    return retained if isinstance(retained, dict) else {}


def _guide_is_unresolved(source: dict[str, Any], stage: dict[str, Any]) -> bool:
    guide_n = _retained_rows(source).get("guide_constraints")
    observed = stage.get("observed_channels", [])
    return guide_n == 0 and (not isinstance(observed, list) or not any("guide" in str(value) for value in observed))


def build_register(
    source_level: dict[str, Any],
    profile: dict[str, Any],
    sensitivity: dict[str, Any],
    stage_pattern: dict[str, Any],
    ardens_envelope: dict[str, Any],
) -> dict[str, Any]:
    """Summarize compatible and non-comparable conclusions across model families."""
    source_ranked = _rank(_records(source_level, "full_evidence"), "log_marginal_compatibility", descending=True)
    profile_ranked = _rank(_records(profile, "results"), "best_log_likelihood", descending=True)
    stage_ranked = _rank(_records(stage_pattern, "model_scores"), "mean_absolute_error", descending=False)
    source_winner = str(source_ranked[0]["scenario"])
    profile_winner = str(profile_ranked[0]["scenario"])
    stage_winner = str(stage_ranked[0]["model"])
    source_rank_summary = _records(sensitivity, "rank_summary")
    sensitivity_winner = _by_label(source_rank_summary, "scenario", source_winner)
    if sensitivity_winner is None:
        raise ValueError(f"sensitivity output lacks source-level winner {source_winner!r}")

    stage_hierarchy_rank = _rank_number(stage_ranked, "model", "pollinator_hierarchy")
    stage_environment_rank = _rank_number(stage_ranked, "model", "environment_only")
    source_environment_rank = _rank_number(source_ranked, "scenario", "environment_only")
    envelope_rank_min = ardens_envelope.get("pollinator_hierarchy_best_rank")
    envelope_rank_max = ardens_envelope.get("pollinator_hierarchy_worst_rank")
    envelope_count = ardens_envelope.get("configuration_count")
    all_ablation = _all_ablation_winners(source_level, source_winner)
    profile_agrees = profile_winner == source_winner
    guide_unresolved = _guide_is_unresolved(source_level, stage_pattern)
    low_ess_warning = int(sensitivity_winner.get("warning_cells", 0)) > 0
    source_preference_status = (
        "conditional_support_with_monte_carlo_warning"
        if profile_agrees and all_ablation and low_ess_warning
        else "conditional_support"
        if profile_agrees and all_ablation
        else "restricted_family_preference_requires_manual_review"
    )

    claims = [
        {
            "claim_id": "source_level_preference",
            "status": source_preference_status,
            "claim": "Within the declared source-level scenario family, one scenario fits the retained direct-table channels best.",
            "source_level_evidence": (
                f"marginal winner={source_winner}; profile winner={profile_winner}; "
                f"winner retained in every leave-one-channel-out ranking={str(all_ablation).lower()}; "
                f"rank-one fraction={float(sensitivity_winner['rank_one_fraction']):.3f}; "
                f"warning cells={int(sensitivity_winner.get('warning_cells', 0))}."
            ),
            "stage_pattern_evidence": "The stage-pattern analysis does not fit this same restricted scenario family, so it cannot independently confirm this source-level preference.",
            "current_safe_wording": (
                f"Among the currently declared source-level scenarios, {source_winner} is the best compatible model region; "
                "its marginal-compatibility magnitude remains numerically fragile where importance-sampling ESS is low."
            ),
            "what_would_change_this": "More/adapted Monte Carlo integration, an explicitly comparable isolation-order scenario in the source-level family, and matched contemporary pollinator–reproduction measurements.",
        },
        {
            "claim_id": "stage_pattern_preference",
            "status": "conditional_support_for_stage_benchmark",
            "claim": "The simple island-stage signal is closer to one declared benchmark than to the bridge hierarchy benchmark.",
            "source_level_evidence": "The source-level family has no directly comparable isolation_order scenario, so it cannot test this stage benchmark symmetrically.",
            "stage_pattern_evidence": (
                f"{stage_winner} ranks first by mean absolute error. pollinator_hierarchy rank={stage_hierarchy_rank}; "
                f"the B. ardens non-report envelope has {envelope_count} configurations with hierarchy rank range {envelope_rank_min}–{envelope_rank_max}."
            ),
            "current_safe_wording": (
                f"For the currently locked, low-dimensional island-stage signal, {stage_winner} is the closest declared benchmark; "
                "this does not identify isolation as the causal evolutionary driver."
            ),
            "what_would_change_this": "A stage model that separates geographic order from measured pollinator service and a source-level model that includes an explicit isolation-order alternative.",
        },
        {
            "claim_id": "environment_only_not_leading",
            "status": "supported_across_model_families",
            "claim": "The declared environment-only explanation is not the leading model in either current family.",
            "source_level_evidence": f"environment_only source-level rank={source_environment_rank} of {len(source_ranked)}.",
            "stage_pattern_evidence": f"environment_only stage-pattern rank={stage_environment_rank} of {len(stage_ranked)}.",
            "current_safe_wording": "The particular temperature–precipitation proxy gradient currently implemented is insufficient as the leading stand-alone explanation in either analysis.",
            "what_would_change_this": "A preregistered environmental model with island-resolved microclimate, habitat, and demographic pathways rather than only the present proxy gradient.",
        },
        {
            "claim_id": "guide_loss_unidentified",
            "status": "blocked_by_missing_observation_channel" if guide_unresolved else "requires_manual_review",
            "claim": "Neither analysis identifies nectar-guide/spot loss or its mechanism.",
            "source_level_evidence": f"retained guide constraints={_retained_rows(source_level).get('guide_constraints', 'unknown')}",
            "stage_pattern_evidence": "The stage-pattern observed channels do not include island-resolved guide/spot measurements.",
            "current_safe_wording": "No current model comparison supports a claim about guide loss, its direction, or its selective cause.",
            "what_would_change_this": "Geographically verified, double-blind, island-resolved guide/spot measurements paired with pollinator handling and fitness-relevant outcomes.",
        },
        {
            "claim_id": "no_historical_causal_identification",
            "status": "not_identified",
            "claim": "The current analyses do not establish historical colonization, pollinator occupancy, pollination effectiveness, or causal evolutionary sequence.",
            "source_level_evidence": "Source-level likelihood uses reported summaries and declared residual terms; it is not a dated historical reconstruction or raw-individual fit.",
            "stage_pattern_evidence": "The stage comparison is a deterministic pattern score and the non-report envelope is not an occupancy/detection model.",
            "current_safe_wording": "Current outputs rank compatibility within declared model families; they do not prove the historical mechanism.",
            "what_would_change_this": "Replicated current island observations, explicit detection/occupancy design, reproductive-effectiveness measurements, and genetic or temporal evidence targeted to the competing pathways.",
        },
    ]

    return {
        "schema_version": 1,
        "boundary": (
            "This register compares conclusions, not numerical scores across model families. The source-level and stage-pattern rankings use different candidates, units, likelihoods, and objectives; their values must never be pooled or treated as one common evidence scale."
        ),
        "source_level_summary": {
            "winner": source_winner,
            "winner_log_marginal_compatibility": float(source_ranked[0]["log_marginal_compatibility"]),
            "profile_winner": profile_winner,
            "profile_best_log_likelihood": float(profile_ranked[0]["best_log_likelihood"]),
            "profile_agrees_with_marginal_winner": profile_agrees,
            "all_leave_one_channel_out_rank_one": all_ablation,
            "sensitivity_rank_one_fraction": float(sensitivity_winner["rank_one_fraction"]),
            "sensitivity_warning_cells": int(sensitivity_winner.get("warning_cells", 0)),
            "sensitivity_min_ess": float(sensitivity_winner.get("min_ess", 0.0)),
            "sensitivity_median_ess": float(sensitivity_winner.get("median_ess", 0.0)),
            "retained_rows": _retained_rows(source_level),
        },
        "stage_pattern_summary": {
            "winner": stage_winner,
            "winner_mean_absolute_error": float(stage_ranked[0]["mean_absolute_error"]),
            "pollinator_hierarchy_rank": stage_hierarchy_rank,
            "pollinator_hierarchy_envelope_configuration_count": envelope_count,
            "pollinator_hierarchy_envelope_rank_range": [envelope_rank_min, envelope_rank_max],
        },
        "claims": claims,
    }


def write_register(register: dict[str, Any], output_json: Path, output_csv: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(register, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import csv

    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CLAIM_COLUMNS)
        writer.writeheader()
        writer.writerows(register["claims"])

    source = register["source_level_summary"]
    stage = register["stage_pattern_summary"]
    lines = [
        "# Izu model-result register",
        "",
        str(register["boundary"]),
        "",
        "## What each analysis is allowed to answer",
        "",
        "| analysis family | unit and objective | candidates compared | non-transferable feature |",
        "|---|---|---|---|",
        "| source-level multichannel | direct source rows with declared summary-error likelihoods and restricted evolutionary scenarios | bridge loss, small-bee substitution, body-size-only, environment-only | no explicit isolation-order scenario; importance-sampling ESS can limit numerical resolution |",
        "| island-stage pattern | island-level composite signal matched to simple declared stage benchmarks | pollinator hierarchy, environment-only, isolation order | no source-row likelihood, no within-island variation, no causal or occupancy model |",
        "",
        "## Current outputs",
        "",
        "| result | value |",
        "|---|---|",
        f"| source-level best scenario | {source['winner']} |",
        f"| source-level profile best scenario | {source['profile_winner']} |",
        f"| source-level profile agrees with marginal winner | {str(source['profile_agrees_with_marginal_winner']).lower()} |",
        f"| source-level winner in every leave-one-channel-out run | {str(source['all_leave_one_channel_out_rank_one']).lower()} |",
        f"| source-level winner sensitivity rank-one fraction | {source['sensitivity_rank_one_fraction']:.3f} |",
        f"| source-level winner importance ESS (min / median) | {source['sensitivity_min_ess']:.2f} / {source['sensitivity_median_ess']:.2f} |",
        f"| stage-pattern best benchmark | {stage['winner']} |",
        f"| pollinator hierarchy stage rank | {stage['pollinator_hierarchy_rank']} |",
        f"| B. ardens envelope configurations / hierarchy rank range | {stage['pollinator_hierarchy_envelope_configuration_count']} / {stage['pollinator_hierarchy_envelope_rank_range'][0]}–{stage['pollinator_hierarchy_envelope_rank_range'][1]} |",
        "",
        "## Claim register",
        "",
        "| id | status | claim | safe current wording |",
        "|---|---|---|---|",
    ]
    for row in register["claims"]:
        lines.append(f"| {row['claim_id']} | {row['status']} | {row['claim']} | {row['current_safe_wording']} |")
    lines.extend((
        "",
        "## Interpretation discipline",
        "",
        "Do not resolve the different winners by averaging ranks, converting a likelihood to a pattern error, or treating island order as a historical cause. The informative result is a structured limitation: source-level restricted scenarios favor bridge loss, while the low-dimensional stage benchmark favors island order. The next analysis must make those alternatives comparable on the same observation scale.",
    ))
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
