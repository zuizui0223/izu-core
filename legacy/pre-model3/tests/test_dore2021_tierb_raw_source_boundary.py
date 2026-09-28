import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/results/dore2021_zenodo_v1_raw_interaction_source_lock.json"


def test_zenodo_raw_source_is_topology_only_not_weighted_tier_b():
    x = json.loads(LOCK.read_text())
    assert x["raw_source"]["published_md5"] == x["raw_source"]["verified_md5"]
    assert x["schema"]["interaction_weight"] is None
    assert x["frozen_coverage"]["total"] == 26
    assert x["frozen_coverage"]["topology_recovered"] == 22
    assert set(x["frozen_coverage"]["topology_absent"]) == {"RP160", "RP163", "RP197", "RP222"}
    assert x["decision"] == "topology_source_locked_weighted_tier_b_not_admitted_from_zenodo_table"


def test_frequency_topology_rows_cannot_be_promoted_to_weights():
    x = json.loads(LOCK.read_text())
    assert "RP18" in x["frequency_networks_with_topology_but_no_weight"]
    assert "RP42" in x["frequency_networks_with_topology_but_no_weight"]
    assert "must not be treated as visit counts" in x["claim_boundary"]
