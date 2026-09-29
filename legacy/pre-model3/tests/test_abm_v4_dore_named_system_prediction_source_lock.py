import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/abm_v4_dore_named_system_prediction_source_lock.json"


def load():
    return json.loads(RESULT.read_text())


def test_named_system_primary_result_is_source_locked_and_robust():
    x = load()
    assert x["source_workflow_run"] == 32246531384
    assert x["source_artifact_id"] == 9362979083
    assert x["overall_coverage"]["source_locked_dore_targets_with_dist"] == 26
    assert x["overall_coverage"]["n_systems"] == 6
    assert x["decision"] == "primary_distance_mapping_has_robust_mechanistic_predictive_gain"
    for target in ("pollinator_richness", "link_richness"):
        s = x["primary_distance_ecdf"]["summary"][target]
        assert s["saturations_beating_effort_only"] == 5
        assert s["saturations_beating_geography_quadratic"] == 5
        assert s["robust_predictive_gain_over_geography"] is True


def test_secondary_pc1_does_not_get_promoted_over_primary():
    x = load()
    poll = x["secondary_geography_only_pc1"]["summary"]["pollinator_richness"]
    links = x["secondary_geography_only_pc1"]["summary"]["link_richness"]
    assert poll["saturations_beating_geography_quadratic"] == 0
    assert poll["robust_predictive_gain_over_geography"] is False
    assert links["saturations_beating_geography_quadratic"] == 5
    assert links["robust_predictive_gain_over_geography"] is True


def test_primary_mae_beats_both_baselines_at_every_saturation():
    x = load()
    for sat, outcomes in x["primary_distance_ecdf"]["mae_by_saturation"].items():
        assert sat in {"1.0", "1.5", "2.0", "2.5", "3.0"}
        for outcome in outcomes.values():
            assert outcome["abm_plus_sampling_design"] < outcome["effort_only"]
            assert outcome["abm_plus_sampling_design"] < outcome["geography_quadratic"]
