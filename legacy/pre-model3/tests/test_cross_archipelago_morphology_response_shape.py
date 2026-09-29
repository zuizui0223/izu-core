import json
from pathlib import Path

from scripts.audit_cross_archipelago_morphology_response_shape import build_audit


ROOT = Path(__file__).resolve().parents[1]
SWP = ROOT / "data/results/southwest_pacific_pairs/analysis_summary.json"
SWP_COUPLING = ROOT / "data/results/southwest_pacific_pairs/measurement_error_coupling_sensitivity_summary.json"
HENDRIKS = ROOT / "data/results/hendriks_2019/flower_area_reconstruction_summary.json"
CHECKED = ROOT / "data/results/cross_archipelago_morphology_response_shape_summary.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_checked_directional_replication_is_deterministically_rebuilt():
    observed = build_audit(load(SWP), load(SWP_COUPLING), load(HENDRIKS))
    assert observed == load(CHECKED)


def test_two_independent_systems_replicate_ols_response_shape_direction():
    audit = load(CHECKED)
    assert audit["directional_replication"][
        "source_native_ols_island_cluster_direction_replicated"
    ] is True
    assert audit["directional_replication"]["systems_with_cluster_interval_below_isometry"] == 2
    assert audit["directional_replication"]["independent_systems_evaluated"] == 2
    assert all(system["direct_ols_slope"] < 1.0 for system in audit["systems"])
    assert all(system["island_cluster_interval"][1] < 1.0 for system in audit["systems"])


def test_directional_replication_does_not_open_formal_pooling():
    audit = load(CHECKED)
    boundary = audit["robustness_boundary"]
    assert boundary["errors_in_variables_jointly_resolved"] is False
    assert boundary["source_provenance_jointly_locked"] is True
    assert boundary["trait_definitions_identical"] is False
    assert boundary["formal_same_family_meta_analysis_ready"] is False
    assert audit["effect_registry_eligible"] is False
    assert audit["formal_cross_system_fit_ready"] is False
    assert all(system["formal_effect_registry_eligible"] is False for system in audit["systems"])


def test_hendriks_sma_boundary_remains_visible():
    audit = load(CHECKED)
    hendriks = next(
        system for system in audit["systems"]
        if system["system_id"] == "new_zealand_hendriks_2019"
    )
    assert hendriks["sma_island_cluster_interval"][0] < 1.0
    assert hendriks["sma_island_cluster_interval"][1] > 1.0
    assert hendriks["sma_interval_excludes_isometry"] is False
