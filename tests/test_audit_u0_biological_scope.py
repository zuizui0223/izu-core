"""Tests for biological-scope filtering before floral screening."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "audit_u0_biological_scope.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_u0_biological_scope", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_nonplant_is_excluded_even_when_it_entered_occurrence_facet():
    module = load_module()
    decision, reason = module.classify({"kingdom": "Animalia", "phylum": "Chordata", "class": "Aves"})
    assert decision == "exclude_nonplant"
    assert "Animalia" in reason


def test_fern_is_excluded_from_floral_screening_not_from_raw_occurrence_audit():
    module = load_module()
    decision, reason = module.classify({"kingdom": "Plantae", "phylum": "Tracheophyta", "class": "Polypodiopsida"})
    assert decision == "exclude_nonflowering_plant"
    assert "Polypodiopsida" in reason


def test_flowering_candidate_is_retained_without_assuming_entomophily():
    module = load_module()
    decision, reason = module.classify({"kingdom": "Plantae", "phylum": "Tracheophyta", "class": "Magnoliopsida"})
    assert decision == "retain_flowering_candidate"
    assert "Magnoliopsida" in reason
