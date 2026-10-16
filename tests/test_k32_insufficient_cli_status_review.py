"""Non-evaluable scientific outcomes remain readable CLI results."""
import importlib
import json
import sys

import pytest


@pytest.mark.parametrize("suffix,runner,status", [
    ("fixed_frequency_heterozygosity", "run_fixed_frequency",
     "INSUFFICIENT_SHARED_ALIVE_SOURCE_PARENT_PATHS"),
    ("heterozygosity_reproductive_channels", "run_channels",
     "NOT_ENOUGH_SURVIVORS"),
    ("self_transmission_curvature", "run_self_curvature",
     "INSUFFICIENT_SOURCE_YEAR8_PARENT_SURVIVORS"),
])
def test_insufficient_survivors_preserve_status_and_exit_normally(
    suffix, runner, status, tmp_path, monkeypatch, capsys
):
    module = importlib.import_module("scripts.audit_model3_k32_" + suffix)
    result = {"status": status, "n": 3}
    monkeypatch.setattr(module, runner, lambda **kwargs: result)
    output = tmp_path / "result.json"
    monkeypatch.setattr(sys, "argv", ["audit", "--out", str(output)])
    module.main()
    assert json.loads(output.read_text()) == result
    summary = json.loads(capsys.readouterr().out)
    assert summary["status"] == status
    assert summary["budget"] == 8.0
