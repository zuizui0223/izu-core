import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data" / "design" / "abm_v12_heliconia_source_gate.json"


def load_gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_target_opens_only_after_distinct_package_route_recovers_exact_bytes():
    gate = load_gate()
    recovery = gate["selection_source"]["current_byte_recovery"]
    assert recovery["individual_file_stream_route"]["recovered"] is False
    package = recovery["full_dataset_package_route"]
    assert package["recovered"] is True
    assert package["package_bytes"] == 174400
    assert package["package_sha256"] == "9813060432d788cc46c49268b09b70a6eb2df8b9483814be3272c769c2143218"
    assert package["target_metrics_calculated"] is True
    assert gate["target_contract"]["status"] == "opened_after_selection_bytes_schema_and_visit_weights_locked"


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
    assert "locked source-native 2013 sex-specific" in rule
    forbidden = " ".join(gate["target_contract"]["forbidden_rescues"]).lower()
    assert "floral phenotype" in forbidden
    assert "seed-set" in forbidden


def test_visit_weights_are_locked_without_replicating_pooled_bihai_counts():
    gate = load_gate()
    visits = gate["source_native_visit_weights"]["units"]
    assert visits["bihai_boeri_2008"] == {
        "female_fraction": 1.0,
        "female_visits": None,
        "male_visits": None,
        "count_scope": "pooled_bihai_N14_exclusive_female",
    }
    assert visits["caribaea_red_syndicate_2008"]["female_visits"] == 8
    assert visits["caribaea_red_syndicate_2008"]["male_visits"] == 14
    assert visits["caribaea_yellow_la_savanne_2009"]["female_fraction"] == 0.5
    assert "duplicate the pooled H. bihai N=14" in gate["source_native_visit_weights"]["forbidden_inference"]


def test_validation_is_not_claimed_as_literature_blind():
    gate = load_gate()
    context = gate["known_literature_context_not_used_for_mapping"]
    assert context["outcomes_are_literature_known"] is True
    assert context["validation_class"] == "new_exact_derived_statistic_test_not_literature_blind"
    assert gate["decision"] == "open_heliconia_v12_exact_target_after_package_and_visit_weight_recovery"


def test_mapping_is_not_promoted_to_universal_optimum():
    gate = load_gate()
    assert gate["frozen_signed_position_mapping"]["not_a_universal_geometry_law"] is True
    assert "not a universal floral optimum" in gate["claim_boundary"]


def test_primary_model_and_direction_are_frozen_before_result_interpretation():
    gate = load_gate()
    contract = gate["target_contract"]
    assert "beta_multi" in contract["primary_selection_response"]
    assert contract["primary_between_unit_model"].startswith("unweighted OLS")
    assert contract["predeclared_supported_direction"] == "negative"
    assert gate["frozen_signed_position_mapping"]["mapping_frozen_before_target_commit"] == "62fb08e"
