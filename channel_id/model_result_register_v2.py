"""Five-candidate, tempered-SMC-aware Izu result register.

This register compares conclusions across model families. It does not pool
source-level compatibility values with island-stage pattern errors, and it does
not interpret ordinal proxy fit as historical causation.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

COLUMNS = (
    "claim_id", "status", "claim", "source_level_evidence",
    "stage_pattern_evidence", "current_safe_wording", "what_would_change_this",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def _rows(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f"missing row list: {key}")
    return value


def _rank(rows: Iterable[dict[str, Any]], key: str, reverse: bool = True) -> list[dict[str, Any]]:
    values = list(rows)
    if not values or any(key not in row for row in values):
        raise ValueError(f"cannot rank rows by {key}")
    return sorted(values, key=lambda row: float(row[key]), reverse=reverse)


def _find(rows: Iterable[dict[str, Any]], scenario: str) -> dict[str, Any] | None:
    return next((row for row in rows if str(row.get("scenario")) == scenario), None)


def _rank_position(rows: list[dict[str, Any]], scenario: str) -> int | None:
    for position, row in enumerate(rows, 1):
        if str(row.get("scenario", row.get("model", ""))) == scenario:
            return position
    return None


def _ablation_winners(source: dict[str, Any]) -> dict[str, str]:
    blocks = source.get("leave_one_channel_out")
    if not isinstance(blocks, dict):
        raise ValueError("missing source ablations")
    answer: dict[str, str] = {}
    for channel, rows in blocks.items():
        answer[str(channel)] = str(_rank(rows, "log_marginal_compatibility")[0]["scenario"])
    return answer


def build_register(
    source: dict[str, Any],
    profile: dict[str, Any],
    sensitivity: dict[str, Any],
    smc: dict[str, Any],
    stage: dict[str, Any],
    envelope: dict[str, Any],
) -> dict[str, Any]:
    source_ranked = _rank(_rows(source, "full_evidence"), "log_marginal_compatibility")
    profile_ranked = _rank(_rows(profile, "results"), "best_log_likelihood")
    smc_ranked = sorted(
        _rows(smc, "rank_summary"),
        key=lambda row: (-float(row["rank_one_fraction"]), -float(row["mean_log_marginal_compatibility"])),
    )
    stage_ranked = _rank(_rows(stage, "model_scores"), "mean_absolute_error", reverse=False)
    full_winner = str(source_ranked[0]["scenario"])
    profile_winner = str(profile_ranked[0]["scenario"])
    smc_winner = str(smc_ranked[0]["scenario"])
    order_smc = _find(smc_ranked, "isolation_order")
    bridge_smc = _find(smc_ranked, "ardens_bridge_loss")
    if order_smc is None or bridge_smc is None:
        raise ValueError("SMC output lacks order or bridge candidate")
    deltas = _rows(smc, "bridge_order_deltas")
    mean_delta = mean(float(row["order_minus_bridge"]) for row in deltas)
    all_order_higher = all(bool(row["order_higher"]) for row in deltas)
    ablations = _ablation_winners(source)
    guide_n = source.get("retained_rows", {}).get("guide_constraints", 0)
    stage_order_rank = _rank_position(stage_ranked, "isolation_order")
    stage_hierarchy_rank = _rank_position(stage_ranked, "pollinator_hierarchy")
    stage_environment_rank = _rank_position(stage_ranked, "environment_only")
    source_environment_rank = _rank_position(source_ranked, "environment_only")
    bridge_without = [name for name, winner in ablations.items() if winner == "ardens_bridge_loss"]

    claims = [
        {
            "claim_id": "ordinal_proxy_source_level_preference",
            "status": "conditional_support_with_channel_dependence",
            "claim": "The fixed ordinal island-order proxy currently leads the source-level candidate family.",
            "source_level_evidence": f"full={full_winner}; profile={profile_winner}; smc={smc_winner}; order SMC rank-one fraction={float(order_smc['rank_one_fraction']):.3f}; mean order-minus-bridge={mean_delta:.3f}; all order higher={str(all_order_higher).lower()}; ablations={ablations}.",
            "stage_pattern_evidence": f"The collapsed stage benchmark also ranks isolation_order={stage_order_rank} and pollinator_hierarchy={stage_hierarchy_rank}.",
            "current_safe_wording": "The fixed ordinal proxy is currently most compatible within the declared source-level family, but its lead depends on retaining the flower-length channel and does not identify a causal isolation process.",
            "what_would_change_this": "Independent population-resolved flower data, an alternative preregistered order scaffold, and guide/handling/fitness evidence not collinear with island order.",
        },
        {
            "claim_id": "bridge_loss_not_unique",
            "status": "not_uniquely_supported",
            "claim": "The B. ardens bridge-loss explanation is not uniquely selected by the retained summaries.",
            "source_level_evidence": f"bridge SMC rank-one fraction={float(bridge_smc['rank_one_fraction']):.3f}; it becomes ablation winner when omitted={';'.join(bridge_without) or 'none'}.",
            "stage_pattern_evidence": f"pollinator_hierarchy stage rank={stage_hierarchy_rank}; non-report envelope rank range={envelope.get('pollinator_hierarchy_best_rank')}–{envelope.get('pollinator_hierarchy_worst_rank')}.",
            "current_safe_wording": "Bridge loss remains a plausible restricted explanation in the non-flower channels, but the retained flower-length channel currently shifts the matched comparison toward the ordinal proxy; bridge loss is not uniquely preferred.",
            "what_would_change_this": "Matched pollinator-handling and reproductive-effectiveness data, plus flower-length replication that separates service effects from order-correlated effects.",
        },
        {
            "claim_id": "environment_only_not_leading",
            "status": "supported_across_model_families",
            "claim": "The present environment-only proxy is not leading in either family.",
            "source_level_evidence": f"source rank={source_environment_rank} of {len(source_ranked)}; SMC mean rank={float((_find(smc_ranked, 'environment_only') or {}).get('mean_rank', 0.0)):.3f}.",
            "stage_pattern_evidence": f"stage rank={stage_environment_rank} of {len(stage_ranked)}.",
            "current_safe_wording": "The implemented climate proxy is insufficient as a stand-alone explanation; this does not make environment irrelevant.",
            "what_would_change_this": "A preregistered model with island-resolved microclimate, habitat, demography, and temporal pathways.",
        },
        {
            "claim_id": "guide_loss_unidentified",
            "status": "blocked_by_missing_observation_channel" if guide_n == 0 else "requires_manual_review",
            "claim": "Guide or spot loss is not identified.",
            "source_level_evidence": f"reviewed guide constraints={guide_n}; SMC cannot add information to an absent channel.",
            "stage_pattern_evidence": "No island-resolved guide channel enters the stage model.",
            "current_safe_wording": "No current model ranking supports a claim about guide loss or its mechanism.",
            "what_would_change_this": "Blind-reviewed, geographically verified guide/spot measurements with handling and fitness outcomes.",
        },
        {
            "claim_id": "no_historical_causal_identification",
            "status": "not_identified",
            "claim": "The analyses do not prove historical sequence, occupancy, effectiveness, or causal mechanism.",
            "source_level_evidence": "Tempered SMC stabilizes integration within a restricted model family; it adds no historical observation.",
            "stage_pattern_evidence": "Stage scores and the non-report envelope are not historical or occupancy models.",
            "current_safe_wording": "Current outputs compare declared compatibility models, not historical causation.",
            "what_would_change_this": "Repeated modern observation, detection-aware sampling, per-visit effectiveness, mating outcomes, and targeted genetic or temporal evidence.",
        },
    ]
    return {
        "schema_version": 2,
        "boundary": "Do not pool source-level likelihood, profile, sensitivity, or tempered-SMC values with stage-pattern errors. The ordinal candidate is a fixed proxy, not distance, history, or causal isolation.",
        "source_level_summary": {
            "full_winner": full_winner,
            "profile_winner": profile_winner,
            "smc_winner": smc_winner,
            "smc_order_rank_one_fraction": float(order_smc["rank_one_fraction"]),
            "smc_mean_order_minus_bridge": mean_delta,
            "smc_order_higher_all_replicates": all_order_higher,
            "ablation_winners": ablations,
            "retained_rows": source.get("retained_rows", {}),
        },
        "stage_pattern_summary": {
            "winner": str(stage_ranked[0]["model"]),
            "isolation_order_rank": stage_order_rank,
            "pollinator_hierarchy_rank": stage_hierarchy_rank,
        },
        "claims": claims,
    }


def write_register(register: dict[str, Any], output_json: Path, output_csv: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(register, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(register["claims"])
    source = register["source_level_summary"]
    stage = register["stage_pattern_summary"]
    lines = [
        "# Izu model-result register", "", str(register["boundary"]), "",
        "| result | value |", "|---|---|",
        f"| source full/profile/SMC winners | {source['full_winner']} / {source['profile_winner']} / {source['smc_winner']} |",
        f"| SMC mean order-minus-bridge | {source['smc_mean_order_minus_bridge']:.3f} |",
        f"| order higher in all SMC replicates | {str(source['smc_order_higher_all_replicates']).lower()} |",
        f"| source ablation winners | {source['ablation_winners']} |",
        f"| stage winner / hierarchy rank | {stage['winner']} / {stage['pollinator_hierarchy_rank']} |",
        "", "## Claim register", "", "| id | status | safe wording |", "|---|---|---|",
    ]
    for row in register["claims"]:
        lines.append(f"| {row['claim_id']} | {row['status']} | {row['current_safe_wording']} |")
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
