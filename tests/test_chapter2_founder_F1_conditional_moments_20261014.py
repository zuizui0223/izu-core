"""Original source t0 exact conditional zygote moments: no sampled births."""
import inspect
import math
import numpy as np

from scripts.model3_island import reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, original_context, manipulate_homologs,
    matched_draw,
)
from scripts.audit_chapter2_original_founder_transplant_20261014 import (
    fixed48_projection,
)
from scripts.audit_chapter2_founder_F1_conditional_moments_20261014 import (
    conditional_f1_moments, technical_report,
)


def test_exact_first_offspring_marginal_moments_against_enumerated_meiosis():
    doc = original_fixture()
    state = source_state(doc, "main")
    changed = manipulate_homologs(state, block="main", overlap=6)
    _, sampled = matched_draw(state, changed.state, 2)
    c,vis = original_context(doc,"main",3)
    ledger = reproduction.reproduce(sampled, vis, c)
    x = conditional_f1_moments(sampled, ledger)
    assert x["eligible"]
    W = ledger.outcross.copy()
    np.fill_diagonal(W, np.diag(W)+ledger.self_viable)
    W /= W.sum()
    # Independent expectation by enumerating four ordered diploid gamete
    # copy pairs for every possible father/mother, independently per locus.
    for trait in range(3):
        vals, weights = [], []
        for father in range(2):
            for mother in range(2):
                for paternal_copy in range(2):
                    for maternal_copy in range(2):
                        vals.append((sampled.alleles[father,trait,paternal_copy]+
                                     sampled.alleles[mother,trait,maternal_copy])/2)
                        weights.append(W[father,mother]/4)
        mean = np.dot(weights,vals)
        variance = np.dot(weights,(np.array(vals)-mean)**2)
        assert abs(mean-x["expected_single_offspring_mean_M_I_A"][trait]) < 1e-13
        assert abs(variance-x["first_offspring_variance_M_I_A"][trait]) < 1e-13
        assert abs((x["segregation_contribution_M_I_A"][trait]+
                    x["parent_pair_contribution_M_I_A"][trait])-variance)<1e-13


def test_old_A_standing_heterozygosity_expected_F1_variance():
    doc=original_fixture()
    expected=0.0625**2/2
    for block in ("main","confirmation"):
        state=source_state(doc,block)
        for context in (0,3,4):
            c,v=original_context(doc,block,context)
            x=conditional_f1_moments(state,reproduction.reproduce(state,v,c))
            assert x["eligible"]
            assert x["original_A_symmetric_heterozygote_carriers"]==48
            assert x["source_A_phenotypic_variance"]==0
            assert x["expected_single_offspring_mean_M_I_A"][2]==.5
            assert abs(x["first_offspring_variance_M_I_A"][2]-expected)<1e-15
            assert abs(x["parent_pair_contribution_M_I_A"][2])<1e-15


def test_source_I_phenotype_held_but_mendelian_variation_is_controlled():
    doc=original_fixture()
    for block in ("main","confirmation"):
        original=source_state(doc,block)
        for n in (2,8,24,48):
            prior={}
            for m in (0,3,6,12):
                altered=manipulate_homologs(original,block=block,overlap=m)
                _,genotype=matched_draw(original,altered.state,n)
                c,v=original_context(doc,block,3)
                stats=conditional_f1_moments(
                    genotype,reproduction.reproduce(genotype,v,c))
                assert stats["eligible"]
                assert abs(stats["expected_single_offspring_mean_M_I_A"][2]-.5)<1e-15
                prior[m]=stats
            assert abs(prior[0]["first_offspring_variance_M_I_A"][2]-
                       prior[12]["first_offspring_variance_M_I_A"][2])<1e-15


def test_full_192_t0_moments_comparison_without_simulation():
    r=technical_report()
    assert r["initial_state_contrasts"]==192
    assert r["biological_histories_or_population_advance_calls"]==0
    assert len(r["rows"])==192
    assert all(row["edited_expected_f1_variance_A"]>=0 for row in r["rows"])
    assert all(row["edited_expected_f1_variance_I"]>=0 for row in r["rows"])
    assert all(row["edited_f1_A_variance_due_to_segregation"]>=0 for row in r["rows"])
    for block in ("main","confirmation"):
        for context in (0,3,4):
            refs=[x for x in r["rows"]
                  if x["founder_block"]==block
                  and x["ecological_context"]==context
                  and x["founder_donor_n"]==48]
            assert len(refs)==8
            assert all(abs(x["baseline_expected_f1_variance_A"]-0.001953125)<1e-15 for x in refs)


def test_source_never_calls_inherit_or_advance():
    from scripts import audit_chapter2_founder_F1_conditional_moments_20261014 as module
    code=inspect.getsource(module)
    assert "population.advance(" not in code
    assert "population.inherit(" not in code
    assert "model_history(" not in code
    assert "simulate(" not in code
