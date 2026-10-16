"""Read-only AST inventory of all nonlegacy Python source in izu-core.

This is a static risk screen, NOT evidence every numerical algorithm, model
interpretation or historical data artifact has been independently reviewed.
It neither imports arbitrary research modules nor executes 593 scripts.
Flagged code patterns require a human review before being called defects.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_ROOTS = ("scripts", "tests", "data/results", "docs")
RISK_TERMS = (
    "dynamic_code", "unseeded_numpy_rng", "pickle_input", "yaml_unsafe_load",
    "broad_exception_swallowed", "destructive_shell", "archive_extraction",
)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _call_name(node.value) + "." + node.attr
    return ""


def _risk(node: ast.AST) -> str | None:
    if isinstance(node, ast.Call):
        name = _call_name(node.func)
        if name in ("eval", "exec"):
            return "dynamic_code"
        if name in ("np.random.default_rng", "numpy.random.default_rng",
                    "np.random.RandomState", "numpy.random.RandomState"):
            if not node.args and not node.keywords:
                return "unseeded_numpy_rng"
        if name in ("pickle.load", "pickle.loads", "dill.load", "dill.loads",
                    "joblib.load"):
            return "pickle_input"
        if name in ("np.load", "numpy.load"):
            if any(k.arg == "allow_pickle" and isinstance(k.value, ast.Constant)
                   and k.value.value is True for k in node.keywords):
                return "pickle_input"
        if name in ("yaml.load", "ruamel.yaml.load"):
            if not any(k.arg == "Loader" for k in node.keywords):
                return "yaml_unsafe_load"
        if name in ("os.system", "os.popen"):
            return "destructive_shell"
        if name.endswith(".extractall") or name.endswith(".extract"):
            return "archive_extraction"
    if isinstance(node, ast.ExceptHandler) and (
        node.type is None
        or isinstance(node.type, ast.Name) and node.type.id == "Exception"
    ):
        if node.body and all(isinstance(stmt, ast.Pass) for stmt in node.body):
            return "broad_exception_swallowed"
    return None


def scan_source(root: Path = ROOT) -> dict:
    files = sorted({p for directory in AUDIT_ROOTS
                    for p in (root / directory).rglob("*.py")
                    if "__pycache__" not in p.parts and not p.is_symlink()
                    and p.is_file()})
    by_root = Counter()
    total_lines = 0
    findings = defaultdict(list)
    syntax_failures = []
    top_imports = Counter()
    for file in files:
        path = file.relative_to(root).as_posix()
        category = "scripts" if path.startswith("scripts/") else (
            "tests" if path.startswith("tests/") else "support_snapshot")
        by_root[category] += 1
        data = file.read_text(encoding="utf-8")
        total_lines += len(data.splitlines())
        try:
            tree = ast.parse(data, filename=path)
        except (SyntaxError, ValueError) as exc:
            syntax_failures.append({"file": path, "detail": str(exc)})
            continue
        for node in ast.walk(tree):
            tag = _risk(node)
            if tag:
                findings[tag].append({"file": path, "line": getattr(node, "lineno", 0)})
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_imports[alias.name.split(".", 1)[0]] += 1
    return {
        "scope": "All nonlegacy scripts/tests plus data/results and docs Python source",
        "scanned_python_files": len(files),
        "scanned_lines": total_lines,
        "by_kind": dict(by_root),
        "syntax_failures": syntax_failures,
        "risk_counts": {risk: len(findings.get(risk, [])) for risk in RISK_TERMS},
        "risk_examples": {risk: findings.get(risk, [])[:20] for risk in RISK_TERMS},
        "imports_most_common": top_imports.most_common(15),
        "methodological_limits": [
            "Static AST does not check all functions, arrays, statistical decisions or data fidelity",
            "Historical source snapshots may duplicate live source; this is an inventory not independent replications",
            "Pattern flags are not automatically code defects; interpret file contexts separately",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = scan_source()
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out is not None:
        if args.out.exists():
            raise FileExistsError("Do not overwrite existing repository audit")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if report["syntax_failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
