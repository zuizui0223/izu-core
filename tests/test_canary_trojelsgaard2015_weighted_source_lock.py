import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/results/canary_trojelsgaard2015_weighted_source_lock.json"


def load():
    return json.loads(LOCK.read_text())


def test_all_preregistered_canary_site_files_are_recovered():
    x = load()
    r = x["source_recovery"]
    assert r["expected_site_files"] == 12
    assert r["recovered_site_files"] == 12
    assert r["missing_site_files"] == 0


def test_no_canary_row_is_posthoc_promoted_to_dore_exact():
    x = load()
    assert x["exact_dore_frozen_anchor_count"] == 0
    assert set(x["preregistered_aggregation"]) == {"RP100", "RP101", "RP102", "RP103", "RP164"}
    assert all(row["topology_exact"] is False for row in x["preregistered_aggregation"].values())
    assert x["decision"] == "all_canary_weighted_sources_recovered_but_dore_filter_reconciliation_not_recovered"


def test_canary_remains_source_native_weighted_layer():
    x = load()
    assert x["source_native_weighted_system_available"] is True
    assert "site groups are not altered" in x["interpretation"]
    assert "does not trigger post-hoc site selection" in x["claim_boundary"]
