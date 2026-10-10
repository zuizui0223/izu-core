"""Feasibility-only pilot guards: never simulate reserved 16 pilot-history IDs."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_investment_commons_pilot_power import (
    STATUS,contract,initial_genotypes,config,visitors,
    expressed_genome,pilot_path,source_gradient_diagnostics,
    scenario_power,exact_cp_interval_arrays
)


def test_new_pilot_scope_and_single_selected_locus_source():
    d,h=contract()
    assert len(h)==64
    assert d["status"]=="ENGINEERING_FEASIBILITY_PILOT_NOT_CONFIRMATORY"
    assert d["pilot_rng"]["visitor_seeds"]==[9701201,9701216]
    assert d["expected_full_pilot_paths"]==384
    original,support=initial_genotypes(d)
    assert len(original.ids)==8
    assert np.var(original.alleles[:,1,:])>0
    assert np.all(original.alleles[:,0,:]==.2)
    assert np.all(original.alleles[:,2,:]==.35)
    assert 0<support["safe_phenotype_lower"]
    assert support["safe_phenotype_upper"]<1


def test_t0_native_centered_sham_exactly_same_genotypes_and_source_ledger():
    d,_=contract()
    initial,support=initial_genotypes(d)
    a=expressed_genome(initial,support["mean_investment"],"baseline_centered")
    assert a is initial
    z=visitors(d,9701291,"static_matched4")
    x=pilot_path(d,initial,z,9701291,"static_matched4",8,6.,"native")
    y=pilot_path(d,initial,z,9701291,"static_matched4",8,6.,"baseline_centered")
    assert x["initial_expected_viable_seeds"]==y["initial_expected_viable_seeds"]
    assert x["t1_genomic_state_sha256"]==y["t1_genomic_state_sha256"]
    assert x["occupied80"] in (0,1) and y["occupied80"] in (0,1)
    assert x["seed"]==y["seed"]==9701291


def test_investment_beta_group_gamma_externality_source_discrimination():
    d,_=contract()
    o=source_gradient_diagnostics(d)
    assert set(o)=={"8","48"}
    assert o["8"]["expected_source_criterion_beta_neg_gamma_pos_externality_pos"] is True
    assert o["8"]["finite_focal_beta"]<0
    assert o["8"]["collective_viable_seed_gamma"]>0
    assert o["8"]["other_mothers_viable_seed_derivative"]>0


def test_conservative_pair_interval_power_surface_has_explicit_null_scenarios():
    d,_=contract()
    s=scenario_power(d)
    assert len(s)>12
    assert any(not row["feasible"] for row in s)
    assert any(row.get("power_simulated_for_delta_above_5pp",0)>.8 for row in s)
    assert all(0<=r["power_simulated_for_delta_above_5pp"]<=1
               for r in s if r["feasible"])
    for n in (128,256):
        lower,upper=exact_cp_interval_arrays(n)
        assert lower[0]==0
        assert upper[n]==1
        # Exact simultaneous interval for identical paired outcomes narrows
        # with n: n=128 cannot establish ±5pp equivalence, n=256 can.
        if n==128:
            assert lower[0]-upper[0]<-.05
        else:
            assert lower[0]-upper[0]>-.05
        assert lower[n]-upper[0]>.05
    json.dumps(s,allow_nan=False)


def test_disallow_undeclared_pilot_history_and_unsafe_expression():
    d,_=contract()
    with pytest.raises(ValueError):
        visitors(d,61021001,"static_matched4")
    state,support=initial_genotypes(d)
    with pytest.raises(ValueError):
        expressed_genome(state,support["mean_investment"],"not_a_policy")
