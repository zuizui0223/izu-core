import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md"
LONGFORM = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"


def test_1005_ecological_mainline_is_active():
    lock = json.loads(
        (ROOT / "data/design/chapter2_1005_ecological_mainline_lock_20261006.json").read_text(
            encoding="utf-8"
        )
    )
    manuscript = SUBMISSION.read_text(encoding="utf-8")
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
    assert "temporal precedence is not causal necessity" in readme.lower()
    assert "2026-10-05 ecological results" in process
    assert manuscript.startswith(
        "# Reproductive assurance compresses floral-investment divergence under pollinator limitation"
    )
    assert "Assurance evolution is not required for investment decline" in manuscript
    assert "Assurance evolution consistently compresses environmental divergence" in manuscript
    assert "Pollen-deficit and viable-output responses are not equivalent" in manuscript


def test_primary_process_claim_does_not_depend_on_unresolved_continuum_route():
    manuscript = SUBMISSION.read_text(encoding="utf-8")
    abstract = manuscript.split("## Abstract", 1)[1].split("## Keywords", 1)[0].lower()
    figures = manuscript.split("# Primary figure assembly and captions", 1)[1].split("# Data accessibility", 1)[0].lower()
    for forbidden in ("pde", "high-resolution", "continuum replacement", "converged deterministic"):
        assert forbidden not in abstract
    assert "64 independent new visitor histories" in abstract
    assert "assurance capacity was fixed across four reproductive settings" in abstract
    assert "78–90%" in abstract
    assert "not required for pollinator-limitation-driven investment decline" in abstract
    assert "finite genetic realization" in figures
    assert "dynamic mediation" in figures


def test_confirmatory_methods_are_explicit_in_longform_provenance():
    manuscript = LONGFORM.read_text(encoding="utf-8")
    methods = manuscript.split("# Materials and Methods", 1)[1].split("# Results", 1)[0]
    normalized = " ".join(methods.split())
    assert "Prospectively frozen independent confirmation" in methods
    assert "4,096 finite-population trajectories" in normalized
    assert "26100601–26100664" in normalized
    assert "26101601–26101608" in normalized
    assert "lower bound of a 95% visitor-history bootstrap interval to exceed 0.50" in normalized
    assert "secondary cells could not rescue or overturn the primary adjudication" in normalized
    assert "did not increase the independent ecological denominator beyond 64" in normalized


def test_machine_readable_establishment_audit_is_closed():
    audit = json.loads(
        (ROOT / "data/results/chapter2_1005_establishment_audit_20261006.json").read_text(
            encoding="utf-8"
        )
    )
    assert audit["status"] == "established_bounded"
    assert audit["passes"] == audit["total"] == 5
    assert audit["establishment_criteria"]["independent_confirmation"]["status"] == "pass"
    assert audit["establishment_criteria"]["threshold_robustness"]["assurance_first_counts"] == [48, 51, 59]
    assert audit["establishment_criteria"]["scope_generality"]["status"] == "pass_bounded"
    assert audit["establishment_criteria"]["claim_boundary_reproducibility"]["independent_visitor_histories"] == 64
