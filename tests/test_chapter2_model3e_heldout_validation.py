import json
import sys
import warnings
from pathlib import Path

import pytest

from scripts.run_chapter2_model3e_heldout_validation import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
TARGETS = ROOT / "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json"
SCREENING = ROOT / "data/results/chapter2_model3e_h1_h3_screening_20261003.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGETS.read_text(encoding="utf-8")),
        json.loads(SCREENING.read_text(encoding="utf-8")),
    )


def test_model3e_screening_is_frozen_before_holdout() -> None:
    design, _, screening = _load()
    assert screening["held_out_H2_H4_opened"] is False
    assert screening["accepted_parameter_ids"] == ["p010", "p046", "p036", "p032", "p029"]
    assert design["held_out"]["overall_success"].startswith("at least 3 of the 5")


@pytest.mark.skipif(sys.version_info[:2] != (3, 11), reason="held-out H2/H4 opens once on Python 3.11")
def test_model3e_frozen_heldout_H2_H4_validation() -> None:
    design, targets, screening = _load()
    result = run(design, targets, screening)
    assert result["status"] == "complete_model3e_heldout_H2_H4_validation"
    assert result["n_frozen_parameter_sets"] == 5
    assert result["best_training_parameter_id"] == "p010"
    assert isinstance(result["overall_heldout_success"], bool)
    warnings.warn(
        "MODEL3E_HELDOUT_NUMERIC "
        + json.dumps(
            {
                "successful_parameter_ids": result["successful_parameter_ids"],
                "n_successful_parameter_sets": result["n_successful_parameter_sets"],
                "best_training_parameter_passes": result["best_training_parameter_passes"],
                "overall_heldout_success": result["overall_heldout_success"],
                "parameter_results": result["parameter_results"],
            },
            sort_keys=True,
        )
    )
