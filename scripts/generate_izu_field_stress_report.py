"""Generate a fixed-seed robustness report under virtual field misspecification.

This report deliberately generates observations under unmodelled field-style
processes and scores them with the ideal pooled Izu likelihood. It is a stress
test of assumptions, not an empirical estimate or a field sample-size target.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import ScenarioSettings, ScenarioYear
from channel_id.izu_field_misspecification import (
    benchmark_izu_field_stress_recovery,
    default_izu_field_stress_cases,
)
from channel_id.izu_gradient_benchmark import GradientAnalysisMode, IzuGradientLandscape
from channel_id.izu_observational_equivalence import observationally_distinct_candidates
from channel_id.izu_sensitivity_report import (
    IzuObservationPlan,
    default_izu_virtual_worlds,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


REPORT_SEED = 20260630


def report_settings() -> ScenarioSettings:
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


def report_landscape() -> IzuGradientLandscape:
    return IzuGradientLandscape(
        guide_contrast_north=0.10,
        guide_contrast_south=0.90,
        pollinator_service_north=0.80,
        pollinator_service_south=0.40,
        establishment_multiplier_north=1.00,
        establishment_multiplier_south=0.70,
    )


def report_plans() -> tuple[IzuObservationPlan, ...]:
    return (
        IzuObservationPlan("light", 200, 20, 2, 10, 2),
        IzuObservationPlan("camera_heavy", 1_000, 20, 2, 10, 2),
        IzuObservationPlan("genetic_heavy", 200, 60, 2, 10, 5),
        IzuObservationPlan("balanced_high", 1_000, 60, 2, 10, 5),
    )


def render_field_stress_report(replicates: int) -> str:
    if replicates < 1:
        raise ValueError("replicates must be positive")
    settings = report_settings()
    landscape = report_landscape()
    worlds = default_izu_virtual_worlds(landscape)
    plans = report_plans()
    cases = default_izu_field_stress_cases()

    lines = [
        "# Virtual Izu field-misspecification stress report",
        "",
        "**Synthetic only.** Generator-only distortions are intentionally hidden "
        "from the pooled scorer. This report measures fragility to omitted field "
        "processes; it is not an empirical forecast or sample-size recommendation.",
        "",
        f"- Seed: `{REPORT_SEED}`",
        f"- Replicates per world × plan × stress case: `{replicates}`",
        "- Scoring: ideal pooled site-level likelihood under calibrated environmental gradient.",
        "- Candidate menu: structurally distinct observation classes only.",
        "",
        "| world | candidate classes | plan | stress case | truth top | unique truth top | mean truth rank | mean truth log-likelihood gap | no finite candidate |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    stream = REPORT_SEED
    for world in worlds:
        candidates = observationally_distinct_candidates(
            world.candidates,
            settings,
            world.landscape,
            analysis_mode=GradientAnalysisMode.CALIBRATED,
        )
        if world.truth not in candidates:
            raise ValueError(
                "truth must be the representative of its observational equivalence class"
            )
        for plan in plans:
            for case in cases:
                summary = benchmark_izu_field_stress_recovery(
                    truth=world.truth,
                    candidates=candidates,
                    template_settings=settings,
                    landscape=world.landscape,
                    camera_design=plan.camera_design(),
                    seed_design=plan.seed_design(),
                    case=case,
                    analysis_mode=GradientAnalysisMode.CALIBRATED,
                    replicates=replicates,
                    seed=stream,
                )
                lines.append(
                    "| "
                    + " | ".join(
                        (
                            world.label,
                            str(len(candidates)),
                            plan.label,
                            case.label,
                            f"{summary.truth_top_rank_rate:.2f}",
                            f"{summary.unique_truth_top_rate:.2f}",
                            f"{summary.mean_truth_rank:.2f}",
                            f"{summary.mean_truth_log_likelihood_gap:.2f}",
                            f"{summary.no_finite_candidate_rate:.2f}",
                        )
                    )
                    + " |"
                )
                stream += 1
    lines.extend(
        (
            "",
            "## Stress cases",
            "",
            "- `site_maternal_variation`: unmodelled island residuals in visit and handling, plus maternal seed-fate variation.",
            "- `wind_light_detection_loss`: lower mean detection and site-average detection heterogeneity.",
            "- `handling_dependent_detection_loss`: legitimate contacts are detected at 60% of the probability of other visits.",
            "- `outcross_biased_unresolved`: outcross seeds have 3× unresolved-call odds relative to selfed seeds.",
            "- `combined_field_stress`: all deviations simultaneously.",
            "",
            "## Interpretation boundary",
            "",
            "A loss of truth-top recovery identifies an assumption that needs calibration or a richer empirical observation model. It does not prove the listed stress magnitude occurs in the Izu Islands. In particular, the report collapses day, camera-window, and maternal variation to island-level aggregate counts; collect raw IDs and time/exposure metadata so the eventual empirical model can represent them directly.",
        )
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--replicates",
        type=int,
        default=25,
        help="virtual replicates per world × plan × stress case (default: 25)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="optional Markdown output path; stdout is used when omitted",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        rendered = render_field_stress_report(args.replicates)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if args.output is None:
        print(rendered, end="")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
