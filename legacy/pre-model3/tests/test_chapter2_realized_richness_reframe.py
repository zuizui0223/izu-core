import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
LEGACY_DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
UNIFIED_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"


def test_final_submission_promotes_unified_model3_and_demotes_legacy_richness_result():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "annual response-blind richness matching" in lower
    assert "68/128" in text
    assert "41.5%" in text
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "legacy reduced response-geometry analyses" not in lower
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower


def test_reframed_abstract_stays_within_oikos_300_word_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = abstract.lower()
    assert "reproductive selection before demographic change" in lower
    assert "expected inherited evolution without demographic sampling" in lower
    assert "realized evolution in finite populations" in lower
    assert "source-audited island systems" in lower
    assert "24,576-case bridge" in lower
    assert "stable latent branch prevalence" in lower
    assert "stable latent branch prevalence" in lower
    assert "68/128" not in abstract


def test_scientific_gate_requires_active_unified_model3_lock():
    legacy = json.loads(LEGACY_DECISION.read_text(encoding="utf-8"))
    assert legacy["prespecified_gate"]["decision"] == "blocker_failed_reframe_before_author_metadata"
    lock = json.loads(UNIFIED_LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "active_chapter2_unified_model3_bridge_complete"
    validated = validate_scientific_gate()
    assert validated["unification_audit"]["decision"] == "model2_not_required_as_active_scientific_model_or_control_gate"
    assert validated["prospective_bridge"]["status"] == "complete"
    assert validated["prospective_bridge"]["cases_verified"] == 24576
    assert validated["submission_state"]["new_field_data_required"] is False
    assert validated["submission_state"]["original_chapter2_controls_closed"] is True


def test_frozen_legacy_figure_generation_remains_reproducible_supporting_evidence():
    payload = build_figures()
    assert payload["status"] == "realized_richness_reframe_after_relational_regeneration"
    assert payload["realized_richness_headline"] == "mean_regime_richness_sensitive_branching_relational"
    assert payload["figure4_role"] == "metadata_confrontation_and_empirical_claim_ceiling"
    assert payload["figure4_external_systems"] == ["wanshan_yongxing", "ogasawara_anijima"]
    assert "figures/chapter2/figS7_realized_richness_hard_control.svg" in payload["figure_outputs"]
    for rel in payload["figure_outputs"]:
        path = ROOT / rel
        assert path.exists() and path.stat().st_size > 1_000
