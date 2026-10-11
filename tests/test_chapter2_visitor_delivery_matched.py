"""Source-model receptor pollen receipt versus viable seed control."""
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_visitor_delivery_matched import (
    ATOL, MAX_ACTIVITY, STATUS, contract, match_delivered, run_all,
    delivered,
)
from scripts.audit_chapter2_visitor_export_normalized_sensitivity import (
    parent, visitor, REFERENCE, SHIFTED,
)
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config,
)


@pytest.fixture(scope="module")
def matrix():
    return run_all()


def test_delivery_contract_keeps_all_original_archipelago_boundaries_out():
    d = contract()
    assert d["status"] == STATUS
    assert d["expected_blocks"] == 36
    assert d["tolerance_abs"] == ATOL
    assert d["N"] == d["K"] == 8
    assert d["B"] == 48


def test_reference_and_shifted_source_reproduction_is_previously_known():
    source = parent("monomorphic", .2)
    cfg = baseline_config("fixed")
    a = visitor(REFERENCE, .18, 1.)
    b = visitor(SHIFTED, .18, 1.)
    assert delivered(source, a, cfg, cfg.activity) > 0
    assert delivered(source, b, cfg, cfg.activity) > 0
    root = match_delivered(
        source,b,cfg,delivered(source,a,cfg,cfg.activity))
    assert root["status"] == "MATCHED"
    assert 0 < root["activity"] < MAX_ACTIVITY
    assert abs(root["error"]) < ATOL


def test_36_source_matched_or_explicit_unmatchable(matrix):
    assert matrix["status"] == STATUS
    assert matrix["n_registered_blocks"] == 36
    assert matrix["n_matched"] + matrix["n_unmatchable"] == 36
    assert matrix["n_new_visitor_histories"] == 0
    assert matrix["n_real_plant_island_populations"] == 0
    for c in matrix["by_block"]:
        assert c["reference"]["n_parent"] == c["shifted_raw"]["n_parent"] == 8
        assert c["reference"]["n_visitor_types"] == c["shifted_raw"]["n_visitor_types"] == 4
        if c["root"]["status"] == "MATCHED":
            assert c["shifted_delivery_matched"] is not None
            assert abs(c["root"]["error"]) < ATOL
            assert abs(c["shifted_delivery_matched"]["total_pollen_delivered"] -
                       c["reference"]["total_pollen_delivered"]) < ATOL
            assert np.isfinite(c["matched_group_seed_delta"])
            assert np.isfinite(c["matched_beta_median_delta"])
            assert np.isfinite(c["matched_gamma_delta"])
        else:
            assert c["root"]["status"] == "UNMATCHABLE_AT_MAX_ACTIVITY"
            assert c["shifted_delivery_matched"] is None
            assert c["matched_group_seed_delta"] is None


def test_exchangeable_clonal_mothers_negative_control(matrix):
    m = [c for c in matrix["by_block"]
         if c["parental_state"]=="monomorphic"
         and c["root"]["status"]=="MATCHED"]
    assert m, "source reference monomorphic baseline should be feasible"
    assert max(abs(c["matched_group_seed_delta"]) for c in m) < 1e-7, (
        "in the source reproductive operator, exchangeable mothers with "
        "equal receipt must have equal total viable seeds"
    )


def test_original_108_reference_rows_still_recovered(matrix):
    for label, seeds in (
        ("monomorphic", (11.992565534924456, 10.882505800430955)),
        ("mixed_diploid", (11.931506679026661, 10.888561409910444)),
    ):
        c = [x for x in matrix["by_block"]
             if x["parental_state"]==label and x["matching"]==.2
             and x["breadth"]==.18 and x["effectiveness"]==1.]
        assert len(c)==1
        np.testing.assert_allclose(
           [c[0]["reference"]["total_viable_seed"],
            c[0]["shifted_raw"]["total_viable_seed"]],
           seeds,atol=1e-9,rtol=1e-9)


def test_immutable_original_delivery_result_receipt(matrix):
    """Verify archived source receipt without treating 36 cases as ecology samples."""
    p = (Path(__file__).resolve().parents[1] /
         "data/results/chapter2_visitor_delivery_matched_receipt_20261010.json")
    archive = json.loads(p.read_text(encoding="utf-8"))
    assert archive["original_sha256"] == (
        "52b55ff8ab4d7651ac86068a6cf256967d86275518f7dbb04b7909cd847ed7e3"
    )
    assert archive["blocks_declared"] == matrix["n_registered_blocks"] == 36
    assert archive["blocks_matched"] == matrix["n_matched"] == 36
    assert archive["blocks_unmatchable"] == matrix["n_unmatchable"] == 0
    np.testing.assert_allclose(
        archive["max_total_delivery_abs_match_error"],
        matrix["max_abs_delivery_match_error"], rtol=1e-7, atol=1e-14,
    )
    for group in ("monomorphic", "mixed_diploid"):
        a = archive["summary_by_parental_state"][group]
        cases = [x for x in matrix["by_block"]
                 if x["parental_state"] == group]
        assert a["n"] == len(cases) == 18
        assert a["conflict_classification_flips_delivery_matched"] == sum(
            x["matched_conflict_flip"] for x in cases
        )
        raw = np.array([
            x["shifted_raw"]["total_viable_seed"] -
            x["reference"]["total_viable_seed"] for x in cases
        ])
        delta = np.array([x["matched_group_seed_delta"] for x in cases])
        np.testing.assert_allclose(
            a["mean_abs_seed_contrast_raw"], np.mean(np.abs(raw)),
            atol=1e-12, rtol=1e-10
        )
        np.testing.assert_allclose(
            a["mean_abs_seed_contrast_delivery_matched"], np.mean(np.abs(delta)),
            atol=1e-12, rtol=1e-10
        )
        np.testing.assert_allclose(
            a["max_abs_seed_contrast_delivery_matched"], np.max(np.abs(delta)),
            atol=1e-12, rtol=1e-10
        )
    for group, old in archive["previous_original_fixture"].items():
        sub = [x for x in matrix["by_block"] if x["parental_state"] == group
               and x["matching"] == .2 and x["breadth"] == .18
               and x["effectiveness"] == 1.]
        assert len(sub) == 1
        src, matched = sub[0]["reference"], sub[0]["shifted_delivery_matched"]
        for key, actual in (
            ("baseline_delivered",src["total_pollen_delivered"]),
            ("matched_delivered",matched["total_pollen_delivered"]),
            ("baseline_seeds",src["total_viable_seed"]),
            ("matched_seeds",matched["total_viable_seed"]),
            ("baseline_export",src["total_pollen_export"]),
            ("matched_export",matched["total_pollen_export"]),
            ("baseline_beta_median",src["focal_beta_median"]),
            ("matched_beta_median",matched["focal_beta_median"]),
            ("baseline_gamma",src["collective_gamma_log_seed"]),
            ("matched_gamma",matched["collective_gamma_log_seed"]),
            ("activity_matched",sub[0]["root"]["activity"]),
        ):
            np.testing.assert_allclose(old[key],actual,rtol=1e-10,atol=1e-10)
        assert old["baseline_conflict"] is src["beta_negative_gamma_positive_conflict"]
        assert old["matched_conflict"] is matched["beta_negative_gamma_positive_conflict"]
