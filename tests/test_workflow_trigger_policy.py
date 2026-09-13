from __future__ import annotations

import re
from pathlib import Path


WORKFLOW_DIR = Path(".github/workflows")
AUTOMATIC_WORKFLOWS = {"ci.yml", "chapter2-scientific-gate.yml"}
EVENT_RE = re.compile(r"\b(push|pull_request|workflow_dispatch|schedule|workflow_call|workflow_run)\b")
TOP_LEVEL_EVENT_RE = re.compile(r"^  ([A-Za-z0-9_-]+)\s*:")


def _trigger_block(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.startswith(("on:", "'on':", '"on":')):
            start = index
            break
    else:
        raise AssertionError(f"{path}: missing top-level on block")

    if lines[start].split(":", 1)[1].strip():
        return [lines[start]]

    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith((" ", "\t", "#")):
            break
        end += 1
    return lines[start:end]


def _events(path: Path) -> set[str]:
    block = _trigger_block(path)
    if len(block) == 1:
        return set(EVENT_RE.findall(block[0]))

    events: set[str] = set()
    for line in block[1:]:
        match = TOP_LEVEL_EVENT_RE.match(line)
        if match:
            events.add(match.group(1))
    return events


def test_pull_request_signal_is_limited_to_current_ci_surfaces() -> None:
    workflows = sorted((*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml")))
    assert workflows
    assert not (WORKFLOW_DIR / "workflow-trigger-migration.yml").exists()

    seen_automatic: set[str] = set()
    for path in workflows:
        events = _events(path)
        if path.name in AUTOMATIC_WORKFLOWS:
            assert "pull_request" in events, (path.name, events)
            assert "push" in events, (path.name, events)
            seen_automatic.add(path.name)
        else:
            assert events == {"workflow_dispatch"}, (path.name, events)

    assert seen_automatic == AUTOMATIC_WORKFLOWS
