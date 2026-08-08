import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_community_response.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_community_trait_matching_is_more_consistently_lower_post_than_generality():
    metrics = load_data()["metrics"]
    tm = metrics["corrected_community_trait_matching_TM_z"]
    pol_fg = metrics["pollinator_functional_generality_FG_Pol_z"]
    pla_fg = metrics["plant_functional_generality_FG_Pla_z"]
    assert tm["mean_delta"] < -1.7
    assert tm["n_lower_post_seasons"] == 4
    assert pol_fg["mean_delta"] > 1.5
    assert pol_fg["n_higher_post_seasons"] == 4
    assert pla_fg["mean_delta"] > 0
    assert pla_fg["n_higher_post_seasons"] == 3


def test_seasons_are_not_independent_boundary_replications():
    data = load_data()
    assert data["independent_oshima_bridge_sites"] == 1
    assert data["temporal_repeats"] == 5
    assert "not five independent geographic boundary replications" in data["claim_boundary"]
    assert "cannot identify a causal second-boundary effect" in data["claim_boundary"]
