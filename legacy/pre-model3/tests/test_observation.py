from random import Random

from channel_id.observation import (
    SimultaneousIntervalPlan,
    bonferroni_marginal_confidence,
    normal_mean_interval,
    poisson_sample,
)


def test_bonferroni_plan_exposes_required_marginal_confidence() -> None:
    plan = SimultaneousIntervalPlan(0.95, 4)

    assert plan.marginal_confidence == bonferroni_marginal_confidence(0.95, 4)
    assert plan.marginal_confidence == 0.9875


def test_marginal_95_intervals_undercover_when_used_as_one_joint_observation() -> None:
    """A deterministic operating check for the failure mode seen in the old tests.

    Four independent per-maternal count observables are measured from the same
    declared true mean.  Treating four 95% intervals as a joint 95% statement
    loses substantial simultaneous coverage.  Bonferroni calibration materially
    improves coverage, but this normal approximation is still not a substitute
    for validating the actual field observation model.
    """

    rng = Random(20260629)
    true_mean = 5.0
    maternal_individuals = 30
    replicates = 1_200
    observables = 4
    raw_joint_hits = 0
    corrected_joint_hits = 0
    corrected_confidence = SimultaneousIntervalPlan(0.95, observables).marginal_confidence

    for _ in range(replicates):
        raw_contains_truth = True
        corrected_contains_truth = True
        for _ in range(observables):
            values = [poisson_sample(true_mean, rng) for _ in range(maternal_individuals)]
            raw_contains_truth &= normal_mean_interval(values, 0.95).contains(true_mean)
            corrected_contains_truth &= normal_mean_interval(
                values,
                corrected_confidence,
            ).contains(true_mean)
        raw_joint_hits += raw_contains_truth
        corrected_joint_hits += corrected_contains_truth

    raw_coverage = raw_joint_hits / replicates
    corrected_coverage = corrected_joint_hits / replicates

    assert raw_coverage < 0.92
    assert corrected_coverage > 0.88
    assert corrected_coverage > raw_coverage
