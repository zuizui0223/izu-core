import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data" / "design" / "abm_v12_heliconia_source_gate.json"


def load_gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_target_is_closed_while_dryad_bytes_are_unrecovered():
    gate = load_gate()
    recovery = gate["selection_source"]["current_byte_recovery"]
    assert recovery["recovered"] is False
    assert recovery["target_metrics_calculated"] is False
    assert gate["future_target_contract"]["status"] == "closed_until_selection_bytes_recovered_and_schema_locked"


def test_mapping_exactly_reproduces_independent_2011_anchors():
    gate = load_gate()
    mapping = gate["frozen_signed_position_mapping"]
    intercept = mapping["intercept_mm"]
    slope = mapping["slope_corolla_per_bill"]
    male = intercept + slope * 19.8
    female = intercept + slope * 26.6
    assert math.isclose(male, 35.8, abs_tol=1e-12)
    assert math.isclose(female, 47.8, abs_tol=1e-12)


def test_pollinator_center_cannot_be_inferred_from_flower_or_outcome():
    gate = load_gate()
    rule = gate["frozen_signed_position_mapping"]["population_year_pollinator_center"].lower()
    assert "source-native 2013 sex-specific" in rule
    assert "do not substitute a canonical sex" in rule
    forbidden = " ".join(gate["future_target_contract"]["forbidden_rescues"]).lower()
    assert "floral phenotype" in forbidden
    assert "seed-set" in forbidden


def test_validation_is_not_claimed_as_literature_blind():
    gate = load_gate()
    context = gate["known_literature_context_not_used_for_mapping"]
    assert context["outcomes_are_literature_known"] is True
    assert context["validation_class"] == "new_exact_derived_statistic_test_not_literature_blind"
    assert gate["decision"].startswith("admit_heliconia_as_next_v12_source_candidate")


def test_mapping_is_not_promoted_to_universal_optimum():
    gate = load_gate()
    assert gate["frozen_signed_position_mapping"]["not_a_universal_geometry_law"] is True
    assert "does not estimate a universal floral optimum" in gate["claim_boundary"]
