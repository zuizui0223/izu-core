import json
from pathlib import Path

from scripts.run_abm_v12_branch_generator_independent_robustness import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/abm_v12_branch_generator_independent_robustness_frozen.json"


def test_independent_result_regenerates_exactly():
    assert build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_independent_block_replicates_minimal_branch_generator():
    result = build()
    assert result["seed"] == 90260825
    assert result["decision"] == "replicated_minimal_generator"
    assert result["stop_rule_honored"] is True
    assert result["design"]["external_targets_loaded"] is False
    assert result["full_residual"]["mixed_sign_run_fraction"] > 0
    assert result["drop_one"]["initial_trait_heterogeneity"]["mixed_sign_run_fraction"] == 0.0
    assert result["drop_one"]["initial_trait_heterogeneity"]["mean_within_run_branching_balance"] == 0.0
    assert result["drop_one"]["trait_adjustment_heterogeneity"]["mixed_sign_run_fraction"] > 0
    assert result["drop_one"]["assurance_ceiling_heterogeneity"]["mixed_sign_run_fraction"] > 0
