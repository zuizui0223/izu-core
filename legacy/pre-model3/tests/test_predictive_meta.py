from pathlib import Path

from channel_id.predictive_meta import (
    Direction,
    Scenario,
    aggregate_observations,
    assess_contrasts,
    build_contrasts,
    load_observations,
    load_prediction_rules,
    score_scenarios,
)

ROOT = Path(__file__).resolve().parent.parent


def test_campanula_calibration_favours_declared_two_breakpoint_signature():
    observations = load_observations(ROOT / "data/predictive_meta/campanula_calibration_observations.csv")
    rules = load_prediction_rules(ROOT / "data/predictive_meta/two_breakpoint_prediction_contract.csv")
    scores = {row.scenario: row for row in score_scenarios(observations, rules, "calibration")}
    assert scores[Scenario.ARDENS_REPLACEMENT_LOSS].net_score == 1.0
    assert scores[Scenario.ARDENS_REPLACEMENT_LOSS].net_score > scores[Scenario.BODY_SIZE_ONLY].net_score
    assert scores[Scenario.ARDENS_REPLACEMENT_LOSS].net_score > scores[Scenario.SMALL_BEE_SUBSTITUTION].net_score
    assert scores[Scenario.ENVIRONMENT_ONLY].net_score is None


def test_generalist_negative_control_requires_flat_second_threshold():
    observations = load_observations(ROOT / "data/predictive_meta/synthetic_holdout_generalist.csv")
    rules = load_prediction_rules(ROOT / "data/predictive_meta/two_breakpoint_prediction_contract.csv")
    contrasts = build_contrasts(aggregate_observations(observations))
    assessments = assess_contrasts(contrasts, rules, Scenario.ARDENS_REPLACEMENT_LOSS, "holdout")
    second = [row for row in assessments if row.contrast.transition.value == "ardens_to_no_bombus"]
    assert len(second) == 1
    assert second[0].observed_direction is Direction.FLAT
    assert second[0].assessment == "supported"
