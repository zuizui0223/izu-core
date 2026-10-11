"""Pinned original 192 fresh-donor/future source receipt: no outcome re-generation."""
import json
from pathlib import Path
import numpy as np

SOURCE=Path("data/results/chapter2_assurance_independent_source_future_192_receipt_20261010.json")


def test_original_192_source_history_fresh_visitor_cohort_and_no_field_claim():
    d=json.loads(SOURCE.read_text())
    assert d["independent_model_source_visitor_rng_histories"]==192
    assert d["independent_model_future_visitor_rng_innovations"]==192
    assert d["old_outcome_exposed_source_history_ids_reused"]==0
    assert d["source_pre20_pair_eligible"]==168
    assert d["source_pre20_pair_ineligible"]==24
    assert d["genotype_draws_nested_per_eligible_source"]==2
    assert d["new_future_trajectories"]==168*2*4*2==2688
    assert d["independent_natural_island_systems"]==0


def test_primary_model_result_is_not_called_confirmatory():
    d=json.loads(SOURCE.read_text())
    x=d["outcomes"]["K8"]
    assert x["n_nested_genomes_per_arm"]==336
    assert x["occupied_counts"]["neutral_all"]==146
    assert x["occupied_counts"]["selected_assurance_only"]==211
    assert x["occupied_counts"]["selected_nonassurance_only"]==145
    assert x["occupied_counts"]["selected_all"]==222
    assert np.isclose(x["primary_assurance_only_delta"],(211-146)/336)
    assert x["primary_history_cluster_bootstrap_95"][0]>.05
    assert x["primary_hoeffding_95"][0]<0
    assert x["predeclared_strict_5pp_primary_verdict"]=="INCONCLUSIVE"


def test_all_genotype_module_total_moment_contrasts_consistent():
    d=json.loads(SOURCE.read_text())
    for k in ("K8","K48"):
        x=d["outcomes"][k]
        v=x["occupied_counts"]
        total=(v["selected_all"]-v["neutral_all"])/336
        assert np.isclose(x["full_source_genome_delta"],total)
        assert np.isclose(
            x["two_order_assurance_allocation"]+
            x["two_order_other_loci_allocation"],
            x["full_source_genome_delta"],rtol=0,atol=1e-12)
        assert x.get("predeclared_strict_5pp_primary_verdict",
                     x.get("secondary_strict_verdict"))=="INCONCLUSIVE"
    assert d["outcomes"]["K48"]["occupied_counts"]=={
        "neutral_all":284,"selected_assurance_only":314,
        "selected_nonassurance_only":290,"selected_all":317}
