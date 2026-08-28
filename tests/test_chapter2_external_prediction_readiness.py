import json
from pathlib import Path

from scripts.run_chapter2_external_prediction_readiness import (
    DESIGN,
    LEDGER,
    OUT,
    build,
    hypothesis_flags,
    load_ledger,
    validate_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
SUPPLEMENT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md"
MAINLINE = ROOT / "data/design/chapter2_active_manuscript_mainline_20260827.json"
MANIFEST = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"


def test_frozen_design_defines_model_derived_axes_and_competing_hypotheses():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "fixed_before_new_readiness_evaluation"
    assert [row["axis_id"] for row in design["model_derived_control_axes"]] == [
        "T",
        "D0",
        "C",
        "F",
    ]
    assert [row["id"] for row in design["competing_hypotheses"]] == [
        "H0",
        "H1",
        "H2",
        "H3",
        "H4",
    ]
    assert design["frozen_synthetic_parent"]["retuning_allowed"] is False
    assert design["chronology_boundary"]["new_evaluation_is_literature_blind"] is False


def test_admission_ledger_is_complete_and_fail_closed():
    rows = load_ledger(LEDGER)
    validate_ledger(rows)
    assert len(rows) == 25
    assert len({row["system_id"] for row in rows}) == 25
    assert all(row["source_reference"] for row in rows)
    assert all(row["evidence_note"] for row in rows)
    assert not any(
        row["admission_class"] == "admissible_prospective_like_challenge"
        for row in rows
    )
    assert all(row["chapter2_target_contract"] == "fail" for row in rows)


def test_hypothesis_flags_require_target_and_prespecified_inputs():
    complete = {
        "chapter2_target_contract": "pass",
        "response_outcome": "direct_measurement",
        "source_functional_state": "source_derived_proxy",
        "partner_loss": "direct_measurement",
        "partner_arrival_replacement": "source_derived_proxy",
        "community_functional_shift": "direct_measurement",
        "local_filtering": "direct_measurement",
    }
    assert hypothesis_flags(complete) == {
        "H0": True,
        "H1": True,
        "H2": True,
        "H3": True,
        "H4": True,
    }
    missing_state = dict(complete, source_functional_state="unavailable")
    assert hypothesis_flags(missing_state) == {
        "H0": True,
        "H1": False,
        "H2": True,
        "H3": False,
        "H4": False,
    }


def test_frozen_readiness_result_matches_deterministic_rebuild():
    frozen = json.loads(OUT.read_text(encoding="utf-8"))
    assert frozen == build()
    assert frozen["decision"].startswith("C_")
    assert frozen["maximum_supported_claim_level"] == "Level 2"
    gate = frozen["formal_evaluation_gate"]
    assert gate["passed"] is False
    assert gate["H0_to_H4_model_comparison"] == "not_evaluable"
    assert gate["leave_one_system_out"] == "not_evaluable"
    assert frozen["izu_anchor_selection"][
        "formal_preoutcome_selection_score_available"
    ] is False
    assert frozen["izu_anchor_selection"][
        "chapter3_data_used_for_chapter2_validation"
    ] is False
    assert frozen["admission"]["class_counts"] == {
        "retrospective_explanatory_test_only": 12,
        "reality_boundary_only": 8,
        "source_gated_unusable": 5,
    }


def test_manuscript_and_submission_surfaces_preserve_level2_ceiling():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    mainline = json.loads(MAINLINE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert "None of the 25 audited entries passed" in manuscript
    assert "The result is a data-readiness and identifiability stop" in manuscript
    assert "not the result of an outcome-independent global ranking" in manuscript
    assert "# Appendix S13. Frozen external-prediction readiness audit" in supplement
    assert "No classifier was fitted" in supplement

    readiness = mainline["external_prediction_readiness"]
    assert readiness["full_chapter2_target_contract_passes"] == 0
    assert readiness["formal_H0_to_H4_comparison"] == "not_evaluable"
    assert readiness["maximum_supported_level"] == 2
    external = manifest["external_system_role"]
    assert external["full_external_prediction_contract_passes"] == 0
    assert external["maximum_supported_claim_level"] == 2
    assert manifest["model_reporting"]["external_prediction_readiness"][
        "posthoc_retuning_or_system_replacement"
    ] is False
