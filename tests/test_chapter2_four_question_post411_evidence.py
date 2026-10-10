"""Protect the Chapter 2 post-411 four-question interpretation (no new biology)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/design/chapter2_four_question_post411_evidence_spine_20261010.json"
NARRATIVE = ROOT / "docs/CHAPTER2_FOUR_QUESTION_POST411_EVIDENCE_SPINE_20261010.md"


def load():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_four_question_order_and_non_simulation_status():
    evidence = load()
    stages = evidence["ordered_stages"]
    assert [(s["id"], s["name"], s["japanese"]) for s in stages] == [
        ("Q1", "threshold", "閾値"),
        ("Q2", "order", "順序"),
        ("Q3", "realization", "実現"),
        ("Q4", "consequence", "帰結"),
    ]
    assert evidence["status"] == "EVIDENCE_RANKED_EDITORIAL_DESIGN_ONLY"
    assert evidence["biological_simulations_run"] == 0
    assert evidence["new_visitor_histories_run"] == 0
    assert evidence["new_confirmatory_claims"] == 0
    assert evidence["active_submission_unchanged"] is True


def test_no_retrospective_result_is_promoted_to_confirmation():
    evidence = load()
    rows = evidence["evidence"]
    assert any(r["pr"] == 411 and r["rank"] == "PREREGISTERED_SUPPORTED" for r in rows)
    assert any(r["pr"] == 442 and r["rank"] == "PREREGISTERED_SUPPORTED_INDEPENDENT" for r in rows)
    assert all(
        r["rank"] not in ("PREREGISTERED_SUPPORTED", "PREREGISTERED_SUPPORTED_INDEPENDENT")
        for r in rows if r["pr"] in (452, 455, 457)
    )
    assert {r["rank"] for r in rows if r["pr"] == 457} == {
        "RETROSPECTIVE_ORIGINAL_GENOME_SOURCE_REPLAY",
        "RETROSPECTIVE_SOURCE_FALSIFIER_NOT_PERSISTENCE",
    }
    assert any(r["pr"] == 422 and r["rank"] == "PREREGISTERED_NONREPLICATION" for r in rows)
    assert any(r["pr"] == 448 and r["rank"] == "PREREGISTERED_INCONCLUSIVE" for r in rows)


def test_assigned_order_equivalence_is_not_mislabeled():
    row = next(r for r in load()["evidence"] if r["pr"] == 418)
    assert row["rank"] == "PREREGISTERED_PRACTICAL_EQUIVALENCE"
    assert row["ci95"][0] < row["estimate"] < row["ci95"][1] < 0
    assert row["rope"][0] < row["ci95"][0]
    assert row["ci95"][1] < row["rope"][1]


def test_demographic_K_result_remains_distinct_from_evolution_to_survival():
    evidence = load()
    row = next(r for r in evidence["evidence"] if r["pr"] == 442)
    assert row["estimate"] == 0.0077457139
    assert row["ci95"] == [0.0024971581, 0.0130154788]
    assert row["independent_history_clusters"] == 64
    assert row["n_futures"] == 114688
    assert [g["verdict"] for g in evidence["transition_gates"]] == ["UNIDENTIFIED"] * 3
    assert evidence["evidence"][-1]["new_longitudinal_persistence_estimate"] is False


def test_claim_and_stop_boundaries_visible_in_human_document():
    text = NARRATIVE.read_text(encoding="utf-8")
    for stage in ("Q1 — Threshold", "Q2 — Order", "Q3 — Realization", "Q4 — Consequence"):
        assert stage in text
    for important in ("#411", "#418", "#422", "#442", "#448", "#452", "#455", "#457"):
        assert important in text
    assert "NOT a new experiment" in text
    assert "NO-GO" in text
    assert "untouched" in text
