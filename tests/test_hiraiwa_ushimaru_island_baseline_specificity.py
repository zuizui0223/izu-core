import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_island_baseline_specificity.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_oshima_is_uniquely_coherent_baseline_among_five_islands():
    data = load_data()
    ranking = {row["baseline_island"]: row for row in data["baseline_ranking"]}
    assert data["n_complete_species"] == 7
    assert ranking["oshima"]["n_other_islands_mean_lower_than_baseline"] == 7
    assert ranking["oshima"]["specificity_rank"] == 1
    assert ranking["kozu"]["n_other_islands_mean_lower_than_baseline"] == 5
    assert ranking["niijima"]["n_other_islands_mean_lower_than_baseline"] == 5
    assert ranking["miyake"]["n_other_islands_mean_lower_than_baseline"] == 2
    assert ranking["hachijo"]["n_other_islands_mean_lower_than_baseline"] == 1


def test_specificity_does_not_remove_single_oshima_site_confounding():
    data = load_data()
    text = data["claim_boundary"].lower()
    assert "post-hoc descriptive" in text
    assert "sole bridge-state geographic site" in text
    assert "remains inseparable" in text
    assert "not seven independent geographic boundary experiments" in text


def test_source_defined_subset_not_selected_by_specificity_result():
    data = load_data()
    assert "source-defined pollen-success target species" in data["source_subset"]
    assert set(data["complete_species"]) == {
        "Ampelopsis glandulosa var. hancei",
        "Calystegia soldanella",
        "Farfugium japonicum",
        "Lysimachia mauritiana",
        "Melanthera prostrata",
        "Oxalis corniculata var. trichocaulon",
        "Vitex rotundifolia",
    }
