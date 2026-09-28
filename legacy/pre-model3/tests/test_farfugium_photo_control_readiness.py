import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "predictive_meta" / "farfugium_photo_control_readiness.json"
LEDGER = ROOT / "data" / "predictive_meta" / "generalist_negative_control_card_ledger.csv"


def test_farfugium_photo_control_remains_inferentially_blocked():
    data = json.loads(READINESS.read_text(encoding="utf-8"))
    assert data["current_status"] == "descriptive_flat_inferentially_inconclusive"
    assert data["three_regime_inference_gate_open"] is False
    assert data["scored_open_comparable_observations"]["large_bombus"]["n"] == 5
    assert data["scored_open_comparable_observations"]["ardens"]["n"] == 1
    assert data["scored_open_comparable_observations"]["no_bombus"]["n"] == 1
    assert data["gbif_herbarium_rescue"]["media_candidates_in_fixed_region_proxies"] == 0
    assert "No equivalence" in data["claim_boundary"]


def test_new_oshima_farfugium_score_is_one_independent_observation():
    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
    matches = [row for row in rows if row["taxon"] == "Farfugium japonicum" and row["obs_id"] == "329756251"]
    assert len(matches) == 1
    row = matches[0]
    assert row["region_after_key_join"] == "Oshima"
    assert row["pollinator_regime_after_key_join"] == "ardens"
    assert row["flowering_state"] == "open"
    assert row["comparable"] == "yes"
    assert float(row["trait_score"]) == 3.0
    assert row["scored_before_key_join"] == "yes"
