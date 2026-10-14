"""Native-shaped synthetic genotype foundation: static checks, no evolution."""
from __future__ import annotations

import ast
from pathlib import Path
import numpy as np
import pytest

from scripts.audit_chapter2_native_founder_source_20261014 import (
    PINNED_MODULE_BLOBS, construct_virtual_source, design_gate,
    native_gate, ordered_ids, static_config, static_return_parity,
    static_visitor_state, subset_founders, synthetic_reference, technical_receipt,
)


def test_source_pins_are_the_original_model3_files():
    assert PINNED_MODULE_BLOBS == {
        'types.py': '0bc427b3261e7baf1651648ee879b368f9bf935b',
        'reproduction.py': '95314698a3296b6f13b8c053c36f2df0b7b744ca',
    }
    native_gate()


def test_virtual_source_shapes_pairwise_phenotypes_and_ancestry():
    base = synthetic_reference()
    original_means = base.alleles.mean(axis=2)
    assert original_means.shape == (48, 3)
    assert np.ptp(original_means[:, 0]) > 0
    assert np.ptp(original_means[:, 1]) > 0
    assert np.all(original_means[:, 2] == 0.5)
    A_fixed = None
    for m in (0, 3, 6, 12):
        virtual = construct_virtual_source(base, co_carriers=m, source_seed=991)
        state = virtual.state
        assert state.alleles.shape == (48, 3, 2)
        assert np.array_equal(state.ids, base.ids)
        assert np.array_equal(state.birth_years, base.birth_years)
        assert np.array_equal(state.allele_origin, base.allele_origin)
        assert np.array_equal(state.mutation_flags, base.mutation_flags)
        assert np.array_equal(state.alleles[:, 0, :], base.alleles[:, 0, :])
        assert np.array_equal(state.alleles.mean(axis=2), original_means)
        A = set(virtual.A_ids)
        I = set(virtual.I_ids)
        assert len(A) == len(I) == 12 and len(A & I) == m
        if A_fixed is None:
            A_fixed = A
        else:
            assert A_fixed == A
        for trait, carriers in ((2, A), (1, I)):
            observed = set(np.flatnonzero(state.alleles[:, trait, 0] !=
                                          state.alleles[:, trait, 1]).tolist())
            assert observed == carriers


def test_same_founders_across_overlap_and_ledger_parity():
    base = synthetic_reference()
    config = static_config()
    v0 = static_visitor_state(())
    v1 = static_visitor_state((.3, .3, .7, .7))
    for n in (2, 8, 24, 48):
        prior = subset_founders(base, n, draw_seed=199)
        for m in (0, 3, 6, 12):
            virtual = construct_virtual_source(base, co_carriers=m, source_seed=101)
            after = subset_founders(virtual.state, n, draw_seed=199)
            assert np.array_equal(after.ids, prior.ids)
            assert np.array_equal(after.alleles.mean(axis=2),
                                  prior.alleles.mean(axis=2))
            for visitor in (v0, v1):
                digest = static_return_parity(prior, after, visitor, config)
                assert len(digest) == 64


def test_seed_determinism_and_no_replacement():
    ids=np.arange(48)
    assert np.array_equal(ordered_ids(ids, 7, 'unit'),
                          ordered_ids(ids, 7, 'unit'))
    assert not np.array_equal(ordered_ids(ids, 7, 'unit'),
                              ordered_ids(ids, 8, 'unit'))
    base=synthetic_reference()
    for n in (2, 8, 24, 48):
        draw=subset_founders(base,n,draw_seed=3344)
        assert len(draw.ids)==len(set(draw.ids))==n
        assert set(draw.ids).issubset(set(base.ids))
        for f in ('alleles','allele_origin','mutation_flags','birth_years'):
            assert np.array_equal(getattr(draw,f),getattr(base,f)[draw.ids])


def test_technical_receipt_has_no_biology_or_new_histories():
    r=technical_receipt()
    assert r['virtual_mainland_sources']==4
    assert r['paired_founder_subsets']==16
    assert r['static_return_parity_checks']==32
    assert r['new_genetic_or_demographic_histories']==0
    assert r['offspring_or_future_update_calls']==0
    for n in (2,8,24,48):
        rows=[x for x in r['rows'] if x['n_founders']==n]
        assert len(rows)==4
        assert all(row['selected_ids']==rows[0]['selected_ids'] for row in rows)
        assert all(row['static_ledger_sha256_by_visitor']==
                   rows[0]['static_ledger_sha256_by_visitor'] for row in rows)


def test_original_genotypes_cannot_be_relabelled_as_synthetic_source():
    b=synthetic_reference()
    alleles=b.alleles.copy()
    alleles[:,2,:]=(.4375,.5625)
    from scripts.model3_island.types import PlantState
    impostor=PlantState(alleles=alleles,allele_origin=b.allele_origin,
                        mutation_flags=b.mutation_flags,ids=b.ids,birth_years=b.birth_years)
    with pytest.raises(ValueError,match='symmetric homozygotes'):
        construct_virtual_source(impostor,co_carriers=3,source_seed=1)
    broken_origins=b.allele_origin.copy()
    broken_origins[0,2,0]+=1
    forged=PlantState(alleles=b.alleles,allele_origin=broken_origins,
                      mutation_flags=b.mutation_flags,ids=b.ids,birth_years=b.birth_years)
    with pytest.raises(ValueError,match='ancestry'):
        construct_virtual_source(forged,co_carriers=3,source_seed=1)


@pytest.mark.parametrize('bad_m',(-1,13,True,3.0))
def test_invalid_overlap_stops(bad_m):
    with pytest.raises(ValueError,match='overlap'):
        construct_virtual_source(synthetic_reference(),co_carriers=bad_m,source_seed=10)


@pytest.mark.parametrize('bad_seed',(-1,True,1.5,2**64))
def test_unregistered_seed_fails(bad_seed):
    with pytest.raises(ValueError,match='seed'):
        construct_virtual_source(synthetic_reference(),co_carriers=3,source_seed=bad_seed)


def test_invalid_founder_count_and_individual_phenotype_rejected():
    base=synthetic_reference()
    with pytest.raises(ValueError,match='founder-count'):
        subset_founders(base,7,draw_seed=4)
    variant=construct_virtual_source(base,co_carriers=3,source_seed=10).state
    rows=variant.alleles.copy()
    rows[0,1,:]=[0.2,0.2]
    from scripts.model3_island.types import PlantState
    altered=PlantState(alleles=rows,allele_origin=variant.allele_origin,
                       mutation_flags=variant.mutation_flags,
                       ids=variant.ids,birth_years=variant.birth_years)
    with pytest.raises(ValueError,match='phenotype mismatch'):
        static_return_parity(base,altered,static_visitor_state((.5,)*4),static_config())


def test_no_birth_or_trajectory_code_is_imported_or_called_here():
    path=Path(__file__).resolve().parents[1] / 'scripts/audit_chapter2_native_founder_source_20261014.py'
    tree=ast.parse(path.read_text(encoding='utf-8'))
    calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call)
           and isinstance(n.func,ast.Attribute)}
    assert not ({'advance','inherit','simulate','make_history'} & calls)
    design_gate()
