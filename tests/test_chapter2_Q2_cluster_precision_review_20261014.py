"""Pure source-cluster precision and future six-class schema review, NO Model3 runs."""
from copy import deepcopy
from hashlib import sha256
from math import isclose

import pytest

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    ARMS, CLASSES, DESIGN, OLD_CONTEXTS, POSSIBLE_ALLOCATIONS,
    independent_source_hoeffding_required,
    independent_source_hoeffding_radius,
    paired_source_level_class_contrasts,
    read_review_design, verify_review_design,
)


def test_all_candidate_source_history_budgets_are_equally_costly():
    r=read_review_design()
    assert r["status"]=="REVIEW_ONLY_BOUNDED_SOURCE_CLUSTER_PRECISION_NOT_POWER"
    assert r["biological_simulations_executed"]==0
    assert r["approved_stochastic_history_seeds"]==0
    assert len(r["candidate_equal_compute_allocations"])==5
    assert {x["technical_only_cases_if_executed"]
            for x in r["candidate_equal_compute_allocations"]}=={1536}
    assert all(x["conditional_future_update_calls_if_authorized"]==
               1536*200 for x in r["candidate_equal_compute_allocations"])
    assert [x["source_clusters_for_uncertainty"]
            for x in r["candidate_equal_compute_allocations"]] == [16,32,64,128,256]
    assert r["not_a_power_analysis"].startswith("Hoeffding")


def test_conservative_familywise_Hoeffding_bound_is_source_level():
    r=read_review_design()
    target={row["target_halfwidth"]:row for row in
            r["conservative_independent_source_precision_targets"]}
    assert target[0.2]["n_independent_sources_for_all_18_six_class_probability_differences"]==329
    assert target[0.2]["n_independent_sources_for_three_secondary_D_differences"]==958
    assert target[0.1]["n_independent_sources_for_all_18_six_class_probability_differences"]==1316
    assert target[0.3]["n_independent_sources_for_all_18_six_class_probability_differences"]==147
    # Four independent source pools, not four extra within-source futures,
    # halve worst-case cluster uncertainty at equal cluster-level variance.
    a=independent_source_hoeffding_radius(16,18,1.)
    b=independent_source_hoeffding_radius(64,18,1.)
    assert isclose(a/b,2.0,rel_tol=0,abs_tol=1e-13)
    assert independent_source_hoeffding_required(.2,18,1.)==329


def test_fail_closed_authorization_and_effect_definition():
    import json
    d=json.loads(DESIGN.read_text())
    bad=deepcopy(d)
    bad["experimental_author_approval"]=True
    with pytest.raises(ValueError,match="no-execution"):
        verify_review_design(bad)
    bad=deepcopy(d)
    bad["biological_histories_generated"]=1
    with pytest.raises(ValueError,match="no-execution"):
        verify_review_design(bad)
    bad=deepcopy(d)
    bad["sustained_occupied_censuses"]=19
    with pytest.raises(ValueError,match="no-execution"):
        verify_review_design(bad)
    bad=deepcopy(d)
    bad["original_six_classes"][0]="made_up"
    with pytest.raises(ValueError,match="no-execution"):
        verify_review_design(bad)
    bad=deepcopy(d)
    bad["source_distribution_approved"]=True
    with pytest.raises(ValueError,match="no-execution"):
        verify_review_design(bad)
    for key,not_allowed in (
        ("original_model3_mutation_traits",[True,True,True]),
        ("original_model3_biology_sha","some_unreviewed_new_model_sha"),
        ("independent_scientific_review_complete",True),
        ("actual_launch_case_budget",1536),
        ("source_pool_counts_are_options_not_approved",False),
        ("original_archival_raw_genomes_and_independent_readback","SKIP"),
    ):
        bad=deepcopy(d)
        bad[key]=not_allowed
        with pytest.raises(ValueError,match="no-execution"):
            verify_review_design(bad)


