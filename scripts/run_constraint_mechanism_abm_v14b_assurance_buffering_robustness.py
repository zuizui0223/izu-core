from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/run_constraint_mechanism_abm_v14_assurance_buffering.py"
DEFAULT_OUT = ROOT / "data/results/constraint_mechanism_abm_v14b_assurance_buffering_robustness.json"

REPLICATES = 40
CONTEXTS = 4
LINEAGES = 24
STEPS = 120
SEED = 120260822
EXPECTED_CONTRASTS = 2880


def load_parent():
    spec = importlib.util.spec_from_file_location("abm_v14_parent_for_v14b", PARENT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build() -> dict:
    parent = load_parent()
    base = parent.build(
        replicates=REPLICATES,
        contexts=CONTEXTS,
        n_lineages=LINEAGES,
        steps=STEPS,
        seed=SEED,
    )
    overall = base["overall"]
    if overall["lineage_contrasts"] != EXPECTED_CONTRASTS:
        raise ValueError("unexpected v14b lineage contrast count")
    if not base["upstream_service_identical_between_assurance_ablations"]:
        raise ValueError("v14b assurance ablation changed upstream service")

    sign_rescues = int(overall["assurance_sign_rescues"])
    magnitude_rescues = int(overall["assurance_magnitude_rescues"])
    service_declines = int(overall["service_decline_lineages"])
    magnitude_fraction = (magnitude_rescues / service_declines) if service_declines else None
    broad_magnitude_effect = magnitude_fraction is not None and magnitude_fraction > 0.5

    if sign_rescues > 0:
        decision = "synthetic_sign_buffering_replicates_in_independent_seed_block"
    elif magnitude_rescues > 0:
        decision = "initial_sign_rescue_not_replicated_but_assurance_magnitude_effect_persists"
    else:
        decision = "assurance_buffering_capability_not_robust_in_independent_seed_block"

    return {
        "analysis": "constraint_mechanism_abm_v14b_assurance_buffering_robustness",
        "status": "independent_seed_block_complete",
        "design": "data/design/abm_v14b_assurance_buffering_robustness_freeze.json",
        "parent_v14_result": "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json",
        "configuration": {
            "saturations": [1.0, 2.0, 3.0],
            "replicates": REPLICATES,
            "contexts": CONTEXTS,
            "lineages": LINEAGES,
            "steps": STEPS,
            "seed": SEED,
            "local_support_strength": base["configuration"]["local_support_strength"],
            "partner_effectiveness_strength": base["configuration"]["partner_effectiveness_strength"],
            "parameter_changes_from_v14": False,
            "threshold_changes_from_v14": False,
        },
        "upstream_service_identical_between_assurance_ablations": base["upstream_service_identical_between_assurance_ablations"],
        "upstream_service_mismatch_count": base["upstream_service_mismatch_count"],
        "overall": overall,
        "by_saturation": base["by_saturation"],
        "robustness": {
            "assurance_sign_rescues": sign_rescues,
            "sign_level_replication": sign_rescues > 0,
            "assurance_magnitude_rescues": magnitude_rescues,
            "service_decline_lineages": service_declines,
            "magnitude_rescue_fraction": magnitude_fraction,
            "broad_magnitude_effect_majority": broad_magnitude_effect,
        },
        "decision": decision,
        "empirical_mechanism_admission_changed": False,
        "hawaii_assurance_candidate_state": "candidate_only_no_abm_admission",
        "claim_boundary": (
            "This independent seed block can establish stochastic robustness of a synthetic ABM capability only. "
            "It does not validate Hawaiʻi or any other empirical island system and does not estimate natural buffering prevalence."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
