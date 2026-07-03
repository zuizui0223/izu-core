"""Offline tests for Crossref lead deduplication and review priority."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "triage_u1_crossref_leads.py"


def load_module():
    spec = importlib.util.spec_from_file_location("triage_u1_crossref_leads", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_group_key_prefers_doi_over_title_variants():
    module = load_module()
    assert module.group_key({"doi": "10.1000/ABC", "title": "one"}) == "doi:10.1000/abc"
    assert module.group_key({"doi": "", "title": " A Floral Study ", "year": "2010"}) == "title:a floral study|year:2010"


def test_direct_comparative_metadata_is_reviewed_first():
    module = load_module()
    rows = [{"automated_triage": "review_first", "taxon_title_match": "yes", "comparative_title_match": "yes", "trait_title_match": "yes"}]
    code, priority, role = module.priority(rows)
    assert code == 0
    assert priority == "direct_geographic_candidate"
    assert role == "primary_geographic_candidate"


def test_taxon_only_metadata_is_not_promoted_to_primary_effect():
    module = load_module()
    rows = [{"automated_triage": "taxon_lead", "taxon_title_match": "yes", "comparative_title_match": "no", "trait_title_match": "no"}]
    code, priority, role = module.priority(rows)
    assert code == 3
    assert priority == "taxon_context_candidate"
    assert role == "comparative_context"
