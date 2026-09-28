import json
from pathlib import Path

from scripts.audit_cross_archipelago_morphology_eiv_envelope import build_envelope


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SHAPE = ROOT / "data/results/cross_archipelago_morphology_response_shape_summary.json"
SUMMARY = ROOT / "data/results/cross_archipelago_morphology_eiv_envelope_summary.json"
CSV = ROOT / "data/results/cross_archipelago_morphology_eiv_envelope.csv"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_checked_joint_thresholds_are_binding_on_southwest_pacific():
    summary = load(SUMMARY)
    thresholds = summary["joint_lower_bound_thresholds"]
    assert thresholds["both_points_below_isometry_requires_reliability_gt"] == 0.8490052881072875
    assert thresholds["binding_system_for_point"] == "southwest_pacific_ciarle_2025_animal"
    assert thresholds["both_island_cluster_intervals_below_isometry_requires_reliability_gt"] == 0.9258005353502381
    assert thresholds["binding_system_for_cluster_interval"] == "southwest_pacific_ciarle_2025_animal"


def test_selected_scenarios_show_point_then_cluster_transition():
    summary = load(SUMMARY)
    scenarios = summary["selected_scenarios"]
    assert scenarios["r_0_90"]["all_points_below_isometry"] is True
    assert scenarios["r_0_90"]["all_island_cluster_intervals_below_isometry"] is False
    assert scenarios["r_0_93"]["all_points_below_isometry"] is True
    assert scenarios["r_0_93"]["all_island_cluster_intervals_below_isometry"] is True
    assert scenarios["r_1_00"]["all_island_cluster_intervals_below_isometry"] is True


def test_envelope_does_not_turn_sensitivity_into_observed_reliability_or_formal_fit():
    summary = load(SUMMARY)
    assert summary["reliability_is_empirically_estimated_in_either_system"] is False
    assert summary["structural_sensitivity_boundary"]["hendriks_sma_interval_excludes_isometry"] is False
    assert summary["effect_registry_eligible"] is False
    assert summary["formal_same_family_meta_analysis_ready"] is False
    boundary = summary["claim_boundary"].lower()
    assert "does not estimate reliability" in boundary
    assert "does not" in boundary and "pooling" in boundary


def test_checked_summary_and_csv_are_deterministically_rebuilt():
    expected = load(SUMMARY)
    observed, rows = build_envelope(load(RESPONSE_SHAPE))
    assert observed == expected

    import csv
    with CSV.open(encoding="utf-8", newline="") as handle:
        checked_rows = list(csv.DictReader(handle))
    assert len(checked_rows) == len(rows)
    assert [float(row["reliability_lower_bound"]) for row in checked_rows] == [
        row["reliability_lower_bound"] for row in rows
    ]
    assert checked_rows[7]["all_points_below_isometry"] == "True"  # r=0.90
    assert checked_rows[7]["all_island_cluster_intervals_below_isometry"] == "False"
    assert checked_rows[9]["all_island_cluster_intervals_below_isometry"] == "True"  # r=0.93
