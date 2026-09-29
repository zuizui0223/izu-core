import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "design" / "specialist_survivorship_constraint.json"


def load_design():
    return json.loads(DESIGN.read_text(encoding="utf-8"))


def test_clean_same_lineage_specialist_holdout_is_selection_conditioned():
    data = load_design()
    assert data["answer"] == "no"
    assert data["clean_bombus_holdout_status"] == "biologically_selection_conditioned_not_merely_data_missing"
    assert "conditions the analysis on survival/establishment" in data["reason"]


def test_survivor_only_trait_analysis_and_establishment_filtering_are_separate_domains():
    consequence = load_design()["analysis_consequence"]
    assert "survivor-conditional" in consequence["same_lineage_trait_holdout"]
    assert "separate response domain" in consequence["occupancy_or_establishment_filtering"]
    assert "separate response mode" in consequence["hybrid_replacement"]


def test_strict_dependency_can_be_selected_out_of_survivor_comparisons():
    bias = load_design()["selection_bias"]
    assert "strict Bombus dependence without alternative reproductive or interaction pathways" in bias["selected_against"]
    assert "interaction rewiring" in bias["selected_for"]
    assert "hybridization or other lineage change" in bias["selected_for"]


def test_design_does_not_promote_survivorship_constraint_to_causality():
    data = load_design()
    assert "does not prove" in data["claim_boundary"].lower()
    assert "habitat" in data["claim_boundary"].lower()
    assert "dispersal" in data["claim_boundary"].lower()
