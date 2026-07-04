import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_fixed_proxy_assignment_does_not_promote_outside_records():
    audit = load_module("audit_gbif_herbarium_media", "paper/audit_gbif_herbarium_media.py")
    region, regime, distance = audit.assign_region(34.7385, 139.4024)
    assert region == "Oshima"
    assert regime == "ardens_proxy"
    assert distance == 0.0
    region, regime, distance = audit.assign_region(35.8, 140.5)
    assert region == ""
    assert regime == ""
    assert distance is None


def test_media_rows_requires_a_real_identifier():
    audit = load_module("audit_gbif_herbarium_media", "paper/audit_gbif_herbarium_media.py")
    record = {"media": [{"identifier": "https://example.org/a.jpg", "type": "StillImage"}, {"identifier": "", "type": "StillImage"}]}
    result = audit.media_rows(record)
    assert len(result) == 1
    assert result[0]["media_url"] == "https://example.org/a.jpg"


def test_blind_sheet_gate_requires_two_candidates_in_every_regime():
    sheets = load_module("build_gbif_herbarium_blind_sheets", "paper/build_gbif_herbarium_blind_sheets.py")
    def row(candidate_id: str, regime: str) -> dict[str, str]:
        return {
            "candidate_id": candidate_id, "taxon": "Example", "analysis_group": "specialist",
            "trait_candidate": "flower", "trait_family": "floral_size", "media_url": f"https://example.org/{candidate_id}.jpg",
            "regime_proxy": regime, "region_proxy": "proxy", "gbif_occurrence_key": candidate_id, "source_url": "https://example.org",
        }
    candidates = [row("a1", "large_bombus_proxy"), row("a2", "large_bombus_proxy"), row("b1", "ardens_proxy"), row("b2", "ardens_proxy"), row("c1", "no_bombus_proxy")]
    selected, summary = sheets.choose_cards(candidates, min_per_regime=2, max_per_regime=3, seed=1)
    assert selected == []
    assert summary[0]["sheet_created"] == "no"
    candidates.append(row("c2", "no_bombus_proxy"))
    selected, summary = sheets.choose_cards(candidates, min_per_regime=2, max_per_regime=3, seed=1)
    assert len(selected) == 6
    assert summary[0]["sheet_created"] == "yes"
    assert all("region_proxy" in row for row in selected)
