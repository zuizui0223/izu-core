import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / "data/design/island_ecology_hypothesis_recovery_20260824.json"
MAINLINE = ROOT / "data/design/simulation_study_mainline_20260824.json"
ROOT_MAINLINE = ROOT / "data/design/active_development_mainline.json"
READINESS = ROOT / "data/design/island_ecology_submission_readiness_20260824.json"
ARCHITECTURE = ROOT / "data/design/simulation_manuscript_results_architecture.json"
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"


def test_h1_h5_are_formally_closed_with_narrow_results():
    recovery = json.loads(RECOVERY.read_text(encoding="utf-8"))
    hypotheses = {row["id"]: row["result"] for row in recovery["hypotheses"]}
    assert hypotheses == {
        "H1": "rejected",
        "H2": "supported_within_declared_abm_and_independently_replicated",
        "H3": "supported_as_bidirectional_branch_allocator_within_declared_abm",
        "H4": "magnitude_attenuation_supported_sign_rescue_rejected",
        "H5": "supported_at_qualitative_response_state_level",
    }

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    assert readiness["scientific_state"]["primary_hypotheses_closed_for_submission"] is True
    assert readiness["scientific_validation_gate"]["status"] == "passed"
    assert all(readiness["scientific_validation_gate"]["checks"].values())


def test_validation_gate_is_closed_and_only_submission_packaging_remains():
    mainline = json.loads(MAINLINE.read_text(encoding="utf-8"))
    assert mainline["active_gate"]["name"] == "journal_submission_packaging"
    completed = {row["name"]: row["status"] for row in mainline["completed_gates"]}
    assert completed["island_ecology_manuscript_validation"].startswith("passed_against_frozen_results")

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    assert readiness["scientific_work_not_required_for_current_submission"] == [
        "additional_simulation",
        "new_field_data",
        "additional_island_system_search",
        "empirical_mechanism_mapping",
        "formal_cross_system_meta_analysis",
    ]
    assert [row["id"] for row in readiness["remaining_submission_tasks"]] == [
        "E1_target_journal",
        "E2_references",
        "E3_authorship_and_declarations",
        "E4_submission_assets",
        "E5_immutable_release",
    ]

    root_mainline = json.loads(ROOT_MAINLINE.read_text(encoding="utf-8"))
    assert root_mainline["submission_mainline"] == "data/design/simulation_study_mainline_20260824.json"
    assert root_mainline["current_submission"]["hypotheses"] == {
        key: value
        for key, value in readiness["scientific_state"].items()
        if key != "primary_hypotheses_closed_for_submission"
    }
    assert root_mainline["current_submission"]["active_gate"] == "journal_submission_packaging"


def test_primary_manuscript_is_wired_to_frozen_figure_and_table_architecture():
    architecture = json.loads(ARCHITECTURE.read_text(encoding="utf-8"))
    text = MANUSCRIPT.read_text(encoding="utf-8")

    assert architecture["manuscript_end_state"] == (
        "H1_H5_island_ecology_primary_manuscript_scientifically_validated_and_frozen_for_submission_packaging"
    )
    for figure in ["Fig. 1", "Fig. 2", "Fig. 3", "Fig. 4"]:
        assert figure in text
    for table in ["Table 1", "Table 2", "Table 3"]:
        assert table in text
    assert "## Figure legends" in text
    assert "## Table titles" in text
    assert "scientifically validated primary manuscript" in text.lower()
