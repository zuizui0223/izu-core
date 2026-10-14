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
