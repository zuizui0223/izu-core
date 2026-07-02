import json
from pathlib import Path

from channel_id.model_result_register_v2 import build_register, load_json, write_register


def source() -> dict:
    return {
        "retained_rows": {"outcrossing": 17, "bagging": 7, "flower": 6, "guide_constraints": 0},
        "full_evidence": [
            {"scenario": "isolation_order", "log_marginal_compatibility": -80.0},
            {"scenario": "ardens_bridge_loss", "log_marginal_compatibility": -83.0},
            {"scenario": "environment_only", "log_marginal_compatibility": -100.0},
        ],
        "leave_one_channel_out": {
            "outcrossing": [{"scenario": "isolation_order", "log_marginal_compatibility": -50.0}],
            "bagging": [{"scenario": "isolation_order", "log_marginal_compatibility": -50.0}],
            "flower": [{"scenario": "ardens_bridge_loss", "log_marginal_compatibility": -50.0}],
            "guide_order": [{"scenario": "isolation_order", "log_marginal_compatibility": -50.0}],
        },
    }


def profile() -> dict:
    return {"results": [
        {"scenario": "isolation_order", "best_log_likelihood": -50.0},
        {"scenario": "ardens_bridge_loss", "best_log_likelihood": -51.0},
    ]}


def sensitivity() -> dict:
    return {"rank_summary": [
        {"scenario": "isolation_order", "rank_one_fraction": 0.8, "mean_rank": 1.2},
        {"scenario": "ardens_bridge_loss", "rank_one_fraction": 0.2, "mean_rank": 1.8},
        {"scenario": "environment_only", "rank_one_fraction": 0.0, "mean_rank": 3.0},
    ]}


def smc() -> dict:
    return {
        "rank_summary": [
            {"scenario": "isolation_order", "rank_one_fraction": 1.0, "mean_log_marginal_compatibility": -81.0, "mean_rank": 1.0},
            {"scenario": "ardens_bridge_loss", "rank_one_fraction": 0.0, "mean_log_marginal_compatibility": -83.0, "mean_rank": 2.0},
            {"scenario": "environment_only", "rank_one_fraction": 0.0, "mean_log_marginal_compatibility": -100.0, "mean_rank": 5.0},
        ],
        "bridge_order_deltas": [
            {"seed": 1, "order_minus_bridge": 1.5, "order_higher": True},
            {"seed": 2, "order_minus_bridge": 2.0, "order_higher": True},
        ],
    }


def stage() -> dict:
    return {"model_scores": [
        {"model": "isolation_order", "mean_absolute_error": 0.1},
        {"model": "pollinator_hierarchy", "mean_absolute_error": 0.2},
        {"model": "environment_only", "mean_absolute_error": 0.3},
    ]}


def envelope() -> dict:
    return {"pollinator_hierarchy_best_rank": 2, "pollinator_hierarchy_worst_rank": 2}


def test_register_records_order_lead_without_causal_upgrade() -> None:
    register = build_register(source(), profile(), sensitivity(), smc(), stage(), envelope())

    assert register["source_level_summary"]["full_winner"] == "isolation_order"
    assert register["source_level_summary"]["smc_winner"] == "isolation_order"
    assert register["source_level_summary"]["smc_order_higher_all_replicates"] is True
    claims = {row["claim_id"]: row for row in register["claims"]}
    assert claims["ordinal_proxy_source_level_preference"]["status"] == "conditional_support_with_channel_dependence"
    assert claims["bridge_loss_not_unique"]["status"] == "not_uniquely_supported"
    assert claims["guide_loss_unidentified"]["status"] == "blocked_by_missing_observation_channel"
    assert "not identify a causal" in claims["ordinal_proxy_source_level_preference"]["current_safe_wording"]


def test_write_register_outputs_json_csv_markdown(tmp_path: Path) -> None:
    register = build_register(source(), profile(), sensitivity(), smc(), stage(), envelope())
    output_json = tmp_path / "register.json"
    output_csv = tmp_path / "claims.csv"
    output_md = tmp_path / "register.md"

    write_register(register, output_json, output_csv, output_md)

    assert json.loads(output_json.read_text(encoding="utf-8"))["schema_version"] == 2
    assert "bridge_loss_not_unique" in output_csv.read_text(encoding="utf-8")
    assert "SMC mean order-minus-bridge" in output_md.read_text(encoding="utf-8")


def test_load_json_rejects_list(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("[]\n", encoding="utf-8")

    try:
        load_json(path)
    except ValueError as error:
        assert "expected object" in str(error)
    else:
        raise AssertionError("list was accepted")
