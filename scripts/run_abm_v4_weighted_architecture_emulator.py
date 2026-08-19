from __future__ import annotations

import argparse
import importlib.util
import json
import random
import statistics
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
GRADIENT = ROOT / "scripts/run_abm_v4_global_continuous_isolation_gradient.py"
OUT = ROOT / "data/results/abm_v4_weighted_architecture_emulator.json"
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_weighted_network(
    isolation_index: float,
    seed: int,
    saturation: float,
    n_lineages: int = 24,
    steps: int = 120,
) -> WeightedNetwork:
    v4 = load_module(V4, "abm_v4_weighted_core")
    gradient = load_module(GRADIENT, "abm_v4_weighted_gradient")
    scenario = gradient.scenario_at(v4, isolation_index)
    templates = v4.make_lineages(random.Random(seed), n_lineages)
    rng = random.Random(seed + 100_000)
    lineages = [v4.LineageState(template=t, trait=t.trait) for t in templates]
    pollinators = [v4.make_pollinator(rng, scenario) for _ in range(scenario.n_pollinator_types)]

    for _ in range(steps):
        pollinators = [p for p in pollinators if rng.random() >= scenario.partner_loss]
        if rng.random() < scenario.partner_arrival:
            pollinators.append(v4.make_pollinator(rng, scenario))
        for lineage in lineages:
            scores = [v4.encounter_score(lineage, pollinator) for pollinator in pollinators]
            pollination = v4.fixed_budget_pollination(scores, saturation)
            dependency = lineage.template.pollinator_dependency
            autonomous = lineage.template.assurance_ceiling * lineage.assurance
            lineage.reproduction = v4.clamp(
                1.0
                - (1.0 - dependency * pollination)
                * (1.0 - (1.0 - dependency) * autonomous)
            )
            if pollinators and pollination < 0.45:
                best = max(pollinators, key=lambda p: v4.encounter_score(lineage, p))
                lineage.trait = v4.clamp(
                    lineage.trait
                    + lineage.template.trait_adjustment * (best.trait - lineage.trait)
                )
            if lineage.reproduction < 0.50:
                lineage.assurance = min(
                    lineage.template.assurance_ceiling,
                    lineage.assurance + lineage.template.assurance_responsiveness,
                )

    if not pollinators:
        # A weighted network is undefined with no pollinator columns. One zero-opportunity
        # placeholder is used only so the transparent network class can represent the state;
        # callers treat no-positive-interaction runs separately.
        return WeightedNetwork.from_rows(
            [f"lineage_{i+1}" for i in range(len(lineages))],
            ["no_pollinator"],
            [[0.0] for _ in lineages],
        )

    denominator = float(len(pollinators))
    matrix = []
    for lineage in lineages:
        scores = [v4.encounter_score(lineage, pollinator) for pollinator in pollinators]
        # Fixed visit-budget observation layer: pair opportunity weights sum to the mean
        # effective service score used by v4 before the saturation transform. Richness
        # therefore changes composition/opportunity without becoming visit frequency.
        matrix.append([score / denominator for score in scores])

    return WeightedNetwork.from_rows(
        [f"lineage_{i+1}" for i in range(len(lineages))],
        [f"pollinator_{j+1}" for j in range(len(pollinators))],
        matrix,
    )


def summarize_at(isolation_index: float, saturation: float, replicates: int, seed: int) -> dict:
    rows = []
    empty = 0
    for replicate in range(replicates):
        network = run_weighted_network(
            isolation_index,
            seed + replicate,
            saturation,
        )
        try:
            rows.append(network_metrics(network))
        except ValueError as exc:
            if "no positive interactions" not in str(exc):
                raise
            empty += 1
    if not rows:
        return {
            "isolation_index": isolation_index,
            "replicates": replicates,
            "positive_network_replicates": 0,
            "empty_network_replicates": empty,
            "interaction_shannon_mean": None,
            "plant_niche_overlap_mean": None,
        }
    return {
        "isolation_index": isolation_index,
        "replicates": replicates,
        "positive_network_replicates": len(rows),
        "empty_network_replicates": empty,
        "interaction_shannon_mean": statistics.mean(float(row["interaction_shannon"]) for row in rows),
        "plant_niche_overlap_mean": statistics.mean(
            float(row["mean_plant_niche_overlap_morisita_horn"])
            for row in rows
            if row["mean_plant_niche_overlap_morisita_horn"] is not None
        ),
        "positive_links_mean": statistics.mean(float(row["n_positive_links"]) for row in rows),
        "pollinator_types_mean": statistics.mean(float(row["n_pollinators"]) for row in rows),
    }


def build(replicates: int = 60, seed: int = 20260819) -> dict:
    envelope = {}
    for saturation in SATURATIONS:
        envelope[str(saturation)] = [
            summarize_at(index / 10, saturation, replicates, seed)
            for index in range(11)
        ]
    return {
        "analysis": "abm_v4_weighted_architecture_observation_layer",
        "status": "mechanistic_emulator_not_empirical_evidence",
        "pair_weight_definition": "encounter_score / number_of_extant_pollinator_types",
        "fixed_budget_identity": "For each plant lineage, the sum of pair weights equals the mean encounter/service score used by v4 before the saturation transform.",
        "empirical_inputs_loaded": [],
        "metric_implementation": "channel_id.external_archipelago_network.network_metrics",
        "tier_b_targets": ["interaction_shannon", "mean_plant_niche_overlap_morisita_horn"],
        "saturation_values": list(SATURATIONS),
        "isolation_grid": [index / 10 for index in range(11)],
        "replicates_per_grid_point": replicates,
        "envelope": envelope,
        "claim_boundary": "This freezes the ABM-to-weighted-network observation mapping before cross-system Tier-B fit. It does not use empirical Tier-B outcomes, and the saturation envelope is retained rather than selected by fit. Pair weights are opportunity/service weights, not observed visit counts or pollinator effectiveness.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260819)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    result = build(args.replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "analysis": result["analysis"],
        "pair_weight_definition": result["pair_weight_definition"],
        "saturation_values": result["saturation_values"],
    }, indent=2))


if __name__ == "__main__":
    main()
