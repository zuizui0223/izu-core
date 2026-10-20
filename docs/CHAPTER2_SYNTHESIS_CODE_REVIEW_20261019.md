# Two-axis review and repairs for completed-evidence synthesis

Reviewed baseline: `439099ca6e3b8137f7884132f143d56d5e72e8be`.
Reviewed head: `d2c24ceae3bf8d955f2a77a98695ea800944393c`.
Diff: `git diff 439099ca...d2c24cea` (217 files). Two independent reviewers inspected the high-risk code and scientific contracts below, not every changed line.

## Standards

**One P2 correctness finding; no documented coding-standard violation established.**
The pollen auditor range-checked `q_first`, `q_pre_last`, `q_future_first` and
`q_future_last` but did not bind them to their already checked reproductive
records. A complete synthetic allocation with ledger q=0.5 but reported future
q=0.99 passed. This is an admission gap, not evidence of corrupted archived results.

**Repair:** `check_observations` now compares the four summaries to reproductive
updates 0, prefix−1, prefix and last, with matching missingness, finite values and
absolute tolerance 1e-12. Sixteen corruption cases failed before the fix;
19 selected arithmetic-only tests passed after it. The existing 384-row archive
passed a fresh read-only audit. Old and corrected auditors produced exactly the
same output in the same runtime; comparison with the original deposited receipt
retains only cross-runtime floating differences up to 5.55e-16. Original receipts,
protocol and biological producer remain unchanged. The [new receipt](audits/CHAPTER2_BASELINE_POLLEN_384_ENDPOINT_LINKAGE_REAUDIT_20261019.json)
is separate from the original source audit.

Inspected: pollen producer/auditor; variation reader; confirm160 raw auditor;
most readaptation raw-auditor sections (not all); historical manuscript validator;
pollen/variation tests; pollen, variation, confirm160 and transfer workflows;
README, REPRODUCE and repository cleanup policy. No tracked AGENTS,
CONTRIBUTING or CODING_STANDARDS file was found. Independent-reader duplication
is intentional and is not mechanically refactored as a code smell.

## Spec

**One P2 integration gap; no critical scientific implementation mismatch found in the inspected scope.**
The historical editorial validator checks old Q1–Q4 but not the four completed
studies now supporting the manuscript. Its passing result cannot certify that
those newer claims still match their readouts. Existing source audits remain
scientific evidence; the gap concerns ongoing manuscript consistency.

**Repair:** a separate [completed-evidence validator](../scripts/validate_chapter2_completed_evidence_20261019.py)
binds selected pollen interactions/intervals, confirm160 G/S counts and intervals,
variation I-duration contrasts, and transfer receipt/table identities, nested
allocations and destination occupancy. Sixteen tests include deliberate source,
claim, direction, status and denominator corruption. They pass; a second reviewer
read both new files and independently obtained 16 passes. CI invokes the new gate.
The historical validator retains its old meaning; this new gate is explicitly
selected documentary consistency, not all-results or raw-archive reproduction.

Inspected: four named protocols/designs; pollen producer/auditor; variation reader;
confirm160 candidate, aggregation and inference with targeted native-runner reads;
transfer contract, assay, summary and targeted raw-auditor reads; manuscript,
route validator and tests. No scientific simulation was run for the review.

## Synthesis review

A third review mapped all S1–S33 and F1–F8 and checked the added supplement/main
claims. It found two editorial issues: pooled Q4 effects must be described as
averaged equally, not equal across mating settings; the eight-history micro-pilot
must link to its own source, not the distinct equal-initial-A pilot. Both were
corrected. The demographic supplement now states the positive fixed-B48 contrast
and the failed/inconclusive companion findings. Restoration of I variation lowers
terminal I in that experiment; it is not restoration of ancestral flowers.

## Validation scope

Use the current CI result for integrated tests. The new gates, regression tests,
source links and raw readback increase coverage, but no reviewer certifies all
4,691 tracked files or every historical raw array. Full source coverage and the
remaining publication work are documented in the [coverage report](CHAPTER2_REPOSITORY_SYNTHESIS_COVERAGE_20261019.md).
