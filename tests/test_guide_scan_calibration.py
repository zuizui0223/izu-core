from pathlib import Path

from channel_id.guide_scan_calibration import (
    load_guide_summary,
    summarize_second_transition,
    validate_contract_v1_1,
    validate_observation_bridge,
)
from channel_id.predictive_meta import (
    Direction,
    Scenario,
    aggregate_observations,
    assess_contrasts,
    build_contrasts,
    load_observations,
    load_prediction_rules,
)

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "data/predictive_meta/campanula_guide_scan_summary.csv"
CONTRACT_V11 = ROOT / "data/predictive_meta/campanula_channel_shape_v1_1.csv"
OBSERVATIONS = ROOT / "data/predictive_meta/campanula_calibration_observations.csv"
SCENARIOS = ROOT / "data/predictive_meta/two_breakpoint_prediction_contract.csv"


def test_measured_guide_summary_supports_a_robust_second_decline():
    rows = load_guide_summary(GUIDE)
    summary = summarize_second_transition(rows)
    assert summary.ardens_island == "Oshima"
    assert summary.ardens_guide_cov_pct == 28.39
    assert abs(summary.no_bombus_equal_island_mean_pct - 5.9325) < 1e-9
    assert abs(summary.second_transition_delta_pct_points - (-22.4575)) < 1e-9
    assert summary.no_bombus_islands_below_ardens == 4
    assert all(delta < 0 for delta in summary.leave_one_island_out_deltas)


def test_v11_contract_and_observation_bridge_are_consistent():
    rows = load_guide_summary(GUIDE)
    validate_contract_v1_1(CONTRACT_V11)
    validate_observation_bridge(OBSERVATIONS, rows)


def test_guide_channel_is_a_supported_focal_second_transition_only():
    observations = load_observations(OBSERVATIONS)
    rules = load_prediction_rules(SCENARIOS)
    contrasts = build_contrasts(aggregate_observations(observations))
    guide = [row for row in contrasts if row.trait_family == "visible_signal"]
    assert len(guide) == 1
    assert guide[0].transition.value == "ardens_to_no_bombus"
    assert abs(guide[0].delta - (-22.4575)) < 1e-9
    assessments = assess_contrasts(
        contrasts, rules, Scenario.ARDENS_REPLACEMENT_LOSS, "calibration"
    )
    guide_assessments = [
        row for row in assessments if row.contrast.trait_family == "visible_signal"
    ]
    assert len(guide_assessments) == 1
    assert guide_assessments[0].observed_direction is Direction.DECREASE
    assert guide_assessments[0].assessment == "supported"
