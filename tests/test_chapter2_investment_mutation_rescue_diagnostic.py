import json
import warnings
from pathlib import Path

from scripts.run_chapter2_investment_mutation_rescue_diagnostic import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_investment_mutation_rescue_diagnostic_20261002.json"


def test_prospectively_frozen_investment_mutation_rescue_diagnostic() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_diagnostic_frozen_before_execution"

    result = run(design)

    # This is a decision-tree diagnostic, not a success gate. All outcomes are
    # scientifically admissible; the frozen contrasts decide the interpretation.
    assert result["n_trajectories"] == 128
    assert set(result["decisions"]) == {
        "standing_variation_bottleneck",
        "de_novo_mutation_rescue",
        "finite_establishment_bottleneck",
    }
    assert all(isinstance(v, bool) for v in result["decisions"].values())
    warnings.warn(
        "MUT_RESCUE_NUMERIC "
        + json.dumps(
            {
                "contrasts": result["contrasts"],
                "decisions": result["decisions"],
                "cell_summary": result["cell_summary"],
            },
            sort_keys=True,
        )
    )
