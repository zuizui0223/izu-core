import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import render_reference_list_text
from scripts.render_island_ecology_submission_manuscript import render_submission_manuscript
from scripts.render_oikos_submission_rtf import render_manuscript_rtf, render_plain_text_rtf

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
REFERENCES = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
INTERNAL_REFERENCE_PATH = "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md"


def test_active_manuscript_reports_current_breadth_without_reopening_frozen_audit():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()

    assert "42 research entries across 37 exact geographic labels" in lower
    assert "frozen 25-entry identifiability" in lower
    assert "formal external prediction remains `not_evaluable`" in lower
    assert "cyclamen creticum" in lower
    assert "trinidad and tobago" in lower
    assert "campanula uniflora" in lower
    assert "self-compatible but cannot set seed without pollinators" in lower
    assert "distinct assurance route" in lower
    assert "these cases strengthen falsification and mechanism breadth" in lower


def test_value_selected_cases_survive_clean_submission_render():
    rendered = render_submission_manuscript()
    lower = rendered.lower()

    assert "## global confrontation:" in lower
    assert "42 research entries across 37 exact geographic labels" in lower
    assert "cyclamen creticum" in lower
    assert "trinidad and tobago" in lower
    assert "campanula uniflora" in lower
    assert "not equivalent to validation" in lower
    assert "formal external prediction remains `not_evaluable`" in lower
    assert "references are supplied in the accompanying reference list" in lower
    assert INTERNAL_REFERENCE_PATH.lower() not in lower


def test_value_selected_cases_survive_oikos_rtf_render():
    rtf = render_manuscript_rtf().lower()

    assert "42 research entries across 37 exact geographic labels" in rtf
    assert "cyclamen creticum" in rtf
    assert "trinidad and tobago" in rtf
    assert "campanula uniflora" in rtf
    assert "not equivalent to validation" in rtf
    assert "not_evaluable" in rtf
    assert "references are supplied in the accompanying reference list" in rtf
    assert INTERNAL_REFERENCE_PATH.lower() not in rtf


def test_reference_ledger_contains_only_explicitly_promoted_breadth_sources():
    text = REFERENCES.read_text(encoding="utf-8")
    lower = text.lower()

    assert "affre, l. & thompson, j.d. (1997)" in lower
    assert "feinsinger, p., wolfe, j.a. & swarm, l.a. (1982)" in lower
    assert "ægisdóttir, h.h. & thórhallsdóttir, t.e. (2006)" in lower
    assert "value-selected breadth source boundary" in lower
    assert "does not change the frozen 25-entry identifiability denominator" in lower


def test_submission_reference_list_contains_active_references_only():
    text = render_reference_list_text()
    lower = text.lower()

    assert text.startswith("# References\n\n")
    assert "affre, l. & thompson, j.d. (1997)" in lower
    assert "feinsinger, p., wolfe, j.a. & swarm, l.a. (1982)" in lower
    assert "ægisdóttir, h.h. & thórhallsdóttir, t.e. (2006)" in lower
    assert "hiraiwa, m.k. & ushimaru, a. (2024)" in lower
    assert "value-selected breadth source boundary" not in lower
    assert "hygiene decisions" not in lower
    assert INTERNAL_REFERENCE_PATH.lower() not in lower

    rtf = render_plain_text_rtf(text).lower()
    assert rtf.startswith("{\\rtf1")
    assert "affre, l. & thompson, j.d. (1997)" in rtf
    assert "feinsinger, p., wolfe, j.a. & swarm, l.a. (1982)" in rtf


def test_manifest_and_manuscript_keep_descriptive_and_formal_denominators_separate():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]

    assert breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] == 42
    assert breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 37
    assert breadth["formal_identifiability_research_entries"] == 25
    assert breadth["frozen_exact_geographic_overlap_labels"] == 21
    assert claims["external_full_contracts"] == "0_of_25"
    assert claims["formal_external_prediction"] == "not_evaluable"
