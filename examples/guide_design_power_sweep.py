"""Illustrative sample-size and measurement-plan sweep for guide scenarios.

Run:
    python examples/guide_design_power_sweep.py

The values below are deliberately virtual. They are not recommendations for
Campanula field sample sizes until the individual-level SDs are replaced by
pilot observations and n is converted to an effective independent sample size.
"""

from channel_id.guide_design_power import (
    MeasurementDesign,
    MeasurementPlan,
    rank_measurement_plans,
    sweep_common_sample_sizes,
)
from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideScenario, ScenarioMetric, ScenarioSettings, ScenarioYear
from channel_id.guide_spatial import Patch
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


CANDIDATES = (
    GuideScenario.NULL,
    GuideScenario.VISIT_ATTRACTION,
    GuideScenario.HANDLING,
    GuideScenario.ASSURANCE,
)

SETTINGS = ScenarioSettings(
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
        baseline_pollen_export=1.0,
        display_export_gain=0.0,
        guide_export_gain=1.0,
        baseline_siring_success=0.2,
    ),
    post_seed_survival=PostSeedSurvival(outcrossed_survival=0.4, late_inbreeding_depression=0.5),
    years=(ScenarioYear("typical", pollinator_service=0.7),),
    spatial_patches=(Patch("occupied", establishment_probability=0.8, capacity=100.0),),
    spatial_dispersal=(1.0,),
)

visit_only = MeasurementPlan(
    name="guild-resolved visits",
    measurements=(
        MeasurementDesign(
            metric=ScenarioMetric.EXPECTED_VISITS,
            year_label="typical",
            sample_size=1,
            individual_standard_deviation=2.0,
        ),
    ),
)

visit_plus_outcross = MeasurementPlan(
    name="visits plus outcross seed",
    measurements=(
        MeasurementDesign(
            metric=ScenarioMetric.EXPECTED_VISITS,
            year_label="typical",
            sample_size=1,
            individual_standard_deviation=2.0,
        ),
        MeasurementDesign(
            metric=ScenarioMetric.OUTCROSS_VIABLE_SEEDS,
            year_label="typical",
            sample_size=1,
            individual_standard_deviation=3.0,
        ),
    ),
)

plans = (
    *sweep_common_sample_sizes(visit_only, (10, 30, 90)),
    *sweep_common_sample_sizes(visit_plus_outcross, (10, 30, 90)),
)

rankings = rank_measurement_plans(
    truth_scenario=GuideScenario.VISIT_ATTRACTION,
    candidate_scenarios=CANDIDATES,
    settings=SETTINGS,
    plans=plans,
    replicates=2_000,
    random_seed=20260627,
)

print("rank | plan | truth retained | unique truth | mean compatible")
for ranked in rankings:
    result = ranked.result
    print(
        f"{ranked.rank:>4} | {result.plan_name:<42} | "
        f"{result.truth_retention_rate:>13.3f} | "
        f"{result.unique_truth_recovery_rate:>12.3f} | "
        f"{result.mean_compatible_scenarios:>15.3f}"
    )
