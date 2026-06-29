from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import (
    GuideRoutes,
    GuideScenario,
    ScenarioMetric,
    ScenarioSettings,
    ScenarioYear,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait
from channel_id.operating_characteristics import (
    FiniteSampleRecoveryDesign,
    benchmark_scenario_recovery,
)


def settings() -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.8, 0.4, 0.5),
        maternal_parameters=NectarGuideParameters(
            10.0,
            0.0,
            0.0,
            0.1,
            0.2,
            0.0,
            1.0,
            0.2,
            0.8,
            1.0,
            0.6,
            1.0,
        ),
        paternal_parameters=PaternalGuideParameters(1.0, 0.0, 1.0, 0.2),
        post_seed_survival=PostSeedSurvival(0.4, 0.5),
        years=(ScenarioYear("typical", 0.7),),
    )


def test_finite_sample_benchmark_is_deterministic_and_reports_recovery_metrics() -> None:
    truth = GuideRoutes("visit_assurance", visit_attraction=True, assurance=True)
    candidates = (
        GuideScenario.NULL,
        GuideScenario.VISIT_ATTRACTION,
        GuideScenario.ASSURANCE,
        truth,
    )
    design = FiniteSampleRecoveryDesign(
        maternal_individuals=80,
        metrics=(
            ScenarioMetric.EXPECTED_VISITS,
            ScenarioMetric.OUTCROSS_VIABLE_SEEDS,
            ScenarioMetric.SELFED_VIABLE_SEEDS,
        ),
    )

    first = benchmark_scenario_recovery(
        truth,
        candidates,
        settings(),
        "typical",
        design,
        replicates=60,
        seed=20260629,
    )
    second = benchmark_scenario_recovery(
        truth,
        candidates,
        settings(),
        "typical",
        design,
        replicates=60,
        seed=20260629,
    )

    assert first == second
    assert first.truth_retained_rate >= first.unique_truth_recovery_rate
    assert 0.0 <= first.empty_compatible_set_rate <= 1.0
    assert first.mean_compatible_scenarios >= 0.0
