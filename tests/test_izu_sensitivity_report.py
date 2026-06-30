from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideScenario, ScenarioSettings, ScenarioYear
from channel_id.izu_gradient_benchmark import (
    GradientAnalysisMode,
    IzuGradientLandscape,
    IzuGradientRecoverySummary,
    IzuGradientSite,
)
from channel_id.izu_sensitivity_report import (
    IzuObservationPlan,
    IzuRecoveryThresholds,
    IzuSensitivityReport,
    IzuSensitivityRow,
    IzuVirtualWorld,
    crossed_izu_observation_plans,
    default_izu_virtual_worlds,
    report_as_markdown_table,
    run_izu_sensitivity_report,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


def settings() -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.1, 0.4, 0.5),
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
        years=(ScenarioYear("template", 0.7),),
    )


def landscape() -> IzuGradientLandscape:
    return IzuGradientLandscape(
        guide_contrast_north=0.1,
        guide_contrast_south=0.9,
        pollinator_service_north=0.8,
        pollinator_service_south=0.4,
        establishment_multiplier_north=1.0,
        establishment_multiplier_south=0.7,
    )


def plan(label: str, windows: int, mothers: int, fruits: int, genotyped: int) -> IzuObservationPlan:
    return IzuObservationPlan(
        label=label,
        flower_camera_windows=windows,
        maternal_individuals=mothers,
        fruits_per_maternal=fruits,
        potential_ovules_per_fruit=10,
        genotyped_mature_seeds_per_fruit=genotyped,
        visit_detection_probability=1.0,
        legitimate_annotation_sensitivity=1.0,
        legitimate_annotation_specificity=1.0,
        paternity_unresolved_probability=0.0,
    )


def test_plan_effort_is_explicit_per_site_and_across_sites() -> None:
    observation_plan = plan("balanced", 100, 20, 2, 3)

    assert observation_plan.fruit_count == 40
    assert observation_plan.genotype_seed_cap == 120
    assert observation_plan.totals_for_sites(3) == (300, 120, 360)


def test_crossed_plan_grid_has_unique_labels() -> None:
    plans = crossed_izu_observation_plans(
        camera_windows=(100, 200),
        maternal_individuals=(20,),
        fruits_per_maternal=(1, 2),
        genotyped_mature_seeds_per_fruit=(2,),
    )

    assert len(plans) == 4
    assert len({candidate.label for candidate in plans}) == 4


def test_default_worlds_cover_the_five_declared_mechanism_stress_tests() -> None:
    worlds = default_izu_virtual_worlds(landscape())

    assert [world.label for world in worlds] == [
        "null_environment_gradient",
        "visit_environment_gradient",
        "handling_environment_gradient",
        "assurance_environment_gradient",
        "visit_assurance_environment_gradient",
    ]
    assert worlds[0].truth is GuideScenario.NULL
    assert worlds[1].truth is GuideScenario.VISIT_ATTRACTION
    assert worlds[2].truth is GuideScenario.HANDLING
    assert worlds[3].truth is GuideScenario.ASSURANCE


def test_report_emits_calibrated_and_flat_rows_and_markdown() -> None:
    sites = (IzuGradientSite("north", 0.0), IzuGradientSite("south", 1.0))
    world = IzuVirtualWorld(
        "null_gradient",
        GuideScenario.NULL,
        landscape(),
        (GuideScenario.NULL, GuideScenario.VISIT_ATTRACTION),
    )
    report = run_izu_sensitivity_report(
        worlds=(world,),
        plans=(plan("small", 100, 10, 1, 2),),
        template_settings=settings(),
        sites=sites,
        replicates=2,
        seed=20260630,
    )

    assert len(report.rows) == 2
    assert report.sites == sites
    assert {row.analysis_mode for row in report.rows} == {
        GradientAnalysisMode.CALIBRATED,
        GradientAnalysisMode.FLAT_ENVIRONMENT,
    }
    table = report_as_markdown_table(report)
    assert "| world | mode | plan |" in table
    assert "null_gradient" in table
    assert "small" in table


def test_pareto_frontier_removes_only_resource_dominated_passing_plans() -> None:
    world = IzuVirtualWorld(
        "null",
        GuideScenario.NULL,
        landscape(),
        (GuideScenario.NULL,),
    )
    efficient = plan("efficient", 100, 10, 2, 2)
    dominated = plan("dominated", 100, 20, 2, 2)
    tradeoff = plan("tradeoff", 50, 20, 2, 4)
    summary = IzuGradientRecoverySummary(
        truth=GuideScenario.NULL,
        analysis_mode=GradientAnalysisMode.CALIBRATED,
        replicates=10,
        truth_retained_rate=1.0,
        unique_truth_recovery_rate=1.0,
        empty_compatible_set_rate=0.0,
        mean_compatible_scenarios=1.0,
    )
    report = IzuSensitivityReport(
        rows=(
            IzuSensitivityRow(efficient, world, GradientAnalysisMode.CALIBRATED, summary, True),
            IzuSensitivityRow(dominated, world, GradientAnalysisMode.CALIBRATED, summary, True),
            IzuSensitivityRow(tradeoff, world, GradientAnalysisMode.CALIBRATED, summary, True),
        ),
        thresholds=IzuRecoveryThresholds(),
        sites=(IzuGradientSite("north", 0.0),),
        replicates=10,
    )

    assert report.passing_plans() == (efficient, dominated, tradeoff)
    assert report.pareto_minimal_passing_plans() == (efficient, tradeoff)
