# Repository coverage and scientific review scope

## Frozen inventory

Inventory revision: `d2c24ceae3bf8d955f2a77a98695ea800944393c` (PR #609 narrative before this synthesis).
The [complete tracked-file inventory](audits/CHAPTER2_REPOSITORY_FILE_INVENTORY_20261019.tsv)
was generated from `git ls-tree -r` at that exact revision. Every tracked file is
listed once with its Git blob object ID and a structural role. The roles are
path-based navigation labels, not scientific admission verdicts. This inventory
excludes untracked workspace files and does not enumerate remote release assets
or unmerged branches. New synthesis files necessarily postdate this snapshot.

| Structural role | Files |
|---|---:|
| documentation | 480 |
| figures | 34 |
| historical_retained_not_current_model_evidence | 1917 |
| other | 91 |
| saved_data_or_design | 918 |
| source_code | 666 |
| tests | 536 |
| workflow | 49 |
| **Total** | **4691** |

## What was actually integrated

- Every historical S1–S33 section and F1–F8 card has an explicit outcome,
  limitation and proposed main/supplement location in the
  [41-unit disposition map](CHAPTER2_HISTORICAL_RESULTS_DISPOSITION_20261019.md).
- The [current supplement](CHAPTER2_COMPLETED_EVIDENCE_SUPPLEMENT_20261019.md)
  incorporates those preserved sections by reference and records newer completed
  evidence separately. Negative and inconclusive results remain included.
- The current manuscript now includes the previously omitted carrier-distribution,
  genetic-restoration, temporal-environment and predictive-limit findings.
- Legacy Model 2, old submission routes, software verification and natural-system
  motivation remain accessible; they are not silently counted as independent
  Model 3 evidence or pooled into current effect estimates.

## What was actually code-reviewed

The fixed change range is `439099ca6e3b8137f7884132f143d56d5e72e8be...d2c24ceae3bf8d955f2a77a98695ea800944393c`:
217 files, 44,844 insertions and 16 deletions. The two independent reviews inspect
specified high-risk scientific scripts and protocols within this range; they do
not certify every line of all 217 files. Historical S1–S33 coverage is document
and outcome mapping, not a fresh independent replay of every archived experiment.
See the [review findings and repairs](CHAPTER2_SYNTHESIS_CODE_REVIEW_20261019.md).

## Remaining boundary

This is full tracked-file inventory plus explicit integration of the maintained
historical evidence register and named completed follow-ups. It is not proof that
every result embedded anywhere in 4,691 files has been discovered, scientifically
revalidated and admitted. Unregistered material, inaccessible external assets and
unmerged work need separate source admission before scientific use. No manuscript
claim is licensed merely by a row in this inventory. Final rendered figures,
supplement typesetting, complete reference/author checks and immutable archival
preparation remain publication work.
