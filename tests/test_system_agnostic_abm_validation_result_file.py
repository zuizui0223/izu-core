import json
from pathlib import Path


def test_frozen_system_agnostic_validation_result_preserves_current_state_classes():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "data/results/system_agnostic_abm_multi_system_validation_frozen.json").read_text(encoding="utf-8"))
    summary = data["summary"]
    assert summary["systems"] == 6
    assert summary["qualitatively_covered_branching"] == 1
    assert summary["sign_class_compatible_but_unmapped"] == 1
    assert summary["synthetic_buffering_class_available_empirical_mechanism_unmapped"] == 2
    assert summary["empirical_axis_decoupling_constraints"] == 1
    assert summary["retained_falsifications"] == 1
    assert data["campanula_specific_tuning"] is False
    assert data["parameters_retuned_to_systems"] is False
    rows = {row["system_id"]: row for row in data["system_results"]}
    assert rows["puerto_rico_mona_guaiacum"]["decision"] == "empirical_axis_decoupling_constraint"
    assert rows["hawaii_lobelioids_2026"]["decision"] == "synthetic_buffering_class_available_empirical_mechanism_unmapped"
