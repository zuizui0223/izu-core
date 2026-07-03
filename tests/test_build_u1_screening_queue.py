"""Tests for U1 search-queue ranking."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "build_u1_screening_queue.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_u1_screening_queue", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_boundary_coverage_outweighs_equal_availability_without_ecology():
    module = load_module()
    boundary_row = {"n_islands": "4", "total_occ": "20", "Oshima_present": "yes", "Toshima_present": "yes", "Hachijo_present": "no"}
    no_boundary_row = {"n_islands": "4", "total_occ": "20", "Oshima_present": "yes", "Toshima_present": "no", "Hachijo_present": "no"}
    boundary_score, boundary_reason = module.priority(boundary_row)
    no_boundary_score, no_boundary_reason = module.priority(no_boundary_row)
    assert boundary_score > no_boundary_score
    assert "Oshima-Toshima boundary" in boundary_reason
    assert "Oshima-Toshima boundary" not in no_boundary_reason


def test_more_islands_rank_higher_than_more_records_when_difference_is_large():
    module = load_module()
    high_coverage = {"n_islands": "5", "total_occ": "5", "Oshima_present": "no", "Toshima_present": "no", "Hachijo_present": "no"}
    low_coverage = {"n_islands": "2", "total_occ": "100000", "Oshima_present": "no", "Toshima_present": "no", "Hachijo_present": "no"}
    assert module.priority(high_coverage)[0] > module.priority(low_coverage)[0]
