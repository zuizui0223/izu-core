import pytest

from channel_id.camera_visit_handling import CameraVisitHandlingDesign
from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideScenario, ScenarioSettings, ScenarioYear
from channel_id.izu_field_misspecification import (
    IzuFieldDistortion,
    IzuFieldStressCase,
    benchmark_izu_field_stress_recovery,
    default_izu_field_stress_cases,
    simulate_izu_field_misspecified_dataset,
)
from channel_id.izu_gradient_benchmark import IzuGradientLandscape, IzuGradientSite
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait
from channel_id.seed_set_paternity import SeedSetPaternityDesign


def settings() -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.1, 0.4, 0.5),
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


def landscape() -> IzuGradientLandscape:
    return IzuGradientLandscape(
        guide_contrast_north=0.1,
        guide_contrast_south=0.9,
        pollinator_service_north=0.8,
        pollinator_service_south=0.4,
        establishment_multiplier_north=1.0,
        establishment_multiplier_south=0.7,
    )


def camera_design() -> CameraVisitHandlingDesign:
    return CameraVisitHandlingDesign(
        flower_camera_windows=5_000,
        exposure_multiplier_per_window=1.0,
        visit_detection_probability=0.9,
        legitimate_annotation_sensitivity=0.95,
        legitimate_annotation_specificity=0.95,
    )


def seed_design() -> SeedSetPaternityDesign:
    return SeedSetPaternityDesign(
        maternal_individuals=100,
        fruits_per_maternal=2,
        potential_ovules_per_fruit=10,
        genotyped_mature_seeds_per_fruit=5,
        unresolved_probability=0.20,
        outcross_to_self_error=0.01,
        self_to_outcross_error=0.01,
    )


def sites() -> tuple[IzuGradientSite, ...]:
    return (IzuGradientSite("north", 0.0), IzuGradientSite("south", 1.0))


def test_default_stress_suite_has_all_declared_failure_modes() -> None:
    assert [case.label for case in default_izu_field_stress_cases()] == [
        "ideal",
        "site_maternal_variation",
        "wind_light_detection_loss",
        "handling_dependent_detection_loss",
        "outcross_biased_unresolved",
        "combined_field_stress",
    ]


def test_distorted_generator_is_reproducible_and_preserves_count_accounting() -> None:
    case = IzuFieldDistortion(
        site_visit_log_sd=0.4,
        site_legitimate_logit_sd=0.4,
        maternal_seed_log_sd=0.4,
        detection_mean_multiplier=0.7,
        site_detection_logit_sd=0.5,
        legitimate_detection_relative=0.6,
        outcross_unresolved_odds_multiplier=2.0,
    )
    first = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        case,
        sites=sites(),
        seed=20260630,
    )
    second = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        case,
        sites=sites(),
        seed=20260630,
    )

    assert first == second
    for observation in first.sites:
        camera = observation.camera.counts
        paternity = observation.seed_set_paternity.paternity_calls
        assert camera.called_legitimate + camera.called_nonlegitimate == camera.detected_visits
        assert camera.detected_visits <= camera.true_visits
        assert paternity.outcross_calls + paternity.self_calls + paternity.unresolved_calls == paternity.sampled_mature_seeds
        assert observation.seed_set_paternity.seed_fates.total_ovules == seed_design().total_ovules


def test_wind_light_loss_reduces_detected_visits_under_fixed_seed() -> None:
    ideal = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        IzuFieldDistortion(),
        sites=sites(),
        seed=20260630,
    )
    weather_limited = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        IzuFieldDistortion(detection_mean_multiplier=0.40),
        sites=sites(),
        seed=20260630,
    )

    ideal_detected = sum(item.camera.counts.detected_visits for item in ideal.sites)
    weather_detected = sum(item.camera.counts.detected_visits for item in weather_limited.sites)
    assert weather_detected < ideal_detected


def test_outcross_biased_resolution_increases_unresolved_calls_under_fixed_seed() -> None:
    ideal = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        IzuFieldDistortion(),
        sites=sites(),
        seed=20260630,
    )
    biased = simulate_izu_field_misspecified_dataset(
        GuideScenario.VISIT_ATTRACTION,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        IzuFieldDistortion(outcross_unresolved_odds_multiplier=4.0),
        sites=sites(),
        seed=20260630,
    )

    ideal_unresolved = sum(
        item.seed_set_paternity.paternity_calls.unresolved_calls for item in ideal.sites
    )
    biased_unresolved = sum(
        item.seed_set_paternity.paternity_calls.unresolved_calls for item in biased.sites
    )
    assert biased_unresolved >= ideal_unresolved


def test_ideal_stress_case_recovers_strong_visit_truth_reproducibly() -> None:
    candidates = (
        GuideScenario.NULL,
        GuideScenario.VISIT_ATTRACTION,
        GuideScenario.HANDLING,
    )
    case = IzuFieldStressCase("ideal", IzuFieldDistortion())
    first = benchmark_izu_field_stress_recovery(
        GuideScenario.VISIT_ATTRACTION,
        candidates,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        case,
        sites=sites(),
        replicates=12,
        seed=20260630,
    )
    second = benchmark_izu_field_stress_recovery(
        GuideScenario.VISIT_ATTRACTION,
        candidates,
        settings(),
        landscape(),
        camera_design(),
        seed_design(),
        case,
        sites=sites(),
        replicates=12,
        seed=20260630,
    )

    assert first == second
    assert first.truth_top_rank_rate >= 0.90
    assert first.unique_truth_top_rate >= 0.90
    assert first.mean_truth_rank <= 1.10
    assert first.no_finite_candidate_rate == 0.0


def test_invalid_distortions_are_rejected() -> None:
    with pytest.raises(ValueError, match="detection_mean_multiplier"):
        IzuFieldDistortion(detection_mean_multiplier=0.0)
    with pytest.raises(ValueError, match="legitimate_detection_relative"):
        IzuFieldDistortion(legitimate_detection_relative=0.0)
    with pytest.raises(ValueError, match="outcross_unresolved_odds_multiplier"):
        IzuFieldDistortion(outcross_unresolved_odds_multiplier=0.0)
