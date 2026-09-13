from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
KEEP_AUTOMATIC = {"ci.yml", "chapter2-scientific-gate.yml"}
MIGRATION = WORKFLOWS / "workflow-trigger-migration.yml"


def _trigger_block(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.startswith(("on:", "'on':", '"on":')):
            start = index
            break
    else:
        raise AssertionError(f"{path}: missing top-level on: block")

    if lines[start].split(":", 1)[1].strip():
        return [lines[start]]

    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith((" ", "\t", "#")):
            break
        end += 1
    return lines[start:end]


def _events(block: list[str]) -> set[str]:
    if len(block) == 1 and block[0].split(":", 1)[1].strip():
        return set(
            re.findall(
                r"\b(?:push|pull_request|workflow_dispatch|schedule|workflow_call)\b",
                block[0],
            )
        )

    found: set[str] = set()
    for line in block[1:]:
        match = re.match(r"^  ([A-Za-z0-9_-]+)\s*:", line)
        if match:
            found.add(match.group(1))
    return found


def test_only_current_chapter_checks_run_automatically() -> None:
    if MIGRATION.exists():
        pytest.skip("one-shot workflow trigger migration is still in progress")

    workflows = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    assert {path.name for path in workflows}.issuperset(KEEP_AUTOMATIC)

    for path in workflows:
        events = _events(_trigger_block(path))
        if path.name in KEEP_AUTOMATIC:
            assert "pull_request" in events, (path.name, events)
        else:
            assert events == {"workflow_dispatch"}, (path.name, events)
