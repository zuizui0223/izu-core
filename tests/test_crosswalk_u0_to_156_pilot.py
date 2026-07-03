"""Small tests for U0-to-pilot crosswalk helpers."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "crosswalk_u0_to_156_pilot.py"


def load_module():
    spec = importlib.util.spec_from_file_location("crosswalk_u0_to_156_pilot", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_normalise_is_case_and_space_insensitive():
    module = load_module()
    assert module.normalise("  Weigela   coraeensis ") == "weigela coraeensis"


def test_normalise_keeps_taxonomic_tokens():
    module = load_module()
    assert module.normalise("Lilium auratum") != module.normalise("Lilium maculatum")
