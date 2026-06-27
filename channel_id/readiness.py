"""Readiness checks for a declared floral-performance factorisation.

The module does not infer a biological mechanism from a flower trait, a visitor
count, or an island mean.  It checks whether a *predeclared study design* supplies
the observation classes needed to reason under

    W(z) = F(z) E(z),

where ``W`` is total retained recruitment on a shared census scale, ``F`` is
local viable reproductive output conditional on adult survival, and ``E`` is
establishment/reachability conditional on viable seed production.

The factorisation is a modelling assumption.  The checker only reports the
logical status conditional on that declaration.
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


@dataclass(frozen=True)
class ChannelDesign:
    """Declared observation design for a comparison of island regimes.

    Fields describe *whether* an observation class is supplied, not whether an
    empirical result supports a specific channel.  The same trait domain and
    census window must be used across compared regimes.
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


@dataclass(frozen=True)
class ChannelReadinessReport:
    """Auditable readiness status and the exact missing observation classes."""

    readiness: ChannelReadiness
    pollinator_component_status: PollinatorComponentStatus
    missing_requirements: tuple[str, ...]
    direct_factor_available: bool
    proxy_available: bool
    conditional_assumptions: tuple[str, ...]

    @property
    def theorem_ready(self) -> bool:
        return self.readiness in {
            ChannelReadiness.READY_DIRECT_FACTOR,
            ChannelReadiness.READY_RELATIVE_STABLE_PROXY,
        }


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

    return ChannelReadinessReport(
        readiness=readiness,
        pollinator_component_status=pollinator_status,
        missing_requirements=tuple(missing),
        direct_factor_available=direct_factor,
        proxy_available=proxy,
        conditional_assumptions=tuple(assumptions),
    )
