from pathlib import Path

import pytest

from channel_id.empirical_gradient_anchor import (
    EmpiricalAnchorBundle,
    EmpiricalGradientAssumptions,
    InbreedingFitnessAnchor,
    PollinatorAvailabilityAnchor,
    PopulationTraitAnchor,
    PstFstAnchor,
    apply_inbreeding_anchor,
    empirical_gradient_cases,
    focal_guild_availability,
    load_empirical_anchor_bundle,
    render_empirical_anchor_report,
    trait_gradient_sites,
    write_empirical_anchor_templates,
)
from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import ScenarioSettings, ScenarioYear
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


def bundle() -> EmpiricalAnchorBundle:
    return EmpiricalAnchorBundle(
        population_traits=(
            PopulationTraitAnchor("low_spot", 2.0, 10, 0.4),
            PopulationTraitAnchor("mid_spot", 5.0, 12, 0.5),
            PopulationTraitAnchor("high_spot", 8.0, 11, 0.6),
        ),
        pst_fst=PstFstAnchor("spot_fraction", pst=0.42, fst=0.12, critical_c_over_h2=0.3),
        inbreeding=InbreedingFitnessAnchor("post_seed", 0.45, 0.90),
        pollinator_availability=(
            PollinatorAvailabilityAnchor("low_spot", "bumblebee", False, 45.0),
            PollinatorAvailabilityAnchor("mid_spot", "bumblebee", True, 30.0),
            PollinatorAvailabilityAnchor("high_spot", "bumblebee", False, 0.0),
        ),
    )


def settings() -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.2, 0.4, 0.5),
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
        post_seed_survival=PostSeedSurvival(0.8, 0.1),
        years=(ScenarioYear("template", 0.7),),
    )


def test_trait_gradient_uses_observed_trait_not_geography() -> None:
    sites = trait_gradient_sites(bundle().population_traits)

    assert [(site.label, site.archipelago_position) for site in sites] == [
        ("low_spot", 0.0),
        ("mid_spot", 0.5),
        ("high_spot", 1.0),
    ]


def test_all_equal_trait_means_cannot_define_empirical_gradient() -> None:
    with pytest.raises(ValueError, match="must not all be equal"):
        trait_gradient_sites(
            (
                PopulationTraitAnchor("one", 1.0, 4),
                PopulationTraitAnchor("two", 1.0, 4),
            )
        )


def test_pst_fst_is_retained_as_selection_compatible_metadata_only() -> None:
    anchor = bundle().pst_fst

    assert anchor.selection_compatible
    assert anchor.critical_c_over_h2 == pytest.approx(0.3)


def test_only_post_seed_inbreeding_maps_to_existing_survival_layer() -> None:
    anchored = apply_inbreeding_anchor(settings(), bundle().inbreeding)

    assert anchored.post_seed_survival.outcrossed_survival == pytest.approx(0.8)
    assert anchored.post_seed_survival.late_inbreeding_depression == pytest.approx(0.5)
    with pytest.raises(ValueError, match="only a non-negative post_seed"):
        apply_inbreeding_anchor(
            settings(),
            InbreedingFitnessAnchor("total_lifetime", 0.4, 0.8),
        )


def test_presence_absence_is_reported_without_turning_non_detection_into_absence() -> None:
    availability = focal_guild_availability(bundle(), "bumblebee")

    assert availability == (
        ("low_spot", "not_detected_with_effort", 45.0),
        ("mid_spot", "detected", 30.0),
        ("high_spot", "unobserved", 0.0),
    )


def test_anchor_cases_bracket_service_direction_over_same_trait_axis() -> None:
    assumptions = EmpiricalGradientAssumptions(
        focal_guild="bumblebee",
        pollinator_service_low=0.2,
        pollinator_service_high=0.8,
    )
    cases = empirical_gradient_cases(bundle(), assumptions)

    assert [case.label for case in cases] == [
        "flat_pollinator_service",
        "service_increases_with_spot_axis",
        "service_decreases_with_spot_axis",
    ]
    assert cases[0].landscape.pollinator_service_north == pytest.approx(0.5)
    assert cases[0].landscape.pollinator_service_south == pytest.approx(0.5)
    assert cases[1].landscape.pollinator_service_north == pytest.approx(0.2)
    assert cases[1].landscape.pollinator_service_south == pytest.approx(0.8)
    assert cases[2].landscape.pollinator_service_north == pytest.approx(0.8)
    assert cases[2].landscape.pollinator_service_south == pytest.approx(0.2)
    assert [site.label for site in cases[0].sites] == [
        "low_spot", "mid_spot", "high_spot"
    ]


def test_anchor_report_separates_observed_values_from_scenario_assumptions() -> None:
    report = render_empirical_anchor_report(
        bundle(),
        EmpiricalGradientAssumptions(focal_guild="bumblebee"),
    )

    assert "## Observed anchors" in report
    assert "## Declared, non-empirical scenario assumptions" in report
    assert "not a visit-rate estimate" in report
    assert "P_ST--F_ST comparison is evidence about trait divergence" in report


def test_templates_and_loader_round_trip(tmp_path: Path) -> None:
    write_empirical_anchor_templates(tmp_path)
    (tmp_path / "population_traits.csv").write_text(
        "population_id,spot_trait_mean,spot_trait_sd,trait_n\n"
        "low,1.0,0.2,8\n"
        "high,5.0,0.3,9\n",
        encoding="utf-8",
    )
    (tmp_path / "pst_fst.csv").write_text(
        "trait_name,pst,fst,critical_c_over_h2\nspot,0.4,0.1,0.2\n",
        encoding="utf-8",
    )
    (tmp_path / "inbreeding_fitness.csv").write_text(
        "census_interval,selfed_mean_fitness,outcrossed_mean_fitness\npost_seed,0.4,0.8\n",
        encoding="utf-8",
    )
    (tmp_path / "pollinator_availability.csv").write_text(
        "population_id,guild,detected,effort_minutes\nlow,bumblebee,false,30\nhigh,bumblebee,true,20\n",
        encoding="utf-8",
    )

    loaded = load_empirical_anchor_bundle(tmp_path)

    assert loaded.pst_fst.selection_compatible
    assert loaded.inbreeding.inbreeding_depression == pytest.approx(0.5)
    assert [site.label for site in trait_gradient_sites(loaded.population_traits)] == [
        "low", "high"
    ]
