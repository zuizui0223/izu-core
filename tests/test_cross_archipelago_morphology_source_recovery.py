import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/design/cross_archipelago_morphology_source_recovery.json"


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_recovery_registry_keeps_unlocked_sources_out_of_formal_admission():
    document = load_registry()
    sources = {row["source_id"]: row for row in document["sources"]}

    hendriks = sources["hendriks_2019_flower_area"]
    assert hendriks["admission_gate"]["checksum_locked"] is False
    assert hendriks["admission_gate"]["formal_same_family_effect_admitted"] is False
    assert hendriks["admission_gate"]["empirical_mainland_trait_reliability_identified"] is False

    hrj = sources["hetherington_rauth_johnson_2020_136_pairs"]
    assert hrj["theses_canada_oclc"] == "1335043730"
    assert hrj["admission_gate"]["source_native_pair_table_recovered"] is False
    assert hrj["admission_gate"]["formal_effect_admitted"] is False
    assert "Do not reconstruct" in hrj["next_action"]


def test_136_pair_metadata_route_is_not_misrepresented_as_numeric_source():
    document = load_registry()
    hrj = next(
        row
        for row in document["sources"]
        if row["source_id"] == "hetherington_rauth_johnson_2020_136_pairs"
    )
    assert hrj["current_numeric_state"] == "no_source_native_pair_effect_admitted"
    assert all(route["exact_source_bytes_recovered"] is False for route in hrj["known_routes"] if "exact_source_bytes_recovered" in route)
    boundary = hrj["claim_boundary"].lower()
    assert "do not supply" in boundary
    assert "slope" in boundary
    assert "uncertainty" in boundary
