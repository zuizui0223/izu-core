"""Regression tests for archived high-I genetic-support loss, not evolution runs."""
from __future__ import annotations

import csv
import json
import shutil

import numpy as np
import pytest

from scripts.audit_ch3_high_i_access_20261017 import (
    EXPECTED_CENSUSES, ROOT, SOURCE_DIR, audit, first_loss, interpret_case,
)


def synthetic_row():
    return {
        "block": "main", "context": "0", "replicate": "0",
        "initial_I": "0.53125", "target": "0.48125",
        "first_exclusion": "3", "first_single_allele_fixation": "3",
        "exclusion_before_fixation": "False",
        "terminal_alive": "False", "terminal_support": "1",
        "original_category": "assurance_only", "original_A": "1",
        "original_I": "", "raw_sha256": "toy",
    }


def toy_arrays():
    maximum = np.full(EXPECTED_CENSUSES, np.nan)
    minimum = np.full(EXPECTED_CENSUSES, np.nan)
    allele_var = np.full(EXPECTED_CENSUSES, np.nan)
    phenotype_var = np.full(EXPECTED_CENSUSES, np.nan)
    support = np.zeros(EXPECTED_CENSUSES, dtype=int)
    maximum[:4] = [.625, .625, .5, .5]
    minimum[:4] = [.375, .375, .375, .5]
    support[:4] = [3, 3, 2, 1]
    allele_var[:4] = [.01, .01, .003, 0.]
    phenotype_var[:4] = [.01, .01, .003, 0.]
    return maximum, minimum, support, allele_var, phenotype_var


def test_high_i_loss_before_fixation_not_confused_with_low_i_loss():
    row = interpret_case(synthetic_row(), *toy_arrays())
    a = row["restoration_targets"]["return_to_founder_mean"]
    assert a["first_high_exclusion"] == 2
    assert a["before_single_allele_fixation"]
    assert a["still_has_multiple_I_alleles"]
    assert a["expressed_I_variance_positive_at_loss"]
    assert a["loss_before_assurance_window_completion"]
    assert row["first_low_I_exclusion"] == 3
    assert row["first_single_allele_fixation"] == 3
    assert row["first_extinction"] == 4


def test_extra_high_target_must_declare_initial_inaccessibility():
    maximum, *_ = toy_arrays()
    alive = np.isfinite(maximum)
    assert first_loss(maximum, alive, .53125) == 2
    assert first_loss(maximum, alive, .58125) == 2
    assert first_loss(maximum, alive, .7) == 0  # baseline invalid: never classify new loss


def test_rejects_reopening_after_loss_without_mutation():
    arrays = list(toy_arrays())
    arrays[0][3] = .625
    with pytest.raises(ValueError, match="I maximum rose"):
        interpret_case(synthetic_row(), *arrays)


def test_rejects_original_low_I_source_classification_mismatch():
    row = synthetic_row()
    row["first_exclusion"] = "2"
    with pytest.raises(ValueError, match="original LOW-I first exclusion"):
        interpret_case(row, *toy_arrays())


def test_rejects_absent_census_as_zero_phenotype():
    arrays = list(toy_arrays())
    arrays[0][5] = 0.  # noncontiguous reappearance after a missing census
    with pytest.raises(ValueError, match="resurrected|noncontiguous"):
        interpret_case(synthetic_row(), *arrays)


def test_full_original_signed_source_high_I_audit():
    report = audit()
    assert report["status"].startswith("READ_ONLY_")
    assert report["new_biological_histories"] == 0
    assert report["simulation_updates_executed"] == 0
    assert report["cases"] == 2304
    assert report["original_low_I_first_exclusions"] == 1238
    assert report["original_low_I_exclusions_before_fixation"] == 703
    for label, part in report["analyses"].items():
        row = part["all"]
        assert 0 <= row["first_high_I_support_loss"] <= row["initially_accessible"]
        assert row["before_fixation"] + row["at_fixation"] == row["first_high_I_support_loss"]
        assert sum(x["first_high_I_support_loss"] for x in part["by_cell"]) == row[
            "first_high_I_support_loss"]
        assert len(part["by_cell"]) == 18
    assert report["analyses"]["return_to_founder_mean"]["all"]["initially_accessible"] == 2304


def test_source_sha_guard_refuses_a_reformatted_original_receipt(tmp_path):
    directory = tmp_path / SOURCE_DIR
    directory.mkdir(parents=True)
    for name in ("READOUT.json", "ALL_CASES.csv", "ALL_CENSUS_SUPPORT.npz"):
        shutil.copyfile(ROOT / SOURCE_DIR / name, directory / name)
    receipt = directory / "READOUT.json"
    text = receipt.read_text(encoding="utf-8")
    receipt.write_text(text + " ", encoding="utf-8")
    with pytest.raises(ValueError, match="Git blob changed"):
        audit(tmp_path)


def test_committed_18_cell_result_is_exactly_recomputable_from_original_npz():
    stored = json.loads(
        (ROOT / "data/results/ch3_high_i_access_original_retrospective_20261017.json")
        .read_text(encoding="utf-8")
    )
    independently_recomputed = audit()
    assert stored == independently_recomputed
    assert stored["analyses"]["return_to_founder_mean"]["all"][
        "first_high_I_support_loss"
    ] == 1455
    assert stored["analyses"]["return_to_founder_mean"]["all"][
        "before_fixation"
    ] == 758
    assert stored["analyses"]["return_to_founder_mean"]["all"][
        "at_fixation"
    ] == 697
    assert stored["analyses"]["return_to_founder_mean"]["all"][
        "historically_extinct"
    ] == 0


def test_coarse_three_allele_grid_makes_plus_005_sensitivity_redundant():
    result = audit(include_cases=True)
    for case in result["case_details"]:
        old = case["restoration_targets"]["return_to_founder_mean"]
        higher = case["restoration_targets"]["founder_mean_plus_0p05"]
        assert old["first_high_exclusion"] == higher["first_high_exclusion"]
        assert old["baseline_support"] == higher["baseline_support"]
    assert result["analyses"]["return_to_founder_mean"]["all"] == (
        result["analyses"]["founder_mean_plus_0p05"]["all"]
    )
