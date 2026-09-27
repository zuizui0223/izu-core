from scripts.audit_chapter2_submission_closure import build_audit


def test_submission_closure_tracks_unified_model3_science_and_open_package_qa():
    audit = build_audit()
    assert audit["scientific_gate_complete"] is True
    assert audit["unified_model3_locked"] is True
    assert audit["real_island_abc_confrontation_locked"] is True
    assert audit["scientific_question_closed"] is False
    assert audit["field_e3_e4_required"] is False
    assert audit["submission_ready"] is False


def test_submission_closure_retains_declared_nonmetadata_blockers_until_figures_and_qa_are_done():
    audit = build_audit()
    assert audit["nonmetadata_submission_errors"] == []
    assert audit["nonmetadata_submission_preflight_ready"] is False
    assert set(audit["active_nonmetadata_package_blockers"]) == {
        "complete frozen Model 3 original-Chapter-2 bridge campaign",
        "regenerate unified Model 3 main figures",
        "pass unified renderers and fail-closed submission audits",
    }
    assert audit["only_author_supplied_metadata_and_confirmations_remain"] is False
    assert audit["next_transition"].startswith("complete frozen Model 3 original-Chapter-2 bridge campaign")


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
