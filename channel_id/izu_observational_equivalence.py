"""Detect candidate mechanisms that make identical declared observations.

A candidate menu may contain biologically distinct route labels that collapse to
the same observable predictions under a particular virtual parameterisation.
For example, a guide-cost route is observationally identical to its no-cost
counterpart when the declared guide-cost coefficient is zero.  Ranking both as
though they were separate models guarantees a top-score tie and falsely makes a
well-performing assay look non-identifying.

This module groups candidates by their deterministic prediction signature over
the observation metrics used by the Izu camera and seed/paternity pipeline.
It does not declare biological mechanisms equivalent in general; equivalence is
conditional on the supplied settings, landscape, sites, and analysis mode.
"""

from __future__ import annotations

from math import isclose
from typing import Sequence

from .guide_scenarios import GuideScenario, ScenarioMetric, ScenarioSettings, ScenarioSpec, simulate_guide_scenario
from .izu_gradient_benchmark import (
    GradientAnalysisMode,
    IzuGradientLandscape,
    IzuGradientSite,
    default_izu_gradient_sites,
    settings_for_izu_gradient_site,
)


OBSERVED_IZU_METRICS = (
    ScenarioMetric.EXPECTED_VISITS,
    ScenarioMetric.LEGITIMATE_CONTACT_FRACTION,
    ScenarioMetric.OUTCROSS_VIABLE_SEEDS,
    ScenarioMetric.SELFED_VIABLE_SEEDS,
)


def scenario_label(scenario: ScenarioSpec) -> str:
    """Return a stable user-facing label for named and composed candidates."""

    return scenario.value if isinstance(scenario, GuideScenario) else scenario.label


def izu_observation_signature(
    candidate: ScenarioSpec,
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    sites: Sequence[IzuGradientSite] | None = None,
    analysis_mode: GradientAnalysisMode = GradientAnalysisMode.CALIBRATED,
) -> tuple[float, ...]:
    """Return predicted camera/seed metrics over a declared island set.

    Values are ordered by site, then by ``OBSERVED_IZU_METRICS``.  The signature
    intentionally includes only quantities with an observation model in the
    present Izu virtual pipeline; unobserved life-history outputs cannot make
    candidates distinguishable here.
    """

    selected_sites = tuple(default_izu_gradient_sites() if sites is None else sites)
    if not selected_sites:
        raise ValueError("at least one site is required")
    signature: list[float] = []
    for site in selected_sites:
        settings = settings_for_izu_gradient_site(
            template_settings,
            site,
            landscape,
            analysis_mode,
        )
        result = simulate_guide_scenario(candidate, settings)
        signature.extend(result.metric(metric, site.label) for metric in OBSERVED_IZU_METRICS)
    return tuple(signature)


def observational_equivalence_groups(
    candidates: Sequence[ScenarioSpec],
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    sites: Sequence[IzuGradientSite] | None = None,
    analysis_mode: GradientAnalysisMode = GradientAnalysisMode.CALIBRATED,
    tolerance: float = 1e-12,
) -> tuple[tuple[ScenarioSpec, ...], ...]:
    """Group candidates with numerically identical observed predictions.

    The first member of every group is the representative used by
    :func:`observationally_distinct_candidates`.  Candidate declaration order is
    preserved, so users can choose a preferred name for a structural class by
    ordering the supplied candidate menu deliberately.
    """

    if not candidates:
        raise ValueError("at least one candidate is required")
    if len(set(candidates)) != len(candidates):
        raise ValueError("candidate scenarios must be unique")
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")

    groups: list[list[ScenarioSpec]] = []
    signatures: list[tuple[float, ...]] = []
    for candidate in candidates:
        signature = izu_observation_signature(
            candidate,
            template_settings,
            landscape,
            sites,
            analysis_mode,
        )
        for index, representative_signature in enumerate(signatures):
            if all(
                isclose(value, reference, rel_tol=0.0, abs_tol=tolerance)
                for value, reference in zip(signature, representative_signature)
            ):
                groups[index].append(candidate)
                break
        else:
            signatures.append(signature)
            groups.append([candidate])
    return tuple(tuple(group) for group in groups)


def observationally_distinct_candidates(
    candidates: Sequence[ScenarioSpec],
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    sites: Sequence[IzuGradientSite] | None = None,
    analysis_mode: GradientAnalysisMode = GradientAnalysisMode.CALIBRATED,
    tolerance: float = 1e-12,
) -> tuple[ScenarioSpec, ...]:
    """Return the first representative from every conditional equivalence group."""

    groups = observational_equivalence_groups(
        candidates,
        template_settings,
        landscape,
        sites,
        analysis_mode,
        tolerance,
    )
    return tuple(group[0] for group in groups)
