from __future__ import annotations

import re
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRODUCE = ROOT / "REPRODUCE.md"
SCIENTIFIC_GATE = ROOT / ".github/workflows/chapter2-scientific-gate.yml"
MODULE_RE = re.compile(r"^\s*python\s+-m\s+(scripts\.[A-Za-z0-9_.]+)\b", re.MULTILINE)
COMMAND_RE = re.compile(
    r"^[ \t]*python\s+-m\s+scripts\.[A-Za-z0-9_.]+\b[^\n]*$",
    re.MULTILINE,
)
PATH_FLAGS = {"--out", "--phase1", "--joint", "--thresholds"}


def _collapse_shell_continuations(text: str) -> str:
    return re.sub(r"\\\n[ \t]*", " ", text)


def _commands(text: str) -> list[str]:
    return [line.strip() for line in COMMAND_RE.findall(_collapse_shell_continuations(text))]


def _semantic_tokens(command: str) -> list[str]:
    tokens = shlex.split(command)
    normalized: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        normalized.append(token)
        if token in PATH_FLAGS:
            if index + 1 >= len(tokens):
                raise AssertionError(f"missing value after {token}: {command}")
            normalized.append("<PATH>")
            index += 2
        else:
            index += 1
    return normalized


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
    modules = MODULE_RE.findall(text)
    assert modules

    for module in modules:
        path = ROOT / (module.replace(".", "/") + ".py")
        assert path.is_file(), f"REPRODUCE.md points to missing module: {module}"


def test_documented_full_gate_matches_workflow_semantics() -> None:
    text = REPRODUCE.read_text(encoding="utf-8")
    section = re.search(
        r"For the full current Chapter 2 scientific gate.*?```bash\n(.*?)\n```",
        text,
        flags=re.DOTALL,
    )
    assert section, "REPRODUCE.md is missing the full scientific-gate command block"

    documented = _commands(section.group(1))
    workflow = _commands(SCIENTIFIC_GATE.read_text(encoding="utf-8"))

    assert len(documented) == 6
    assert len(workflow) == 6
    assert [_semantic_tokens(command) for command in documented] == [
        _semantic_tokens(command) for command in workflow
    ]
