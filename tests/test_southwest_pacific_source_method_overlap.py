import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKED = ROOT / "data/results/southwest_pacific_pairs/source_method_geographic_overlap_sensitivity.json"


def test_online_only_signal_persists_with_source_method_geographic_overlap():
    report = json.loads(CHECKED.read_text(encoding="utf-8"))
    online = report["online_only_within_mixed_source_islands"]
    assert len(report["mixed_source_islands"]) == 7
    assert online["n_pairs"] == 66
    assert online["n_islands"] == 7
    assert online["slope"] < 1.0
    assert online["island_cluster_95"][1] < 1.0
    assert report["formal_consequence"]["online_only_result_explained_by_nonoverlapping_island_composition"] is False


def test_overlap_adversary_does_not_promote_source_method_or_reliability_claims():
    report = json.loads(CHECKED.read_text(encoding="utf-8"))
    consequence = report["formal_consequence"]
    assert consequence["source_method_causal_effect_identified"] is False
    assert consequence["empirical_reliability_identified"] is False
    assert consequence["formal_admission_opened"] is False
