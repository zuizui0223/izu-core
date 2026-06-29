from channel_id.readiness import (
    ChannelDesign,
    ChannelReadiness,
    GuideCausalStatus,
    PollinatorComponentStatus,
    assess_channel_readiness,
)


def _base_design(**overrides: bool) -> ChannelDesign:
    values = {
        "common_trait_domain": True,
        "total_performance_w": True,
        "factorisation_declared": True,
        "boundary_and_zero_plan": True,
        "direct_local_factor_f": False,
        "direct_establishment_factor_e": False,
        "proxy_for_f": False,
        "proxy_calibrated_or_stable": False,
        "pollinator_component_question": False,
        "pollinator_component_model_declared": False,
        "guide_effect_question": False,
        "within_site_trait_contrast": False,
        "guide_manipulation_with_sham_control": False,
        "guide_covariates_controlled": False,
        "temporal_or_weather_blocking": False,
    }
    values.update(overrides)
    return ChannelDesign(**values)


def test_direct_factor_design_is_theorem_ready() -> None:
    report = assess_channel_readiness(_base_design(direct_local_factor_f=True))
    assert report.readiness is ChannelReadiness.READY_DIRECT_FACTOR
    assert report.theorem_ready
    assert not report.missing_requirements


def test_stable_proxy_only_identifies_relative_channel_change() -> None:
    report = assess_channel_readiness(
        _base_design(proxy_for_f=True, proxy_calibrated_or_stable=True)
    )
    assert report.readiness is ChannelReadiness.READY_RELATIVE_STABLE_PROXY
    assert report.theorem_ready


def test_uncalibrated_proxy_is_not_silently_accepted() -> None:
    report = assess_channel_readiness(_base_design(proxy_for_f=True))
    assert report.readiness is ChannelReadiness.CONDITIONAL_ON_PROXY_STABILITY
    assert not report.theorem_ready
    assert report.conditional_assumptions


def test_published_pattern_only_is_not_ready() -> None:
    report = assess_channel_readiness(
        ChannelDesign(
            common_trait_domain=False,
            total_performance_w=False,
            factorisation_declared=False,
            boundary_and_zero_plan=False,
            proxy_for_f=True,
        )
    )
    assert report.readiness is ChannelReadiness.NOT_READY
    assert "trait-specific total performance W on a shared census scale" in report.missing_requirements


def test_pollinator_question_requires_separate_component_model() -> None:
    report = assess_channel_readiness(
        _base_design(direct_local_factor_f=True, pollinator_component_question=True)
    )
    assert report.pollinator_component_status is PollinatorComponentStatus.REQUIRES_COMPONENT_DECOMPOSITION


def test_declared_component_model_is_recorded_without_claiming_validation() -> None:
    report = assess_channel_readiness(
        _base_design(
            direct_local_factor_f=True,
            pollinator_component_question=True,
            pollinator_component_model_declared=True,
        )
    )
    assert report.pollinator_component_status is PollinatorComponentStatus.COMPONENT_MODEL_DECLARED


def test_between_site_guide_association_is_not_upgraded_to_a_causal_mechanism() -> None:
    report = assess_channel_readiness(
        _base_design(direct_local_factor_f=True, guide_effect_question=True)
    )

    assert report.guide_causal_status is GuideCausalStatus.ASSOCIATION_ONLY
    assert "within-site or matched-population guide contrast" in report.guide_causal_missing_requirements


def test_blocked_within_site_guide_comparison_remains_conditional_without_manipulation() -> None:
    report = assess_channel_readiness(
        _base_design(
            direct_local_factor_f=True,
            guide_effect_question=True,
            within_site_trait_contrast=True,
            guide_covariates_controlled=True,
            temporal_or_weather_blocking=True,
        )
    )

    assert report.guide_causal_status is GuideCausalStatus.CONDITIONAL_WITHIN_SITE_CONTRAST
    assert report.guide_causal_missing_requirements == (
        "residual genetic and microenvironmental confounding remains without guide manipulation",
    )


def test_sham_controlled_guide_manipulation_is_ready_for_a_causal_contrast() -> None:
    report = assess_channel_readiness(
        _base_design(
            direct_local_factor_f=True,
            guide_effect_question=True,
            within_site_trait_contrast=True,
            guide_manipulation_with_sham_control=True,
            guide_covariates_controlled=True,
            temporal_or_weather_blocking=True,
        )
    )

    assert report.guide_causal_status is GuideCausalStatus.READY_MANIPULATED_CONTRAST
    assert not report.guide_causal_missing_requirements
