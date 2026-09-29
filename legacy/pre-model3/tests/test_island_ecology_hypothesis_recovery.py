import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / "data/design/island_ecology_hypothesis_recovery_20260824.json"
CORE = ROOT / "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
SPEC = ROOT / "docs/ISLAND_ECOLOGY_MANUSCRIPT_REASSEMBLY_SPEC_20260824.md"


def test_hypothesis_recovery_closes_primary_science_without_new_data_blocker():
    recovery = json.loads(RECOVERY.read_text(encoding="utf-8"))
    assert recovery["primary_question"].startswith("Why does island-associated simplification")
    hypotheses = {row["id"]: row for row in recovery["hypotheses"]}
    assert list(hypotheses) == ["H1", "H2", "H3", "H4", "H5"]

    assert hypotheses["H1"]["result"] == "rejected"
    assert hypotheses["H2"]["result"] == "supported_within_declared_abm"
    assert hypotheses["H3"]["result"] == "supported_bidirectionally_within_declared_abm"
    assert hypotheses["H4"]["result"] == "partially_supported_and_narrowed"
    assert hypotheses["H5"]["result"] == "supported_at_qualitative_state_level"

    h2 = hypotheses["H2"]["evidence"]
    assert h2["original_full_mixed_sign"] == 0.4166666666666667
    assert h2["original_initial_position_off_mixed_sign"] == 0.0
    assert h2["independent_full_mixed_sign"] == 0.4166666666666667
    assert h2["independent_initial_position_off_mixed_sign"] == 0.0

    h3 = hypotheses["H3"]["evidence"]
    assert h3["network_context_sign_rescues"] == 16
    assert h3["network_context_worsenings"] == 11

    h4 = hypotheses["H4"]["evidence"]
    assert h4["independent_magnitude_attenuations"] == 207
    assert h4["independent_sign_rescues"] == 0
    assert h4["broadened_sign_rescues"] == 0

    h5 = hypotheses["H5"]["evidence"]
    assert h5["strict_systems"] == 13
    assert h5["branching"] == 3
    assert h5["same_direction"] == 6
    assert h5["buffering_or_alternative"] == 2
    assert h5["axis_decoupling_constraint"] == 1
    assert h5["retained_falsification"] == 1
    assert h5["generative_challenges_covered_or_sign_compatible"] == 11

    decision = recovery["submission_decision"]
    assert decision["primary_scientific_hypotheses_closed_for_submission"] is True
    assert decision["unresolved_sidelines_block_submission"] is False
    assert decision["new_simulation_required"] is False
    assert decision["new_field_data_required"] is False
    assert decision["new_external_system_search_required"] is False


def test_only_three_empirical_translation_questions_are_prioritized_for_next_programme():
    recovery = json.loads(RECOVERY.read_text(encoding="utf-8"))
    sidelines = {row["id"]: row for row in recovery["unresolved_sidelines"]}
    assert sidelines["U1_real_signed_functional_position"]["priority"] == "highest_future_test"
    assert sidelines["U2_real_network_context_mechanism"]["priority"] == "high_future_test"
    assert sidelines["U3_complete_empirical_causal_bridge"]["priority"] == "high_future_test"
    assert sidelines["U5_colonization_filter_partition"]["status"] == "outside_current_post_establishment_estimand"
    assert sidelines["U6_formal_cross_system_meta_analysis"]["priority"] == "do_not_force"


def test_core_story_and_reassembly_spec_keep_island_ecology_primary():
    core = CORE.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")

    assert "## Hypothesis recovery" in core
    for hypothesis in ["H1", "H2", "H3", "H4", "H5"]:
        assert hypothesis in core
    assert "aggregate island syndrome does not imply a universal within-lineage trajectory" in core
    assert "not a random prevalence sample" in core
    assert "must not survive in the primary island-ecology manuscript" in core

    assert "Do not end the Introduction with sensitivity/specificity as the main question." in spec
    assert "The inverse problem is the main methodological result" in spec
    assert "replaces the current method-first heading" in spec
    assert "State-separability" in spec or "state-separability" in spec
    assert "new simulation runs for narrative cleanliness" in spec
