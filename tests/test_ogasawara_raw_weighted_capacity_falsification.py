from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_ogasawara_raw_weighted_capacity_falsification.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ogasawara_capacity_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_capacity_interpolation_reproduces_reference_grid():
    module = load_module()
    reference = [math.log1p(1.0), math.log1p(9.0), math.log1p(99.0)]
    assert module.frozen_capacity_index(1.0, reference) == 1.0
    assert module.frozen_capacity_index(9.0, reference) == 0.5
    assert module.frozen_capacity_index(99.0, reference) == 0.0
    assert module.frozen_capacity_index(0.1, reference) == 1.0
    assert module.frozen_capacity_index(999.0, reference) == 0.0


def test_exact_one_sided_rank_test_has_n4_resolution():
    module = load_module()
    capacity = [1.0, 0.7, 0.3, 0.0]
    shannon = [1.0, 2.0, 3.0, 4.0]
    overlap = [4.0, 3.0, 2.0, 1.0]
    low = module.exact_permutation_test(capacity, shannon, "less")
    high = module.exact_permutation_test(capacity, overlap, "greater")
    assert low["rho"] == -1.0
    assert high["rho"] == 1.0
    assert low["permutation_count"] == 24
    assert high["permutation_count"] == 24
    assert math.isclose(low["exact_permutation_p"], 1 / 24)
    assert math.isclose(high["exact_permutation_p"], 1 / 24)


def test_pairwise_concordance_is_direction_explicit():
    module = load_module()
    rows = [
        {"island": "small", "capacity_index": 1.0, "interaction_shannon": 1.0, "plant_niche_overlap": 4.0},
        {"island": "mid", "capacity_index": 0.5, "interaction_shannon": 2.0, "plant_niche_overlap": 3.0},
        {"island": "large", "capacity_index": 0.0, "interaction_shannon": 3.0, "plant_niche_overlap": 2.0},
    ]
    shannon = module.pairwise_concordance(rows, "interaction_shannon", "decrease")
    overlap = module.pairwise_concordance(rows, "plant_niche_overlap", "increase")
    assert shannon["concordant_pairs"] == 3
    assert shannon["discordant_pairs"] == 0
    assert overlap["concordant_pairs"] == 3
    assert overlap["discordant_pairs"] == 0
