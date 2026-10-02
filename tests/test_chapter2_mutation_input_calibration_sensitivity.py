import json
import warnings
from pathlib import Path

from scripts.run_chapter2_mutation_input_calibration_sensitivity import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json"


def test_prospectively_frozen_mutation_input_calibration_sensitivity() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"

    result = run(design)

    # Preferred outcome is not enforced. The ranking may survive or reverse.
    assert result["headline_decision"] in {
        "retain_standing_variation_dominates_with_finite_horizon_qualification",
        "drop_standing_variation_dominance_claim",
    }
    warnings.warn(
        "MUTATION_CALIBRATION_NUMERIC "
        + json.dumps(
            {
                "n_trajectories": result["n_trajectories"],
                "central_anchor_comparison": result["central_anchor_comparison"],
                "decisions": result["decisions"],
                "headline_decision": result["headline_decision"],
                "cell_summaries": result["cell_summaries"],
            },
            sort_keys=True,
        )
    )
