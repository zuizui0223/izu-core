"""Source-only t20 placebo checks; NO exposure of 61022001..61022064."""
import json
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_chapter2_investment_mean_expression_clamp import (
    contract,config,genotype_founders,visitor_history,expression_mean_clamp,
    source_and_paired_paths,ledger_for,STATUS,SOURCE_SEEDS,
)


def test_source_lock_n0_equal_K_distinct_and_full_genetic_variation():
    d,digest=contract()
    assert len(digest)==64
    assert d["design"]["total_future_paths"]==1024
    assert len(SOURCE_SEEDS)==64
    assert all(s not in SOURCE_SEEDS for s in (990221,990222))
    for K in (8,48):
        c=config(d,K)
        assert c.capacity==K and c.years==80
        assert c.seed_arrival.supply==0
        assert c.mutation_rate==0 and c.survival==0
    initial=genotype_founders(d,.35)
    assert len(initial.ids)==8
    assert initial.alleles.shape==(8,3,2)
    assert np.var(initial.alleles[:,1,:])>0
    assert np.var(initial.alleles[:,2,:])>0


def test_mean_clamp_is_noop_at_same_target_and_preserves_all_variation():
    d,_=contract()
    state=genotype_founders(d,.65)
    target=float(state.alleles[:,1,:].mean())
    assert expression_mean_clamp(state,target) is state
    shifted=expression_mean_clamp(state,target+.04)
    assert shifted is not state
    assert np.array_equal(shifted.ids,state.ids)
    assert np.array_equal(shifted.allele_origin,state.allele_origin)
    assert np.array_equal(shifted.mutation_flags,state.mutation_flags)
    np.testing.assert_array_equal(shifted.alleles[:,0,:],state.alleles[:,0,:])
    np.testing.assert_array_equal(shifted.alleles[:,2,:],state.alleles[:,2,:])
    np.testing.assert_allclose(
        shifted.alleles[:,1,:].var(),state.alleles[:,1,:].var(),
        atol=1e-14,rtol=0,
    )
    np.testing.assert_array_equal(state.alleles,
                                  genotype_founders(d,.65).alleles)
    with pytest.raises(ValueError,match="exceeds"):
        expression_mean_clamp(state,.99)


def test_simulator_sham_same_mean_exact_reproduction_parity():
    d,_=contract()
    st=genotype_founders(d,.35)
    hist=visitor_history(d,990221)
    assert len(hist.visitors)==80
    assert not any(len(x.ids) for x in hist.seed_candidates)
    cfg=config(d,8)
    target=float(st.alleles[:,1,:].mean())
    for gate in ("baseline","half_self"):
        natural=ledger_for(
            st,hist.visitors[0],cfg,gate,
            "native_genotype_expression",None
        )
        clamped=ledger_for(
            st,hist.visitors[0],cfg,gate,
            "investment_population_mean_clamp",target
        )
        for field in natural.__dataclass_fields__:
            np.testing.assert_array_equal(
                getattr(natural,field),getattr(clamped,field)
            )


def test_pre20_genomes_and_year21_offspring_identical_across_modes():
    d,_=contract()
    hist=visitor_history(d,990222)
    for K in (8,48):
        for gate in ("baseline","half_self"):
            row=source_and_paired_paths(d,hist,990222,K,.65,gate)
            assert row["seed"]==990222
            assert row["pre20_occupied"] in (0,1)
            assert row["native"]["initial_post20_ledger_sha256"]==(
                row["clamp"]["initial_post20_ledger_sha256"])
            assert row["native"]["year21_genotype_state_sha256"]==(
                row["clamp"]["year21_genotype_state_sha256"])
            assert row["not_pure_genetic_evolution_freeze"] is True
            assert row["native"]["occupied80"] in (0,1)
            assert row["clamp"]["occupied80"] in (0,1)
            assert row["native"]["occupied80"]<=row["pre20_occupied"]
            assert row["clamp"]["occupied80"]<=row["pre20_occupied"]
            json.dumps(row,allow_nan=False)
