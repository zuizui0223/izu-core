"""Receipt checks reject damaged records without running scientific arithmetic."""
import copy
import json
import sys

import pytest

from scripts import audit_chapter2_original_F1_signed_quadrant_null_20261015 as audit


@pytest.mark.parametrize("damage", ["truncated", "nan", "metadata", "none"])
def test_check_compares_complete_finite_record(tmp_path, monkeypatch, damage, capsys):
    current = {"status": "source_fixture", "new_biological_trajectories": 0,
               "contexts": [{"context": 0, "m0_signed_events": {k: 0.0 for k in audit.SIGNED_CELLS},
                             "m6_signed_events": {k: 0.125 for k in audit.SIGNED_CELLS}}]}
    saved = copy.deepcopy(current)
    if damage == "truncated": saved["contexts"] = []
    if damage == "nan": saved["contexts"][0]["m6_signed_events"][audit.SIGNED_CELLS[0]] = float("nan")
    if damage == "metadata": saved["new_biological_trajectories"] = 99
    path = tmp_path / "saved.json"
    path.write_text(json.dumps(saved), encoding="utf-8")
    monkeypatch.setattr(audit, "OUTPUT", path)
    monkeypatch.setattr(audit, "audit", lambda: current)
    monkeypatch.setattr(sys, "argv", ["audit", "--check"])
    if damage == "none":
        audit.main()
        assert "PASS:" in capsys.readouterr().out
    else:
        with pytest.raises(SystemExit, match="source record differs"):
            audit.main()
        assert "PASS:" not in capsys.readouterr().out
