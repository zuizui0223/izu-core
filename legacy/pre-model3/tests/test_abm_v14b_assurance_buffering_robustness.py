import json
from pathlib import Path

from scripts import run_constraint_mechanism_abm_v14b_assurance_buffering_robustness as v14b


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v14b_assurance_buffering_robustness_freeze.json"


def test_v14b_uses_nonoverlapping_seed_block_without_parameter_changes():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    lock = design["model_and_parameter_lock"]
    assert design["status"] == "independent_seed_block_frozen_before_run"
    assert lock["replicates"] == v14b.REPLICATES == 40
    assert lock["contexts"] == v14b.CONTEXTS == 4
    assert lock["lineages"] == v14b.LINEAGES == 24
    assert lock["steps"] == v14b.STEPS == 120
    assert lock["seed"] == v14b.SEED == 120260822
    assert lock["parameter_changes_from_v14"] is False
    assert lock["threshold_changes_from_v14"] is False
    assert design["expected_total_lineage_contrasts"] == v14b.EXPECTED_CONTRASTS == 2880


def test_v14b_primary_decision_was_frozen_before_run():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    rule = design["primary_robustness_rule"]
    assert rule["metric"] == "assurance_sign_rescues"
    assert rule["independent_confirmation_condition"] == "assurance_sign_rescues > 0 in the non-overlapping seed block"
    assert rule["decision_if_met"] == "synthetic_sign_buffering_replicates_in_independent_seed_block"
    assert design["secondary_robustness_rule"]["broad_effect_condition"] == "> 0.5"
    assert design["empirical_target_use"]["observed_natural_buffering_frequency_targeted"] is False
