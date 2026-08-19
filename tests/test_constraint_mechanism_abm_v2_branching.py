import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v2_branching.py"


def load_module():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm_v2", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_lineage_parameters_are_independent_of_geography_labels():
    m = load_module()
    import random
    xs = m.make_lineages(random.Random(1), 20)
    assert len(xs) == 20
    assert all(0.35 <= x.pollinator_dependency <= 0.95 for x in xs)
    assert all(0.10 <= x.assurance_ceiling <= 0.90 for x in xs)


def test_v2_can_generate_both_response_signs_without_izu_tuning():
    m = load_module()
    rows = [m.paired_run(20260819 + i, n_lineages=16, steps=120) for i in range(40)]
    s = m.summarize(rows)
    assert s["positive_lineage_responses"] > 0
    assert s["negative_lineage_responses"] > 0
    assert s["mixed_sign_runs"] > 0
