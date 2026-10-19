"""Guard normal CI against reintroducing unreachable PR #420-only jobs.

This is workflow hygiene. Original K32 sources, frozen readouts, and original
Git/Actions provenance remain outside the current shared CI.
PR #597 adds an explicitly bounded, same-repository Q3 engineering DAG.
Keep its allowlist and limits explicit instead of permitting arbitrary jobs.
"""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github/workflows/ci.yml"
GATE = ROOT / ".github/workflows/chapter2-scientific-gate.yml"
PROVENANCE = ROOT / "docs/CI_PR420_RETIRED_JOB_PROVENANCE_20261015.md"


def test_general_matrix_and_explicitly_gated_q3_jobs_are_only_active_ci_jobs():
    text = CI.read_text(encoding="utf-8")
    assert text.startswith("name: CI\n")
    jobs = text.split("jobs:\n", 1)[1]
    names = re.findall(r"^  ([a-zA-Z][\w-]*):\s*$", jobs, flags=re.MULTILINE)
    assert names == ["tests", "q3-prepare", "q3-worker", "q3-collect"]
    _assert_q3_topology(text)
    assert "python-version: ['3.10', '3.11', '3.12']" in jobs
    assert "python -m pip install -e '.[dev]'" in jobs
    assert "pytest -q --junitxml=" in jobs
    assert "test ${PIPESTATUS[0]} -eq 0" in jobs
    assert "Upload pytest reports on failure" in jobs
    assert "cancel-in-progress: true" in text


def test_closed_pr420_never_gates_current_workflows():
    ci_text = CI.read_text(encoding="utf-8")
    assert "github.event.pull_request.number == 420" not in ci_text
    assert "model3-k32-" not in ci_text
    assert "on:\n  push:\n    branches: [main]\n  pull_request:" in ci_text
    gate = GATE.read_text(encoding="utf-8")
    assert "name: Chapter 2 scientific gate" in gate
    assert "test_chapter2_unified_el_review_bundle_20261010.py" in gate


def test_historical_provenance_links_original_workflow_and_exact_20_jobs():
    doc = PROVENANCE.read_text(encoding="utf-8")
    original_jobs = set(re.findall(r"`(model3-k32-[a-z-]+)`", doc))
    assert len(original_jobs) == 20
    assert "ae91c6aaf66637b23db14067eb08d135cb9f4172" in doc
    assert "264ed7d7185d6c205b6f02c019dd15bddfee982b" in doc
    assert "PR #420" in doc
    assert "no original Model 3" in doc.lower() or "No original Model 3" in doc



def _assert_q3_topology(text):
    """Static contract for this exact approved engineering workflow, not all YAML."""
    entries = list(re.finditer(r"^  ([a-zA-Z][\w-]*):[ \t]*$",
                              text.split("jobs:\n", 1)[1], re.MULTILINE))
    jobs = text.split("jobs:\n", 1)[1]
    assert [m.group(1) for m in entries] == [
        "tests", "q3-prepare", "q3-worker", "q3-collect"]
    blocks = {m.group(1): jobs[m.end():entries[i+1].start()
                              if i+1 < len(entries) else len(jobs)]
              for i, m in enumerate(entries)}
    gate = blocks["q3-prepare"].split("runs-on:", 1)[0]
    assert " ".join(gate.split()) == (
        "if: >- github.event_name == 'pull_request' && "
        "github.event.pull_request.number == 597 && "
        "github.event.pull_request.head.repo.full_name == github.repository")
    for name in ("q3-prepare", "q3-worker", "q3-collect"):
        b = blocks[name]
        head = b.split("    steps:\n", 1)[0]
        assert "    runs-on: ubuntu-24.04\n" in head
        assert "    timeout-minutes: 20\n" in head
        assert "    permissions:\n      contents: read\n      actions: read\n" in head
        assert not re.search(r"^\s+[^:#]+:\s*(?:write|write-all)\s*$", head, re.MULTILINE)
        assert "continue-on-error:" not in b
        assert "persist-credentials: false" in b
        assert "numpy==2.2.6 scipy==1.15.3" in b
        if name != "q3-prepare":
            assert not re.search(r"^    if:", head, re.MULTILINE)
            assert "ref: ${{ needs.q3-prepare.outputs.source }}" in b
            assert "python-version: ${{ needs.q3-prepare.outputs.python }}" in b
    assert "ref: ${{ github.event.pull_request.head.sha }}" in blocks["q3-prepare"]
    worker = blocks["q3-worker"]
    assert "    needs: q3-prepare\n" in worker
    assert "      max-parallel: 3\n" in worker
    assert "        shard: [0, 1, 2]\n" in worker
    assert "--max-updates 48" in worker
    assert "assert d['new_updates']==0 and d['complete']" in worker
    collect = blocks["q3-collect"]
    assert "    needs: [q3-prepare, q3-worker]\n" in collect
    assert "{'shard-0.zip','shard-1.zip','shard-2.zip'}" in collect
    assert "python -m scripts.audit_q3_native_pipeline_20261019" in collect
    assert "assert a['confirmation_seeds_consumed']==0" in collect
    assert "cmp Q3_COLLECTION.json Q3_RECOLLECTION.json" in collect


def test_new_q3_jobs_cannot_restore_retired_or_unreviewed_jobs():
    text = CI.read_text(encoding="utf-8")
    for name in ("model3-k32-replay", "unexpected-production"):
        with pytest.raises(AssertionError):
            _assert_q3_topology(text + f"\n  {name}:\n    runs-on: ubuntu-latest\n")


@pytest.mark.parametrize("before,after", [
    ("github.event.pull_request.number == 597 &&", "true &&"),
    ("github.event.pull_request.head.repo.full_name == github.repository", "true"),
    ("      max-parallel: 3", "      max-parallel: 32"),
    ("        shard: [0, 1, 2]", "        shard: [0, 1, 2, 3]"),
    ("    needs: [q3-prepare, q3-worker]", "    needs: q3-prepare"),
    ("      actions: read", "      actions: write"),
    ("          persist-credentials: false", "          persist-credentials: true"),
    ("assert a['confirmation_seeds_consumed']==0", "assert True"),
    ("    timeout-minutes: 20", "    timeout-minutes: 360"),
])
def test_q3_limits_and_source_pairing_cannot_be_silently_relaxed(before, after):
    text = CI.read_text(encoding="utf-8")
    assert before in text
    with pytest.raises(AssertionError):
        _assert_q3_topology(text.replace(before, after))
