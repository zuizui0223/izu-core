from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/abm_v4_dense_pair_support_diagnosis.json"

# Frozen bounds from run_constraint_mechanism_abm_v4_fixed_visit_budget.py:
# lineage and pollinator traits are clamped to [0,1], so mismatch <= 1.
# Pollinator breadth is either 0.16 (specialist) or 0.42 (generalist).
# Introduced pollinators multiply the match score by 0.82, otherwise by 1.
MAX_TRAIT_MISMATCH = 1.0
MIN_POLLINATOR_BREADTH = 0.16
MIN_INTRODUCED_FACTOR = 0.82


def minimum_possible_positive_encounter_score() -> float:
    return math.exp(-((MAX_TRAIT_MISMATCH / MIN_POLLINATOR_BREADTH) ** 2)) * MIN_INTRODUCED_FACTOR


def build() -> dict:
    minimum = minimum_possible_positive_encounter_score()
    if not minimum > 0.0:
        raise RuntimeError("expected strictly positive lower bound on v4 encounter score")
    return {
        "schema_version": "1.0",
        "analysis": "abm_v4_dense_pair_support_diagnosis",
        "status": "deterministic_structural_diagnosis_not_empirical_evidence",
        "frozen_v4_bounds": {
            "plant_trait_range": [0.0, 1.0],
            "pollinator_trait_range": [0.0, 1.0],
            "maximum_trait_mismatch": MAX_TRAIT_MISMATCH,
            "pollinator_breadths": [0.16, 0.42],
            "minimum_breadth": MIN_POLLINATOR_BREADTH,
            "introduced_multiplier_minimum": MIN_INTRODUCED_FACTOR,
        },
        "minimum_possible_encounter_score_under_frozen_bounds": minimum,
        "strictly_positive_for_every_finite_plant_pollinator_pair": True,
        "weighted_observation_rule": "pair_weight = encounter_score / number_of_extant_pollinator_types",
        "consequence": {
            "positive_v4_weighted_network_support": "complete bipartite across all plant lineages and every extant pollinator column",
            "v6_nonempty_column_mask": "cannot make any positive plant row partnerless because every retained pollinator has positive weight to every plant",
            "v7_joint_support_closure_on_native_v4_states": "cannot drop a partnerless positive plant row unless all pollinator columns are removed, which v6 explicitly prevents",
        },
        "interpretation": "v4 represents plant-pollinator compatibility only by continuous weight magnitude, not by structural pair membership. Therefore a plant-specific local-support mechanism cannot be exercised by the native v4 weighted state space even if the closure operator itself is correct on sparse-support inputs.",
        "next_mechanism_constraint": "Any integrated successor that is expected to generate local plant turnover must distinguish pair-level interaction support from positive weight magnitude before or during local realization. Do not rescue v7 by fitting a plant-dropout probability to Giannutri.",
        "empirical_inputs_loaded": [],
        "claim_boundary": "This is a mathematical diagnosis of the frozen v4 observation mapping. It does not choose a threshold for sparse support and does not itself validate a replacement pair-support rule.",
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
