from scripts.augment_cross_archipelago_effect_registry import (
    augment_external_documents,
    augment_registry,
)


def base_row(**updates: str) -> dict[str, str]:
    row = {
        "effect_id": "placeholder",
        "system_id": "ogasawara_2026",
        "system_cluster": "ogasawara_oceanic_archipelago",
        "source_path": "old.json",
        "evidence_family": "source_state",
        "response": "source_or_schema_readiness",
        "predictor_or_contrast": "not applicable",
        "estimate": "",
        "uncertainty_type": "",
        "uncertainty_value": "",
        "unit": "",
        "independent_unit": "",
        "row_role": "source_state",
        "admission_status": "blocked",
        "cross_system_model_eligible": "no",
        "causal_claim_allowed": "no",
        "notes": "placeholder",
    }
    row.update(updates)
    return row


def ogasawara_document() -> dict[str, object]:
    return {
        "effects": [
            {
                "effect_id": "oga_turnover",
                "system_id": "ogasawara_2026",
                "system_cluster": "ogasawara_oceanic_archipelago",
                "evidence_family": "matched_shared_plant_pollinator_assemblage_turnover",
                "response": "pollinator_morisita_horn_turnover",
                "predictor_or_contrast": "anole presence versus absence",
                "estimate": 0.68,
                "uncertainty_type": "exact_nonparametric_bootstrap_percentile_interval_for_median",
                "uncertainty_value": [0.50, 0.97],
                "unit": "turnover",
                "independent_unit": "plants within one context contrast",
                "row_role": "external_context_effect",
                "admission_status": "empirical_context_effect",
                "cross_system_model_eligible": False,
                "causal_claim_allowed": False,
                "notes": "context-specific",
            }
        ]
    }


def southwest_document() -> dict[str, object]:
    return {
        "effects": [
            {
                "effect_id": "sw_animal_size_slope",
                "system_id": "southwest_pacific_flower_size",
                "system_cluster": "southwest_pacific_ten_archipelagos",
                "evidence_family": "animal_pollinated_island_mainland_flower_size_starting_value_slope",
                "response": "flower_size_log10_response_ratio",
                "predictor_or_contrast": "log10 mainland flower size",
                "estimate": -0.15,
                "uncertainty_type": "island_cluster_bootstrap_percentile_interval",
                "uncertainty_value": [-0.30, -0.07],
                "unit": "log response-ratio slope",
                "independent_unit": "colonisation events nested in island groups",
                "row_role": "external_effect",
                "admission_status": "empirical_numeric_effect",
                "cross_system_model_eligible": True,
                "causal_claim_allowed": False,
                "notes": "morphology-only",
            }
        ]
    }


def test_context_effect_replaces_placeholder_without_opening_formal_fit():
    rows = [
        base_row(
            effect_id="wanshan_turnover",
            system_id="wanshan_yongxing",
            system_cluster="wanshan_yongxing_paired_system",
            evidence_family="matched_shared_plant_pollinator_assemblage_turnover",
            response="pollinator_morisita_horn_turnover",
            estimate="0.98",
            uncertainty_type="exact_nonparametric_bootstrap_percentile_interval_for_median",
            uncertainty_value="[0.94,1.0]",
            row_role="external_effect",
            admission_status="empirical_numeric_effect",
            cross_system_model_eligible="yes",
        ),
        base_row(),
    ]
    combined, summary = augment_registry(
        rows,
        ogasawara_document(),
        source_path="data/results/ogasawara/context_analysis/effect_rows.json",
    )
    ogasawara = [row for row in combined if row["system_id"] == "ogasawara_2026"]
    assert len(ogasawara) == 1
    assert ogasawara[0]["effect_id"] == "oga_turnover"
    assert ogasawara[0]["cross_system_model_eligible"] == "no"
    assert ogasawara[0]["uncertainty_value"] == "[0.5,0.97]"
    assert summary["external_context_effect_rows"] == 1
    assert summary["cross_system_model_eligible_rows"] == 1
    assert summary["effect_families_with_two_or_more_independent_systems"] == []
    assert summary["formal_cross_system_fit_ready"] is False


def test_two_external_documents_replace_only_their_source_states():
    rows = [
        base_row(
            effect_id="wanshan_visits",
            system_id="wanshan_yongxing",
            system_cluster="wanshan_yongxing_paired_system",
            evidence_family="matched_shared_plant_visitation_log_response_ratio",
            response="visitation_log_response_ratio",
            estimate="-2.5",
            uncertainty_type="exact_nonparametric_bootstrap_percentile_interval_for_median",
            uncertainty_value="[-3.3,-2.1]",
            row_role="external_effect",
            admission_status="empirical_numeric_effect",
            cross_system_model_eligible="yes",
        ),
        base_row(),
        base_row(
            effect_id="sw_source_state",
            system_id="southwest_pacific_pairs",
            system_cluster="southwest_pacific_multi_archipelago_pairs",
        ),
    ]
    combined, summary = augment_external_documents(
        rows,
        ogasawara_document=ogasawara_document(),
        southwest_pacific_document=southwest_document(),
        ogasawara_source_path="oga.json",
        southwest_pacific_source_path="sw.json",
    )
    assert not any(row["system_id"] == "southwest_pacific_pairs" for row in combined)
    southwest = [
        row for row in combined if row["system_id"] == "southwest_pacific_flower_size"
    ]
    assert len(southwest) == 1
    assert southwest[0]["cross_system_model_eligible"] == "yes"
    assert summary["total_registry_rows"] == 3
    assert summary["empirical_numeric_rows"] == 3
    assert summary["numeric_rows_with_effect_uncertainty"] == 3
    assert summary["cross_system_model_eligible_rows"] == 2
    assert summary["cross_system_model_eligible_systems"] == [
        "southwest_pacific_ten_archipelagos",
        "wanshan_yongxing_paired_system",
    ]
    assert summary["effect_families_with_two_or_more_independent_systems"] == []
    assert summary["formal_cross_system_fit_ready"] is False
    assert all(row["causal_claim_allowed"] == "no" for row in combined)


def test_effect_document_must_match_target_system():
    document = ogasawara_document()
    document["effects"][0]["system_id"] = "wrong"
    try:
        augment_registry([], document, source_path="effects.json")
    except ValueError as error:
        assert "unexpected system" in str(error)
    else:
        raise AssertionError("unexpected system should fail")
