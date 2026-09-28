import json
from pathlib import Path


def test_tierb1_runlock_preserves_primary_failure_and_secondary_sensitivity():
    x = json.loads(Path("data/results/abm_v4_dore_structure_prediction_runlock.json").read_text())
    p = x["primary_distance_ecdf"]
    s = x["secondary_geography_pc1"]

    assert p["decision"] == "does_not_have_robust_architecture_transfer_across_all_metrics_and_strata"
    assert p["Connectance"]["system_saturations_beating_geography"] == 5
    assert p["Connectance"]["stratum_saturations_beating_geography"] == 0
    assert p["Li"]["system_saturations_beating_geography"] == 0
    assert p["Li"]["stratum_saturations_beating_geography"] == 5
    assert p["Lp"]["system_saturations_beating_geography"] == 0
    assert p["Lp"]["stratum_saturations_beating_geography"] == 0

    for metric in ("Connectance", "Li", "Lp"):
        assert s[metric]["system_saturations_beating_geography"] == 5
        assert s[metric]["stratum_saturations_beating_geography"] == 5

    assert "cannot replace" in x["claim_boundary"]
