import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
SCREENING = ROOT / "data/results/chapter2_model3e_h1_h3_screening_20261003.json"
HELDOUT = ROOT / "data/results/chapter2_model3e_heldout_H2_H4_20261003.json"


def test_model3e_first_empirical_emulation_failure_is_frozen() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    screening = json.loads(SCREENING.read_text(encoding="utf-8"))
    heldout = json.loads(HELDOUT.read_text(encoding="utf-8"))
    assert screening["held_out_H2_H4_opened"] is False
    assert screening["accepted_parameter_ids"] == ["p010", "p046", "p036", "p032", "p029"]
    assert heldout["status"] == "complete_model3e_heldout_H2_H4_failure"
    assert heldout["overall_heldout_success"] is False
    assert heldout["n_successful_parameter_sets"] == 0
    assert heldout["best_training_parameter_passes"] is False
    assert design["held_out"]["overall_success"].startswith("at least 3 of the 5")


def test_model3e_failure_modes_are_not_silently_rescued() -> None:
    heldout = json.loads(HELDOUT.read_text(encoding="utf-8"))
    screening = json.loads(SCREENING.read_text(encoding="utf-8"))
    assert screening["interpretation"]["display"].startswith("not reproduced")
    assert heldout["failure_diagnosis"]["training_display"].startswith("display dulling already failed")
    assert heldout["failure_diagnosis"]["heldout_H4"].startswith("the best H1/H3 fit predicts")
