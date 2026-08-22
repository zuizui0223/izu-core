import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/results/island_propagation_hypothesis_ledger.json"
MATRIX = ROOT / "data/results/island_system_propagation_matrix_v1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def hypotheses():
    data = load(LEDGER)
    return {row["id"]: row for row in data["hypotheses"]}


def test_universal_same_direction_cascade_is_rejected_without_prevalence_claim():
    data = load(LEDGER)
    rows = hypotheses()
    u1 = rows["U1_universal_same_direction_cascade"]
    assert u1["status"] == "rejected_as_universal"
    systems = {row["system"] for row in u1["decisive_evidence"]}
    assert {"izu", "puerto_rico_mona_guaiacum", "hawaii_lobelioids_2026", "dominica_heliconia"}.issubset(systems)
    assert "does not estimate how frequent" in u1["interpretation"]
    assert data["programme_decision"] == "reject_universal_same_direction_cascade_keep_state_dependent_propagation_and_buffering_as_testable_synthesis"


def test_partner_effectiveness_is_reallocation_not_sufficient_generator():
    u2 = hypotheses()["U2_partner_effectiveness_is_sufficient_branch_generator"]
    assert u2["status"] == "rejected_as_sufficient"
    abm = next(row for row in u2["decisive_evidence"] if row.get("source") == "ABM v10")
    assert "501/648" in abm["evidence"]
    assert "17 response signs" in abm["evidence"]
    assert "mixed-sign configurations remained 18 to 18" in abm["evidence"]


def test_dependency_is_not_called_empirically_irrelevant():
    u3 = hypotheses()["U3_dependency_heterogeneity_is_necessary_branch_generator"]
    assert u3["status"] == "rejected_as_necessary_in_declared_abm_not_empirically_resolved"
    assert "important empirical candidate" in u3["interpretation"]
    assert "not identified" in u3["interpretation"]


def test_dominica_failure_is_preserved_against_universal_position_law():
    u4 = hypotheses()["U4_initial_signed_position_universally_predicts_downstream_direction"]
    assert u4["status"] == "rejected_as_universal"
    dominica = next(row for row in u4["decisive_evidence"] if row.get("system") == "dominica_heliconia")
    assert "failed" in dominica["role"]
    assert "not retuned" in u4["interpretation"]


def test_surviving_synthesis_requires_a_matched_end_to_end_bridge():
    data = load(LEDGER)
    s1 = hypotheses()["S1_state_dependent_propagation_architecture"]
    assert s1["status"] == "best_current_synthesis_supported_but_not_causally_identified"
    for term in ("signed functional position", "direct effectiveness", "controlled reproductive dependency", "final reproductive/evolutionary response"):
        assert term in s1["missing_proof"]
    assert "not a demonstrated universal causal graph" in s1["interpretation"]
    assert "another generic ABM layer" in data["next_discriminating_measurement"]


def test_ledger_is_consistent_with_propagation_matrix_counterexamples():
    matrix = load(MATRIX)
    states = {row["system_layer_id"]: row["propagation_state"] for row in matrix["rows"]}
    assert states["izu_hiraiwa_cross_channel"] == "branches_downstream"
    assert states["puerto_rico_mona_guaiacum_2022"] == "buffered_or_resilient"
    assert states["hawaii_lobelioid_post_extinction_pollination_2026"] == "buffered_or_resilient"
    assert states["dominica_heliconia_signed_position_projection"] == "counterdirectional"
