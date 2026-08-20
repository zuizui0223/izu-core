from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/diagnose_abm_v4_dense_pair_support.py"


def load_script():
    spec = importlib.util.spec_from_file_location("dense_pair_support_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_v4_pair_support_has_strict_positive_lower_bound():
    module = load_script()
    expected = math.exp(-((1.0 / 0.16) ** 2)) * 0.82
    assert module.minimum_possible_positive_encounter_score() == expected
    assert expected > 0.0


def test_diagnosis_identifies_complete_bipartite_support_and_pair_support_gap():
    module = load_script()
    result = module.build()
    assert result["strictly_positive_for_every_finite_plant_pollinator_pair"] is True
    assert "complete bipartite" in result["consequence"]["positive_v4_weighted_network_support"]
    assert "cannot make any positive plant row partnerless" in result["consequence"]["v6_nonempty_column_mask"]
    assert "pair-level interaction support" in result["next_mechanism_constraint"]
    assert result["empirical_inputs_loaded"] == []
