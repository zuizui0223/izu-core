"""Offline checks for U1 literature-discovery helpers."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str):
    path = ROOT / "paper" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_manifest_deduplicates_same_query():
    module = load("build_u1_search_query_manifest")
    rows = [
        {"u0_accepted_key": "1", "source_lane": "Crossref", "query_purpose": "taxon_baseline", "query_text": "Weigela coraeensis", "language": "en"},
        {"u0_accepted_key": "1", "source_lane": "Crossref", "query_purpose": "taxon_baseline", "query_text": "Weigela coraeensis", "language": "en"},
        {"u0_accepted_key": "1", "source_lane": "Crossref", "query_purpose": "island_comparison", "query_text": "Weigela coraeensis island mainland floral pollination", "language": "en"},
    ]
    assert len(module.deduplicate(rows)) == 2


def test_crossref_triage_requires_taxon_plus_relevant_title_signal():
    module = load("run_u1_crossref_discovery")
    query = {"search_name": "Weigela coraeensis"}
    assert module.title_flags(query, "Floral differentiation among insular and mainland populations of Weigela coraeensis")[3] == "review_first"
    assert module.title_flags(query, "A phylogeny of Caprifoliaceae")[3] in {"context_only", "noise_likely"}


def test_crossref_priority_prefers_accepted_baseline_query():
    module = load("run_u1_crossref_discovery")
    accepted = {"queue_rank": "1", "query_purpose": "taxon_baseline", "name_type": "accepted_input", "language": "en", "query_id": "a"}
    synonym = {"queue_rank": "1", "query_purpose": "taxon_baseline", "name_type": "gbif_synonym", "language": "en", "query_id": "b"}
    geographic = {"queue_rank": "1", "query_purpose": "island_comparison", "name_type": "accepted_input", "language": "en", "query_id": "c"}
    assert module.priority(accepted) < module.priority(synonym)
    assert module.priority(accepted) < module.priority(geographic)
