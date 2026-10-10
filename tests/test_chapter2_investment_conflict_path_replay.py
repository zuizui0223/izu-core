"""Tests do NOT use any new source histories or call full 384 replay.

The production script separately verifies exact SHA of ALL 384 original
archived per-path outputs before any pathwise mechanism report can succeed.
"""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_investment_conflict_path_replay import (
    STATUS,ORIGINAL_384_PATH_SHA256,contract,actual_mixed_window,
    replay_path,investment_perturb
)
from scripts.audit_chapter2_investment_commons_pilot_power import (
    initial_genotypes,visitors,config,contract as original_contract,
)


def test_frozen_source_and_pilot_path_fingerprint():
    design,sha=contract()
    original,_=original_contract()
    assert len(sha)==64
    assert design["cohort"]["n_paths"]==384
    assert ORIGINAL_384_PATH_SHA256=="0f39b237ecfd115fff34de9dad8090d2a7fdf89f54af39a821016bc3a0a0d0a6"
    assert design["cohort"]["seeds_first"]==9701201
    assert original["pilot_rng"]["visitor_seeds"]==[9701201,9701216]


def test_actual_mixed_beta_and_group_gamma_are_independent_ledger_quantities():
    d,_=original_contract()
    initial,_=initial_genotypes(d)
    v=visitors(d,9701291,"static_matched4").visitors[0]
    cfg=config(d,8,8.)
    result=actual_mixed_window(initial,v,cfg)
    assert sum(result[k] for k in (
        "focal_beta_negative_count","focal_beta_positive_count",
        "focal_beta_unresolved_count"))==8
    assert result["gamma_collective_log_seed"]>0
    assert result["positive_nonneighbor_externality_focal_count"]<=8
    assert result["mixed_genotype_majority_conflict"] in (True,False)
    json.dumps(result,allow_nan=False)


def test_original_source_populations_unchanged_by_diagnostic_gradients():
    d,_=original_contract()
    initial,_=initial_genotypes(d)
    original=initial.alleles.copy()
    v=visitors(d,9701291,"static_matched4").visitors[0]
    _=actual_mixed_window(initial,v,config(d,8,8.))
    np.testing.assert_array_equal(initial.alleles,original)
    x=investment_perturb(initial,0,.005)
    np.testing.assert_array_equal(initial.alleles,original)
    assert x.alleles[0,1,0]!=original[0,1,0]
    singleton=type(initial)(
        alleles=initial.alleles[:1],
        allele_origin=initial.allele_origin[:1],
        mutation_flags=initial.mutation_flags[:1],
        ids=initial.ids[:1],birth_years=initial.birth_years[:1])
    with pytest.raises(ValueError):
        actual_mixed_window(singleton,v,config(d,8,8.))


def test_bounded_smoke_replay_keeps_pair_first_genotype_equal_and_extinction():
    d,_=original_contract()
    initial,_=initial_genotypes(d)
    h=visitors(d,9701291,"stochastic_matched4")
    native=replay_path(
        d,initial,h,9701291,"stochastic_matched4",8,8.,"native",diagnose=True)
    centered=replay_path(
        d,initial,h,9701291,"stochastic_matched4",8,8.,"baseline_centered",
        diagnose=False)
    assert (native["original_pilot_result"]["t1_genomic_state_sha256"]==
            centered["original_pilot_result"]["t1_genomic_state_sha256"])
    assert len(native["complete_native_or_centered_80_annual_states"])==80
    assert len(centered["complete_native_or_centered_80_annual_states"])==80
    assert native["mixed_genotype_assessed_years"]==native["source_conflict_window_years"]
    assert centered["mixed_genotype_assessed_years"]==0
    assert (native["actually_mixed_genotype_conflict_years"]
            <=native["mixed_genotype_assessed_years"])
    assert (native["original_pilot_result"]["occupied80"]
            <=native["original_pilot_result"]["occupied20"])
    json.dumps(native,allow_nan=False)
