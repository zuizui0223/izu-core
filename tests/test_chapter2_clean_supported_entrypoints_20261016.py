"""Minimal package/CLI cleanup contract, separate from frozen biology.

Previously pyproject.toml declared zero base dependencies even though
scripts.model3_island.run uses numpy, scipy, psutil and threadpoolctl.
"""
from __future__ import annotations

import ast
import importlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _toml_python_literal(section: str, field: str):
    source = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    block = source.split("[" + section + "]\n", 1)[1].split("\n[", 1)[0]
    match = re.search(r"(?m)^" + re.escape(field) + r"\s*=\s*(\[.*\]|\".*\")$", block)
    assert match, (section, field)
    return ast.literal_eval(match.group(1))


def test_main_model3_numerical_runtime_deps_not_hidden_in_dev_extras():
    dependencies = _toml_python_literal("project", "dependencies")
    names = {item.split(">", 1)[0].split("<", 1)[0].split("=", 1)[0] for item in dependencies}
    assert names == {"numpy", "scipy", "psutil", "threadpoolctl"}
    # Keep figure dependencies optional for numerical-only installs.
    plotting = _toml_python_literal("project.optional-dependencies", "plotting")
    assert plotting == ["matplotlib>=3.8"]
    dev = _toml_python_literal("project.optional-dependencies", "dev")
    assert {"pytest", "pandas", "matplotlib"}.issubset({v.split(">",1)[0] for v in dev})
    assert names.isdisjoint({v.split(">",1)[0] for v in dev})


def test_readonly_cli_targets_exist_but_frozen_producers_are_not_console_scripts():
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    section = project.split("[project.scripts]\n", 1)[1].split("\n[", 1)[0]
    actual = dict(re.findall(r'^([a-z][a-z-]+)\s*=\s*"([\w.]+:[\w]+)"\s*$', section, re.M))
    expected = {
        "izu-core-source-audit": "scripts.audit_chapter2_repository_wide_static_20261016:main",
        "izu-core-q4-contract": "scripts.audit_chapter2_q4_post_mutation_contract_20261016:main",
        "izu-core-q1-readout": "scripts.summarize_chapter2_q1_fresh_founders_20261016:main",
    }
    assert actual == expected
    for entry in actual.values():
        module, _, method = entry.partition(":")
        target = importlib.import_module(module)
        assert callable(getattr(target, method))
    assert "run_chapter2_assurance_generality" not in section
    assert "run_chapter2_q1_fresh_founders_20261016" not in section
