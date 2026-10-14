"""No locked cohort outcomes accessed: new donor/future source tests with 9909xx."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_assurance_independent_source_future_192 import (
    contract,new_future_seed_from_source,new_ecology_after_t20,
    draw_genomes,history_cluster_intervals,
    TEST_ONLY_SOURCE_SEED,TEST_ONLY_FUTURE_SEED,SOURCE_SEEDS,FUTURE_SEEDS
)
from scripts.audit_chapter2_t20_joint_genome_transplant import (
    original_contract,run_future,visitor_history
)
from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import initial_genotypes
from scripts.audit_chapter2_t20_assurance_locus_hybrid import genotypes_by_module


def test_new_environment_precommitted_192_source_and_future_seeds():
    d,digest=contract()
    assert len(digest)==64
    assert len(SOURCE_SEEDS)==len(FUTURE_SEEDS)==192
    assert SOURCE_SEEDS.start==61028001 and SOURCE_SEEDS.stop==61028193
    assert FUTURE_SEEDS.start==61029001 and FUTURE_SEEDS.stop==61029193
    assert d["history_design"]["whole_diploid_resamples_per_eligible_source"]==2
    assert d["hypotheses"]["primary"].startswith("At recipient K8")
    assert new_future_seed_from_source(61028001)==61029001
    assert new_future_seed_from_source(61028192)==61029192
    with pytest.raises(ValueError):
        new_future_seed_from_source(61024001)


def test_new_post20_ecology_inherits_old_visitor_state_only():
    source,_=original_contract()
    past=visitor_history(source,TEST_ONLY_SOURCE_SEED)
    future=new_ecology_after_t20(source,past,TEST_ONLY_FUTURE_SEED)
    assert len(future.visitors)==len(future.seed_candidates)==80
    for i in range(20):
        assert future.visitors[i] is past.visitors[i]
    np.testing.assert_array_equal(future.visitors[20].ids,past.visitors[20].ids)
    np.testing.assert_array_equal(future.visitors[20].optima,past.visitors[20].optima)
    assert all(len(x.ids)==0 for x in future.seed_candidates)
    with pytest.raises(ValueError):
        new_ecology_after_t20(source,past,61024001)


def test_genotypes_resampled_as_whole_individuals_and_sham_reproduces():
    source,_=original_contract()
    founders=initial_genotypes(source)
    for arm in ("selected_pre20","neutral_pre20"):
        for draw in (0,1):
            genome,indices=draw_genomes(founders,TEST_ONLY_SOURCE_SEED,arm,draw)
            assert len(genome.ids)==len(indices)==8
            np.testing.assert_array_equal(genome.alleles,founders.alleles[indices])
            np.testing.assert_array_equal(
                genome.allele_origin,founders.allele_origin[indices])
            np.testing.assert_array_equal(
                genome.mutation_flags,founders.mutation_flags[indices])
    with pytest.raises(ValueError):
        draw_genomes(founders,TEST_ONLY_SOURCE_SEED,"neutral_pre20",2)


def test_full_locus_mosaic_does_not_require_early_peeking_at_registered_seeds():
    source,_=original_contract()
    parent=initial_genotypes(source)
    n,_=draw_genomes(parent,TEST_ONLY_SOURCE_SEED,"neutral_pre20",0)
    s,_=draw_genomes(parent,TEST_ONLY_SOURCE_SEED,"selected_pre20",0)
    z=genotypes_by_module(n,s)
    assert len(z)==4
    past=visitor_history(source,TEST_ONLY_SOURCE_SEED)
    future=new_ecology_after_t20(source,past,TEST_ONLY_FUTURE_SEED)
    a=run_future(source,future,TEST_ONLY_FUTURE_SEED,z["neutral_all"],8,"selected_source")
    b=run_future(source,future,TEST_ONLY_FUTURE_SEED,z["neutral_all"],8,"selected_source")
    assert a==b


def test_cluster_vs_genotype_draw_uncertainty_fails_closed_at_all_equal():
    z=history_cluster_intervals(np.zeros(150),bootstrap_seed=61029999)
    assert z["classification"]=="inconclusive"
    assert z["hoeffding_95"][0]<-.05 and z["hoeffding_95"][1]>.05
    good=history_cluster_intervals(np.full(150,.3),bootstrap_seed=61029999)
    assert good["classification"]=="resolved_positive"
    assert good["hoeffding_95"][0]>.05
    short=history_cluster_intervals(np.zeros(1),bootstrap_seed=61029999)
    assert short["classification"]=="not_estimable_insufficient_eligible_sources"
    json.dumps(good,allow_nan=False)
