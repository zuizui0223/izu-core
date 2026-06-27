from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import (
    GuideScenario,
    ScenarioMetric,
    ScenarioObservation,
    ScenarioSettings,
    ScenarioYear,
    recover_compatible_scenarios,
    simulate_guide_scenario,
)
from channel_id.guide_spatial import Patch
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


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


def test_coarse_total_contribution_leaves_multiple_scenarios() -> None:
    spec = settings()
    truth = simulate_guide_scenario(GuideScenario.VISIT_ATTRACTION, spec)
    total = truth.metric(ScenarioMetric.TOTAL_CONTRIBUTION, "typical")
    compatible = recover_compatible_scenarios(
        tuple(GuideScenario),
        spec,
        (ScenarioObservation(ScenarioMetric.TOTAL_CONTRIBUTION, total - 3.0, total + 3.0, "typical"),),
    )
    assert len(compatible) > 1


def test_intermediate_measurements_recover_visit_scenario() -> None:
    spec = settings()
    truth = simulate_guide_scenario(GuideScenario.VISIT_ATTRACTION, spec)
    visits = truth.metric(ScenarioMetric.EXPECTED_VISITS, "typical")
    outcross = truth.metric(ScenarioMetric.OUTCROSS_VIABLE_SEEDS, "typical")
    compatible = recover_compatible_scenarios(
        tuple(GuideScenario),
        spec,
        (
            ScenarioObservation(ScenarioMetric.EXPECTED_VISITS, visits - 1e-8, visits + 1e-8, "typical"),
            ScenarioObservation(ScenarioMetric.OUTCROSS_VIABLE_SEEDS, outcross - 1e-8, outcross + 1e-8, "typical"),
        ),
    )
    assert [report.scenario for report in compatible] == [GuideScenario.VISIT_ATTRACTION]


def test_spatial_scenario_requires_spatial_inputs() -> None:
    spec = settings()
    missing_spatial = ScenarioSettings(
        trait=spec.trait,
        maternal_parameters=spec.maternal_parameters,
        paternal_parameters=spec.paternal_parameters,
        post_seed_survival=spec.post_seed_survival,
        years=spec.years,
    )
    try:
        simulate_guide_scenario(GuideScenario.SPATIAL, missing_spatial)
    except ValueError as error:
        assert "spatial" in str(error)
    else:
        raise AssertionError("spatial scenario must require patch inputs")


def test_geometric_mean_is_summary_metric() -> None:
    result = simulate_guide_scenario(GuideScenario.MIXED, settings())
    assert result.metric(ScenarioMetric.GEOMETRIC_MEAN_CONTRIBUTION) >= 0.0
