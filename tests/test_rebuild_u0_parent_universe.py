"""Unit tests for the GBIF U0 parent-universe rebuild helpers."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "rebuild_u0_parent_universe.py"


def load_module():
    spec = importlib.util.spec_from_file_location("rebuild_u0_parent_universe", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_circle_wkt_is_closed_polygon():
    module = load_module()
    wkt = module.circle_wkt(34.75, 138.95, 25.0, vertices=8)
    assert wkt.startswith("POLYGON((")
    assert wkt.endswith("))")
    coordinates = wkt.removeprefix("POLYGON((").removesuffix("))").split(",")
    assert coordinates[0] == coordinates[-1]
    assert len(coordinates) == 9


def test_facet_entries_requires_species_key_facet():
    module = load_module()
    payload = {"facets": [{"field": "SPECIES_KEY", "counts": [{"name": "123", "count": 4}]}]}
    assert module.facet_entries(payload) == [{"name": "123", "count": 4}]


def test_facet_url_keeps_offset_and_profile_filters():
    module = load_module()
    url = module.facet_url("POLYGON((0 0,1 0,1 1,0 0))", 1000)
    assert "facetOffset=1000" in url
    assert "facetLimit=1000" in url
    assert "kingdom=Plantae" in url
    assert "hasCoordinate=true" in url
