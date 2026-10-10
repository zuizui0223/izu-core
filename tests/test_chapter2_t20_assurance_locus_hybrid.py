"""Genome whole-locus transplant controls, no independent visitor seeds generated."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_t20_assurance_locus_hybrid import (
    contract,genotypes_by_module,_paired_contrast,ARMS,
)
from scripts.audit_chapter2_t20_joint_genome_transplant import (
    original_contract,initial_genotypes,transplant_diploid_source
)


def test_contract_discloses_post_outcome_locus_mosaic_scope():
    d,digest=contract()
    assert len(digest)==64
    assert d["hybrid_genotype_arms"]==list(ARMS)
    assert d["replay_source_pre20"]["n_both_eligible"]==50
    assert d["future"]["all_eligible_source_futures"]==400
    assert "counterfactual" in d["limitations"][0]


def test_full_diploid_alleles_and_ancestry_swapped_only_at_named_loci():
    original,_=original_contract()
    founder=initial_genotypes(original)
    neutral,_=transplant_diploid_source(founder,seed=990481,
                                       donor_label="neutral_pre20")
    selected,_=transplant_diploid_source(founder,seed=990481,
                                        donor_label="selected_pre20")
    # Ensure even source ancestry labels track the donor and no individual
    # genealogical identity in the recipient namespace collides.
    arms=genotypes_by_module(neutral,selected)
    assert set(arms)==set(ARMS)
    for k,v in arms.items():
        assert len(v.ids)==8
        assert np.array_equal(v.ids,np.arange(8))
        assert np.array_equal(v.birth_years,np.full(8,20))
        assert v.alleles.shape==(8,3,2)
        json.dumps(v.alleles.tolist())


def test_module_operator_equal_source_is_identity_for_every_relevant_array():
    original,_=original_contract()
    src=initial_genotypes(original)
    single,_=transplant_diploid_source(src,seed=990482,
                                       donor_label="selected_pre20")
    hybrids=genotypes_by_module(single,single)
    for state in hybrids.values():
        for name in ("alleles","allele_origin","mutation_flags",
                     "ids","birth_years"):
            np.testing.assert_array_equal(getattr(state,name),getattr(single,name))


def test_fails_closed_with_improper_bio_parent_sizes():
    original,_=original_contract()
    st=initial_genotypes(original)
    donor,_=transplant_diploid_source(st,seed=990483,
                                     donor_label="neutral_pre20")
    with pytest.raises(ValueError):
        genotypes_by_module(donor,st)


def test_exact_paired_contrast_does_not_manufacture_survivors():
    rows=[{"futures":{
        "neutral_all|K8":{"occupied80":int(i%3==0)},
        "selected_all|K8":{"occupied80":int(i%3!=0)},
    }} for i in range(50)]
    got=_paired_contrast(rows,8,"selected_all","neutral_all")
    assert got["n_conditional_source_histories"]==50
    assert got["paired_positive_only"]==33
    assert got["paired_negative_only"]==17
    assert got["delta"]==(33-17)/50
    assert got["post_outcome_secondary"]
