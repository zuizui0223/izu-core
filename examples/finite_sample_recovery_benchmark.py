"""Run a finite-sample guide-scenario recovery benchmark.

This example is a pre-data design check, not an analysis of Campanula field data.
It reports how often a virtual visit-plus-assurance truth is retained or
uniquely recovered after individual-level count noise and simultaneous interval
calibration.

Run with:

    python examples/finite_sample_recovery_benchmark.py
"""

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
        trait=NectarGuideTrait(guide_contrast=0.8, display=0.4, assurance=0.5),
        maternal_parameters=NectarGuideParameters(
            seed_budget=10.0,
            display_cost=0.0,
            guide_cost=0.0,
            assurance_cost=0.1,
            baseline_visit_rate=0.2,
            display_visit_gain=0.0,
            guide_visit_gain=1.0,
            baseline_legitimate_fraction=0.2,
            guide_handling_gain=0.8,
            pollen_to_outcross_fraction=1.0,
            selfing_viability=0.6,
            baseline_establishment=1.0,
        ),
        paternal_parameters=PaternalGuideParameters(
            male_weight=1.0,
            baseline_pollen_export=0.0,
            guide_export_gain=1.0,
            baseline_siring_success=0.2,
        ),
        post_seed_survival=PostSeedSurvival(
            outcrossed_survival=0.4,
            late_inbreeding_depression=0.5,
        ),
        years=(ScenarioYear("typical", pollinator_service=0.7),),
    )


def main() -> None:
    truth = GuideRoutes("visit_assurance", visit_attraction=True, assurance=True)
    candidates = (
        GuideScenario.NULL,
        GuideScenario.VISIT_ATTRACTION,
        GuideScenario.HANDLING,
        GuideScenario.COST,
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
        familywise_confidence=0.95,
    )
    summary = benchmark_scenario_recovery(
        truth=truth,
        candidates=candidates,
        settings=settings(),
        year_label="typical",
        design=design,
        replicates=1_000,
        seed=20260629,
    )
    print(summary)


if __name__ == "__main__":
    main()
