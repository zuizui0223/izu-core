import json
import warnings
from pathlib import Path

from scripts.run_chapter2_trait_accessibility_pilot import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_accessibility_pilot_20261002.json"


def test_prospectively_frozen_trait_accessibility_pilot() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_pilot_frozen_before_execution"
    assert design["operator"]["operator_changes_allowed"] is False
    assert design["operator"]["mutation_rate"] == 0.0

    result = run(design)

    # Prospectively declared prediction. Failure is a scientific result; do not
    # weaken this assertion after inspecting the output.
    compact_b = {
        "contrasts": result["contrasts"],
        "rows": result["rows"],
    }
    warnings.warn("STAGE_B_NUMERIC " + json.dumps(compact_b, sort_keys=True))
    assert result["standing_variation_filter_supported"] is True
