"""Build an unapproved source-bound candidate; this command never grants approval."""
import argparse
from pathlib import Path
import re

from q3_triangle_contract_20261014 import NAMESPACE, require
from q3_triangle_execution_gate_20261014 import (
    SOURCE_FILES, LIMITS, PREFLIGHT_SHA, DESIGN_SHA, ARCHIVE_SHA, digest, exclusive_json)


def build_candidate(repo, reviewed_commit):
    repo = Path(repo)
    require(re.fullmatch('[0-9a-f]{40}', reviewed_commit) is not None, 'reviewed commit identity')
    require(digest(repo/'data/designs/q3_triangle_preflight_20261014.json') == PREFLIGHT_SHA,
            'preflight identity')
    require(digest(repo/'docs/CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md') == DESIGN_SHA,
            'design identity')
    return dict(approved=False, namespace=NAMESPACE, reviewed_commit=reviewed_commit,
                approval=dict(scope=NAMESPACE, reference=''),
                preflight_sha256=PREFLIGHT_SHA, design_sha256=DESIGN_SHA, archive_sha256=ARCHIVE_SHA,
                code_sha256={name: digest(repo/name) for name in SOURCE_FILES}, limits=LIMITS.copy(),
                python='3.11.14', numpy='2.2.6')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, type=Path)
    p.add_argument('--reviewed-commit', required=True)
    p.add_argument('--out', required=True, type=Path)
    a = p.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    exclusive_json(a.out, build_candidate(a.repo, a.reviewed_commit))


if __name__ == '__main__':
    main()
