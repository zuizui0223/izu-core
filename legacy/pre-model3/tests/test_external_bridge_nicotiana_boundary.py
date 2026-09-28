import json
from pathlib import Path


def load_audit():
    path = Path("data/design/external_bridge_nicotiana_source_audit.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_nicotiana_is_partial_bridge_not_complete_or_formal():
    audit = load_audit()
    assert audit["admission_state"] == "bridge_system_partial"
    assert audit["bridge_complete"] is False
    assert audit["formal_cross_system_model_eligible"] is False


def test_nicotiana_source_bytes_are_not_falsely_locked():
    audit = load_audit()
    sources = {row["source_id"]: row for row in audit["sources"]}
    assert sources["schueller_2004_self_pollination"]["source_route"]["checksum_locked"] is False
    assert sources["schueller_2007_corolla_selection"]["source_route"]["checksum_locked"] is False


def test_nicotiana_keeps_cross_paper_linkage_boundary_explicit():
    audit = load_audit()
    linkage = audit["cross_source_linkage"]
    assert "Santa Catalina Island" in linkage["shared_named_sites"]
    assert "Starr Ranch" in linkage["strongest_overlap"]
    blocked = " ".join(linkage["blocked_claims"])
    assert "complete causal chain" in blocked
    assert "same individual-level observations" in blocked
