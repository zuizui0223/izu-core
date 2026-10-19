# izu-core code cleanup — Phase 2: complete reference inventory (2026-10-16)

## Objective and status

The repo has 590+ active `scripts/*.py`, 470+ tests, ~40 GitHub Actions workflows, and a large historical `legacy/` tree. A code cleanup that only checks import statements would misclassify research executables called from shell scripts, documentation, manifests or external source receipts.

The **first cleanup PR #572** fixes package dependencies and narrows the supported read-only entrypoints. **This phase** adds a read-only repository-wide script inventory and static-reference map, without deleting or moving any research source.

## Executed engineering

```bash
python -m scripts.audit_repository_code_references_20261016 \
  --out outputs/repository_code_references_20261016.json
pytest -q tests/test_repository_code_references_20261016.py
```

The scan uses `git ls-files` when working in a Git checkout, examines the tracked `scripts/` tree, parses Python AST imports from nonlegacy code, and searches bounded text in tests, workflows, documentation, designs and source notes. It records every script's SHA-256, reference examples and counts, and lists byte-identical script groups for **review only**. It does not import arbitrary analysis modules or execute biological experiments.

**Source-pin gate:** The inventory also recognizes bare SHA-256 and Git blob SHA-1 fingerprints in tracked text without any filename or import. It records fingerprint-reference examples for each script and protects all identical historical copies when their bytes are cited. These are *retention references*, not proof that the source executed, the model is correct, or a DOI deposit exists. Git blob SHA-1 calculated from checked-out bytes may differ when line endings are converted; the original archival source receipt remains authoritative.

When a source file has no statically detected reference, it is labelled **`unresolved_do_not_delete`**. Reference hits are conservative pointers, not a proof of executable reachability. Dynamically assembled imports, private archived receipts, notebooks, commit-pinned experiments, external citations and texts above the scan size limit may not be captured.

### Interpretation of categories

| Label | Permitted action |
| --- | --- |
| `frozen_model_or_producer_protect` | Preserve original Model3 core and pinned Q1/Q4 producers without path, byte, or behavioural changes; make versioned successors instead |
| `source_fingerprint_reference_protect` | Preserve files whose source SHA-256 or Git blob SHA-1 appears in another tracked file, even without a path-based reference |\n| `workflow_reference_check_before_edit` | Inspect CI invocations and source-integrity contracts before changing signatures, paths or behaviour |
| `referenced_review_before_edit` | Review importer/caller tests, documentation and source hashes; small refactors only with equivalence tests |
| `unresolved_do_not_delete` | Investigate dynamic execution, external manuscripts, authors' notebooks and source provenance; **not** an automated deletion target |

## Remaining cleanup sequence

1. **Dependency and CLI cleanup:** PR #572. Do not modify frozen producers to simplify imports. Confirm full supported `pip install -e .` and `.[dev]` behaviour in Linux CI.
2. **Global source-reference inventory:** this PR. Record true repository denominators, per-source read-only digests and byte-identical groups without issuing deletion decisions.
3. **Curated refactors:** choose *nonfrozen* current validators/packagers only after proof no externally pinned source bytes are changed; add negative-input and provenance tests.
4. **Historical organization:** preserve `legacy/model2/`, source-pinned old numerical attempts, failed experiments and SI provenance. Rehome only after explicit archive reference and DOI checks with a reversible redirect/mapping.
5. **Integration:** merge independently verified small PRs, not a single giant reformat. Recheck the one-paper source readouts (Q1 4/4 original, 3/4 new founders; Q3 access; separate Q4 occupancy) and the unchanged scientific-gate CI.

## Explicit scientific boundary

This inventory cannot establish unusedness, biological correctness, independent ecological replication or universal novelty. Its purpose is **maintenance safety**: avoid losing the source needed to reproduce the one-paper results while reducing the *supported day-to-day* software surface. It does not alter model parameters, mutation, genotype data, visitor histories, bootstrap units, population survival, frozen readouts, publication assets or SI S1–S33.

Before removing any file, require an individual proof that (1) it is not source/manifest/DOI referenced, (2) it has no live CLI/workflow or dynamic caller, (3) its output has a preserved reproducible replacement, (4) tests and source checks pass, and (5) reversible archival storage is in place. This scan alone does not satisfy those requirements.
