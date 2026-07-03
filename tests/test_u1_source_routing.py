"""Offline tests for OpenAlex access-route interpretation."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "route_u1_review_sources.py"


def load_module():
    spec = importlib.util.spec_from_file_location("route_u1_review_sources", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_route_prefers_open_pdf_when_available():
    module = load_module()
    routed = module.route({
        "open_access": {"is_oa": True, "oa_status": "gold"},
        "best_oa_location": {"pdf_url": "https://example.org/paper.pdf", "landing_page_url": "https://example.org/paper", "source": {"display_name": "Example Journal"}},
        "primary_location": {},
    })
    assert routed["is_oa"] == "yes"
    assert routed["best_oa_pdf_url"] == "https://example.org/paper.pdf"
    assert routed["next_action"].startswith("inspect_OA_PDF")


def test_route_does_not_call_closed_source_unavailable():
    module = load_module()
    routed = module.route({"open_access": {"is_oa": False, "oa_status": "closed"}, "best_oa_location": None, "primary_location": {}})
    assert routed["is_oa"] == "no"
    assert routed["next_action"].startswith("library_or_author_route")
