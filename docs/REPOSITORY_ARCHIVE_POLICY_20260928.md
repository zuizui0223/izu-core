# Repository archive and size policy — 2026-09-28

## Purpose

Keep the scientific repository reviewable and reproducible without letting generated campaign payloads become the permanent interface of the codebase.

The current repository already contains large frozen outputs. This policy does **not** rewrite history or delete evidence needed by existing frozen checks. Instead it freezes the present large-file debt and prevents new growth while submission packaging is finalized.

## Boundary

- `data/design/` is for compact declarations: parameters, seeds, stopping rules, hashes, and references to externally archived enumerations.
- Full enumerated campaign tables and large endpoint matrices belong in a permanent data archive (Zenodo/Dryad) or a workflow artifact, with a compact checksum/provenance receipt committed here.
- Regenerable figures should stay below the tracked SVG budget. Publication figures may be committed when they are compact and part of the review surface.
- The number of simulated cases is provenance, not automatically an inferential sample size. For the Model 3 prospective bridge, 24,576 cases are organized around 128 independent visitor histories.

## CI size budget

`tests/test_repository_size_budget.py` enforces:

- ordinary tracked files: <= 5,000,000 bytes;
- files under `data/design/`: <= 1,000,000 bytes;
- tracked SVG files: <= 1,000,000 bytes.

Existing violations at reviewed HEAD `54db0b79` are grandfathered **only at or below their audited byte size**. They may shrink or disappear; they may not grow. New paths cannot be added to the grandfathered set without an explicit policy change.

The largest current debt includes:

- `data/results/model3_assurance_summary_20260925/endpoints.csv.gz` — 18,715,386 bytes;
- `data/design/model3_assurance_robustness_20260925.json` — 14,791,554 bytes;
- `data/design/model3_evolution_20260925.json` — 10,181,145 bytes;
- `data/results/model3_evolution_summary_20260925/endpoints.csv.gz` — 9,488,521 bytes;
- `data/results/model3_ch2_bridge_summary_20260927/case_receipts.csv` — 6,957,008 bytes;
- `data/results/model3_island_v2_summary/case_receipts.csv` — 5,057,905 bytes.

The two large Model 3 design JSONs are specifically treated as archive debt because they contain materialized campaign enumeration rather than only a compact design declaration.

## Submission packaging

For a reviewer-facing archive, prefer a clean release/export containing code, compact design locks, frozen compact summaries, manuscript surfaces, tests, and checksums. Large raw enumerations should be referenced by DOI once deposited.

Removing large blobs from the **current tip** does not reduce clone history. Reducing existing Git history would require a history rewrite (for example `git filter-repo`) and force-updating refs. That is a separate destructive operation and is not performed by this policy PR. If clone-size reduction is required before deposition, do it only after a release freeze with an old-SHA -> new-SHA provenance map and a permanent archive of the pre-rewrite state.
