import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/design/cross_archipelago_morphology_source_recovery.json"


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_recovery_registry_tracks_completed_provenance_without_formal_admission():
    sources = {row["source_id"]: row for row in load_registry()["sources"]}
    hendriks = sources["hendriks_2019_flower_area"]
    assert hendriks["institutional_repository"]["exact_record_recovered"] is True
    assert hendriks["institutional_repository"]["identifier"] == "10.26686/wgtn.17136800"
    assert hendriks["admission_gate"]["checksum_locked"] is True
    assert hendriks["admission_gate"]["all_35_pairs_verified_against_locked_bytes"] is True
    assert hendriks["admission_gate"]["island_assignments_verified_against_locked_bytes"] is True
    assert hendriks["admission_gate"]["formal_same_family_effect_admitted"] is False
    assert hendriks["admission_gate"]["empirical_mainland_trait_reliability_identified"] is False

    hrj = sources["hetherington_rauth_johnson_2020_136_pairs"]
    assert hrj["theses_canada_oclc"] == "1335043730"
    assert hrj["admission_gate"]["checksum_locked"] is True
    assert hrj["admission_gate"]["source_native_pair_identity_table_recovered"] is True
    assert hrj["admission_gate"]["public_original_bundle_inventory_complete"] is True
    assert hrj["admission_gate"]["public_original_bundle_tabular_attachment_count"] == 0
    assert hrj["admission_gate"]["source_native_numeric_pair_table_recovered"] is False
    assert hrj["admission_gate"]["numeric_table_unrecoverable_from_inspected_public_routes"] is True
    assert hrj["admission_gate"]["formal_effect_admitted"] is False
    assert hrj["completion_state"]["completion_met"] is True


def test_136_pair_identity_table_is_not_misrepresented_as_numeric_source():
    hrj = next(row for row in load_registry()["sources"] if row["source_id"] == "hetherington_rauth_johnson_2020_136_pairs")
    assert hrj["current_numeric_state"] == "public_source_audit_complete_pair_identity_verified_numeric_136_pair_table_unrecoverable"
    assert hrj["source_native_thesis_findings"]["supplemental_table_a2_found"] is True
    assert hrj["source_native_thesis_findings"]["supplemental_table_a2_selected_pdf_page"] == 83
    assert hrj["source_native_thesis_findings"]["numeric_flower_size_or_log_ratio_column_verified_in_a2"] is False
    assert hrj["admission_gate"]["source_native_numeric_pair_table_recovered"] is False
    assert hrj["admission_gate"]["third_response_shape_computable_from_recovered_source_native_values"] is False
    boundary = hrj["claim_boundary"].lower()
    assert "source-availability result" in boundary
    assert "no third effect" in boundary


def test_nonfloral_island_rule_study_is_boundary_comparator_not_third_floral_system():
    song = next(row for row in load_registry()["sources"] if row["source_id"] == "song_2026_eastern_china_functional_traits")
    assert song["article_doi"] == "10.1111/nph.71040"
    assert song["same_family_floral_replication"] is False
    assert song["formal_floral_effect_admitted"] is False
    assert song["role"] == "non_floral_island_rule_boundary_comparator"
    assert "do not count" in song["next_action"].lower()
