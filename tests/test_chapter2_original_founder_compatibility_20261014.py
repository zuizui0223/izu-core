"""Source-authenticated Model3 founder compatibility, no biological futures."""
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, technical_report,
)

def test_two_original_t0_founders():
    source = original_fixture()
    assert set(source["original_founders"]) == {"main", "confirmation"}
    for name in ("main", "confirmation"):
        assert source_state(source, name).alleles.shape == (48, 3, 2)

def test_original_t0_static_expected_returns():
    result = technical_report()
    assert result["original_full48_return_checks"] == 6
    assert result["technical_t0_reproductive_ledger_parity_checks"] == 96
    assert result["all_biology_futures_or_new_evolutionary_histories"] == 0


def test_intervention_preserves_per_individual_phenotypes():
    import numpy as np
    from scripts.audit_chapter2_original_founder_compatibility_20261014 import manipulate_homologs
    d = original_fixture()
    for block in ("main", "confirmation"):
        old = source_state(d, block)
        for overlap in (0, 3, 6, 12):
            change = manipulate_homologs(old, block=block, overlap=overlap)
            assert len(change.A_ids) == len(change.I_ids) == 12
            assert len(set(change.A_ids) & set(change.I_ids)) == overlap
            assert np.array_equal(change.state.alleles.mean(axis=2),
                                  old.alleles.mean(axis=2))
            assert np.array_equal(change.state.alleles[:, 0], old.alleles[:, 0])
            assert np.all(change.state.allele_origin[:, 1:, :] >= 10**12)


def test_mismatched_source_or_founder_count_fails_closed():
    from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
        manipulate_homologs, matched_draw
    )
    import pytest
    d = original_fixture()
    main = source_state(d, "main")
    altered = main.alleles.copy()
    altered[0, 2, :] = .5
    from scripts.model3_island.types import PlantState
    invalid = PlantState(alleles=altered, allele_origin=main.allele_origin,
                         mutation_flags=main.mutation_flags,
                         ids=main.ids, birth_years=main.birth_years)
    with pytest.raises(ValueError, match="exact original source genome"):
        manipulate_homologs(invalid, block="main", overlap=3)
    treated = manipulate_homologs(main, block="main", overlap=3).state
    with pytest.raises(ValueError, match="founder-sample"):
        matched_draw(main, treated, 7)
