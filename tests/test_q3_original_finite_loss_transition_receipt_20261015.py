"""Source-only admission guard for finite Q3 allele-loss transitions.

Ported from the *numeric* parts of PR #537 and PR #538. This test never runs
Model 3, changes reproductive law, or forces historical manuscript word counts.
The first-exclusion transitions are selected from the SAME original 2,304
histories and are not an independent cohort or prospective loss hazard.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
ACCESS = ROOT / "data/results/directional_access_20261013/READOUT.json"
LOSS = ROOT / "data/results/low_allele_loss_20261014/extracted/READOUT.json"
CASES = ROOT / "data/results/low_allele_loss_20261014/extracted/ALL_CASES.csv"
ACCESS_REVIEW = ROOT / "data/results/directional_access_20261013/INDEPENDENT_REVIEW.json"
LOSS_REVIEW = ROOT / "data/results/low_allele_loss_20261014/INDEPENDENT_REVIEW.json"
SOURCE_MAP = ROOT / "docs/CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _loss_rows() -> tuple[dict, list[dict[str, str]]]:
    source = _read(LOSS)
    raw = CASES.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source["cases_sha256"]
    return source, list(csv.DictReader(raw.decode("utf-8").splitlines()))


def test_original_source_cohort_and_verified_readback_are_distinct_from_subsets() -> None:
    access, loss = _read(ACCESS), _read(LOSS)
    direction_review, loss_review = _read(ACCESS_REVIEW), _read(LOSS_REVIEW)
    assert access["cases"] == loss["cases"] == 2_304
    assert access["cases_sha256"] == loss["input_cases_sha256"]
    assert access["ever_excluded"] == loss["eligible_loss"] == 1_238
    assert access["excluded_before_fixation"] == 703
    assert access["excluded_at_fixation"] == 535
    assert access["missing_I_excluded_before_fixation"] == 702
    assert access["excluded_with_expressed_variance"] == 703
    assert loss["statuses"] == {"no_exclusion": 1_066, "eligible_loss": 1_238}
    assert loss["direction_counts"] == {
        "favouring_needed": 315,
        "opposing_needed": 923,
        "screened_near_zero": 0,
    }
    assert access["new_biological_histories"] == 0
    assert loss["new_biological_histories"] == loss["reproduction_advances"] == 0
    assert direction_review["readout_sha256"] == hashlib.sha256(ACCESS.read_bytes()).hexdigest()
    assert loss_review["readout_sha256"] == hashlib.sha256(LOSS.read_bytes()).hexdigest()
    assert loss_review["cases_sha256"] == loss["cases_sha256"]
    assert loss_review["gamete_enumerations"] == 10_994_304


def test_native_parental_weighting_and_finite_transmission_reconcile() -> None:
    source, all_rows = _loss_rows()
    assert len(all_rows) == source["cases"] == 2_304
    first_loss = [r for r in all_rows if r["transition_status"] == "eligible_loss"]
    assert len(first_loss) == source["eligible_loss"] == 1_238
    positives = [r for r in first_loss if r["loss_direction"] == "favouring_needed"]
    negatives = [r for r in first_loss if r["loss_direction"] == "opposing_needed"]
    assert (len(positives), len(negatives)) == (315, 923)

    for r in first_loss:
        n = int(r["retained_resident_count"])
        q0 = float(r["q0"])
        expected = float(r["expected_frequency"])
        current = float(r["current_frequency"])
        response = float(r["parent_weighting_response"])
        residual = float(r["sampling_transmission_residual"])
        assert n == 48
        assert math.isclose(float(r["conditional_loss_probability"]), q0 ** n, rel_tol=0, abs_tol=1e-13)
        assert math.isclose(expected - current, response, rel_tol=0, abs_tol=1e-13)
        assert math.isclose(residual, -expected, rel_tol=0, abs_tol=1e-13)
        assert (response > 0) if r["loss_direction"] == "favouring_needed" else (response < 0)

    assert median(int(r["needed_copies_before"]) for r in positives) == 2
    assert math.isclose(median(float(r["expected_frequency"]) for r in positives),
                        0.021133482709469034, rel_tol=0, abs_tol=1e-13)
    assert math.isclose(median(float(r["conditional_loss_probability"]) for r in positives),
                        0.3260053119547402, rel_tol=0, abs_tol=1e-13)
    assert math.isclose(median(float(r["conditional_loss_probability"]) for r in negatives),
                        0.38693881062178476, rel_tol=0, abs_tol=1e-13)


def test_original_sex_specific_components_are_conditional_not_causal() -> None:
    _, all_rows = _loss_rows()
    positives = [r for r in all_rows if
                 r["transition_status"] == "eligible_loss"
                 and r["loss_direction"] == "favouring_needed"]
    assert len(positives) == 315
    self_positive = lambda r: float(r["self_response"]) > 1e-12
    maternal_negative = lambda r: float(r["female_response"]) < -1e-12
    paternal_negative = lambda r: float(r["paternal_response"]) < -1e-12
    assert sum(self_positive(r) for r in positives) == 305
    assert sum(maternal_negative(r) for r in positives) == 234
    assert sum(paternal_negative(r) for r in positives) == 266
    assert sum(self_positive(r) and maternal_negative(r) and paternal_negative(r)
               for r in positives) == 234
    source_map = SOURCE_MAP.read_text(encoding="utf-8").lower()
    assert "source-map preservation notice" in source_map
    assert "not" in source_map and "causal" in source_map and "same 2,304 original histories" in source_map
