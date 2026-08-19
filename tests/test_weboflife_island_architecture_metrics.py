import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/summarize_weboflife_island_architecture.py"


def load_module():
    spec = importlib.util.spec_from_file_location("tier_b_architecture", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def test_weighted_architecture_metrics_on_synthetic_network():
    m = load_module()
    edges = [
        ("poll1", "plant1", 2.0),
        ("poll2", "plant1", 1.0),
        ("poll2", "plant2", 1.0),
    ]
    x = m.network_metrics(edges)
    assert x["pollinator_richness"] == 2
    assert x["plant_richness"] == 2
    assert x["link_richness"] == 3
    assert math.isclose(x["total_connection_strength"], 4.0)
    assert math.isclose(x["plant_partner_jaccard_overlap"], 0.5)
    assert 0.0 <= x["plant_weighted_profile_overlap"] <= 1.0
    assert x["interaction_shannon_effective_number"] > 1.0


def test_replicates_are_not_independent_systems():
    text = SCRIPT.read_text()
    assert '"independent_system_count": 1' in text
    assert "not 72 independent systems" in text
    assert "not single-visit pollen deposition" in text
