from scripts.audit_chapter2_submission_closure import build_audit


def test_submission_closure_tracks_bridge_complete_science_and_open_package_qa():
    audit = build_audit()
    assert audit["scope"] == "historical_bridge_submission_only_not_current_process_manuscript"
    assert audit["current_process_goal_completion_assessed"] is False
    assert audit["scientific_gate_complete"] is True
    assert audit["unified_model3_locked"] is True
    assert audit["real_island_abc_confrontation_locked"] is True
    assert audit["scientific_question_closed"] is True
    assert audit["field_e3_e4_required"] is False
    assert audit["submission_ready"] is False


def test_submission_closure_has_only_author_metadata_after_scientific_package_pass():
    audit = build_audit()
    assert audit["nonmetadata_submission_errors"] == []
    assert audit["nonmetadata_submission_preflight_ready"] is True
    assert audit["active_nonmetadata_package_blockers"] == []
    assert audit["only_author_supplied_metadata_and_confirmations_remain"] is True
    assert audit["submission_ready"] is False
    assert audit["next_transition"].startswith("author supplies the required metadata/confirmation categories")


def test_submission_closure_preserves_author_metadata_requirements():
    audit = build_audit()
    assert audit["metadata_template_validation_error_count"] > 0
    assert audit["unexpected_metadata_errors"] == []
    assert audit["ethics_statement_prefilled"] is True
    assert audit["ethics_statement_author_confirmation_required"] is True
    assert "ethics_statement_author_confirmation" in audit["required_human_input_categories"]
    assert set(audit["optional_not_initial_submission_blockers"]) == {
        "coauthor_orcids",
        "author_contributions_credit_roles",
    }
    assert audit["planned_public_repository_already_fixed"] == "Dryad Digital Repository"
