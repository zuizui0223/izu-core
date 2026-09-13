from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRODUCE = ROOT / "REPRODUCE.md"


def test_documented_pytest_targets_exist() -> None:
    text = REPRODUCE.read_text(encoding="utf-8")
    invocations = re.findall(r"^pytest\s+-q\s+(.+)$", text, flags=re.MULTILINE)
    assert invocations

    documented_targets = []
    for invocation in invocations:
        for token in invocation.split():
            if token.startswith("tests/"):
                documented_targets.append(token.split("::", 1)[0])

    assert documented_targets
    for target in documented_targets:
        assert (ROOT / target).is_file(), f"REPRODUCE.md points to missing pytest target: {target}"


def test_documented_script_module_entrypoints_exist() -> None:
    text = REPRODUCE.read_text(encoding="utf-8")
    modules = re.findall(r"^python\s+-m\s+(scripts\.[A-Za-z0-9_.]+)\b", text, flags=re.MULTILINE)
    assert modules

    for module in modules:
        path = ROOT / (module.replace(".", "/") + ".py")
        assert path.is_file(), f"REPRODUCE.md points to missing module: {module}"
