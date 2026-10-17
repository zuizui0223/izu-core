"""Read-only reverse HIGH-I support from the original archived finite histories."""
from functools import lru_cache

import numpy as np
import pytest

from scripts.audit_chapter2_nee_high_i_support_20261017 import (
    N_CENSUSES, classification, high_i_loss_time, main_result,
)


def toy(maxima, support):
    values = np.full(N_CENSUSES, np.nan, dtype=float)
    kinds = np.zeros(N_CENSUSES, dtype=int)
    values[:len(maxima)] = maxima
    kinds[:len(support)] = support
    return values, kinds


def test_reverse_genetic_support_can_close_before_total_fixation():
    maxima, support = toy([.625, .50, .375], [3, 2, 1])
    result = classification(maxima, support, .53125)
    assert result["first_high_I_founder_mean_access_exclusion"] == 1
    assert result["first_single_allele_fixation"] == 2
    assert result["exclusion_before_single_allele_fixation"] is True
    assert result["exclusion_at_single_allele_fixation"] is False


def test_retained_maximum_only_means_not_structurally_excluded():
    maxima, support = toy([.625, .625, .625], [3, 2, 1])
    result = classification(maxima, support, .53125)
    assert result["first_high_I_founder_mean_access_exclusion"] is None
    # Non-exclusion is NOT a guarantee of evolutionary recovery.
    assert result["source_terminal_occupied"] is False


def test_closed_locus_cannot_increase_maximum_after_support_loss():
    maxima, support = toy([.625, .50, .625], [3, 2, 2])
    with pytest.raises(ValueError, match="HIGH-I maximum grew"):
        classification(maxima, support, .53125)


def test_missing_early_founder_target_is_not_allowed():
    maxima, support = toy([.50, .50], [2, 1])
    with pytest.raises(ValueError, match="founder high-I target"):
        classification(maxima, support, .53125)


def test_zero_and_strict_target_boundaries():
    assert high_i_loss_time([.625, .5], .5) is None
    assert high_i_loss_time([.625, .49], .5) == 1
    assert high_i_loss_time([.625, np.nan], .5) is None


@lru_cache(maxsize=1)
def source_result():
    return main_result()


def test_original_2304_archive_is_consistent_with_reverse_direction():
    result = source_result()
    assert result["actual_new_biological_runs"] == 0
    assert result["schema"] == "nee_high_i_existing_source_support_diagnostic_v1"
    assert result["original_low_I_loss_count_not_reinterpreted"] == 703
    overall = result["overall"]
    assert overall["original_histories"] == 2304
    assert 0 <= overall["high_I_founder_mean_excluded"] <= 2304
    assert sum(z["high_I_founder_mean_excluded"]
               for z in result["by_founder_block"].values()
               ) == overall["high_I_founder_mean_excluded"]
    assert len(result["by_original_visitor_context"]) == 18
    assert all(z["original_histories"] == 128
               for z in result["by_original_visitor_context"])
    assert "NOT IDENTIFIABLE" in " ".join(result["limits"])
    assert result["submission_claim"] == "NONE — source-only retrospective feasibility audit"
