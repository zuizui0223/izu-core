from channel_id.readiness import (
    ChannelDesign,
    ChannelReadiness,
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
