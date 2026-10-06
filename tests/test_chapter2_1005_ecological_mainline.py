import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_1005_ecological_mainline_is_active():
    lock = json.loads(
        (ROOT / "data/design/chapter2_1005_ecological_mainline_lock_20261006.json").read_text(
            encoding="utf-8"
        )
    )
    manuscript = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    process = (ROOT / "docs/CHAPTER2_PROCESS_MAINLINE_20261005.md").read_text(
        encoding="utf-8"
    )

    assert lock["status"] == "active_scientific_mainline"
    assert lock["source_date"] == "2026-10-05"
    assert lock["primary_evidence"]["independent_visitor_histories"] == 64
    assert lock["primary_evidence"]["delayed_assurance_first_histories"] == 51
    assert lock["primary_evidence"]["fixed_assurance_far_investment_change_delayed"] == -0.3099
    assert lock["primary_evidence"]["assurance_evolution_interaction_delayed"] == 0.08468
    assert lock["confirmatory_status"]["status"] == "confirmed"
    assert lock["confirmatory_status"]["primary_sequence"]["assurance_first_histories"] == 51
    assert lock["confirmatory_status"]["primary_sequence"]["bootstrap95"] == [0.6875, 0.890625]
    assert lock["confirmatory_status"]["primary_fixed_assurance"]["far_investment_change"]["mean"] < 0
    assert "sequence ≠ necessity" in readme.lower()
    assert "2026-10-05 ecological results" in process
    assert manuscript.startswith(
        "# How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization"
    )
    assert "Assurance evolution is not required for investment decline" in manuscript
    assert "Lower pollen deficit does not necessarily mean greater viable reproduction" in manuscript


def test_primary_process_claim_does_not_depend_on_unresolved_continuum_route():
    manuscript = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(
        encoding="utf-8"
    )
    abstract = manuscript.split("## Abstract", 1)[1].split("## Keywords", 1)[0].lower()
    figures = manuscript.split("# Primary figure assembly and captions", 1)[1].split("# References", 1)[0].lower()
    for forbidden in ("pde", "high-resolution", "continuum replacement", "converged deterministic"):
        assert forbidden not in abstract
    assert "same plant state" in abstract
    assert "maintained-isolation" in abstract
    assert "fixed-assurance replication" in abstract
    assert "mutation/history" in figures
    assert "supporting information" in figures
