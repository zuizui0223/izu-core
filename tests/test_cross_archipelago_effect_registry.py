import json
from pathlib import Path

from scripts.compile_cross_archipelago_effect_registry import compile_registry


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_izu_subsets_are_numeric_but_not_independent_cross_system_effects(tmp_path: Path):
    write_json(
        tmp_path,
        "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json",
        {
            "fixed_effect_subsets": {
                "all_eight_sites": {"fdq_coefficient": 1.8},
                "izu_five_islands": {"fdq_coefficient": 1.9},
                "post_oshima_four_islands": {"fdq_coefficient": 2.0},
            },
            "leave_one_site_sensitivity": {
                "izu_five_islands": {"fdq_coefficient_range": [1.4, 2.2]}
            },
        },
    )
    rows, summary = compile_registry(tmp_path)
    izu = [row for row in rows if row["system_id"] == "izu_hiraiwa_ushimaru"]
    assert len(izu) == 3
    assert {row["system_cluster"] for row in izu} == {"izu_2024_network"}
    assert all(row["cross_system_model_eligible"] == "no" for row in izu)
    assert summary["empirical_numeric_rows"] == 3
    assert summary["cross_system_model_eligible_systems"] == []
    assert summary["formal_cross_system_fit_ready"] is False


def test_external_island_pairs_remain_nested_descriptive_rows(tmp_path: Path):
    write_json(
        tmp_path,
        "data/results/galapagos/network_analysis/analysis.json",
        {
            "status": "source_resolved_multi_island_network_analysis",
            "pair_metrics": [
                {
                    "left_island": "A",
                    "right_island": "B",
                    "mean_shared_plant_pollinator_turnover": 0.6,
                },
                {
                    "left_island": "A",
                    "right_island": "C",
                    "mean_shared_plant_pollinator_turnover": 0.7,
                },
            ],
        },
    )
    rows, summary = compile_registry(tmp_path)
    galapagos = [row for row in rows if row["system_id"] == "galapagos_networks"]
    assert len(galapagos) == 2
    assert {row["system_cluster"] for row in galapagos} == {
        "galapagos_oceanic_archipelago"
    }
    assert all(row["row_role"] == "descriptive_within_system" for row in galapagos)
    assert all(row["uncertainty_type"] == "none" for row in galapagos)
    assert all(row["cross_system_model_eligible"] == "no" for row in galapagos)
    assert summary["formal_cross_system_fit_ready"] is False


def test_blocked_sources_are_retained_instead_of_becoming_zeros(tmp_path: Path):
    write_json(
        tmp_path,
        "data/results/ogasawara/context_analysis/analysis_blocked.json",
        {
            "status": "blocked_schema_not_uniquely_resolved",
            "next_gate": "verify source table",
        },
    )
    rows, _ = compile_registry(tmp_path)
    ogasawara = [row for row in rows if row["system_id"] == "ogasawara_2026"]
    assert len(ogasawara) == 1
    assert ogasawara[0]["admission_status"] == "blocked_schema_not_uniquely_resolved"
    assert ogasawara[0]["estimate"] == ""
    assert ogasawara[0]["cross_system_model_eligible"] == "no"


