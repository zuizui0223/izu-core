"""Evidence-rank and rendering guards for the standalone capacity companion.

Only old, immutable JSONs are read; never execute new biological simulations.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.audit_chapter2_k_at_b48_crosscohort import audit
from scripts.render_chapter2_capacity_companion_evidence_figure import render_svg

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_CAPACITY_PERSISTENCE_COMPANION_MANUSCRIPT_20261010.md"
FIGURE = ROOT / "figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg"


def test_three_cohorts_are_three_histories_not_three_confirmatory_tests():
    data = audit()
    rows = data["rows"]
    assert len(rows) == 3 and data["model_family_count"] == 1
    assert [r["evidence_rank"] for r in rows] == [
        "post_outcome_secondary_descriptive",
        "preregistered_primary_supported",
        "post_outcome_secondary_descriptive",
    ]
    assert all(r["n_independent_histories"] == 64 for r in rows)
    assert [round(r["effect_mean"], 6) for r in rows] == [
        0.013430, 0.007746, 0.008580,
    ]


def test_embedded_figure_matches_deterministic_no_refit_renderer():
    content = FIGURE.read_text(encoding="utf-8")
    assert content == render_svg()
    root = ET.fromstring(content)
    assert root.tag.endswith("svg")
    assert "one preregistered primary" in content
    assert "secondary/descriptive" in content.lower()
    assert content.count("<circle ") == 2
    assert content.count("<rect x=") == 1


def test_companion_retains_negative_and_inconclusive_boundaries():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for phrase in (
        "practically equivalent",
        "resource-window",
        "inconclusive",
        "0.007746",
        "0.002497",
        "0.013015",
        "114,688",
        "229,376",
        "64 independent",
        "not a universal",
        "separate",
        "Issue #436",
    ):
        assert phrase in text, phrase
    assert "threefold confirmatory success" not in text
    assert "real island plants are rescued" not in text


def test_earlier_preregistered_results_are_not_rewritten():
    import json
    kxb = json.loads(
        (ROOT / "results/chapter2/kb_independent_full_readout_20261009.json").read_text()
    )
    timed = json.loads(
        (ROOT / "results/chapter2/timed_self_viability_independent_readout_20261009.json").read_text()
    )
    fixed = json.loads(
        (ROOT / "results/chapter2/k_fixedB48_independent_primary_20261009.json").read_text()
    )
    assert kxb["primary_verdict"] == "inconclusive"
    assert timed["primary_verdict"] == "inconclusive"
    assert fixed["primary_verdict"] == "supported_controlled_demographic_K_moderation_at_fixed_B48"
