"""Hardening tests for the paper/ meta-analysis pipeline scripts."""

import importlib.util
import pathlib

import pytest

PAPER = pathlib.Path(__file__).resolve().parent.parent / "paper"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, PAPER / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_functional_group_classification_key_species():
    cfg = _load("classify_functional_groups")
    cases = {
        ("Campanula microdonta", "Campanulaceae"): "specialist_bee",
        ("Angelica keiskei", "Apiaceae"): "generalist_open",
        ("Lilium maculatum", "Liliaceae"): "large_flower",
        ("Artemisia princeps", "Asteraceae"): "abiotic_ambig",   # genus override: wind
        ("Aster microcephalus", "Asteraceae"): "generalist_open",  # family default
        ("Dianthus japonicus", "Caryophyllaceae"): "specialist_bee",  # genus override
        ("Camellia japonica", "Theaceae"): "large_flower",       # bird pollination
    }
    for (name, fam), expected in cases.items():
        group, conf, basis = cfg.classify(name, fam)
        assert group == expected, f"{name}: got {group}, want {expected} ({basis})"


def test_all_candidates_classify_no_review():
    cfg = _load("classify_functional_groups")
    import csv
    rows = list(csv.DictReader((PAPER / "izu_entomophilous_candidates.csv").open(encoding="utf-8")))
    assert len(rows) == 156
    groups = [cfg.classify(r["name"], r["family"])[0] for r in rows]
    assert "review" not in groups
    spec = groups.count("specialist_bee")
    gen = groups.count("generalist_open")
    assert spec >= 25 and gen >= 80  # stable moderator contrast


def test_synthesis_polarity_signs():
    ms = _load("meta_synthesis")
    assert ms.polarity("corolla_length", "reduction") == +1
    assert ms.polarity("autonomous_selfing", "increase") == +1
    assert ms.polarity("corolla_size", "enlargement") == -1
    assert ms.polarity("unknown_trait", "reduction") is None


def test_validate_meta_inputs_passes():
    v = _load("validate_meta_inputs")
    v.main()  # exits non-zero (SystemExit) on any integrity failure


def test_quantitative_anchor_is_strong_reduction(capsys):
    ms = _load("meta_synthesis")
    ms.quantitative_anchor()
    out = capsys.readouterr().out
    assert "lnRR=-0.7" in out  # Campanula corolla ~ -54%
