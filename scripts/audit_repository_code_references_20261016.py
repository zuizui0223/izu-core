"""Repository-wide read-only source/reference inventory for safe code cleanup.

No absence-of-reference result is evidence of dead code. Retain original frozen
sources and research archives until their source/DOI references are audited.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FROZEN_PRODUCERS = frozenset({
    "scripts/run_chapter2_assurance_generality.py",
    "scripts/run_chapter2_q1_fresh_founders_20261016.py",
    "scripts/run_chapter2_island_demographic_independent32.py",
})
SCRIPT_PATH = re.compile(r"\bscripts/[A-Za-z0-9_./-]+\.py\b")
SCRIPT_MODULE = re.compile(r"\bscripts(?:\.[A-Za-z_]\w*)+\b")
REFERENCING_SUFFIXES = frozenset({".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt"})
READ_MAX_BYTES = 300_000


def tracked_paths(root: Path):
    root = Path(root)
    if (root / ".git").exists():
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                                capture_output=True, check=True)
        return sorted(Path(v.decode("utf-8")) for v in result.stdout.split(b"\0") if v)
    return sorted(p.relative_to(root) for p in root.rglob("*")
                  if p.is_file() and not p.is_symlink() and ".git" not in p.parts)


def _resolve_module(name: str, sources: set[str]):
    stem = name.replace(".", "/")
    if stem + ".py" in sources:
        return stem + ".py"
    if stem + "/__init__.py" in sources:
        return stem + "/__init__.py"
    return None


def _import_targets(tree: ast.AST, origin: str, sources: set[str]):
    current_package = origin.removesuffix(".py").split("/")[:-1]
    targets = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                depth = len(current_package) - node.level + 1
                if depth < 0:
                    continue
                prefix = ".".join(current_package[:depth])
                name = ".".join(part for part in (prefix, node.module or "") if part)
            else:
                name = node.module or ""
            names = [name] + [name + "." + alias.name for alias in node.names]
        else:
            continue
        for name in names:
            if not name.startswith("scripts."):
                continue
            p = _resolve_module(name, sources)
            if p is not None and p != origin:
                targets.add(p)
    return targets


def audit(root: Path = ROOT):
    root = Path(root)
    all_paths = tracked_paths(root)
    files = {p.as_posix(): root / p for p in all_paths if (root / p).is_file()}
    scripts = {p for p in files if p.startswith("scripts/") and p.endswith(".py")}
    code = {p for p in files if p.endswith(".py") and (
        p.startswith("scripts/") or p.startswith("tests/") or p.startswith("data/results/")
        or p.startswith("docs/"))}
    ref_by = defaultdict(set)
    parse_errors = []
    text_examined = 0
    for p, path in files.items():
        if p.startswith("legacy/") or path.suffix not in REFERENCING_SUFFIXES:
            continue
        if path.stat().st_size > READ_MAX_BYTES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        text_examined += 1
        for match in SCRIPT_PATH.findall(content):
            if match in scripts and match != p:
                ref_by[match].add(p)
        # Documented python -m scripts.module and import strings are references,
        # but a string alone is not proof that the target is used at runtime.
        for name in SCRIPT_MODULE.findall(content):
            ref = _resolve_module(name, scripts)
            if ref is not None and ref != p:
                ref_by[ref].add(p)
        if p not in code:
            continue
        try:
            tree = ast.parse(content, filename=p)
        except (SyntaxError, ValueError) as exc:
            parse_errors.append({"path": p, "reason": str(exc)})
            continue
        for ref in _import_targets(tree, p, scripts):
            ref_by[ref].add(p)

    hashes = defaultdict(list)
    rows = []
    phases = Counter()
    for p in sorted(scripts):
        path = files[p]
        references = sorted(ref_by[p])
        frozen = p.startswith("scripts/model3_island/") or p in FROZEN_PRODUCERS
        if frozen:
            phase = "frozen_model_or_producer_protect"
        elif any(x.startswith(".github/workflows/") for x in references):
            phase = "workflow_reference_check_before_edit"
        elif references:
            phase = "referenced_review_before_edit"
        else:
            phase = "unresolved_do_not_delete"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[digest].append(p)
        phases[phase] += 1
        rows.append({"path": p, "category": phase, "sha256": digest,
                     "references_count": len(references),
                     "references_examples": references[:8],
                     "truncated_references": max(0, len(references)-8)})
    duplicate_groups = [g for g in hashes.values() if len(g) > 1]
    return {
        "scope": "Tracked script files, nonlegacy static imports and bounded text references; read-only",
        "inventory": {"repository_files": len(files), "scripts_python": len(scripts),
                      "tests_python": sum(p.startswith("tests/") and p.endswith(".py") for p in files),
                      "legacy_files": sum(p.startswith("legacy/") for p in files),
                      "workflows": sum(p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml")) for p in files),
                      "reference_text_files_examined": text_examined},
        "categories": dict(sorted(phases.items())),
        "duplicate_byte_identical_groups": sorted(duplicate_groups, key=lambda g: (-len(g), g))[:50],
        "parse_errors": parse_errors,
        "scripts": rows,
        "limits": [
            "No detected reference does not mean unused, safe to delete, or biologically obsolete",
            "Dynamic import, shell construction, external notebooks and private original manifests may be missed",
            "Identical source bytes can represent intentionally separate immutable experiments",
            "Static import/reference counts are not an execution trace, semantic correctness review or cross-host provenance audit",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Refuse to replace existing code-inventory evidence")
    report = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inventory": report["inventory"], "categories": report["categories"],
                      "byte_identical_groups": len(report["duplicate_byte_identical_groups"]),
                      "parse_errors": len(report["parse_errors"])}, indent=2))
    if report["parse_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
