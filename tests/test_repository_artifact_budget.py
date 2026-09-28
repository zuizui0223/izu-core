from __future__ import annotations

import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data/design/repository_artifact_budget_20260928.json"


def _policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _tracked_data_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z", "data"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    rels = [item.decode("utf-8") for item in proc.stdout.split(b"\0") if item]
    return [ROOT / rel for rel in rels if (ROOT / rel).is_file()]


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _ordinary_limit(rel: str, policy: dict) -> int | None:
    thresholds = policy["thresholds_bytes"]
    if rel.startswith("data/design/"):
        return int(thresholds["max_unlisted_design_file"])
    if rel.startswith("data/results/") and rel.endswith(".svg"):
        return int(thresholds["max_unlisted_generated_svg"])
    if rel.startswith("data/results/"):
        return int(thresholds["max_unlisted_result_file"])
    return None


def test_tracked_data_tree_stays_within_submission_budget() -> None:
    policy = _policy()
    total = sum(path.stat().st_size for path in _tracked_data_files())
    assert total <= policy["thresholds_bytes"]["max_tracked_data_tree"], (
        total,
        policy["thresholds_bytes"]["max_tracked_data_tree"],
    )


def test_oversized_designs_results_and_svgs_are_fixed_grandfathered_exceptions() -> None:
    policy = _policy()
    grandfathered = policy["grandfathered_max_bytes"]
    seen: set[str] = set()

    for path in _tracked_data_files():
        rel = _relative(path)
        limit = _ordinary_limit(rel, policy)
        if limit is None:
            continue
        size = path.stat().st_size
        if size <= limit:
            continue
        assert rel in grandfathered, (rel, size, limit)
        assert size <= grandfathered[rel], (rel, size, grandfathered[rel])
        seen.add(rel)

    assert seen == set(grandfathered), (
        "Grandfather list must be exact: remove entries once archived/deleted and "
        "add no new exception without an explicit policy revision.",
        sorted(set(grandfathered) - seen),
        sorted(seen - set(grandfathered)),
    )
