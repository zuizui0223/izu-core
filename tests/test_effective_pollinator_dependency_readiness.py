import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "design" / "effective_pollinator_dependency_field_readiness.json"
PRIORITY = ROOT / "data" / "design" / "effective_dependency_pilot_field_priority.json"


def load_readiness():
    return json.loads(READINESS.read_text(encoding="utf-8"))


def load_priority():
    return json.loads(PRIORITY.read_text(encoding="utf-8"))


def test_field_dependency_design_is_ready_but_empirical_data_are_missing():
    data = load_readiness()
    assert data["schema_version"] == "1.5"
    assert data["status"] == "implementation_ready_field_data_missing"
    assert data["focal_anchor"] == "Campanula microdonta"
    assert data["structural_readiness_only"] is True
    assert data["sample_size_or_power_threshold_locked"] is False


def test_direct_dependency_design_requires_svd_and_three_core_reproductive_treatments():
    channels = load_readiness()["required_linked_channels"]
    assert any("single-visit pollen deposition" in item for item in channels)
    assert "open_pollinated reproductive treatment" in channels
    assert "bagged_autonomous reproductive treatment" in channels
    assert "supplemental_outcross reproductive treatment" in channels
    assert "no-visit SVD controls" in channels


def test_dependency_and_fdq_readiness_are_parallel_not_collapsed():
    data = load_readiness()
    fdq = data["functional_exposure_readiness"]
    assert fdq["dependency_structural_completion_requires_fdq"] is False
    assert fdq["dependency_x_fdq_test_requires_fdq"] is True
    assert fdq["status"] == "execution_ready_historical_trait_table_unrecovered"
    assert fdq["historical_trait_recovery"]["current_named_pollinator_taxa"] == 209
    assert fdq["historical_trait_recovery"]["recovered_numeric_proboscis_taxa"] == 0


def test_fdq_uses_source_locked_rao_q_and_strict_trait_coverage():
    fdq = load_readiness()["functional_exposure_readiness"]
    assert "Rao quadratic entropy" in fdq["estimand"]
    assert fdq["formula"] == "sum_i sum_j p_i p_j abs(L_i - L_j)"
    assert fdq["visitor_taxon_field"] == "visitor_taxon_id"
    assert any("every positive-abundance visitor taxon" in rule for rule in fdq["strict_fdq_gate"])
    assert any("not dropped before renormalization" in rule for rule in fdq["strict_fdq_gate"])


def test_prospective_proboscis_measurement_can_fill_future_fdq_traits_without_table_s2():
    measure = load_readiness()["functional_exposure_readiness"]["prospective_trait_measurement"]
    assert measure["measurement_method"] == "digital_caliper"
    assert measure["unit"] == "mm"
    assert measure["target_independent_specimens_per_taxon_site"] == 5
    assert measure["admitted_trait_status"] == "measured_new"
    assert "all_available_at_site=yes" in measure["below_target_admission"]


def test_field_priority_preserves_fdq_metadata_without_blocking_dependency_panel():
    data = load_priority()
    assert data["schema_version"] == "1.2"
    order = data["within_population_collection_order"]
    assert any("visitor_taxon_id" in item for item in order)
    rules = data["continue_rules"]
    assert any("FDQ incompleteness does not invalidate dependency structural completion" in item for item in rules)
    stop = data["stop_or_do_not_promote_rules"]
    assert any("Do not impute proboscis length" in item for item in stop)


def test_pilot_precision_state_machine_does_not_invent_sample_size_before_dispersion():
    data = load_readiness()
    states = [item["state"] for item in data["pilot_precision_state_machine"]]
    assert states == [
        "implementation_ready_field_data_missing",
        "pilot_dispersion_estimable",
        "precision_goal_locked",
        "confirmatory_replication_proposed",
    ]
    plan = data["precision_planning"]
    assert plan["independent_unit"] == "plant"
    assert set(plan["within_plant_subsamples"]) == {"flowers", "single-visit SVD events"}
    assert plan["draft_goal_generates_sample_size"] is False
    assert plan["normal_approximation_is_final_power_analysis"] is False
    assert "absolute two-sided CI half-width" in plan["precision_target_type"]


def test_official_service_output_is_withheld_without_background_control():
    text = load_readiness()["service_output_guard"].lower()
    assert "withholds background-adjusted svd" in text
    assert "lacks a no-visit svd control" in text


def test_design_does_not_relabel_floral_form_as_dependency():
    data = load_readiness()
    assert "do not assign specialist/generalist classes from floral syndrome labels" in data["comparator_rule"]
    assert "not preassigned from corolla morphology" in data["high_dependency_endpoint_rule"]


def test_claim_boundary_keeps_selfing_historical_causation_and_fdq_separate():
    text = load_readiness()["claim_boundary"].lower()
    assert "does not by itself identify historical bombus loss" in text
    assert "self-compatibility" in text
    assert "realized selfing" in text
    assert "causal oshima-toshima boundary effect" in text
    assert "fdq is a separate functional-exposure gate" in text
