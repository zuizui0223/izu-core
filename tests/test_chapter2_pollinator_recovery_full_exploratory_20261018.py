"""One bounded end-to-end exploratory execution; NOT independent confirmation.

This deliberately evaluates exactly the prospectively scoped four crossed blocks
on the PR source in CI, so the numerical readout can be audited in the run log.
"""
import json
import warnings

from scripts.explore_chapter2_pollinator_recovery_20261018 import (
    CHECKPOINTS, execute_micro_pilot,
)


def test_exploratory_micro_pilot_complete_four_blocks_and_log_readout():
    d = execute_micro_pilot()
    assert d["status"] == "EXPLORATORY_PILOT_ONLY_NO_CONFIRMATORY_CLAIM"
    assert d["historical_paths"] == 8
    assert d["independent_crossed_blocks"] == 4
    assert d["restoration_checkpoints"] == list(CHECKPOINTS)
    # Three prospective future-A modes per founder x visitor x checkpoint.
    # If historic extinction prevents specifying attained A, affected cells
    # become undefined rather than silently generating a survivor.
    assert d["future_trajectories"] <= 144
    assert d["future_trajectories"] >= 96
    assert len(d["by_arm"]) == 18
    for row in d["by_arm"]:
        assert row["conditional_stream_paths"] <= 8
        assert row["previously_extinct_histories"] <= row["conditional_stream_paths"]
        assert row["high_I_target_successes_unconditional"] <= row["survived_final"]
        assert (row["recovery_probability_among_declined_and_occupied"] is None
                or 0 <= row["recovery_probability_among_declined_and_occupied"] <= 1)
    summary = {
        "type": "EXPLORATORY_ONLY_NO_CONFIRMATORY_CONCLUSIONS",
        "status": d["status"],
        "paths": d["future_trajectories"],
        "four_independent_crossed_blocks": d["independent_crossed_blocks"],
        "TE": d["extirpation_time_TE"],
        "checkpoint_rows": [{
            "t": r["checkpoint"],
            "historical_A": r["historical_assurance_policy"],
            "future_A": r["future_assurance_policy"],
            "service": r["environment"],
            "N_nested": r["conditional_stream_paths"],
            "N_eligible": r["declined_and_occupied_future_paths"],
            "P_regain_conditional": r["recovery_probability_among_declined_and_occupied"],
            "N_unconditional_success": r["high_I_target_successes_unconditional"],
            "N_high_I_support_closed_states": r["high_I_support_closures_in_occupied_states"],
            "N_positive_local_return_states": r["positive_relative_return_after_restoration_states"],
        } for r in d["by_arm"]],
    }
    warnings.warn("Q2_Q3_RECOVERY_PILOT_READOUT=" +
                  json.dumps(summary, separators=(",", ":"), ensure_ascii=True),
                  stacklevel=1)
