"""Model3 pollen-export-normalized visitor trait composition sensitivity tests."""
import numpy as np

from scripts.audit_chapter2_visitor_export_normalized_sensitivity import (
    ARMS, BREADTH, EFFECTIVENESS, GENOTYPES, MATCHING, STATUS, contract,
    parent, visitor, pollen_export_total, activity_for_matching_export, run_all,
    ORIGINAL_RESULTS, REFERENCE, SHIFTED,
)
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config,
)


def test_scope_freeze_before_new_grid_outcomes():
    d = contract()
    assert d["status"] == STATUS
    assert d["comparison_arms"] == list(ARMS)
    assert d["parental_states"] == list(GENOTYPES)
    assert d["parent_matching_means"] == list(MATCHING)
    assert d["visitor_breadths"] == list(BREADTH)
    assert d["visitor_effectiveness"] == list(EFFECTIVENESS)
    assert d["total_matched_blocks"] == 36
    assert "AFTER" in d["status"] or "AFTER" in d["scope"].upper()


def test_exact_export_root_matches_target_and_keeps_visitor_traits():
    cfg = baseline_config("fixed")
    s = parent("mixed_diploid", .2)
    a = visitor(REFERENCE, .18, 1.)
    b = visitor(SHIFTED, .18, 1.)
    target = pollen_export_total(s, a, cfg, cfg.activity)
    match, error = activity_for_matching_export(s, b, cfg, target)
    assert abs(error) < 1e-8
    assert abs(pollen_export_total(s, b, cfg, match) - target) < 1e-8
    assert match > 0 and match != cfg.activity
    np.testing.assert_array_equal(a.breadths, b.breadths)
    np.testing.assert_array_equal(a.effectiveness, b.effectiveness)
    assert len(a.ids) == len(b.ids) == 4


def test_source_16_condition_references_are_reproduced():
    for label in GENOTYPES:
        assert set(ORIGINAL_RESULTS[label]) == set(ARMS[:2])
    out = run_all()
    assert out["source_16_condition_fixture_parity"]
    assert out["n_rows"] == 108
    assert len(out["within_fixture_paired_contrasts"]) == 36
    assert out["n_visitor_histories"] == 0
    assert out["n_real_islands"] == 0
    assert out["max_abs_corrected_export_difference"] < 1e-8


def test_all_normalized_blocks_have_common_diploid_context():
    out = run_all()
    for i in range(0, 108, 3):
        a, b, c = out["rows"][i:i+3]
        assert [x["visitor_arm"] for x in (a, b, c)] == list(ARMS)
        for name in ("parental_state", "parent_matching_mean",
                     "visitor_breadth", "visitor_effectiveness",
                     "n_parent", "n_visitor_types"):
            assert a[name] == b[name] == c[name]
        assert a["n_parent"] == 8 and a["n_visitor_types"] == 4
        assert abs(c["total_pollen_export"] - a["total_pollen_export"]) < 1e-8
        for v in (a, b, c):
            assert v["total_viable_seed"] > 0
            assert np.isfinite(v["focal_beta_median"])
            assert np.isfinite(v["collective_gamma_log_seed"])
            np.testing.assert_allclose(
                v["total_viable_seed"],
                v["maternal_outcross_viable_seeds"] + v["viable_self_seeds"],
                rtol=1e-10, atol=1e-10,
            )
