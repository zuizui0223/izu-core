"""CLI admission must not depend on Python optimization or import side effects."""
import csv
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _python(code, *arguments, optimized=False):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    command = [sys.executable] + (["-O"] if optimized else [])
    return subprocess.run(command + ["-c", code, *map(str, arguments)],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          encoding="utf-8", timeout=90)


@pytest.mark.parametrize("optimized", [False, True])
@pytest.mark.parametrize("module, attribute, change, message", [
    ("figure_model3_return_components", "SOURCE", "status", "Return-component summary"),
    ("figure_model3_trait_pollen", "SOURCE", "status", "Trait-pollen summary"),
    ("figure_model3_assurance_compression", "GENERALITY", "adjudication", "Generality results"),
    ("figure_model3_assurance_compression", "ARM", "status", "Arm decomposition"),
    ("figure_model3_assurance_compression", "GRADIENT", "status", "Gradient diagnostic"),
    ("figure_model3_assurance_compression", "GENERALITY", "settings", "expected four settings"),
])
def test_figure_rejects_unadmitted_input_before_writing(
    tmp_path, optimized, module, attribute, change, message
):
    # Keep realistic, otherwise renderable inputs; corrupt only admission metadata
    # or remove one registered setting. All writes stay in the temporary directory.
    result = _python("""
import importlib, json, sys
from pathlib import Path
module, attribute, change, directory = sys.argv[1:]
m = importlib.import_module('scripts.' + module)
root = Path(directory)
payload = json.loads(getattr(m, attribute).read_text(encoding='utf-8'))
if change == 'adjudication':
    payload['adjudication']['status'] = 'incomplete'
elif change == 'settings':
    payload['settings'].pop()
else:
    payload['status'] = 'incomplete'
fixture = root / 'invalid.json'
fixture.write_text(json.dumps(payload), encoding='utf-8')
setattr(m, attribute, fixture)
m.OUT = root / 'rendered'
m.main()
""", module, attribute, change, tmp_path, optimized=optimized)
    assert result.returncode != 0
    assert "ValueError:" in result.stderr, result.stderr
    assert message in result.stderr
    assert not (tmp_path / "rendered").exists()


def test_genetic_figure_import_does_not_read_data_or_render():
    result = _python("""
from pathlib import Path
from unittest.mock import patch
import numpy
with patch.object(Path, 'read_text', side_effect=RuntimeError('read at import')), \
     patch.object(Path, 'mkdir', side_effect=RuntimeError('write at import')):
    from scripts import figure_model3_genetic_realization_safe as figure
if not callable(figure.main):
    raise RuntimeError('missing command entrypoint')
""")
    assert result.returncode == 0, result.stderr


def test_genetic_figure_command_preserves_source_values(tmp_path):
    result = _python("""
import sys
from pathlib import Path
from scripts import figure_model3_genetic_realization_safe as figure
figure.OUT = Path(sys.argv[1])
figure.main()
""", tmp_path)
    assert result.returncode == 0, result.stderr
    assert str(tmp_path) in result.stdout
    for suffix in ("png", "svg", "pdf"):
        assert (tmp_path / f"genetic_realization.{suffix}").stat().st_size > 1000
    with (tmp_path / "plotted_values.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    bridge = json.loads((ROOT / "data/results/model3_ch2_bridge_summary_20260927/summary.json").read_text(encoding="utf-8"))["campaigns"]["main"]["pairs"]
    variability = json.loads((ROOT / "data/results/model3_mutation_variability_20261005.json").read_text(encoding="utf-8"))["rows"]
    for row in rows:
        if row["panel"] == "A":
            source = bridge[row["condition"]][row["model"]]
            value, interval = source["mean"], source["mean_ci"]
        else:
            measure = "allele_count" if row["panel"] == "B" else "last100_change"
            source = next(r for r in variability
                          if r["capacity"] == int(row["capacity"])
                          and r["mutation_rate"] == float(row["mutation"])
                          and r["past"] == row["past"] and r["measure"] == measure)
            value, interval = source["mean"], source["descriptive_bootstrap_95"]
        assert float(row["value"]) == pytest.approx(value, abs=1e-13)
        assert [float(row["lower"]), float(row["upper"])] == interval
    receipt = json.loads((tmp_path / "provenance.json").read_text(encoding="utf-8"))
    assert receipt["rows"] == len(rows)
    assert receipt["scope"] == "existing result visualization; no re-estimation or new simulation"
