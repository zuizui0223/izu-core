import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data/results/island_system_propagation_matrix_v1.json"
BROAD = ROOT / "data/design/island_system_response_axis_matrix.json"
AXES = ROOT / "data/design/island_comparative_response_axis_registry.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_layer_matrix_counts_and_propagation_counts_are_self_consistent():
    data = load(MATRIX)
    rows = data["rows"]
    assert len(rows) == data["summary"]["biological_system_layers"] == 14
    counts = Counter(row["propagation_state"] for row in rows)
    assert dict(counts) == data["summary"]["propagation_state_counts"]
    assert data["summary"]["propagation_state_counts_are_descriptive_not_inferential"] is True
    assert len(set(data["summary"]["geographic_clusters_represented"])) == data["summary"]["geographic_cluster_count"] == 12


def test_hawaii_system_layers_are_separate_but_not_two_geographic_replicates():
    data = load(MATRIX)
    hawaii = [row for row in data["rows"] if row["geographic_cluster"] == "hawaii"]
    assert {row["system_layer_id"] for row in hawaii} == {
        "hawaii_native_dryland_pollination_2019",
        "hawaii_lobelioid_post_extinction_pollination_2026",
    }
    assert sum(bool(row["independent_geographic_cluster"]) for row in hawaii) == 1
    lobelioid = next(row for row in hawaii if row["system_layer_id"].endswith("2026"))
    assert lobelioid["propagation_state"] == "buffered_or_resilient"
    assert "reproductive_buffering" in lobelioid["mechanism_tags"]


def test_ogasawara_psychotria_is_same_direction_only_for_contemporary_access_chain():
    data = load(MATRIX)
    row = next(
        row for row in data["rows"]
        if row["system_layer_id"] == "ogasawara_psychotria_homalosperma_pollinator_replacement"
    )
    assert row["geographic_cluster"] == "ogasawara"
    assert row["independent_geographic_cluster"] is True
    assert row["propagation_state"] == "propagates_same_direction"
    assert "categorical_physical_access" in row["mechanism_tags"]
    assert row["axes"]["visual_signal"] == "absent"
    assert "Historical replacement causation is inferred" in row["boundary"]
    assert "numeric signed mismatch" in row["boundary"]


def test_izu_branching_and_dominica_failed_projection_are_both_preserved():
    data = load(MATRIX)
    izu = next(row for row in data["rows"] if row["system_layer_id"] == "izu_hiraiwa_cross_channel")
    dominica = next(row for row in data["rows"] if row["system_layer_id"] == "dominica_heliconia_signed_position_projection")
    assert izu["propagation_state"] == "branches_downstream"
    assert dominica["propagation_state"] == "counterdirectional"
    assert "failed_prediction" in dominica["mechanism_tags"]


def test_broad_matrix_links_layer_matrix_and_uses_same_axis_vocabulary():
    broad = load(BROAD)
    axes = load(AXES)
    assert broad["propagation_layer_matrix"] == "data/results/island_system_propagation_matrix_v1.json"
    axis_ids = [row["id"] for row in axes["response_axes"]]
    assert broad["response_axes"] == axis_ids
    assert broad["current_pattern"]["uniform_response_syndrome_supported"] is False
    assert broad["current_pattern"]["response_heterogeneity_recurs"] is True
    assert broad["current_pattern"]["incomplete_propagation_recurs"] is True
    for system in broad["systems"]:
        assert set(system["axes"]) == set(broad["response_axes"])


def test_matrix_does_not_claim_formal_cross_system_fit():
    data = load(MATRIX)
    assert data["summary"]["formal_cross_system_same_estimand_fit_ready"] is False
    assert "not a meta-analytic effect size" in data["claim_boundary"]
