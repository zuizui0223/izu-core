from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v12_residual_trait_causes.py"
NOTE = ROOT / "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md"


def load_v12():
    spec = importlib.util.spec_from_file_location("h2_sign_decomposition_v12", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sign(x: float, eps: float = 1e-12) -> int:
    if x > eps:
        return 1
    if x < -eps:
        return -1
    return 0


def test_v12_fixed_endpoint_parameters_match_analytical_note():
    v12 = load_v12()
    assert v12.COMMON_DEPENDENCY == 0.65
    assert v12.INITIAL_ASSURANCE == 0.08
    assert v12.FIXED_ASSURANCE_RESPONSIVENESS == 0.0


def test_reproduction_sign_preserves_functional_opportunity_sign():
    v12 = load_v12()
    opportunity_pairs = [
        (0.05, 0.20),
        (0.20, 0.05),
        (0.35, 0.35),
        (0.15, 0.90),
        (0.90, 0.15),
    ]
    for saturation in (1.0, 2.0, 3.0):
        for assurance_ceiling in (0.1, 0.5, 0.9):
            for mainland_o, island_o in opportunity_pairs:
                mainland_r = v12.reproduction_from_row(
                    (mainland_o,),
                    saturation=saturation,
                    assurance_ceiling=assurance_ceiling,
                )
                island_r = v12.reproduction_from_row(
                    (island_o,),
                    saturation=saturation,
                    assurance_ceiling=assurance_ceiling,
                )
                assert sign(island_r - mainland_r) == sign(island_o - mainland_o)


def test_algebraic_coefficient_is_strictly_positive_over_declared_ceiling_range():
    d = 0.65
    initial_assurance = 0.08
    for ceiling in (0.1, 0.5, 0.9):
        autonomous = ceiling * initial_assurance
        assurance_route = (1.0 - d) * autonomous
        coefficient = d * (1.0 - assurance_route)
        assert coefficient > 0.0
        assert math.isfinite(coefficient)


def test_note_states_exact_identity_and_preserves_claim_boundary():
    text = NOTE.read_text(encoding="utf-8")
    assert "sign(Delta R_i)" in text
    assert "sign(Delta S_i)" in text
    assert "sign(Delta O_i)" in text
    assert "cannot manufacture a reproductive sign reversal" in text
    assert "does **not** show that arbitrary heterogeneity" in text
    assert "does not assign the synthetic coordinate to a named empirical trait" in text
