import csv
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
SEQ = ROOT / "data/results/chapter2_1005_confirmatory_primary_sequence_history_20261006.csv"
FIXED = ROOT / "data/results/chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv"


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_primary_sequence_history_level_data_reproduce_51_of_64():
    rows = read_rows(SEQ)
    assert len(rows) == 64
    assert len({int(row["history_seed"]) for row in rows}) == 64
    counts = {}
    for row in rows:
        counts[row["order"]] = counts.get(row["order"], 0) + 1
    assert counts == {"near_simultaneous": 13, "assurance_first": 51}
    assert 51 / 64 == 0.796875


def test_primary_fixed_assurance_history_level_data_reproduce_confirmed_means():
    rows = read_rows(FIXED)
    assert len(rows) == 64
    assert len({int(row["history_seed"]) for row in rows}) == 64
    assert all(int(row["far_eligible_repeats"]) == 8 for row in rows)
    assert all(int(row["paired_eligible_repeats"]) == 8 for row in rows)

    far = mean(float(row["far_investment_change_mean"]) for row in rows)
    pair = mean(float(row["far_minus_near_investment_mean"]) for row in rows)
    assert abs(far - (-0.30602115590337237)) < 1e-15
    assert abs(pair - (-0.43538938011716005)) < 1e-15