def test_one_external_effect_document_opens_rows_but_not_meta_analysis(tmp_path: Path):
    write_json(
        tmp_path,
        "data/results/wanshan_yongxing/effect_rows.json",
        {
            "status": "effect_rows_ready_single_external_system",
            "effects": [
                {
                    "effect_id": "wanshan_visitation_lrr",
                    "system_id": "wanshan_yongxing",
                    "system_cluster": "wanshan_yongxing_paired_system",
                    "evidence_family": "matched_shared_plant_visitation_log_response_ratio",
                    "response": "visitation_log_response_ratio",
                    "predictor_or_contrast": "oceanic versus continental island",
                    "estimate": -2.5,
                    "uncertainty_type": "exact_nonparametric_bootstrap_percentile_interval_for_median",
                    "uncertainty_value": [-3.3, -2.1],
                    "unit": "ln response ratio",
                    "independent_unit": "seven matched plant species within one island pair",
                    "row_role": "external_effect",
                    "admission_status": "empirical_numeric_effect_with_plant_level_uncertainty_single_system",
                    "cross_system_model_eligible": True,
                    "causal_claim_allowed": False,
                    "notes": "Plant bootstrap is not geographic replication.",
                }
            ],
        },
    )
    rows, summary = compile_registry(tmp_path)
    wanshan = [row for row in rows if row["system_id"] == "wanshan_yongxing"]
    assert len(wanshan) == 1
    assert wanshan[0]["cross_system_model_eligible"] == "yes"
    assert wanshan[0]["uncertainty_value"] == "[-3.3,-2.1]"
    assert summary["cross_system_model_eligible_rows"] == 1
    assert summary["cross_system_model_eligible_systems"] == [
        "wanshan_yongxing_paired_system"
    ]
    assert summary["effect_families_with_two_or_more_independent_systems"] == []
    assert summary["formal_cross_system_fit_ready"] is False


def test_two_external_systems_with_noncommensurate_effect_families_keep_fit_closed(tmp_path: Path):
    write_json(
        tmp_path,
        "data/results/wanshan_yongxing/effect_rows.json",
        {
            "effects": [
                {
                    "effect_id": "wanshan_visitation_lrr",
                    "system_id": "wanshan_yongxing",
                    "system_cluster": "wanshan_yongxing_paired_system",
                    "evidence_family": "matched_shared_plant_visitation_log_response_ratio",
                    "response": "visitation_log_response_ratio",
                    "estimate": -2.5,
                    "uncertainty_type": "bootstrap_interval",
                    "uncertainty_value": [-3.3, -2.1],
                    "cross_system_model_eligible": True,
                }
            ]
        },
    )
    write_json(
        tmp_path,
        "data/results/southwest_pacific_pairs/effect_rows.json",
        {
            "effects": [
                {
                    "effect_id": "swp_flower_slope",
                    "system_id": "southwest_pacific_flower_size",
                    "system_cluster": "southwest_pacific_ten_archipelagos",
                    "evidence_family": "animal_pollinated_island_mainland_flower_size_starting_value_slope",
                    "response": "flower_size_log10_response_ratio",
                    "estimate": -0.15,
                    "uncertainty_type": "island_cluster_bootstrap_percentile_interval",
                    "uncertainty_value": [-0.30, -0.07],
                    "cross_system_model_eligible": True,
                }
            ]
        },
    )
    _, summary = compile_registry(tmp_path)
    assert summary["cross_system_model_eligible_rows"] == 2
    assert summary["cross_system_model_eligible_systems"] == [
        "southwest_pacific_ten_archipelagos",
        "wanshan_yongxing_paired_system",
    ]
    assert summary["effect_families_with_two_or_more_independent_systems"] == []
    assert summary["formal_cross_system_fit_ready"] is False


def test_current_repository_has_two_external_systems_but_keeps_formal_fit_closed():
    root = Path(__file__).resolve().parents[1]
    rows, summary = compile_registry(root)
    assert rows
    assert summary["formal_cross_system_fit_ready"] is False
    assert summary["total_registry_rows"] == 17
    assert summary["empirical_numeric_rows"] == 16
    assert summary["numeric_rows_with_effect_uncertainty"] == 9
    assert summary["cross_system_model_eligible_rows"] == 6
    assert summary["external_model_eligible_rows"] == 6
    assert summary["cross_system_model_eligible_systems"] == [
        "southwest_pacific_ten_archipelagos",
        "wanshan_yongxing_paired_system",
    ]
    assert summary["effect_families_with_two_or_more_independent_systems"] == []
    assert all(row["causal_claim_allowed"] == "no" for row in rows)
