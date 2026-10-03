import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = ROOT / "docs/CHAPTER2_MANUSCRIPT_INTEGRATED_MODEL3_SYNDROME_20261003.md"
LOCK = ROOT / "data/design/chapter2_integrated_model3_syndrome_lock_20261003.json"
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
VNEXT = ROOT / "docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md"
SI_EXT = ROOT / "docs/CHAPTER2_SUPPORTING_INFORMATION_INTEGRATED_EXTENSIONS_20261003.md"
BOUNDARY_STAGE1 = ROOT / "data/results/chapter2_deterministic_persistence_boundary_stage1_20261003.json"
BOUNDARY_REFINEMENT = ROOT / "data/results/chapter2_deterministic_persistence_boundary_refinement_20261003.json"


def _text() -> str:
    return INTEGRATED.read_text(encoding="utf-8")


def test_integrated_candidate_keeps_locked_submission_separate() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "integrated_model3_syndrome_candidate_not_active_submission"
    assert lock["active_submission_unchanged"] is True
    assert ACTIVE.exists()
    assert VNEXT.exists()
    assert INTEGRATED.exists()


def test_integrated_manuscript_is_one_model_not_model3_plus_vnext() -> None:
    text = _text()
    lower = text.lower()
    assert "from pollination ecology to island syndrome" in text.splitlines()[0].lower()
    assert "## model lineage and integration" in lower
    assert "all analyses in this manuscript belong to **one model 3**" in lower
    assert "they do not define a second model" in lower
    assert "vnext" not in lower
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["model_identity"]["one_model"] is True
    assert lock["model_identity"]["separate_vnext_model"] is False


def test_integrated_abstract_contains_backbone_and_extensions() -> None:
    text = _text()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    lower = abstract.lower()
    words = abstract.split()
    assert 180 <= len(words) <= 300
    for token in (
        "three nested levels",
        "19,968-case island campaign",
        "24,576-case isolation bridge",
        "functional replacement",
        "failed its preregistered robustness rule",
        "standing genetic variation",
        "one model 3",
        "recurrent coarse functional regime",
        "multiple detailed evolutionary outcomes",
    ):
        assert token in lower


def test_integrated_manuscript_retains_original_model3_spine() -> None:
    lower = _text().lower()
    for token in (
        "reproductive selection before demographic change",
        "deterministic genotype-density",
        "finite-population",
        "24,576-case bridge",
        "128 independent visitor histories",
        "response-blind annual",
        "pooling eight independent visitor histories",
        "increasing plant capacity from 48 to 192",
        "reproductive assurance preserves trajectories",
        "geographic isolation compresses distinct ecological connections",
        "real islands occupy different stages of the same response architecture",
    ):
        assert token in lower


def test_integrated_manuscript_retains_established_extensions_and_failures() -> None:
    lower = _text().lower()
    for token in (
        "prospective extensions of the unified model 3",
        "conditional model mechanism",
        "functional rematching",
        "standing genetic variation filters",
        "mutation narrows the gap",
        "the original depression-0.50, 200-season bridge remains the biologically interpretable focal backbone",
        "retain the depression-0.75 labels only as a mathematical closure sensitivity",
        "was below one individual in 98.18% of history-by-start cells",
        "all 384 corresponding far populations were extinct by season 200",
        "earlier 9.4% mutation-rescue/standing-variation ratio is not retained",
    ):
        assert token in lower


def test_integrated_claim_boundary_stays_synthetic() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    boundary = lock["claim_boundary"]
    assert boundary["calibrated_to_named_islands"] is False
    assert boundary["natural_rates_calibrated"] is False
    assert boundary["literal_colour_or_corolla_mapping"] is False
    assert boundary["external_chapter1_coefficient_reproduction_required"] is False
    assert lock["computational_reproducibility"]["total_fresh_cases"] == 44544


def test_integrated_candidate_is_compact_without_dropping_audit_detail() -> None:
    text = _text()
    words = len(text.split())
    assert 5000 <= words <= 6000
    assert SI_EXT.exists()
    si = SI_EXT.read_text(encoding="utf-8").lower()
    for token in (
        "prospective extensions of the unified model 3",
        "assurance-by-cost route",
        "mutation input",
        "24,576-case bridge",
        "128 independent visitor histories",
        "formal source audit",
    ):
        assert token in si
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    compact = lock["compact_submission_candidate"]
    assert compact["active_oikos_submission_replaced"] is False
    assert compact["supporting_information_extension"].endswith(
        "CHAPTER2_SUPPORTING_INFORMATION_INTEGRATED_EXTENSIONS_20261003.md"
    )


def test_integrated_candidate_excludes_deterministic_nonparallelism_before_persistence_boundary() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    stage1 = json.loads(BOUNDARY_STAGE1.read_text(encoding="utf-8"))
    refinement = json.loads(BOUNDARY_REFINEMENT.read_text(encoding="utf-8"))

    assert lock["claim_boundary"]["deterministic_history_nonparallelism_among_persisting_isolation_populations"] is False
    assert lock["key_results"]["persistence_boundary_scan"]["headline_action"] == (
        "exclude deterministic history-level nonparallelism from persisting-population claims"
    )
    assert "No deterministic mixed/positive history was observed through depression 0.70" in stage1["first_stage_decision"]
    assert refinement["decision"]["pre_quasi_extinction_nonparallelism_detected"] is False

    lower = _text().lower()
    si = SI_EXT.read_text(encoding="utf-8").lower()
    assert "every history retaining all six masses >=1 remained negative-only" in lower
    assert "mixed histories only after at least one near/far starting-state endpoint crossed below mass 1" in si
