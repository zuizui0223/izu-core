"""Regression checks for high-I source-support bounds; no new biology."""
from __future__ import annotations

import json
from pathlib import Path
import shutil

import numpy as np
import pytest

from scripts.audit_ch3_high_i_support_20261017 import (
    ROOT, FOLDER, audit, first_strict_loss, prefix_stats, read_inputs,
)


def test_high_I_and_original_low_I_source_audit():
    output = audit()
    assert output["status"] == "PASS_RETROSPECTIVE_HIGH_I_SUPPORT_BOUNDS_ONLY"
    source = output["original_source"]
    assert source["n_history_paths"] == 2304
    assert source["n_censuses_each"] == 201
    assert source["original_low_i_loss_recalculated"]["ever_by_200"] == 1238
    assert source["original_low_i_loss_recalculated"]["before_I_fixation"] == 703
    assert source["original_low_i_loss_recalculated"]["at_I_fixation"] == 535
    assert output["declared_interpretation"]["does_not_measure_pollinator_extirpation_T_E"]
    assert output["declared_interpretation"]["does_not_identify_assurance_evolution_effect"]
    assert output["declared_interpretation"]["absence_of_loss_is_not_recovery"]
    assert output["the_three_high_I_criteria_have_identical_first_loss_times"] is True
    overlap = output["high_vs_low_loss_same_original_histories"]
    assert overlap["both_high_and_low"] + overlap["high_only"] + overlap["low_only"] + overlap["neither"] == 2304
    assert overlap["both_high_first"] + overlap["both_low_first"] + overlap["both_same_census"] == overlap["both_high_and_low"]
    targets = output["high_i_loss"]
    assert set(targets) == {
        "return_to_actual_founder_I", "founder_I_plus_0.05",
        "loss_of_original_uppermost_allele",
    }
    for entry in targets.values():
        overall = entry["pooled_original_histories_descriptive"]
        assert overall["denominator_original_histories"] == 2304
        assert overall["ever_by_200"] == (
            overall["before_I_fixation"] + overall["at_I_fixation"]
        )
        assert len(entry["by_founder_block_and_visitor_context"]) == 18
        assert sum(row["denominator_original_histories"]
                   for row in entry["by_original_order_class_descriptive"].values()) == 2304
        assert sum(row["denominator_original_histories"]
                   for row in entry["by_founder_block_and_visitor_context"]) == 2304
        assert sum(entry["by_source_founder_block"][name]["denominator_original_histories"]
                   for name in ("main", "confirmation")) == 2304
        count = overall["cumulative_by_census"]
        assert all(0 <= count[str(t)] <= overall["ever_by_200"]
                   for t in (25, 50, 100, 150, 200))
        assert count["200"] == overall["ever_by_200"]
    assert (
        targets["founder_I_plus_0.05"]["pooled_original_histories_descriptive"]["ever_by_200"]
        >= targets["return_to_actual_founder_I"]["pooled_original_histories_descriptive"]["ever_by_200"]
    )


def test_first_strict_loss_handles_equality_nan_and_direction():
    assert first_strict_loss([.625, .5, .375], .5, below=True) == 2
    assert first_strict_loss([.625, .5, .375], .5, below=False) == 0
    assert first_strict_loss([.625, .5, .375], .375, below=True) is None
    assert first_strict_loss([.375, .5, .625], .625, below=False) is None
    assert first_strict_loss([.625, .5, float("nan")], .375, below=True) is None
    assert first_strict_loss([.5, .625, float("nan")], .5, below=False) == 1


def test_allele_loss_before_fixation_is_not_same_as_fixation():
    rows = [27, 41, None, 200]
    fixes = [60, 41, None, 200]
    summary = prefix_stats(rows, fixes)
    assert summary["denominator_original_histories"] == 4
    assert summary["ever_by_200"] == 3
    assert summary["before_I_fixation"] == 1
    assert summary["at_I_fixation"] == 2
    assert summary["cumulative_by_census"]["25"] == 0
    assert summary["cumulative_by_census"]["50"] == 2
    assert summary["cumulative_by_census"]["200"] == 3


def test_cannot_lose_high_support_after_complete_allele_fixation():
    with pytest.raises(ValueError, match="after I fixation"):
        prefix_stats([49], [17])


def test_frozen_input_identity_rejects_tampered_readout(tmp_path):
    original = ROOT / FOLDER
    target = tmp_path / FOLDER
    target.mkdir(parents=True)
    for name in ("READOUT.json", "ALL_CENSUS_SUPPORT.npz", "ALL_CASES.csv"):
        shutil.copyfile(original / name, target / name)
    record = json.loads((target / "READOUT.json").read_text(encoding="utf-8"))
    record["ever_excluded"] += 1
    (target / "READOUT.json").write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="historical READOUT Git blob"):
        read_inputs(tmp_path)


def test_frozen_input_identity_rejects_tampered_source_case(tmp_path):
    original = ROOT / FOLDER
    target = tmp_path / FOLDER
    target.mkdir(parents=True)
    for name in ("READOUT.json", "ALL_CENSUS_SUPPORT.npz", "ALL_CASES.csv"):
        shutil.copyfile(original / name, target / name)
    with (target / "ALL_CASES.csv").open("a", encoding="utf-8") as f:
        f.write("\n")
    with pytest.raises(ValueError, match="source case CSV SHA256"):
        read_inputs(tmp_path)
