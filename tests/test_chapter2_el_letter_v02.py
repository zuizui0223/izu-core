import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_EL_LETTER_DRAFT_V0_2_20260913.md"
DIAG = ROOT / "data/results/chapter2_el_keff2_continuous_contour_diagnostic_20260913.json"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def test_el_v02_format_limits_and_surface():
    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()
    abstract = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords:", text, re.S).group(1)
    main = re.search(r"## Introduction\n\n(.*?)\n\n## Data and code availability", text, re.S).group(1)
    running = re.search(r"\*\*Running title:\*\* (.*?)\s*$", text, re.M).group(1).strip()
    keywords = re.search(r"\*\*Keywords:\*\* (.*?)\n", text).group(1).split(";")

    assert _word_count(abstract) <= 150
    assert _word_count(main) <= 5000
    assert len(running) < 45
    assert len(keywords) <= 10
    assert text.count("**Figure ") == 4
    assert "sufficient statistic" not in lower
    assert "dense grid" not in lower
    assert "post hoc" in lower or "post-hoc" in lower
    assert "natural richness threshold" in lower
    assert "effective independence alone does not determine nonlinear ecological response" in lower


def test_same_keff_continuous_diagnostic_is_primary_not_tie_break():
    payload = json.loads(DIAG.read_text(encoding="utf-8"))
    comparison = payload["comparison"]
    first = comparison["first_point"]
    last = comparison["last_point"]

    assert payload["target_k_eff"] == 2.0
    assert comparison["L1_distance_SCI"] > 0.30
    assert abs(comparison["delta_last_minus_first"]["C"]) > 0.15
    assert comparison["delta_last_minus_first"]["I"] > 0.08
    assert first["I_minus_C"] < 0.0
    assert last["I_minus_C"] > 0.20
    assert first["seed_order_counts"] == {"CIS": 3, "ICS": 3}
    assert last["seed_order_counts"] == {"ICS": 6}
    assert "illustrative only" in payload["interpretation"]["categorical_order_role"]
