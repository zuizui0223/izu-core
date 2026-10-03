import json
import sys
import warnings
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.run_chapter2_model3e_empirical_screening import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
TARGETS = ROOT / "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGETS.read_text(encoding="utf-8")),
    )


def test_model3e_empirical_design_freezes_fit_and_holdout() -> None:
    design, targets = _load()
    assert design["status"] == "prospective_frozen_before_model3e_screening"
    assert targets["status"] == "frozen_empirical_targets_before_model3e_execution"
    assert design["fit"]["data"].startswith("H1 all-analysis")
    assert design["held_out"]["open_only_after_fit_freeze"] is True
    assert "H2" in design["held_out"]
    assert "H4" in design["held_out"]


def test_model3e_screening_smoke() -> None:
    design, targets = _load()
    design = deepcopy(design)
    design["search"]["n_parameter_sets"] = 1
    design["common_operator"]["years"] = 12
    design["pseudo_islands"]["terminal_window_years"] = 4
    design["pseudo_islands"]["distances"] = [0.0, 1.5, 3.0]
    design["pseudo_islands"]["history_seeds"] = [81201]
    result = run(design, targets)
    assert result["n_parameter_sets"] == 1
    assert result["held_out_H2_H4_opened"] is False
    assert len(result["all_parameter_summaries"]) == 1


@pytest.mark.skipif(sys.version_info[:2] != (3, 11), reason="full prospective Model 3E screening runs once on Python 3.11")
def test_prospective_model3e_h1_h3_screening() -> None:
    design, targets = _load()
    result = run(design, targets)

    assert result["n_parameter_sets"] == 48
    assert result["held_out_H2_H4_opened"] is False
    assert len(result["all_parameter_summaries"]) == 48
    assert set(result["accepted_parameter_ids"]).issubset(
        {r["parameter_id"] for r in result["all_parameter_summaries"]}
    )
    warnings.warn(
        "MODEL3E_SCREENING_NUMERIC "
        + json.dumps(
            {
                "fit_success": result["fit_success"],
                "n_eligible": result["n_eligible"],
                "contexts": result["contexts"],
                "accepted_parameter_ids": result["accepted_parameter_ids"],
                "accepted_parameter_sets": result["accepted_parameter_sets"],
                "best_any": sorted(
                    [r for r in result["all_parameter_summaries"] if r["score"] is not None],
                    key=lambda r: r["score"],
                )[:5],
            },
            sort_keys=True,
        )
    )
