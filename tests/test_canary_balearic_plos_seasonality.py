import csv
import importlib.util
import json
from pathlib import Path

import pytest

from scripts.compile_cross_archipelago_effect_registry import compile_registry


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "analyze_canary_balearic_plos_seasonality.py"
SPEC = importlib.util.spec_from_file_location(
    "canary_balearic_plos_seasonality", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def source_row(
    *,
    domain: str,
    specificity: str,
    zone: str,
    species: str,
    month: int,
    richness: float,
    rank: float | None = 1.0,
    evenness: float | None = 0.5,
):
    return {
        "resolved_domain": domain,
        "specificity": specificity,
        "zone": zone,
        "species_code": species,
        "month_index": month,
        "partner_functional_richness": richness,
        "partner_rank_abundance": rank,
        "partner_abundance_evenness": evenness,
    }


def test_species_repeated_across_communities_is_averaged_before_uncertainty():
    rows = [
        source_row(
            domain="plant",
            specificity="Generalized",
            zone="SB",
            species="abc.de",
            month=1,
            richness=1,
        ),
        source_row(
            domain="plant",
            specificity="Generalized",
            zone="SB",
            species="abc.de",
            month=4,
            richness=3,
        ),
        source_row(
            domain="plant",
            specificity="Generalized",
            zone="CM",
            species="abc.de",
            month=1,
            richness=2,
        ),
        source_row(
            domain="plant",
            specificity="Generalized",
            zone="CM",
            species="abc.de",
            month=4,
            richness=6,
        ),
    ]
    community = MODULE.first_last_community_deltas(rows)
    species = MODULE.aggregate_species_deltas(community)
    target = [
        row
        for row in species
        if row["metric"] == "partner_functional_richness"
    ]
    assert len(target) == 1
    assert target[0]["n_communities"] == 2
    assert target[0]["delta"] == pytest.approx(3.0)

    profiles, _ = MODULE.build_profiles(rows, bootstrap_repetitions=200)
    profile = next(
        row
        for row in profiles
        if row["metric"] == "partner_functional_richness"
    )
    assert profile["n_species"] == 1
    assert profile["n_species_community_units"] == 2
    assert profile["median_first_last_delta"] == pytest.approx(3.0)
    assert profile["cross_system_model_eligible"] == "no"


def test_sign_test_and_bh_adjustment_are_exact_and_monotone():
    assert MODULE.exact_two_sided_sign_test(7, 0) == pytest.approx(0.015625)
    adjusted = MODULE.benjamini_hochberg([0.01, 0.04, 0.03, None])
    assert adjusted[0] == pytest.approx(0.03)
    assert adjusted[1] == pytest.approx(0.04)
    assert adjusted[2] == pytest.approx(0.04)
    assert adjusted[3] is None


def test_bootstrap_interval_is_deterministic_and_contains_single_value():
    first = MODULE.bootstrap_median_interval(
        [2.5], repetitions=200, seed=123
    )
    second = MODULE.bootstrap_median_interval(
        [2.5], repetitions=200, seed=123
    )
    assert first == second == pytest.approx((2.5, 2.5))


def test_current_checked_source_has_no_multiplicity_robust_common_direction():
    result_dir = ROOT / "data/results/canary_balearic"
    input_path = result_dir / "plos_derived_partner_traits.csv"
    source_state_path = result_dir / "plos_same_community_source.json"
    checked_summary_path = (
        result_dir / "plos_selected_species_seasonality_summary.json"
    )
    checked_profiles_path = (
        result_dir / "plos_selected_species_seasonality.csv"
    )

    rows = MODULE.load_rows(input_path)
    profiles, summary = MODULE.build_profiles(
        rows, bootstrap_repetitions=300
    )
    source_state = json.loads(source_state_path.read_text(encoding="utf-8"))
    checked_summary = json.loads(
        checked_summary_path.read_text(encoding="utf-8")
    )
    with checked_profiles_path.open(encoding="utf-8", newline="") as handle:
        checked_profiles = list(csv.DictReader(handle))

    assert summary["n_input_rows"] == 457
    assert summary["n_profile_rows"] == 24
    assert summary["n_nominal_sign_tests_below_0_05"] == 3
    assert summary["n_bh_q_values_below_0_05"] == 0
    assert 0.30 < summary["minimum_bh_q_value"] < 0.31
    assert summary["effect_registry_eligible"] is False
    assert source_state["effect_registry_eligible"] is False
    assert source_state["full_network_source_admitted"] is False
    assert all(
        profile["cross_system_model_eligible"] == "no"
        and profile["causal_claim_allowed"] == "no"
        for profile in profiles
    )

    assert checked_summary["n_input_rows"] == summary["n_input_rows"]
    assert checked_summary["n_profile_rows"] == summary["n_profile_rows"]
    assert (
        checked_summary["n_nominal_sign_tests_below_0_05"]
        == summary["n_nominal_sign_tests_below_0_05"]
    )
    assert (
        checked_summary["n_bh_q_values_below_0_05"]
        == summary["n_bh_q_values_below_0_05"]
    )
    assert checked_summary["minimum_bh_q_value"] == pytest.approx(
        summary["minimum_bh_q_value"]
    )
    assert checked_summary["effect_registry_eligible"] is False
    assert len(checked_profiles) == 24
    assert all(
        row["cross_system_model_eligible"] == "no"
        and row["causal_claim_allowed"] == "no"
        for row in checked_profiles
    )

    registry_rows, registry_summary = compile_registry(ROOT)
    assert registry_summary["formal_cross_system_fit_ready"] is False
    assert not any(
        "canary_balearic" in row["source_path"]
        or row["system_id"].startswith("canary_balearic")
        for row in registry_rows
    )
