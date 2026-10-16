"""Exercise receipt verification without rerunning native scientific arithmetic."""
import copy
import json
import sys

import pytest

from scripts import audit_chapter2_Q2_original_F1_focal_return_20261015 as audit


@pytest.mark.parametrize("damage", ["none", "nan", "summary", "truncated"])
def test_check_requires_complete_finite_record(tmp_path, monkeypatch, capsys, damage):
    current = json.loads(audit.OUTPUT.read_text(encoding="utf-8"))
    saved = copy.deepcopy(current)
    if damage == "nan":
        saved["native_four_corner_rows"][0]["static_focal_expected_returns_by_sign"]["A_up_I_down"]["parental_genome_W"] = float("nan")
    elif damage == "summary":
        saved["context_mean_W_summary"] = {"incorrect": "altered summary"}
    elif damage == "truncated":
        saved["native_four_corner_rows"].pop()
    path = tmp_path / "saved.json"
    path.write_text(json.dumps(saved), encoding="utf-8")
    monkeypatch.setattr(audit, "OUTPUT", path)
    monkeypatch.setattr(audit, "audit", lambda: current)
    monkeypatch.setattr(sys, "argv", ["audit", "--check"])
    if damage == "none":
        audit.main()
        assert "PASS:" in capsys.readouterr().out
    else:
        with pytest.raises(SystemExit):
            audit.main()
        assert "PASS:" not in capsys.readouterr().out
