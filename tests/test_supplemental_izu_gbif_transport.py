import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "run_supplemental_izu_gbif.py"
SPEC = importlib.util.spec_from_file_location("_supplemental_transport", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_counterclockwise_reverses_clockwise_exterior_ring() -> None:
    clockwise = [
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (1.0, 0.0),
        (0.0, 0.0),
    ]
    oriented = MODULE._counterclockwise(clockwise)

    assert MODULE._signed_area(clockwise) < 0.0
    assert MODULE._signed_area(oriented) > 0.0
    assert oriented[0] == oriented[-1]


def test_counterclockwise_preserves_valid_ring() -> None:
    counterclockwise = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
        (0.0, 0.0),
    ]
    oriented = MODULE._counterclockwise(counterclockwise)

    assert MODULE._signed_area(oriented) > 0.0
    assert oriented == counterclockwise
