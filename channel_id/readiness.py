"""Readiness checks for declared floral-performance and guide-mechanism designs.

The module does not infer a biological mechanism from a flower trait, a visitor
count, or an island mean.  It checks whether a *predeclared study design* supplies
the observation classes needed to reason under

    W(z) = F(z) E(z),

where ``W`` is total retained recruitment on a shared census scale, ``F`` is
local viable reproductive output conditional on adult survival, and ``E`` is
establishment/reachability conditional on viable seed production.

The factorisation is a modelling assumption.  The checker only reports the
logical status conditional on that declaration.  A separate guide-causal status
prevents an F-versus-E-ready design from being misreported as a causal test of a
nectar-guide mechanism when guide contrast is still confounded with site,
display, nectar, plant condition, or observation time.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChannelReadiness(str, Enum):
    """Whether the study can identify the F-versus-E channel under its declaration."""

    NOT_READY = "not_ready"
    READY_DIRECT_FACTOR = "ready_direct_factor"
    READY_RELATIVE_STABLE_PROXY = "ready_relative_stable_proxy"
    CONDITIONAL_ON_PROXY_STABILITY = "conditional_on_proxy_stability"


class PollinatorComponentStatus(str, Enum):
    """Whether pollinator-specific attribution is separately modelled."""

    NOT_ADDRESSED = "not_addressed"
    REQUIRES_COMPONENT_DECOMPOSITION = "requires_component_decomposition"
    COMPONENT_MODEL_DECLARED = "component_model_declared"


class GuideCausalStatus(str, Enum):
    """Strength of a proposed guide-effect comparison before results are observed."""

    NOT_ADDRESSED = "not_addressed"
    ASSOCIATION_ONLY = "association_only"
    CONDITIONAL_WITHIN_SITE_CONTRAST = "conditional_within_site_contrast"
    READY_MANIPULATED_CONTRAST = "ready_manipulated_contrast"


@dataclass(frozen=True)
class ChannelDesign:
    """Declared observation design for a comparison of island regimes.

    Fields describe *whether* an observation class is supplied, not whether an
    empirical result supports a specific channel.  The same trait domain and
    census window must be used across compared regimes.

    Guide-causal fields are intentionally separate from the F-versus-E fields:
    measuring a direct ``F`` factor can identify a life-history channel without
    making naturally covarying guide contrast a causal exposure.
    """

    common_trait_domain: bool
    total_performance_w: bool
    factorisation_declared: bool
    boundary_and_zero_plan: bool
    direct_local_factor_f: bool = False
    direct_establishment_factor_e: bool = False
    proxy_for_f: bool = False
    proxy_calibrated_or_stable: bool = False
    pollinator_component_question: bool = False
    pollinator_component_model_declared: bool = False
    guide_effect_question: bool = False
    within_site_trait_contrast: bool = False
    guide_manipulation_with_sham_control: bool = False
    guide_covariates_controlled: bool = False
    temporal_or_weather_blocking: bool = False


@dataclass(frozen=True)
class ChannelReadinessReport:
    """Auditable readiness status and the exact missing observation classes."""

    readiness: ChannelReadiness
    pollinator_component_status: PollinatorComponentStatus
    missing_requirements: tuple[str, ...]
    direct_factor_available: bool
    proxy_available: bool
    conditional_assumptions: tuple[str, ...]
    guide_causal_status: GuideCausalStatus = GuideCausalStatus.NOT_ADDRESSED
    guide_causal_missing_requirements: tuple[str, ...] = ()

    @property
    def theorem_ready(self) -> bool:
        return self.readiness in {
            ChannelReadiness.READY_DIRECT_FACTOR,
            ChannelReadiness.READY_RELATIVE_STABLE_PROXY,
        }


def _assess_guide_causal_readiness(
    design: ChannelDesign,
) -> tuple[GuideCausalStatus, tuple[str, ...]]:
    """Classify guide-effect claims without upgrading an observational comparison.

    A within-site comparison with measured covariates and time/weather blocks is
    still observational, so it remains conditional on residual confounding.  A
    guide manipulation only reaches the strongest pre-data status when it has a
    sham control and the same blocking/covariate plan.  Neither status claims
    that an evolutionary mechanism is already established; heritable variation,
    intermediate transfer measurements, and a declared fitness census remain
    additional requirements in the guide-evolution model.
    """

    if not design.guide_effect_question:
        return GuideCausalStatus.NOT_ADDRESSED, ()

    missing: list[str] = []
    if not design.within_site_trait_contrast:
        missing.append("within-site or matched-population guide contrast")
    if not design.guide_covariates_controlled:
        missing.append("control or measurement of display, nectar, plant condition, and site covariates")
    if not design.temporal_or_weather_blocking:
        missing.append("time, flower-age, and weather blocking for interaction observations")

    if design.guide_manipulation_with_sham_control:
        if missing:
            return GuideCausalStatus.ASSOCIATION_ONLY, tuple(missing)
        return GuideCausalStatus.READY_MANIPULATED_CONTRAST, ()

    if not design.within_site_trait_contrast:
        missing.append("guide manipulation with a sham control for a causal contrast")
        return GuideCausalStatus.ASSOCIATION_ONLY, tuple(missing)

    if design.guide_covariates_controlled and design.temporal_or_weather_blocking:
        return GuideCausalStatus.CONDITIONAL_WITHIN_SITE_CONTRAST, (
            "residual genetic and microenvironmental confounding remains without guide manipulation",
        )

    missing.append("guide manipulation with a sham control for a causal contrast")
    return GuideCausalStatus.ASSOCIATION_ONLY, tuple(missing)


def assess_channel_readiness(design: ChannelDesign) -> ChannelReadinessReport:
    """Evaluate a declared study design without upgrading proxy assumptions.

    ``W`` plus a direct observation of either ``F`` or ``E`` permits the other
    factor to be reconstructed in the positive interior.  A proxy for ``F`` can
    identify only relative change when its conversion is stable across compared
    regimes or separately calibrated.  A visit count without this condition is
    explicitly returned as conditional rather than silently accepted.
    """

    missing: list[str] = []
    if not design.common_trait_domain:
        missing.append("common trait domain across compared regimes")
    if not design.total_performance_w:
        missing.append("trait-specific total performance W on a shared census scale")
    if not design.factorisation_declared:
        missing.append("declared W = F E factorisation and life-cycle definitions")
    if not design.boundary_and_zero_plan:
        missing.append("positive-interior and zero/boundary handling plan")

    direct_factor = design.direct_local_factor_f or design.direct_establishment_factor_e
    proxy = design.proxy_for_f
    base_ready = not missing

    assumptions: list[str] = []
    if proxy and not design.proxy_calibrated_or_stable:
        assumptions.append("proxy-to-F conversion must be stable or independently calibrated")

    if base_ready and direct_factor:
        readiness = ChannelReadiness.READY_DIRECT_FACTOR
    elif base_ready and proxy and design.proxy_calibrated_or_stable:
        readiness = ChannelReadiness.READY_RELATIVE_STABLE_PROXY
    elif base_ready and proxy:
        readiness = ChannelReadiness.CONDITIONAL_ON_PROXY_STABILITY
    else:
        if not direct_factor and not proxy:
            missing.append("direct F/E factor or an informative proxy")
        readiness = ChannelReadiness.NOT_READY

    if not design.pollinator_component_question:
        pollinator_status = PollinatorComponentStatus.NOT_ADDRESSED
    elif design.pollinator_component_model_declared:
        pollinator_status = PollinatorComponentStatus.COMPONENT_MODEL_DECLARED
    else:
        pollinator_status = PollinatorComponentStatus.REQUIRES_COMPONENT_DECOMPOSITION

    guide_status, guide_missing = _assess_guide_causal_readiness(design)
    return ChannelReadinessReport(
        readiness=readiness,
        pollinator_component_status=pollinator_status,
        missing_requirements=tuple(missing),
        direct_factor_available=direct_factor,
        proxy_available=proxy,
        conditional_assumptions=tuple(assumptions),
        guide_causal_status=guide_status,
        guide_causal_missing_requirements=guide_missing,
    )
