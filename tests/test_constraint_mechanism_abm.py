import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm.py"


def load_module():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_default_scenarios_encode_monotone_opportunity_constraint():
    m = load_module()
    mainland, continental, oceanic = m.default_scenarios()
    assert mainland.n_pollinator_types > continental.n_pollinator_types > oceanic.n_pollinator_types
    assert mainland.partner_loss < continental.partner_loss < oceanic.partner_loss
    assert mainland.partner_arrival > continental.partner_arrival > oceanic.partner_arrival


def test_model_can_generate_multiple_architectures_without_hardcoding_one_island_syndrome():
    m = load_module()
    rows = []
    for si, s in enumerate(m.default_scenarios()):
        for r in range(60):
            rows.append(m.run_one(s, seed=1234 + si * 10000 + r, steps=90, n_plants=50))
    labels = {r["architecture"] for r in rows}
    assert len(labels) >= 2


def test_reproduction_is_bounded_and_model_is_not_empirical_evidence():
    m = load_module()
    rows = [m.run_one(s, seed=42 + i, steps=30, n_plants=25) for i, s in enumerate(m.default_scenarios())]
    assert all(0.0 <= r["mean_reproduction"] <= 1.0 for r in rows)
    assert all(0.0 <= r["mean_assurance"] <= 1.0 for r in rows)
