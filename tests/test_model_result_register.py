import json
from pathlib import Path

from channel_id.model_result_register import build_register, load_json, write_register


def _source() -> dict:
    return {
        "retained_rows": {"outcrossing": 17, "bagging": 7, "flower": 6, "guide_constraints": 0},
        "full_evidence": [
            {"scenario": "ardens_bridge_loss", "log_marginal_compatibility": -10.0},
            {"scenario": "small_bee_substitution", "log_marginal_compatibility": -12.0},
            {"scenario": "environment_only", "log_marginal_compatibility": -15.0},
        ],
        "leave_one_channel_out": {
            "outcrossing": [
                {"scenario": "ardens_bridge_loss", "log_marginal_compatibility": -7.0},
                {"scenario": "environment_only", "log_marginal_compatibility": -9.0},
            ],
            "bagging": [
                {"scenario": "ardens_bridge_loss", "log_marginal_compatibility": -6.0},
                {"scenario": "environment_only", "log_marginal_compatibility": -8.0},
            ],
        },
    }


def _profile(*, winner: str = "ardens_bridge_loss") -> dict:
    rows = [
        {"scenario": "ardens_bridge_loss", "best_log_likelihood": -5.0},
        {"scenario": "environment_only", "best_log_likelihood": -9.0},
    ]
    if winner == "environment_only":
        rows = [
            {"scenario": "environment_only", "best_log_likelihood": -4.0},
            {"scenario": "ardens_bridge_loss", "best_log_likelihood": -5.0},
        ]
    return {"results": rows}


def _sensitivity() -> dict:
    return {
        "rank_summary": [
            {
                "scenario": "ardens_bridge_loss",
                "rank_one_fraction": 1.0,
                "warning_cells": 9,
                "min_ess": 1.1,
                "median_ess": 2.0,
            }
        ]
    }


def _stage() -> dict:
    return {
        "observed_channels": ["outcrossing_rate", "bagged_seed_or_capsule_set", "flower_length"],
        "model_scores": [
            {"model": "isolation_order", "mean_absolute_error": 0.1},
            {"model": "pollinator_hierarchy", "mean_absolute_error": 0.2},
            {"model": "environment_only", "mean_absolute_error": 0.3},
        ],
    }


def _envelope() -> dict:
    return {
        "configuration_count": 32,
        "pollinator_hierarchy_best_rank": 2,
        "pollinator_hierarchy_worst_rank": 2,
    }


def test_register_retains_model_family_non_equivalence_and_ess_warning() -> None:
    register = build_register(_source(), _profile(), _sensitivity(), _stage(), _envelope())

    assert register["source_level_summary"]["winner"] == "ardens_bridge_loss"
    assert register["source_level_summary"]["profile_winner"] == "ardens_bridge_loss"
    assert register["source_level_summary"]["profile_agrees_with_marginal_winner"] is True
    assert register["source_level_summary"]["all_leave_one_channel_out_rank_one"] is True
    assert register["stage_pattern_summary"]["winner"] == "isolation_order"
    assert register["stage_pattern_summary"]["pollinator_hierarchy_envelope_rank_range"] == [2, 2]
    claims = {row["claim_id"]: row for row in register["claims"]}
    assert claims["source_level_preference"]["status"] == "conditional_support_with_monte_carlo_warning"
    assert claims["environment_only_not_leading"]["status"] == "supported_across_model_families"
    assert claims["guide_loss_unidentified"]["status"] == "blocked_by_missing_observation_channel"
    assert "must never be pooled" in register["boundary"]


def test_profile_disagreement_downgrades_source_family_claim() -> None:
    register = build_register(_source(), _profile(winner="environment_only"), _sensitivity(), _stage(), _envelope())

    claims = {row["claim_id"]: row for row in register["claims"]}
    assert register["source_level_summary"]["profile_agrees_with_marginal_winner"] is False
    assert claims["source_level_preference"]["status"] == "restricted_family_preference_requires_manual_review"


def test_write_register_creates_machine_and_human_readable_outputs(tmp_path: Path) -> None:
    register = build_register(_source(), _profile(), _sensitivity(), _stage(), _envelope())
    json_path = tmp_path / "register.json"
    csv_path = tmp_path / "register.csv"
    markdown_path = tmp_path / "register.md"

    write_register(register, json_path, csv_path, markdown_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["stage_pattern_summary"]["winner"] == "isolation_order"
    assert "source_level_preference" in csv_path.read_text(encoding="utf-8")
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Izu model-result register" in markdown
    assert "Do not resolve the different winners by averaging ranks" in markdown


def test_load_json_rejects_non_object(tmp_path: Path) -> None:
    path = tmp_path / "list.json"
    path.write_text("[]\n", encoding="utf-8")

    try:
        load_json(path)
    except ValueError as error:
        assert "expected a JSON object" in str(error)
    else:
        raise AssertionError("load_json accepted a list")
