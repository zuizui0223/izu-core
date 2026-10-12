"""Retain all 24 PR471 contrasts and compare them with native source operators."""
import csv
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pytest
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data/results/chapter2_statewise_pollen_readout_20261012.csv"
RECEIPT = ROOT / "data/results/chapter2_statewise_pollen_readout_receipt_20261012.json"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
EXPECTED = set(itertools.product(SETTINGS, (6.0, 8.0), (0.25, 0.5, 1.0)))


def stored_rows():
    assert TABLE.is_file(), "The complete PR471 table must be tracked"
    with TABLE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [{k: v if k == "setting" else float(v) for k, v in row.items()} for row in rows]


def test_stored_table_is_complete_unique_finite_and_arithmetic_consistent():
    rows = stored_rows()
    keys = [(r["setting"], r["budget"], r["mismatch_fraction"]) for r in rows]
    assert len(keys) == len(set(keys)) == 24 and set(keys) == EXPECTED
    for r in rows:
        assert all(np.isfinite(v) for k, v in r.items() if k != "setting")
        for k in ("P80_plain_matched", "P80_shifted", "P80_statewise_equalized"):
            assert 0.0 <= r[k] <= 1.0
        assert r["shift_minus_plain_pp"] == pytest.approx(
            100 * (r["P80_shifted"] - r["P80_plain_matched"]), abs=1e-12, rel=0
        )
        assert r["shift_minus_equalized_pp"] == pytest.approx(
            100 * (r["P80_shifted"] - r["P80_statewise_equalized"]), abs=1e-12, rel=0
        )
        assert abs(r["fixed_expression_shift_minus_equalized_pp"]) < 1e-10


def test_receipt_binds_table_and_keeps_the_evidence_scope():
    assert RECEIPT.is_file(), "The table requires a provenance receipt"
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert hashlib.sha256(TABLE.read_bytes()).hexdigest() == receipt["table_sha256"]
    assert receipt["scope"]["new_biological_histories"] == 0
    assert receipt["scope"]["natural_mediation_identified"] is False
    assert receipt["scope"]["formal_equivalence_test"] is False
    assert receipt["local_native_repository_execution"] is False
    assert receipt["source_commit"] == "bb150519507c82d75c1ba4bef1d7e9b3d5889b7c"


def test_reported_maximum_uses_all_eight_settings_at_each_shift():
    rows = stored_rows()
    for fraction, expected_maximum in (
        (0.25, 0.004470588129878994),
        (0.5, 0.003944008492984263),
        (1.0, 0.0000002409992760910029),
    ):
        selected = [r for r in rows if r["mismatch_fraction"] == fraction]
        assert len(selected) == 8
        assert max(abs(r["shift_minus_equalized_pp"]) for r in selected) == pytest.approx(
            expected_maximum, abs=1e-12, rel=0
        )


def test_native_source_blobs_are_the_audited_inputs():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    for path, expected in receipt["direct_input_git_blobs"].items():
        raw = (ROOT / path).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        assert actual == expected, f"Audited input changed: {path}"


def test_native_all_24_contexts_reproduce_stored_probabilities_and_fixed_control():
    # Import only here: static artifact tests can run independently of a checkout.
    from scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011 import audit
    from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import transition, p80

    with threadpool_limits(limits=1):
        result = audit()
        native = {(r["setting"], r["budget"], r["mismatch_fraction"]): r for r in result["results"]}
        assert len(native) == 24 and set(native) == EXPECTED
        baselines = {}
        for row in stored_rows():
            setting, budget, fraction = row["setting"], row["budget"], row["mismatch_fraction"]
            source = native[setting, budget, fraction]
            arms = source["full_arms"]
            base_key = (setting, budget)
            if base_key not in baselines:
                baselines[base_key] = p80(transition(setting, budget, 0.0, "native"))
            actual = {
                "P80_plain_matched": baselines[base_key],
                "P80_shifted": arms["native|shifted4"]["P80_occupied"],
                "P80_statewise_equalized": arms["native|original4_statewise_equal_delivery"]["P80_occupied"],
                "fixed_expression_shift_minus_equalized_pp": 100 * source["P80_fixed_shift_minus_equalized"],
            }
            for metric, value in actual.items():
                assert row[metric] == pytest.approx(value, abs=1e-12, rel=0), (base_key, fraction, metric)
        assert len(baselines) == 8
