from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_martinique_2025_author_r_reconstruction_semantics.py"


def load_script():
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("martinique_author_r_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_author_r_audit_is_target_free():
    text = SCRIPT.read_text().lower()
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita" not in text
    assert "predictive" not in text.replace("v9 prediction", "")


def test_num_sp_aggregation_is_only_flagged_when_explicit():
    module = load_script()
    matches = [
        {"line": 1, "text": "x <- df$Num_sp"},
        {"line": 2, "text": "y <- sum(df$Num_sp)"},
        {"line": 3, "text": "filter(df, Num_sp != 'NA')"},
    ]
    result = module.num_sp_use_class(matches)
    assert result["num_sp_reference_count"] == 3
    assert len(result["aggregation_like_num_sp_lines"]) == 1
    assert len(result["filter_like_num_sp_lines"]) >= 1


def test_structural_match_returns_context_lines_without_executing_r():
    module = load_script()
    text = "a <- 1\nraw <- read.csv('x')\nraw$Num_sp <- raw$Num_sp\nz <- group_by(raw, Site, Period)\nq <- 2\n"
    matches = module.structural_matches(text)
    lines = {row["line"] for row in matches}
    assert 3 in lines
    assert 4 in lines
