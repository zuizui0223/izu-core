import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_abm_v4_global_continuous_isolation_gradient.py"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_v4_global_gradient_test", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def test_continuous_gradient_recovers_directional_network_simplification():
    m = load_module()
    out = m.build(replicates=20, seed=20260819)
    t = out["tests"]
    assert t["partner_types_decline"]
    assert t["effective_links_decline"]
    assert t["interaction_diversity_declines"]
    assert t["plant_niche_overlap_increases"]
    assert t["reproduction_not_forced_to_monotonic_decline"]


def test_gradient_is_continuous_not_three_class_lookup():
    m = load_module()
    out = m.build(replicates=5, seed=20260819)
    xs = [x["isolation_index"] for x in out["gradient"]]
    assert xs == [i / 10 for i in range(11)]
    assert out["empirical_target"]["target_level"].startswith("directional continuous-gradient")
