from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from scripts.audit_chapter2_relational_robustness import summarize_matrix
from scripts.run_response_geometry_parameter_robustness import BASE

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_joint_structural_crosscheck_20260908.json"


def build() -> dict:
    # Deliberately reuse values already present in the frozen one-factor audits.
    # No new parameter values or model components are introduced here.
    cfg = replace(BASE, steps=240, trait_adjustment=0.0)
    result = summarize_matrix(cfg, seed=20260826, replicates=96)
    return {
        "schema_version": "1.0",
        "analysis": "chapter2_joint_structural_crosscheck",
        "status": "derived_existing_harness_crosscheck",
        "question": "Does mixed branch geometry persist when the two existing structural sensitivities—long horizon and zero trait adjustment—are imposed simultaneously?",
        "configuration": {
            "base": "scripts.run_response_geometry_parameter_robustness.BASE",
            "replace_arguments": {"steps": 240, "trait_adjustment": 0.0},
            "seed": 20260826,
            "matched_community_realizations": 96,
            "new_parameter_values_introduced": False,
        },
        "result": result,
        "claim_boundary": "This is a derived cross-check using two parameter values already present in the frozen one-factor audit. It strengthens structural generality within the declared synthetic model but is not a new calibration, prevalence estimate or empirical validation.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
