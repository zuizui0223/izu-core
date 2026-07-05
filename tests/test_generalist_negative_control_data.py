import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data/predictive_meta/generalist_negative_control_card_ledger.csv"
HOLDOUT = ROOT / "data/predictive_meta/generalist_negative_control_holdout_observations.csv"


def test_all_scored_cards_passed_blind_stage_zero_before_key_join():
    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
    assert len(rows) == 46
    for row in rows:
        if row["trait_score"]:
            assert row["flowering_state"] == "open"
            assert row["focal_flower_visible"] == "yes"
            assert row["comparable"] == "yes"
            assert row["scored_before_key_join"] == "yes"
        else:
            assert row["comparable"] == "no"


def test_ajania_is_the_only_complete_three_regime_generalist_contrast():
    rows = list(csv.DictReader(HOLDOUT.open(encoding="utf-8")))
    by_taxon_regime = defaultdict(list)
    for row in rows:
        by_taxon_regime[(row["taxon"], row["pollinator_regime"])].append(float(row["value"]))
    ajania = {regime: values for (taxon, regime), values in by_taxon_regime.items() if taxon == "Ajania pacifica"}
    assert {regime: len(values) for regime, values in ajania.items()} == {
        "large_bombus": 3, "ardens": 4, "no_bombus": 3
    }
    assert all(value == 3.0 for values in ajania.values() for value in values)
    farfugium = {regime: len(values) for (taxon, regime), values in by_taxon_regime.items() if taxon == "Farfugium japonicum"}
    assert farfugium == {"large_bombus": 5, "no_bombus": 1}
