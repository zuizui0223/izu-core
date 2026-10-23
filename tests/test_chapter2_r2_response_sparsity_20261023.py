"""Read-only regression guards for independent archived 384-path R2 diagnostics."""
from __future__ import annotations

import json

import pytest

import scripts.audit_chapter2_r2_response_sparsity_20261023 as audit


def test_exact_original_sources_are_admitted_but_not_new_biology():
    r = audit.analyze()
    assert r["status"] == "SOURCE_BOUND_EXPLORATORY_R2_RESPONSE_SPARSITY_NO_NEW_BIOLOGY"
    assert r["source_run_sha"] == "eb785dc6865ca1842ec9d6c7d511778c74e03478"
    assert r["original_rows"] == 384
    assert r["independent_founders"] == 12
    assert r["nested_demographic_repeats_per_founder"] == 4
    assert r["all_trajectories_survived"]
    assert r["registered_R1_R2_R3_R4_R5_inference_unchanged"]
    assert r["new_biological_simulations"] == r["new_statistical_tests"] == 0


def test_zero_response_counts_and_prefix_fixation_are_not_confused():
    r = audit.analyze()
    got = {(x["initial_A"], x["baseline"].startswith("strong")): x
           for x in r["strata"]}
    expected = {
        (0.3, True): (45, 3, 22, 23),
        (0.3, False): (8, 40, 1, 7),
        (0.5, True): (42, 6, 10, 32),
        (0.5, False): (8, 40, 1, 7),
    }
    for key, (zero, nonzero, fixed, zero_nonfixed) in expected.items():
        x = got[key]
        assert x["paired_nested_future_pairs_n"] == 48
        assert x["zero_exact_A_contrast_pairs"] == zero
        assert x["nonzero_exact_A_contrast_pairs"] == nonzero
        assert x["prefix_fixed_A_pairs"] == fixed
        assert x["zero_among_prefix_polymorphic_pairs"] == zero_nonfixed
        assert x["lower_bound_only_no_joint_path_identity_reconstructed"]
        assert x["nonzero_fraction"] == pytest.approx(nonzero / 48)
        assert x["mean_signed_contrast_given_exact_nonzero"] * nonzero / 48 == pytest.approx(
            x["unconditional_signed_mean_A_contrast"], abs=1e-14
        )
        assert x["mean_signed_contrast_given_prefix_polymorphic"] * (48-fixed)/48 == pytest.approx(
            x["unconditional_signed_mean_A_contrast"], abs=1e-14
        )


def test_joint_terminal_fixed_and_zero_bounds_from_three_sets():
    rows = {(x["initial_A"], x["baseline"].startswith("strong")): x
            for x in audit.analyze()["strata"]}
    expected = {
        (0.3, True): (46, 48, 24, 26, 43),
        (0.3, False): (18, 16, 17, 15, 0),
        (0.5, True): (42, 47, 32, 37, 35),
        (0.5, False): (22, 13, 21, 12, 0),
    }
    for key, (fixed_control, fixed_decline, new_control, new_decline, lower) in expected.items():
        r = rows[key]
        assert r["terminal_fixed_A_control"] == fixed_control
        assert r["terminal_fixed_A_decline"] == fixed_decline
        assert r["newly_fixed_A_control_since_prefix"] == new_control
        assert r["newly_fixed_A_decline_since_prefix"] == new_decline
        assert r["at_least_zero_and_both_terminal_fixed"] == lower
        assert r["at_least_prefix_polymorphic_then_both_fixed_and_zero"] == max(0, lower - r["prefix_fixed_A_pairs"])
        assert lower <= r["zero_exact_A_contrast_pairs"]


def test_conditional_results_are_descriptive_not_fixation_mediation():
    r = audit.analyze()
    x = {(row["initial_A"], row["baseline"]): row for row in r["strata"]}
    assert x[0.3, "strong_baseline_limitation"]["mean_signed_contrast_given_exact_nonzero"] == pytest.approx(0.13975694444444445)
    assert x[0.3, "weak_baseline_limitation"]["mean_signed_contrast_given_exact_nonzero"] == pytest.approx(0.13489583333333335)
    assert x[0.5, "strong_baseline_limitation"]["mean_signed_contrast_given_exact_nonzero"] == pytest.approx(0.0368923611111111)
    assert x[0.5, "weak_baseline_limitation"]["mean_signed_contrast_given_exact_nonzero"] == pytest.approx(0.10579427083333333)
    assert all(row["weak_minus_strong_nonzero_fraction"] > 0 for row in r["comparisons"])
    assert any("Pure causal" in s for s in r["not_identified"])
    assert any("matched" in s.lower() for s in r["not_identified"])
    comparisons = {v["initial_A"]: v for v in r["comparisons"]}
    for a in (0.3, 0.5):
        z = comparisons[a]
        assert z["decomposition_is_not_causal_mediation"]
        assert z["nonzero_frequency_arithmetic_component"] + z[
            "nonzero_conditional_magnitude_arithmetic_component"
        ] == pytest.approx(z["weak_minus_strong_A"], abs=1e-12)
        assert z["prefix_polymorphic_frequency_arithmetic_component"] + z[
            "prefix_polymorphic_conditional_arithmetic_component"
        ] == pytest.approx(z["weak_minus_strong_A"], abs=1e-12)
    assert comparisons[0.3]["nonzero_frequency_arithmetic_component"] == pytest.approx(
        0.10585575810185184, abs=1e-12
    )
    assert comparisons[0.3]["nonzero_conditional_magnitude_arithmetic_component"] == pytest.approx(
        -0.00217737268518519, abs=1e-12
    )
    assert comparisons[0.5]["nonzero_frequency_arithmetic_component"] == pytest.approx(
        0.05053484881365739, abs=1e-12
    )
    assert comparisons[0.5]["nonzero_conditional_magnitude_arithmetic_component"] == pytest.approx(
        0.033015498408564825, abs=1e-12
    )


def test_changed_archival_zero_count_is_rejected(tmp_path, monkeypatch):
    d = json.loads(audit.INDEPENDENT.read_text(encoding="utf-8"))
    d["pair_contrasts"][0]["zero_A_contrast_pairs"] = 19
    p = tmp_path / "fake-reader.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    monkeypatch.setattr(audit, "INDEPENDENT", p)
    # Count change still passes if not checked; tests should ensure exact frozen source
    # by requiring the original distribution of numerical/structural counts.
    with pytest.raises(AssertionError):
        audit.analyze()


def test_changed_source_mean_is_rejected(tmp_path, monkeypatch):
    d = json.loads(audit.REGISTERED_SOURCE.read_text(encoding="utf-8"))
    d["summaries"][0]["terminal_decline_minus_control_A"] += 0.01
    p = tmp_path / "fake-summary.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    monkeypatch.setattr(audit, "REGISTERED_SOURCE", p)
    with pytest.raises(AssertionError, match="disagree"):
        audit.analyze()


def test_changed_prefix_constraint_is_rejected(tmp_path, monkeypatch):
    d = json.loads(audit.INDEPENDENT.read_text(encoding="utf-8"))
    d["pair_contrasts"][0]["prefix_fixed_pairs_all_remain_same_A"] = False
    p = tmp_path / "fake-reader.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    monkeypatch.setattr(audit, "INDEPENDENT", p)
    with pytest.raises(AssertionError, match="fixation"):
        audit.analyze()
