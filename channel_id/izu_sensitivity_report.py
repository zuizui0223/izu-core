"""Compare observation effort across virtual Izu-gradient mechanism worlds.

The virtual-gradient benchmark asks whether one design works at all. This module
turns it into a field-facing sensitivity report: it evaluates several
camera/fruit/genotyping plans across several declared mechanism worlds, then
keeps only plans that meet the predeclared recovery threshold in every
*calibrated* world.

It deliberately does not collapse camera windows, fruit collection, and
parentage assays into one invented cost currency. Instead it returns a Pareto
frontier over three operational resource axes:

* flower-by-camera windows;
* collected fruits;
* maximum number of mature seeds submitted for genotyping.

The `FLAT_ENVIRONMENT` analysis is retained as a diagnostic misspecification
stress test, not as a criterion a valid design must pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .camera_visit_handling import CameraVisitHandlingDesign
from .guide_scenarios import (
    GuideRoutes,
    GuideScenario,
    ScenarioSettings,
    ScenarioSpec,
    core_maternal_scenarios,
)
from .izu_gradient_benchmark import (
    GradientAnalysisMode,
    IzuGradientLandscape,
    IzuGradientRecoverySummary,
    IzuGradientSite,
    benchmark_izu_gradient_recovery,
    default_izu_gradient_sites,
)
from .seed_set_paternity import SeedSetPaternityDesign


@dataclass(frozen=True)
class IzuObservationPlan:
    """One declared camera, fruit, and parentage-assay effort combination.

    Counts are expressed per virtual island site. Use :meth:`totals_for_sites`
    to obtain balanced whole-archipelago totals; an actual field plan may later
    allocate effort unevenly after looking at the sensitivity results.
    """

    label: str
    flower_camera_windows: int
    maternal_individuals: int
    fruits_per_maternal: int
    potential_ovules_per_fruit: int
    genotyped_mature_seeds_per_fruit: int
    exposure_multiplier_per_window: float = 1.0
    visit_detection_probability: float = 0.85
    legitimate_annotation_sensitivity: float = 0.90
    legitimate_annotation_specificity: float = 0.95
    paternity_unresolved_probability: float = 0.10
    outcross_to_self_error: float = 0.01
    self_to_outcross_error: float = 0.01
    familywise_confidence: float = 0.95

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("plan label must be non-empty")
        if self.flower_camera_windows < 1:
            raise ValueError("flower_camera_windows must be positive")
        if self.maternal_individuals < 1 or self.fruits_per_maternal < 1:
            raise ValueError("maternal_individuals and fruits_per_maternal must be positive")
        if self.potential_ovules_per_fruit < 1:
            raise ValueError("potential_ovules_per_fruit must be positive")
        if self.genotyped_mature_seeds_per_fruit < 0:
            raise ValueError("genotyped_mature_seeds_per_fruit must be non-negative")

    @property
    def fruit_count(self) -> int:
        return self.maternal_individuals * self.fruits_per_maternal

    @property
    def genotype_seed_cap(self) -> int:
        """Upper bound, not guaranteed realised parentage calls."""

        return self.fruit_count * self.genotyped_mature_seeds_per_fruit

    def totals_for_sites(self, site_count: int) -> tuple[int, int, int]:
        """Return balanced totals of camera windows, fruits, and genotype cap."""

        if site_count < 1:
            raise ValueError("site_count must be positive")
        return (
            self.flower_camera_windows * site_count,
            self.fruit_count * site_count,
            self.genotype_seed_cap * site_count,
        )

    def camera_design(self) -> CameraVisitHandlingDesign:
        return CameraVisitHandlingDesign(
            flower_camera_windows=self.flower_camera_windows,
            exposure_multiplier_per_window=self.exposure_multiplier_per_window,
            visit_detection_probability=self.visit_detection_probability,
            legitimate_annotation_sensitivity=self.legitimate_annotation_sensitivity,
            legitimate_annotation_specificity=self.legitimate_annotation_specificity,
            familywise_confidence=self.familywise_confidence,
        )

    def seed_design(self) -> SeedSetPaternityDesign:
        return SeedSetPaternityDesign(
            maternal_individuals=self.maternal_individuals,
            fruits_per_maternal=self.fruits_per_maternal,
            potential_ovules_per_fruit=self.potential_ovules_per_fruit,
            genotyped_mature_seeds_per_fruit=self.genotyped_mature_seeds_per_fruit,
            unresolved_probability=self.paternity_unresolved_probability,
            outcross_to_self_error=self.outcross_to_self_error,
            self_to_outcross_error=self.self_to_outcross_error,
            familywise_confidence=self.familywise_confidence,
        )


@dataclass(frozen=True)
class IzuVirtualWorld:
    """A declared synthetic mechanism world to stress-test field designs."""

    label: str
    truth: ScenarioSpec
    landscape: IzuGradientLandscape
    candidates: tuple[ScenarioSpec, ...]

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("world label must be non-empty")
        if not self.candidates:
            raise ValueError("at least one candidate scenario is required")
        if self.truth not in self.candidates:
            raise ValueError("truth must be included in candidates")


@dataclass(frozen=True)
class IzuRecoveryThresholds:
    """Predeclared minimum operating characteristics for calibrated worlds."""

    minimum_truth_retained_rate: float = 0.90
    minimum_unique_truth_recovery_rate: float = 0.80
    maximum_empty_compatible_set_rate: float = 0.10

    def __post_init__(self) -> None:
        for name, value in (
            ("minimum_truth_retained_rate", self.minimum_truth_retained_rate),
            ("minimum_unique_truth_recovery_rate", self.minimum_unique_truth_recovery_rate),
            ("maximum_empty_compatible_set_rate", self.maximum_empty_compatible_set_rate),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie in [0, 1]")

    def passes(self, summary: IzuGradientRecoverySummary) -> bool:
        return (
            summary.truth_retained_rate >= self.minimum_truth_retained_rate
            and summary.unique_truth_recovery_rate >= self.minimum_unique_truth_recovery_rate
            and summary.empty_compatible_set_rate <= self.maximum_empty_compatible_set_rate
        )


@dataclass(frozen=True)
class IzuSensitivityRow:
    """One plan × world × analysis-mode operating-characteristic result."""

    plan: IzuObservationPlan
    world: IzuVirtualWorld
    analysis_mode: GradientAnalysisMode
    summary: IzuGradientRecoverySummary
    passes_calibrated_threshold: bool


@dataclass(frozen=True)
class IzuSensitivityReport:
    """Collection of comparable virtual-world sensitivity results."""

    rows: tuple[IzuSensitivityRow, ...]
    thresholds: IzuRecoveryThresholds
    sites: tuple[IzuGradientSite, ...]
    replicates: int

    def rows_for(
        self,
        plan_label: str | None = None,
        world_label: str | None = None,
        analysis_mode: GradientAnalysisMode | None = None,
    ) -> tuple[IzuSensitivityRow, ...]:
        """Return a filtered immutable view without changing the report."""

        return tuple(
            row
            for row in self.rows
            if (plan_label is None or row.plan.label == plan_label)
            and (world_label is None or row.world.label == world_label)
            and (analysis_mode is None or row.analysis_mode is analysis_mode)
        )

    def passing_plans(self) -> tuple[IzuObservationPlan, ...]:
        """Return plans passing every calibrated virtual world exactly once."""

        calibrated_worlds = {
            row.world.label
            for row in self.rows
            if row.analysis_mode is GradientAnalysisMode.CALIBRATED
        }
        accepted: list[IzuObservationPlan] = []
        seen: set[str] = set()
        for row in self.rows:
            if row.analysis_mode is not GradientAnalysisMode.CALIBRATED:
                continue
            if row.plan.label in seen:
                continue
            plan_rows = self.rows_for(
                plan_label=row.plan.label,
                analysis_mode=GradientAnalysisMode.CALIBRATED,
            )
            if (
                {plan_row.world.label for plan_row in plan_rows} == calibrated_worlds
                and all(plan_row.passes_calibrated_threshold for plan_row in plan_rows)
            ):
                accepted.append(row.plan)
            seen.add(row.plan.label)
        return tuple(accepted)

    def pareto_minimal_passing_plans(self) -> tuple[IzuObservationPlan, ...]:
        """Return non-dominated passing plans across three field resource axes."""

        passing = self.passing_plans()
        frontier: list[IzuObservationPlan] = []
        for plan in passing:
            dominated = False
            for rival in passing:
                if rival is plan:
                    continue
                no_more_of_anything = (
                    rival.flower_camera_windows <= plan.flower_camera_windows
                    and rival.fruit_count <= plan.fruit_count
                    and rival.genotype_seed_cap <= plan.genotype_seed_cap
                )
                strictly_less_of_something = (
                    rival.flower_camera_windows < plan.flower_camera_windows
                    or rival.fruit_count < plan.fruit_count
                    or rival.genotype_seed_cap < plan.genotype_seed_cap
                )
                if no_more_of_anything and strictly_less_of_something:
                    dominated = True
                    break
            if not dominated:
                frontier.append(plan)
        return tuple(frontier)


def _default_candidates() -> tuple[ScenarioSpec, ...]:
    return core_maternal_scenarios()


def default_izu_virtual_worlds(
    landscape: IzuGradientLandscape,
    candidates: Sequence[ScenarioSpec] | None = None,
) -> tuple[IzuVirtualWorld, ...]:
    """Return the five pre-data worlds needed before field effort is fixed."""

    candidate_set = tuple(_default_candidates() if candidates is None else candidates)
    visit_assurance = GuideRoutes("visit_assurance", visit_attraction=True, assurance=True)
    required_truths: tuple[tuple[str, ScenarioSpec], ...] = (
        ("null_environment_gradient", GuideScenario.NULL),
        ("visit_environment_gradient", GuideScenario.VISIT_ATTRACTION),
        ("handling_environment_gradient", GuideScenario.HANDLING),
        ("assurance_environment_gradient", GuideScenario.ASSURANCE),
        ("visit_assurance_environment_gradient", visit_assurance),
    )
    missing = [label for label, truth in required_truths if truth not in candidate_set]
    if missing:
        raise ValueError(
            "candidate set must include all default virtual truths; missing " + ", ".join(missing)
        )
    return tuple(
        IzuVirtualWorld(label, truth, landscape, candidate_set)
        for label, truth in required_truths
    )


def crossed_izu_observation_plans(
    camera_windows: Iterable[int],
    maternal_individuals: Iterable[int],
    fruits_per_maternal: Iterable[int],
    genotyped_mature_seeds_per_fruit: Iterable[int],
    potential_ovules_per_fruit: int = 10,
) -> tuple[IzuObservationPlan, ...]:
    """Build labelled Cartesian-plan combinations for a declared sensitivity grid."""

    plans: list[IzuObservationPlan] = []
    for windows in camera_windows:
        for mothers in maternal_individuals:
            for fruits in fruits_per_maternal:
                for genotyped in genotyped_mature_seeds_per_fruit:
                    plans.append(
                        IzuObservationPlan(
                            label=(
                                f"cam{windows}_mother{mothers}_fruit{fruits}_geno{genotyped}"
                            ),
                            flower_camera_windows=windows,
                            maternal_individuals=mothers,
                            fruits_per_maternal=fruits,
                            potential_ovules_per_fruit=potential_ovules_per_fruit,
                            genotyped_mature_seeds_per_fruit=genotyped,
                        )
                    )
    if not plans:
        raise ValueError("at least one observation plan is required")
    if len({plan.label for plan in plans}) != len(plans):
        raise ValueError("generated observation-plan labels must be unique")
    return tuple(plans)


def run_izu_sensitivity_report(
    worlds: Sequence[IzuVirtualWorld],
    plans: Sequence[IzuObservationPlan],
    template_settings: ScenarioSettings,
    sites: Sequence[IzuGradientSite] | None = None,
    thresholds: IzuRecoveryThresholds = IzuRecoveryThresholds(),
    replicates: int = 100,
    seed: int = 0,
    include_flat_environment_diagnostic: bool = True,
) -> IzuSensitivityReport:
    """Run all declared virtual worlds across all observation plans.

    Every calibrated row is tested against `thresholds`. Flat-environment rows
    are emitted when requested so that users can see sensitivity to ignoring the
    island background gradient, but they never determine `passing_plans()`.
    """

    if not worlds:
        raise ValueError("at least one virtual world is required")
    if not plans:
        raise ValueError("at least one observation plan is required")
    if replicates < 1:
        raise ValueError("replicates must be positive")
    if len({world.label for world in worlds}) != len(worlds):
        raise ValueError("virtual-world labels must be unique")
    if len({plan.label for plan in plans}) != len(plans):
        raise ValueError("observation-plan labels must be unique")

    selected_sites = tuple(default_izu_gradient_sites() if sites is None else sites)
    if not selected_sites:
        raise ValueError("at least one site is required")
    modes = (GradientAnalysisMode.CALIBRATED,)
    if include_flat_environment_diagnostic:
        modes += (GradientAnalysisMode.FLAT_ENVIRONMENT,)

    rows: list[IzuSensitivityRow] = []
    stream = seed
    for world in worlds:
        for plan in plans:
            for mode in modes:
                summary = benchmark_izu_gradient_recovery(
                    truth=world.truth,
                    candidates=world.candidates,
                    template_settings=template_settings,
                    landscape=world.landscape,
                    camera_design=plan.camera_design(),
                    seed_design=plan.seed_design(),
                    sites=selected_sites,
                    analysis_mode=mode,
                    replicates=replicates,
                    seed=stream,
                )
                rows.append(
                    IzuSensitivityRow(
                        plan=plan,
                        world=world,
                        analysis_mode=mode,
                        summary=summary,
                        passes_calibrated_threshold=(
                            mode is GradientAnalysisMode.CALIBRATED and thresholds.passes(summary)
                        ),
                    )
                )
                stream += 1
    return IzuSensitivityReport(
        rows=tuple(rows),
        thresholds=thresholds,
        sites=selected_sites,
        replicates=replicates,
    )


def report_as_markdown_table(report: IzuSensitivityReport) -> str:
    """Render a compact copy-pasteable operating-characteristic table."""

    header = (
        "| world | mode | plan | camera windows/site | mothers/site | fruits/site | "
        "genotype cap/site | retain | unique | empty | mean compatible | pass |"
    )
    rule = "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    body = []
    for row in report.rows:
        plan = row.plan
        summary = row.summary
        passed = "yes" if row.passes_calibrated_threshold else ""
        body.append(
            "| "
            + " | ".join(
                (
                    row.world.label,
                    row.analysis_mode.value,
                    plan.label,
                    str(plan.flower_camera_windows),
                    str(plan.maternal_individuals),
                    str(plan.fruit_count),
                    str(plan.genotype_seed_cap),
                    f"{summary.truth_retained_rate:.2f}",
                    f"{summary.unique_truth_recovery_rate:.2f}",
                    f"{summary.empty_compatible_set_rate:.2f}",
                    f"{summary.mean_compatible_scenarios:.2f}",
                    passed,
                )
            )
            + " |"
        )
    return "\n".join((header, rule, *body))
