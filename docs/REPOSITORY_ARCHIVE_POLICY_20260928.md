# Repository archive and artifact policy — 2026-09-28

## Current decision

The repository remains scientifically usable, but its tracked data surface has become too large for unconstrained continued growth. At baseline commit `8d145da1e312e9767b056fd81f3c4b6c3448d552`, tracked `data/` files occupy **176,634,102 bytes**. The largest objects are enumerated campaign outputs, large campaign-design JSON files, case-receipt tables, and generated SVG diagnostics.

This policy does **not** delete frozen results or rewrite history. It first prevents additional growth without breaking the current submission surface.

## Boundary between design and generated output

`data/design/` should contain compact declarations: parameter values, seeds, factor levels, stopping rules, hashes, and references to externally archived enumerations. It should not normally contain multi-megabyte full case enumerations.

`data/results/` may retain compact frozen receipts and summary statistics required for reviewer verification. Full endpoint tables, exhaustive case receipts, large generated plots, and rerunnable intermediate products belong in GitHub Actions artifacts or the permanent public archive.

Generated diagnostic SVG files are reproducible outputs. New large SVG diagnostics are therefore ignored by default and rejected by the artifact-budget test if they are force-added.

## Grandfathered legacy blobs

The machine-readable policy records the exact current byte ceiling for each legacy oversized file. These files are grandfathered for provenance only:

- they may not grow;
- no new oversized sibling is admitted automatically;
- once the permanent archive is fixed, the repository copy should be replaced by a compact checksum/DOI receipt where doing so does not break the frozen reviewer path.

The policy is `data/design/repository_artifact_budget_20260928.json` and the enforcement test is `tests/test_repository_artifact_budget.py`.

## History rewrite

Removing a file from the current tree does not remove its historical blob from clone cost. A real reduction of `.git` size requires history rewriting (for example with `git filter-repo`) and force-updating rewritten refs.

That operation is intentionally **not** performed here because it is destructive. It should be done only after all of the following are fixed:

1. permanent archive DOI/location and checksums for every removed artifact;
2. a tagged pre-rewrite archival release;
3. the exact branches/tags to rewrite or preserve;
4. collaborator migration instructions for fresh clones/rebases;
5. a post-rewrite verification that the scientific frozen receipts and manuscript hashes still resolve.

Until then, the correct operational move is to freeze growth, not to create another round of CI/debug commits.
