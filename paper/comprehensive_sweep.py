"""Comprehensive simulation sweep for pollinator-loss-driven mating-system evolution.

Generalises the single Izu-gradient virtual benchmark (examples/izu_gradient_virtual_benchmark.py)
into a grid over the phenomenon's controlling parameters:

  * pollinator-loss depth   (service_south: 0.80 = no loss ... 0.05 = near-total loss)
  * environmental confound  (establishment_multiplier_south: 1.00 = none ... 0.40 = strong)
  * number of islands       (n_sites: 2, 4, 8)
  * analysis mode           (CALIBRATED vs FLAT_ENVIRONMENT)

For each cell it reports how often the true (pollinator-loss) mechanism is retained
and uniquely recovered. This maps *where in parameter space the island-syndrome
signature is detectable*, and quantifies the cost of ignoring the environmental
background (the FLAT vs CALIBRATED contrast).

Run:  python paper/comprehensive_sweep.py
"""

from __future__ import annotations

import argparse
import csv
import sys

from channel_id.camera_visit_handling import CameraVisitHandlingDesign
from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideRoutes, GuideScenario, ScenarioSettings, ScenarioYear
from channel_id.izu_gradient_benchmark import (
    GradientAnalysisMode,
    IzuGradientLandscape,
    IzuGradientSite,
    benchmark_izu_gradient_recovery,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait
from channel_id.seed_set_paternity import SeedSetPaternityDesign


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


def sites(n: int) -> tuple[IzuGradientSite, ...]:
    """Evenly spaced ordinal island scaffold with n sites on [0, 1]."""
    if n == 1:
        return (IzuGradientSite("s0", 0.0),)
    return tuple(IzuGradientSite(f"s{i}", i / (n - 1)) for i in range(n))


def main() -> None:
    camera = CameraVisitHandlingDesign(
        flower_camera_windows=1_000,
        exposure_multiplier_per_window=1.0,
        visit_detection_probability=0.85,
        legitimate_annotation_sensitivity=0.90,
        legitimate_annotation_specificity=0.95,
    )
    seed = SeedSetPaternityDesign(
        maternal_individuals=40,
        fruits_per_maternal=2,
        potential_ovules_per_fruit=10,
        genotyped_mature_seeds_per_fruit=3,
    )
    truth = GuideRoutes("visit_assurance", visit_attraction=True, assurance=True)
    candidates = (
        GuideScenario.NULL,
        GuideScenario.VISIT_ATTRACTION,
        GuideScenario.HANDLING,
        GuideScenario.ASSURANCE,
        truth,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=300,
                        help="replicates per cell (use a smaller value in CI for speed)")
    args = parser.parse_args()

    loss_depths = [0.80, 0.60, 0.40, 0.20, 0.05]          # service on southern (isolated) end
    confounds = [1.00, 0.70, 0.40]                        # establishment multiplier south
    site_counts = [2, 4, 8]
    replicates = args.replicates

    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["service_south", "loss_depth", "establishment_south", "n_sites", "mode",
         "truth_retained", "unique_recovery", "empty_set", "mean_compatible"]
    )
    rows = []
    for service_south in loss_depths:
        for est_south in confounds:
            for n in site_counts:
                landscape = IzuGradientLandscape(
                    guide_contrast_north=0.10,
                    guide_contrast_south=0.90,
                    pollinator_service_north=0.80,
                    pollinator_service_south=service_south,
                    establishment_multiplier_north=1.00,
                    establishment_multiplier_south=est_south,
                )
                for mode in (GradientAnalysisMode.CALIBRATED, GradientAnalysisMode.FLAT_ENVIRONMENT):
                    s = benchmark_izu_gradient_recovery(
                        truth=truth,
                        candidates=candidates,
                        template_settings=settings(),
                        landscape=landscape,
                        camera_design=camera,
                        seed_design=seed,
                        sites=sites(n),
                        analysis_mode=mode,
                        replicates=replicates,
                        seed=20260703,
                    )
                    row = [
                        f"{service_south:.2f}",
                        f"{0.80 - service_south:.2f}",
                        f"{est_south:.2f}",
                        n,
                        mode.value,
                        f"{s.truth_retained_rate:.3f}",
                        f"{s.unique_truth_recovery_rate:.3f}",
                        f"{s.empty_compatible_set_rate:.3f}",
                        f"{s.mean_compatible_scenarios:.3f}",
                    ]
                    rows.append(row)
                    writer.writerow(row)


if __name__ == "__main__":
    main()
