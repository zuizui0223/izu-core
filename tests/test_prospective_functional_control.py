import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "data" / "predictive_meta" / "prospective_functional_control.csv"
SENSITIVITY = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_trait_matching_sensitivity.json"


def test_farfugium_is_locked_by_generality_and_coverage_not_response_outcomes():
    with CONTROL.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    row = rows[0]
    assert row["plant"] == "Farfugium japonicum"
    assert int(row["rank_among_coverage_eligible"]) == 1
    assert int(row["n_sites_with_functional_generality"]) == 8
    assert float(row["mean_functional_generality_z"]) > 1.6
    excluded = row["variables_not_used_for_selection"].lower()
    assert "trait matching" in excluded
    assert "pollen receipt" in excluded
    assert "morphology" in excluded
    assert "breeding" in excluded
    assert "not pollinator effectiveness" in row["claim_boundary"]


def test_trait_matching_subgroup_is_not_claimed_fully_leave_one_island_invariant():
    data = json.loads(SENSITIVITY.read_text(encoding="utf-8"))
    sensitivity = data["sensitivity"]
    assert sensitivity["none"] == {"eligible": 8, "lower_post": 8, "higher_post": 0}
    assert sensitivity["omit_niijima"] == {"eligible": 7, "lower_post": 7, "higher_post": 0}
    assert sensitivity["omit_kozu"] == {"eligible": 7, "lower_post": 7, "higher_post": 0}
    assert sensitivity["omit_miyake"]["lower_post"] == 6
    assert sensitivity["omit_miyake"]["higher_post"] == 2
    assert sensitivity["omit_hachijo"]["lower_post"] == 7
    assert sensitivity["omit_hachijo"]["higher_post"] == 1
    assert "not uniformly leave-one-post-island invariant" in data["reading"]
    assert "not a species-independent sign test" in data["claim_boundary"]
