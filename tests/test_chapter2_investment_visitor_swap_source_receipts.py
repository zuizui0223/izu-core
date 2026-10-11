"""Immutably check prior original-pilot matched-visitors source receipts.

Does NOT resimulate ecological histories or interpret correlated annual
states as independent populations.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPLAY=ROOT/"data/results/chapter2_investment_conflict_exact_path_replay_receipt_20261010.json"
SWAP=ROOT/"data/results/chapter2_investment_same_genotype_visitor_swap_receipt_20261010.json"


def test_original_384_paths_exact_sha_and_population_years():
    a=json.loads(REPLAY.read_text())
    assert a["original_full_path_exact_sha_verified"] is True
    assert a["n_original_full_replayed_trajectory_paths"]==384
    assert a["prior_all_384_pilot_path_canonical_sha256"]=="0f39b237ecfd115fff34de9dad8090d2a7fdf89f54af39a821016bc3a0a0d0a6"
    fixed=a["totals_by_visitor_regime"]["static_matched4"]
    dynamic=a["totals_by_visitor_regime"]["stochastic_matched4"]
    assert fixed["N6_9_years"]==1564 and fixed["majority_negative_beta_positive_gamma_years"]==1562
    assert dynamic["N6_9_years"]==1533 and dynamic["majority_negative_beta_positive_gamma_years"]==696


def test_same_genotype_and_N_fixed_richness_four_changes_conflict():
    a=json.loads(SWAP.read_text())
    assert a["source_96_path_parity_verified"] is True
    assert a["source_original_96_pilot_path_sha256"]=="94c45f63d6d2f34b50357aaf4bd55ed89a1a2094559b32b45dbae2e585d73db7"
    x=a["cross_classification"]
    assert x=={
        "both_conflict":696,
        "actual_only_conflict":0,
        "fixed4_only_conflict":835,
        "neither_conflict":2}
    assert sum(x.values())==a["annual_pre_reproduction_census_N6_to9_states"]==1533
    richness4=next(row for row in a["by_original_current_visitor_type_count"]
                   if row["n_visitors"]==4)
    assert richness4["n_years"]==505
    assert richness4["actual_conflict"]==329
    assert richness4["fixed4_counterfactual_conflict"]==505
    assert richness4["fixed4_counterfactual_conflict"]-richness4["actual_conflict"]==176
    assert a["original_exposed_visitor_rng_history_count"]==16
