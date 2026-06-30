"""Run the five virtual Izu-gradient worlds across several observation plans."""

from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import ScenarioSettings, ScenarioYear
from channel_id.izu_gradient_benchmark import IzuGradientLandscape
from channel_id.izu_sensitivity_report import (
    IzuObservationPlan,
    IzuRecoveryThresholds,
    default_izu_virtual_worlds,
    report_as_markdown_table,
    run_izu_sensitivity_report,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


def settings() -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.10, 0.40, 0.50),
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
        paternal_parameters=PaternalGuideParameters(1.0, 0.0, 1.0, 0.2),
        post_seed_survival=PostSeedSurvival(0.4, 0.5),
        years=(ScenarioYear("template", 0.7),),
    )


def main() -> None:
    landscape = IzuGradientLandscape(
        guide_contrast_north=0.10,
        guide_contrast_south=0.90,
        pollinator_service_north=0.80,
        pollinator_service_south=0.40,
        establishment_multiplier_north=1.00,
        establishment_multiplier_south=0.70,
    )
    plans = (
        IzuObservationPlan("light", 200, 20, 2, 10, 2),
        IzuObservationPlan("camera_heavy", 1_000, 20, 2, 10, 2),
        IzuObservationPlan("genetic_heavy", 200, 60, 2, 10, 5),
        IzuObservationPlan("balanced_high", 1_000, 60, 2, 10, 5),
    )
    report = run_izu_sensitivity_report(
        worlds=default_izu_virtual_worlds(landscape),
        plans=plans,
        template_settings=settings(),
        thresholds=IzuRecoveryThresholds(
            minimum_truth_retained_rate=0.90,
            minimum_unique_truth_recovery_rate=0.80,
            maximum_empty_compatible_set_rate=0.10,
        ),
        replicates=200,
        seed=20260630,
        include_flat_environment_diagnostic=True,
    )

    print(report_as_markdown_table(report))
    print("\nPareto-minimal passing plans:")
    for candidate in report.pareto_minimal_passing_plans():
        camera, fruits, genotype_cap = candidate.totals_for_sites(len(report.sites))
        print(
            f"- {candidate.label}: balanced 8-site proxy = "
            f"{camera} camera windows, {fruits} fruits, {genotype_cap} genotype-cap seeds"
        )


if __name__ == "__main__":
    main()
