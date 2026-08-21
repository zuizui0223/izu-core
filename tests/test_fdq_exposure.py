import pytest

from channel_id.fdq_exposure import abundance_weighted_rao_q, source_locked_reference


def test_equal_abundance_two_trait_rao_q() -> None:
    result = abundance_weighted_rao_q(
        {"short": 1, "long": 1},
        {"short": 1.0, "long": 3.0},
    )
    # 0.25*2 + 0.25*2 from the two off-diagonal ordered pairs.
    assert result.fdq == pytest.approx(1.0)
    assert result.trait_coverage_fraction == pytest.approx(1.0)
    assert result.strict_ready is True
    assert result.missing_trait_taxa == ()


def test_abundance_weighting_matches_source_formula() -> None:
    result = abundance_weighted_rao_q(
        {"a": 3, "b": 1},
        {"a": 2.0, "b": 10.0},
    )
    # p=(0.75,0.25), distance=8: 2 * .75 * .25 * 8 = 3.
    assert result.fdq == pytest.approx(3.0)


def test_missing_positive_abundance_trait_blocks_primary_fdq() -> None:
    with pytest.raises(ValueError, match="FDQ blocked"):
        abundance_weighted_rao_q(
            {"known": 9, "missing": 1},
            {"known": 4.0},
        )


def test_non_strict_mode_reports_coverage_without_renormalized_fdq() -> None:
    result = abundance_weighted_rao_q(
        {"known": 9, "missing": 1},
        {"known": 4.0},
        require_complete_traits=False,
    )
    assert result.fdq is None
    assert result.total_abundance == pytest.approx(10)
    assert result.covered_abundance == pytest.approx(9)
    assert result.trait_coverage_fraction == pytest.approx(0.9)
    assert result.missing_trait_taxa == ("missing",)
    assert result.strict_ready is False


def test_zero_count_missing_taxon_does_not_block() -> None:
    result = abundance_weighted_rao_q(
        {"known": 2, "not_observed": 0},
        {"known": 4.0},
    )
    assert result.fdq == pytest.approx(0.0)
    assert result.strict_ready is True


def test_negative_abundance_and_nonpositive_traits_are_rejected() -> None:
    with pytest.raises(ValueError, match="invalid visitor abundance"):
        abundance_weighted_rao_q({"a": -1}, {"a": 2})
    with pytest.raises(ValueError, match="invalid proboscis length"):
        abundance_weighted_rao_q({"a": 1}, {"a": 0})


def test_reference_keeps_missing_trait_rule_explicit() -> None:
    reference = source_locked_reference()
    assert reference["trait_unit"] == "mm"
    assert reference["primary_missing_trait_rule"] == "block_FDQ_do_not_renormalize_observed_subset"
