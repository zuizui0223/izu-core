import json
from pathlib import Path


def test_frozen_system_agnostic_validation_result_preserves_partial_coverage():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "data/results/system_agnostic_abm_multi_system_validation_frozen.json").read_text(encoding="utf-8"))
    assert data["summary"]["systems"] == 6
    assert data["summary"]["qualitatively_covered"] == 1
    assert data["summary"]["sign_class_compatible_but_unmapped"] == 1
    assert data["summary"]["buffer_mechanism_coverage_gaps"] == 3
    assert data["summary"]["retained_falsifications"] == 1
    assert data["campanula_specific_tuning"] is False
    assert data["parameters_retuned_to_systems"] is False
