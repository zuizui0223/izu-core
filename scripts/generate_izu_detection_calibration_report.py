"""Compare nominal and finite-calibrated detection scoring in virtual Izu data.

This is a synthetic sensitivity report.  It treats independent reference visits
as known opportunities and therefore tests an optimistic upper boundary for
camera-detection calibration, not a confirmed field performance level.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideScenario, ScenarioSettings, ScenarioYear
from channel_id.izu_detection_calibration import (
    DetectionCalibrationDesign,
    benchmark_izu_detection_calibration_recovery,
)
from channel_id.izu_field_misspecification import default_izu_field_stress_cases
from channel_id.izu_gradient_benchmark import GradientAnalysisMode, IzuGradientLandscape
from channel_id.izu_observational_equivalence import observationally_distinct_candidates
from channel_id.izu_sensitivity_report import IzuObservationPlan, default_izu_virtual_worlds
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


REPORT_SEED = 20260630


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


def landscape() -> IzuGradientLandscape:
    return IzuGradientLandscape(
        guide_contrast_north=0.10,
        guide_contrast_south=0.90,
        pollinator_service_north=0.80,
        pollinator_service_south=0.40,
        establishment_multiplier_north=1.00,
        establishment_multiplier_south=0.70,
    )


def plans() -> tuple[IzuObservationPlan, ...]:
    return (
        IzuObservationPlan("light", 200, 20, 2, 10, 2),
        IzuObservationPlan("camera_heavy", 1_000, 20, 2, 10, 2),
        IzuObservationPlan("genetic_heavy", 200, 60, 2, 10, 5),
        IzuObservationPlan("balanced_high", 1_000, 60, 2, 10, 5),
    )


def render_detection_calibration_report(replicates: int) -> str:
    if replicates < 1:
        raise ValueError("replicates must be positive")
    model_settings = settings()
    model_landscape = landscape()
    worlds = {
        world.label: world
        for world in default_izu_virtual_worlds(model_landscape)
    }
    selected_worlds = (
        worlds["visit_environment_gradient"],
        worlds["visit_assurance_environment_gradient"],
    )
    stress = {
        case.label: case
        for case in default_izu_field_stress_cases()
    }
    selected_stress = (
        stress["wind_light_detection_loss"],
        stress["combined_field_stress"],
    )
    reference_budgets = (10, 50, 200)

    lines = [
        "# Virtual Izu finite detection-calibration report",
        "",
        "**Synthetic only.** The reference stream is treated as known visit opportunities. "
        "This is an optimistic calibration boundary, not a field estimate.",
        "",
        f"- Seed: `{REPORT_SEED}`",
        f"- Replicates per world × plan × stress × calibration budget: `{replicates}`",
        "- Calibration unit: independent reference visits per virtual site-condition.",
        "- Analysis: nominal fixed detection versus beta-smoothed finite detection calibration.",
        "",
        "| world | candidate classes | plan | stress | reference visits/site | nominal truth top | calibrated truth top | nominal unique top | calibrated unique top | Δ unique top | nominal mean rank | calibrated mean rank |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    stream = REPORT_SEED
    for world in selected_worlds:
        candidates = observationally_distinct_candidates(
            world.candidates,
            model_settings,
            world.landscape,
            analysis_mode=GradientAnalysisMode.CALIBRATED,
        )
        if world.truth not in candidates:
            raise ValueError("truth must be the first representative of its observational class")
        for plan in plans():
            for case in selected_stress:
                for reference_visits in reference_budgets:
                    summary = benchmark_izu_detection_calibration_recovery(
                        truth=world.truth,
                        candidates=candidates,
                        template_settings=model_settings,
                        landscape=world.landscape,
                        camera_design=plan.camera_design(),
                        seed_design=plan.seed_design(),
                        distortion=case.distortion,
                        calibration_design=DetectionCalibrationDesign(reference_visits),
                        analysis_mode=GradientAnalysisMode.CALIBRATED,
                        replicates=replicates,
                        seed=stream,
                    )
                    delta_unique = (
                        summary.calibrated_unique_truth_top_rate
                        - summary.nominal_unique_truth_top_rate
                    )
                    lines.append(
                        "| "
                        + " | ".join(
                            (
                                world.label,
                                str(len(candidates)),
                                plan.label,
                                case.label,
                                str(reference_visits),
                                f"{summary.nominal_truth_top_rank_rate:.2f}",
                                f"{summary.calibrated_truth_top_rank_rate:.2f}",
                                f"{summary.nominal_unique_truth_top_rate:.2f}",
                                f"{summary.calibrated_unique_truth_top_rate:.2f}",
                                f"{delta_unique:+.2f}",
                                f"{summary.nominal_mean_truth_rank:.2f}",
                                f"{summary.calibrated_mean_truth_rank:.2f}",
                            )
                        )
                        + " |"
                    )
                    stream += 1
    lines.extend(
        (
            "",
            "## Interpretation boundary",
            "",
            "The virtual calibration is site-condition-specific and assumes the reference stream reveals true visit opportunities without error. Actual field calibration must be stratified by recorded wind × light conditions, preserve clip selection method, and estimate uncertainty from independent clips. It does not correct handling-dependent detection, annotation error, parentage resolution bias, or site/maternal biological variation; those require their own calibration and later hierarchical model terms.",
        )
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=25)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        rendered = render_detection_calibration_report(args.replicates)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if args.output is None:
        print(rendered, end="")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
