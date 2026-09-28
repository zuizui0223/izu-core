import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "data/results/guaiacum_direct_effectiveness_named_source_check.json"
PREFLIGHT = ROOT / "data/design/guaiacum_network_context_mapping_preflight.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_named_same_taxon_routes_do_not_recover_direct_effectiveness():
    result = load(CHECK)
    assert result["target"].startswith("visitor-specific direct per-visit effectiveness E_k")
    assert len(result["named_sources_checked"]) == 4
    assert result["result"]["visitor_specific_direct_effectiveness_recovered"] is False
    assert result["result"]["mapping_ready"] is False
    assert result["result"]["blocking_term"] == "E_k"
    assert result["result"]["targeted_named_search_state"] == "exhausted_no_source_native_same_taxon_Ek_recovered"


def test_restricted_dissertation_is_nonrecovery_not_absence_evidence():
    result = load(CHECK)
    dissertation = next(row for row in result["named_sources_checked"] if row["source_id"] == "fumero_caban_2019_dissertation")
    assert dissertation["access"] == "restricted_print_catalog_record_and_abstract_only"
    assert dissertation["direct_per_visit_effectiveness_recovered"] is False
    assert "non-recovery" in dissertation["boundary"]
    assert "not proof" in dissertation["boundary"]


def test_other_species_effectiveness_cannot_be_transported():
    result = load(CHECK)
    forbidden = result["forbidden_transport"]
    assert forbidden["focal_taxon"] == "Pitcairnia angustifolia"
    assert "cannot serve as E_k for Guaiacum sanctum" in forbidden["reason"]


def test_preflight_is_closed_until_new_direct_effectiveness_source_or_measurement():
    preflight = load(PREFLIGHT)
    assert preflight["schema_version"] == "1.1"
    assert preflight["direct_effectiveness_source_check"] == "data/results/guaiacum_direct_effectiveness_named_source_check.json"
    gate = preflight["source_effectiveness_gate"]
    assert gate["same_taxon_direct_effectiveness_recovered"] is False
    assert gate["nonrecovery_not_absence_claim"] is True
    assert gate["reopen_only_on_new_named_source_authorized_access_or_prospective_measurement"] is True
    assert preflight["mapping_to_abm"]["status"] == "not_mapping_ready"
    assert preflight["mapping_to_abm"]["support_strength_tuning_allowed"] is False
