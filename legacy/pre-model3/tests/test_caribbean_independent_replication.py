import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/caribbean_island_mainland_replication.json"


def test_caribbean_replication_is_partial_not_full_pathway():
    data = json.loads(RESULT.read_text())
    assert data["replication_verdict"] == "supports_constraint_dependent_architectural_shift_but_not_direct_architecture_to_function_causality"
    assert data["reproductive_assurance_layer"]["autofertility_differs_island_mainland"] is False


def test_caribbean_geography_architecture_signal_is_source_locked():
    data = json.loads(RESULT.read_text())
    assert data["geography_layer"]["insular_functional_specialization_fraction"] == 0.71
    assert data["geography_layer"]["mainland_functional_specialization_fraction"] == 1.0
    assert data["geography_layer"]["hummingbird_visitation_p"] == 0.021