def toy_sixclass_rows():
    """Invented categorical test data; NEVER biological Model3 outcomes."""
    rows=[]
    for source in ("S0","S1"):
        for history in ("h0","h1"):
            for context in OLD_CONTEXTS:
                for arm in ARMS:
                    if source=="S0" and context==0:
                        if history=="h0":
                            category="neither" if arm==0 else "assurance_first"
                        else:
                            category="investment_first" if arm==0 else "assurance_first"
                    elif source=="S1" and context==3:
                        category="investment_only" if arm==0 else "near_simultaneous"
                    else:
                        category="assurance_only" if arm==0 else "neither"
                    rows.append({
                        "source_id":source,
                        "original_source_genome_sha256":
                            sha256(("TOY-SOURCE-"+source).encode()).hexdigest(),
                        "history_id":history,
                        "future_master_identity":f"TOY-NON-BIOLOGY-{source}-{history}",
                        "context":context,
                        "m":arm,
                        "category":category,
                        "extinct_by_horizon":category=="neither",
                    })
    return rows


def test_toy_paired_classification_keeps_six_class_denominators_and_clusters():
    r=paired_source_level_class_contrasts(toy_sixclass_rows())
    assert r["status"]=="CATEGORICAL_PAIRED_SOURCE_CLUSTER_SCHEMA_ONLY"
    assert r["already_given_rows"]==24
    assert r["independent_source_clusters"]==2
    assert r["paired_histories_per_source"]==2
    assert r["source_by_context_contrasts"]==6
    assert r["distinct_source_genome_hashes"]==2
    assert r["hash_validation_is_not_independence_proof"] is True
    assert r["no_source_genotypes_or_futures_generated"] is True
    s0=next(x for x in r["source_records"]
            if x["source_id"]=="S0" and x["context"]==0)
    v=s0["six_class_probability_differences_m12_minus_m0"]
    assert v["assurance_first"]==1.0
    assert v["investment_first"]==-0.5
    assert v["neither"]==-0.5
    assert sum(v.values())==0
    assert s0["secondary_order_score_D_difference"]==1.5
    assert set(v)==set(CLASSES)


@pytest.mark.parametrize("mode",[
    "missing", "duplicate", "unknown_class", "unpaired_rng",
    "seed_reuse_across_sources", "unbalanced_future_history_counts",
    "same_genome_different_sources", "inconsistent_genome_in_arm",
    "invalid_source_genome_hash",
])
def test_incomplete_or_pseudoreplicated_future_design_is_rejected(mode):
    rows=toy_sixclass_rows()
    if mode=="missing":
        rows.pop()
    elif mode=="duplicate":
        rows.append(deepcopy(rows[0]))
    elif mode=="unknown_class":
        rows[0]["category"]="not_one_of_six"
    elif mode=="unpaired_rng":
        rows[0]["future_master_identity"]="an_unpaired_rng"
    elif mode=="seed_reuse_across_sources":
        for row in rows:
            if row["source_id"]=="S1" and row["history_id"]=="h0":
                row["future_master_identity"]="TOY-NON-BIOLOGY-S0-h0"
    elif mode=="same_genome_different_sources":
        for row in rows:
            if row["source_id"]=="S1":
                row["original_source_genome_sha256"]=sha256(
                    b"TOY-SOURCE-S0").hexdigest()
    elif mode=="inconsistent_genome_in_arm":
        rows[0]["original_source_genome_sha256"]=sha256(
            b"NEW_UNVERIFIED_SOURCE").hexdigest()
    elif mode=="invalid_source_genome_hash":
        rows[0]["original_source_genome_sha256"]="not_sha256"
    elif mode=="unbalanced_future_history_counts":
        rows=[r for r in rows if not
              (r["source_id"]=="S1" and r["history_id"]=="h1")]
    with pytest.raises(ValueError):
        paired_source_level_class_contrasts(rows)


@pytest.mark.parametrize("bad",[
    (0,18,1),(-.2,18,1),(.2,0,1),(.2,18,0),
])
def test_invalid_precision_bounds_rejected(bad):
    with pytest.raises(ValueError):
        independent_source_hoeffding_required(*bad)
