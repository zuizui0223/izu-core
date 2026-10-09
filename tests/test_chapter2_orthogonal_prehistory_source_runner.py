"""No new biological histories are ever simulated by these tests."""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from scripts.chapter2_orthogonal_cohort_manifest import tasks
from scripts.chapter2_orthogonal_prehistory_source_runner import (
    prospective_biological_design, main,
)
from scripts.plan_chapter2_order_expression_identification import load_protocol


def test_new_history_range_and_unchanged_canonical_biology():
    original = load_protocol()
    prospective = prospective_biological_design()
    assert prospective["independent_histories"] == {
        "first": 39110901,
        "last": 39110964,
        "count": 64,
        "unit": "visitor_history",
        "new_not_reused": True,
    }
    assert prospective["nested_demographic_repeats"] == [39111901, 39111902]
    assert prospective["prehistory"] == original["prehistory"]
    assert prospective["path_perturbation"] == original["path_perturbation"]
    assert prospective["reproductive_settings"] == original["reproductive_settings"]
    assert prospective["environmental_settings"] == original["environmental_settings"]
    assert [len(group) for group in tasks()] == [32] * 64


def test_dry_run_never_executes_history_or_writes_results(monkeypatch, capsys, tmp_path):
    import scripts.chapter2_orthogonal_prehistory_source_runner as runner

    def forbidden(*args, **kwargs):
        raise AssertionError("Dry-run must never simulate the biological model")

    monkeypatch.setattr(runner, "simulate_prehistory", forbidden)
    monkeypatch.setattr(runner, "run_shard", forbidden)
    monkeypatch.setattr("sys.argv", [
        "orthogonal-runner", "--shard-index", "0", "--dry-run",
        "--out", str(tmp_path / "never-created"),
    ])
    main()
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "status": "PLAN_ONLY_NO_BIOLOGY",
        "shard": 0,
        "sources": 32,
        "scientific_outcomes_generated": False,
    }
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("flags", [[], ["--execute-frozen-cohort"],
                                    ["--acknowledge-resource-cost"]])
def test_production_requires_explicit_dual_opt_in(monkeypatch, flags):
    monkeypatch.setattr("sys.argv", [
        "orthogonal-runner", "--shard-index", "0", *flags,
    ])
    with pytest.raises(PermissionError, match="dual opt-in"):
        main()


def test_historical_biology_is_not_modified_by_new_production_source():
    source = Path("scripts/chapter2_orthogonal_prehistory_source_runner.py").read_text()
    tree = ast.parse(source)
    # The opt-in prehistory runner must be explicit, never execute on import.
    import_simulations = [
        n for n in tree.body
        if isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Call)
        and isinstance(n.value.func, ast.Name)
        and n.value.func.id in {"simulate_prehistory", "run_shard"}
    ]
    assert not import_simulations
    assert 'if __name__ == "__main__":' in source
    assert "RAW_T400_32_SOURCE_SHARD_NOT_ADJUDICATED" in source
    assert "restore_prehistory" in source
