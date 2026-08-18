#!/usr/bin/env python3
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/design/world_island_replication_screen.json"
OUTPUT = ROOT / "data/results/world_island_replication_summary.json"

DIRECT_OR_LINKED = {
    "direct_reproductive_dependency",
    "direct_fitness_treatment_evidence",
    "direct_single_visit_reproductive_outcome",
    "reproductive_success_linked_to_visitation",
    "natural_experiment_strong_pollination_limitation",
    "network_replacement_with_reproductive_mismatch_case",
    "direct_bagging_dependency_with_nonnative_service",
}


def shannon_evenness(counts):
    total = sum(counts.values())
    if total == 0 or len(counts) <= 1:
        return 0.0
    h = -sum((n / total) * math.log(n / total) for n in counts.values())
    return h / math.log(len(counts))


def main():
    data = json.loads(INPUT.read_text())
    systems = data["systems"]
    architecture = Counter(s["architecture_macroclass"] for s in systems)
    basins = Counter(s["ocean_basin"] for s in systems)
    direct_or_linked = [s for s in systems if s["functional_evidence"] in DIRECT_OR_LINKED]
    counterexamples = [
        s for s in systems
        if s["functional_evidence"] == "stable_reproduction_without_detected_pollinator_limitation"
    ]

    result = {
        "schema_version": "1.0",
        "n_systems": len(systems),
        "n_ocean_basin_labels": len(basins),
        "ocean_basin_counts": dict(sorted(basins.items())),
        "n_direct_or_reproductively_linked_systems": len(direct_or_linked),
        "direct_or_linked_fraction": len(direct_or_linked) / len(systems),
        "n_explicit_no_limitation_counterexamples": len(counterexamples),
        "architecture_macroclass_counts": dict(sorted(architecture.items())),
        "n_architecture_macroclasses": len(architecture),
        "architecture_shannon_evenness": shannon_evenness(architecture),
        "functional_recurrence_reading": (
            "Pollination function is directly or reproductively linked in 7 of 8 geographically distant systems; "
            "the Azores case is an explicit no-current-limitation contrast in which generalist redundancy coincides with stable reproduction."
        ),
        "architecture_reading": (
            "The eight systems occupy four predeclared architecture macroclasses, with two systems in each class: "
            "concentrated dependency, complementary/redundant generalism, species-specific mosaic, and novel-partner replacement."
        ),
        "hypothesis_assessment": {
            "H_functional_recurrence": "supported_as_replication_pattern_not_global_prevalence_estimate",
            "H_architecture_divergence": "supported",
            "H_universal_single_syndrome": "contradicted_by_screen"
        },
        "strongest_current_inference": (
            "Across distant island systems, the recurrent feature is not one pollinator guild or one floral syndrome. "
            "What repeats is the reproductive importance of maintaining a viable pollination function; the interaction architecture that supplies that function repeatedly diverges."
        ),
        "claim_boundary": data["claim_boundary"]
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
