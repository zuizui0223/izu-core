import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
V12 = ROOT / "data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json"
V12_INDEPENDENT = ROOT / "data/results/abm_v12_branch_generator_independent_robustness_frozen.json"
NETWORK = ROOT / "data/results/network_context_buffering_capability_robustness_frozen.json"
ASSURANCE = ROOT / "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"
EXTERNAL = ROOT / "data/design/simulation_manuscript_external_system_reference_matrix.json"


def test_primary_manuscript_is_H1_H5_island_ecology_story():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert text.startswith("# One perturbation, multiple island responses")
    for hypothesis in ["H1", "H2", "H3", "H4", "H5"]:
        assert hypothesis in text

    assert "## 4.1 Aggregate island syndromes can coexist with lineage-level branching" in text
    assert "## 4.2 Functional starting state determines branch potential" in text
    assert "## 4.3 Local interaction context governs propagation, whereas assurance mainly dampens it" in text
    assert "## 4.4 Cross-island recurrence supports a response architecture, not a universal mechanism" in text
    assert "## 4.5 What remains unresolved empirically" in text
    assert "## 4.6 Inference boundary" in text
    assert "The inverse problem is the main methodological result" not in text
    assert "supporting rather than primary results" in text


def test_primary_manuscript_headline_numbers_match_frozen_results():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    v12 = json.loads(V12.read_text(encoding="utf-8"))
    independent = json.loads(V12_INDEPENDENT.read_text(encoding="utf-8"))
    network = json.loads(NETWORK.read_text(encoding="utf-8"))
    assurance = json.loads(ASSURANCE.read_text(encoding="utf-8"))

    assert f"{v12['full_residual_model']['mixed_sign_run_fraction']:.4f}" in text
    assert f"{independent['full_residual']['mixed_sign_run_fraction']:.4f}" in text
    assert v12["drop_one"]["initial_trait_heterogeneity"]["mixed_sign_run_fraction_ablated"] == 0.0
    assert independent["drop_one"]["initial_trait_heterogeneity"]["mixed_sign_run_fraction"] == 0.0

    independent_summary = network["independent_summary"]
    assert f"{independent_summary['reproduction_sign_rescue_count']} of {independent_summary['global_decline_and_support_off_reproduction_decline']}" in text
    assert f"{independent_summary['reproduction_magnitude_rescue_count']} of {independent_summary['global_decline_and_support_off_reproduction_decline']}" in text
    assert f"{independent_summary['reproduction_worsening_count']} of {independent_summary['global_decline_and_support_off_reproduction_decline']}" in text

    overall = assurance["overall"]
    assert f"{overall['assurance_magnitude_rescues']} of {overall['service_decline_lineages']}" in text
    assert "zero sign rescues among 525 eligible declines" in text


def test_external_system_contract_and_protected_boundaries_are_preserved():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    matrix = json.loads(EXTERNAL.read_text(encoding="utf-8"))

    assert matrix["strict_system_count"] == 13
    assert matrix["state_count_contract"] == {
        "branches_downstream": 3,
        "propagates_same_direction": 6,
        "buffering_or_alternative": 2,
        "reproductive_axes_decouple": 1,
        "retained_falsification": 1,
    }

    expected_tokens = [
        "Izu multi-taxon",
        "Caribbean Gesneriaceae",
        "Canary Islands Teide",
        "Ogasawara",
        "New Zealand",
        "Guam–Saipan",
        "Seychelles",
        "Mauritius",
        "Bahamas",
        "Hawaiian lobelioids",
        "Channel Islands *Nicotiana*",
        "Puerto Rico–Mona *Guaiacum*",
        "Dominica *Heliconia*",
    ]
    for token in expected_tokens:
        assert token in text

    assert "not a random prevalence sample" in text
    assert "not retuned" in text
    assert "reproductive-axis-decoupling" in text
    assert "does not establish that one empirical mechanism generates all of them" in text


def test_unresolved_empirical_sidelines_are_future_tests_not_submission_gates():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Three empirical questions now follow directly from the paper." in text
    assert "outcome-blind signed-position design" in text
    assert "network-context mechanism needs a matched empirical test" in text
    assert "no current external system closes the full empirical chain" in text
    assert "None of these unresolved questions blocks the present submission" in text
