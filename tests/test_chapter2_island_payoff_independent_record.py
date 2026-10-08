"""Claim ceiling for the independently frozen island-payoff offline readout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_island_payoff_independent_offline_20261008.json"
DESIGN = ROOT / "data/design/chapter2_island_payoff_confirmation_20261008.json"


def test_independent_payoff_record_keeps_failed_global_gate():
    d = json.loads(DESIGN.read_text())
    r = json.loads(RESULT.read_text())
    assert d["status"] == "frozen_before_independent_payoff_confirmation"
    assert d["group_pairs"] == r["n_paired_far_near_groups"] == 1024
    assert d["prehistories_cases"] == r["n_evolutionary_prehistories"] == 2048
    assert r["n_independent_visitor_histories"] == 64
    assert r["n_demographic_repeats_nested"] == 2
    assert r["adjudication"] == {
        "n_passed": 4, "n_expected": 5, "global_pass": False,
        "rule": "all five simultaneously; failures may not be reclassified using secondary readouts",
    }
    rows = r["frozen_primary"]
    assert len(rows) == 5
    assert sum(x["passed"] for x in rows) == 4
    cost = next(x for x in rows if x["setting"] == "assurance_cost")
    assert cost["metric"] == "viable_maternal"
    assert cost["passed"] is False
    assert cost["mean"] < 0
    assert cost["bootstrap95"][0] < 0 < cost["bootstrap95"][1]
    for row in rows:
        lo, hi = row["bootstrap95"]
        if row["passed"] and row["expected"] == "positive":
            assert row["mean"] > 0 and lo > 0
        elif row["passed"] and row["expected"] == "negative":
            assert row["mean"] < 0 and hi < 0


def test_historical_source_and_local_raw_digest_recorded():
    r = json.loads(RESULT.read_text())
    sha = r["provenance"]
    assert len(sha["raw_file_sha256"]) == 64
    assert len(sha["zip_sha256"]) == 64
    assert len(sha["frozen_source_archive_sha256"]) == 64
    assert "offline" in r["status"]
    assert any("mediation" in text for text in r["boundaries"])
    assert any("assurance-cost" in text for text in r["boundaries"])
