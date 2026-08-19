import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/acquire_traveset2016_global_network_supplement.py"


def load_module():
    spec = importlib.util.spec_from_file_location("traveset2016_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_classifies_expected_supplement_tables():
    m = load_module()
    tables = [
        [["Network", "Location", "Archipelago", "Latitude", "Sampling method"], ["A", "x", "y", "1", "focal"]],
        [["Island", "Area", "Age", "Elevation range", "Isolation mainland"], ["x", "1", "2", "3", "4"]],
        [["Network", "Species", "Interactions", "Connectance", "Weighted nestedness"], ["A", "10", "20", "0.2", "12"]],
    ]
    out = m.classify_tables(tables)
    assert set(out) == {"network_inventory", "oceanic_island_traits", "network_metrics"}


def test_missing_tables_do_not_create_ready_state():
    m = load_module()
    out = m.classify_tables([[['foo', 'bar'], ['x', 'y']]])
    assert out == {}
