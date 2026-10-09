"""Source-linked, side-effect-free cross-cohort evidence-rank contract checks."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_k_at_b48_crosscohort import ROOT, SOURCES, audit


def test_sha_locked_independent_history_cohorts_and_prospective_rank():
    d = audit()
    assert d["status"] == "READ_ONLY_POST_OUTCOME_DIRECTIONAL_CONCORDANCE_NOT_NEW_CONFIRMATION"
    assert d["distinct_new_history_cohorts"] == 3
    assert d["model_family_count"] == 1
    assert d["n_history_clusters_per_cohort"] == 64
    assert d["n_future_cells_by_cohort"] == [229376, 114688, 229376]
    assert [row["history_range"] for row in d["rows"]] == [
        [40110901, 40110964],
        [41110901, 41110964],
        [42110901, 42110964],
    ]
    assert d["same_sign_positive"] is True
    assert [row["evidence_rank"] for row in d["rows"]] == [
        "post_outcome_secondary_descriptive",
        "preregistered_primary_supported",
        "post_outcome_secondary_descriptive",
    ]
    assert [row["original_primary"]["decision"] for row in d["rows"]] == [
        "inconclusive",
        "supported_controlled_demographic_K_moderation_at_fixed_B48",
        "inconclusive",
    ]


def test_actual_means_match_unchanged_registered_machine_json():
    d = audit()
    xs = [row["effect_mean"] for row in d["rows"]]
    assert xs == pytest.approx([
        0.013430012166239045,
        0.007745713876893593,
        0.008580259018686977,
    ], abs=1e-15)
    assert d["unweighted_descriptive_mean_not_pooled_estimate"] == pytest.approx(
        0.009918661686606537, abs=1e-14
    )
    assert all(row["bootstrap95"][0] > 0 for row in d["rows"])
    # Positivity of selected secondary CIs is NOT three confirmatory successes.
    assert sum(row["evidence_rank"] == "preregistered_primary_supported"
               for row in d["rows"]) == 1


def test_original_distinct_timing_and_kb_primary_inconclusive_unchanged():
    d = audit()
    timed = json.loads((ROOT / SOURCES[2]["file"]).read_text())
    original_four = json.loads((ROOT / SOURCES[0]["file"]).read_text())
    assert timed["primary_verdict"] == "inconclusive"
    assert timed["original_predeclared_primary"].startswith("[tau_late")
    assert original_four["primary_verdict"] == "inconclusive"
    assert original_four["original_predeclared_primary"] == "tau(K8,B8)-tau(K8,B48)"
    assert d["rows"][2]["original_primary"]["key"] == (
        "primary_late_minus_early_K_moderation"
    )


def test_full_cohort_sha_missing_or_tampered_files_fail_closed(tmp_path, monkeypatch):
    import scripts.audit_chapter2_k_at_b48_crosscohort as a
    original = SOURCES[0]
    bad = dict(original)
    bad["sha256"] = "0" * 64
    monkeypatch.setattr(a, "SOURCES", (bad, *SOURCES[1:]))
    with pytest.raises(AssertionError, match="digest differs"):
        a.audit()


def test_document_bans_unjustified_meta_analysis_and_empirical_transfer():
    report = (Path(__file__).resolve().parents[1] /
              "docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md").read_text()
    assert "post-outcome" in report.lower()
    assert "pooled" in report.lower()
    assert "one model" in report.lower()
    assert "inconclusive" in report.lower()
