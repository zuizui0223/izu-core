import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_cross_channel_concordance.json"
ROWS = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_cross_channel_concordance.csv"


def load_summary():
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


def load_rows():
    with ROWS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_all_shared_targets_have_lower_corrected_matching_but_other_channels_diverge():
    data = load_summary()
    assert data["n_shared_targets"] == 8
    assert data["directions"]["corrected_trait_matching"] == {
        "lower_post": 8,
        "higher_post": 0,
    }
    assert data["directions"]["tube_morphology"] == {
        "shorter_post": 3,
        "longer_post": 4,
        "equal": 1,
    }
    assert data["directions"]["pollen_receipt"] == {
        "lower_post": 4,
        "higher_post": 4,
    }


def test_full_matching_tube_pollen_decline_is_minority_pattern():
    data = load_summary()["concordance"]
    assert data["matching_lower_tube_shorter_pollen_lower_n"] == 2
    assert data["matching_lower_tube_shorter_pollen_lower_plants"] == [
        "Farfugium japonicum",
        "Oxalis corniculata var. trichocaulon",
    ]
    assert data["tube_shorter_but_pollen_higher_plants"] == ["Vitex rotundifolia"]
    assert set(data["tube_longer_or_equal_but_pollen_lower_plants"]) == {
        "Lysimachia mauritiana",
        "Melanthera prostrata",
    }


def test_calystegia_is_explicit_counterexample_to_uniform_decline_cascade():
    rows = {row["plant"]: row for row in load_rows()}
    cal = rows["Calystegia soldanella"]
    assert float(cal["matching_delta_post_minus_oshima"]) < 0
    assert cal["tube_direction"] == "longer_post"
    assert float(cal["tube_delta_mm_post_minus_oshima"]) > 0
    assert cal["pollen_direction"] == "higher_post"
    assert float(cal["pollen_delta_post_minus_oshima"]) > 0


def test_descriptive_rank_alignment_is_not_promoted_to_cross_species_inference():
    data = load_summary()["descriptive_rank_alignment"]
    assert data["inferential_p_values_allowed"] is False
    assert data["matching_delta_vs_tube_delta_spearman"] == 0.09523809523809523
    assert data["matching_delta_vs_pollen_delta_spearman"] == -0.5476190476190477
    assert data["tube_delta_vs_pollen_delta_spearman"] == 0.2857142857142857


def test_claim_boundary_keeps_shared_environment_and_causation_explicit():
    data = load_summary()
    assert data["decision_state"] == "shared_matching_decline_with_multichannel_response_divergence"
    boundary = data["claim_boundary"].lower()
    assert "share environments" in boundary
    assert "lack within-site variance" in boundary
    assert "not a cross-species causal regression" in boundary
    assert "eight independent boundary experiments" in boundary
