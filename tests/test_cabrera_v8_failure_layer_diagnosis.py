from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/cabrera_v8_failure_diagnosis_v1.json"
SCRIPT = ROOT / "scripts/diagnose_cabrera_v8_failure_layers.py"


def test_diagnosis_is_bound_to_preserved_v8_failure_not_rescue():
    design = json.loads(DESIGN.read_text())
    assert design["failure_source"]["pr"] == 205
    assert design["failure_source"]["decision"] == "v8_fails_cabrera_conditional_pair_support_predictive_adequacy"
    assert "cannot convert" in design["purpose"].lower()
    assert "cannot validate" in design["claim_boundary"].lower()


def test_diagnosis_keeps_primary_method_context_and_weight_frozen():
    design = json.loads(DESIGN.read_text())
    source = design["source_lock"]
    assert source["primary_method"] == "obs"
    assert source["network_unit"] == ["COMMUNITY", "visita"]
    assert source["context_count"] == 55
    assert source["interaction_weight"] == "N ind"


def test_diagnosis_decomposes_plant_opportunity_exposure_and_evenness():
    design = json.loads(DESIGN.read_text())
    decomposition = design["diagnostic_decomposition"]
    for key in (
        "global_pair_support_fraction",
        "sampled_positive_plant_fraction",
        "plant_conditioned_pair_opportunity_fraction",
        "pair_realization_given_sampled_plants",
        "unique_census_count",
        "total_unique_census_minutes",
        "observed_flower_exposure",
        "interaction_shannon",
        "positive_pair_count",
        "interaction_evenness",
    ):
        assert key in decomposition


def test_script_does_not_refit_v8_or_change_primary_layer():
    text = SCRIPT.read_text().lower()
    assert "run_constraint_mechanism_abm_v8" not in text
    assert "support_strength" not in text
    assert "weight_strength" not in text
    assert '== "obs"' in text
    assert 'row.get("n ind")' in text
    assert "n visit flowers" not in text
    assert "primary_v8_result_relabelled" in text
    assert "v8_parameters_reestimated" in text


def test_relationships_are_descriptive_with_leave_one_community_robustness():
    design = json.loads(DESIGN.read_text())
    assert "spearman rho descriptively" in design["robustness"].lower()
    assert "leave-one-community-out" in design["robustness"].lower()
    assert "p-values" in design["robustness"].lower()
    text = SCRIPT.read_text()
    assert "leave_one_community_out_rho_range" in text
    assert "spearmanr" in text
