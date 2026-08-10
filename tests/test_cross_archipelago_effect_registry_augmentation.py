from scripts.augment_cross_archipelago_effect_registry import augment_registry


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


def test_effect_document_must_be_ogasawara():
    document = ogasawara_document()
    document["effects"][0]["system_id"] = "wrong"
    try:
        augment_registry([], document, source_path="effects.json")
    except ValueError as error:
        assert "unexpected system" in str(error)
    else:
        raise AssertionError("unexpected system should fail")
