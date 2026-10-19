# Model3 execution, restart, and joint-inference integration

**19 October 2026 — technical integration only; no confirmation authorization.**
Parent: single developing Article #590; working PR #597. Base: `e131da0376a615bceca8770d5d7236a30a5a36fe`.

## Completed this step

The original native diploid operators are connected to a resumable, source-bound
checkpoint writer and the previously implemented joint Q3 endpoint analysis.
All eight imported native/helper/inference files match live GitHub blob hashes.
No original biology, frozen pilot, registered outcome, margin, or production seed
registry was edited. A packaging-only empty `model3_island/__init__.py` in the
uploaded archive was replaced locally with the actual repository docstring before
hash validation; no biological function changed.

`q3_native_runner_20261019.py` executes ONLY an exact 3x3 technical cohort:
founders 9100001..9100003, visitors 9200001..9200003, its own named SHA256 seed
namespace, fixed/evolving A, 35 common-history updates, and B8/B4.5 branches to
census80. There are 18 policy prefixes, 36 descendant branches and 2,250 unique
native updates. All t0 A expressions are .5 with segregating A alleles. This is
real native-model computation for engineering tests, NOT new scientific evidence.
The candidate 160x160 production cohort is not executable by this harness.

## Persistent state and verified behavior

Each task checkpoint is a self-contained compressed NPZ without pickle. It saves:
all five PlantState fields at EVERY completed census, occupied counts, complete
states of all 13 named RNGs, source/runtime/contract hashes, parent checkpoint
hash, exact founder-relative I target and the task identity. Temporary files are
fsynced and atomically renamed. A single-writer lock prevents simultaneous writes;
a stale lock after a hard process kill requires review, not automatic deletion.
Completed tasks are read-only and idempotent. The latest partial checkpoint may
be replaced on resumed progress; older biological source inputs are never altered.
This is local-filesystem checkpointing, not yet a distributed or cloud archive.

Tests compare all state arrays AND every RNG state between continuous execution
and repeated interruptions, including t12, exact fork t35, and descendant updates.
They also compare a stopped trajectory directly with the unchanged native operators
without using the checkpoint driver, reverse the order of all nine crossings,
verify that completed execution performs zero extra updates, and inject failure
before atomic replacement. Missing tasks/budgets, changed contracts/runtimes,
checksum damage, foreign alleles, and unauthorized production plans fail closed.

A separate reviewer imports neither the runner, biology nor inference modules.
It independently reads 54 NPZ files, checks 2,304 saved genotype censuses,
all five fields, 36 fork-start matches, lineage-origin consistency, shrinking
allele sets, absorbing extinction, and both unconditional endpoint matrices.
It rederives the candidate two-axis variance/interval arithmetic and compares the
reported result. This is independent array/arithmetic review, not an independent
implementation of the biological model or a new scientific replication.

## Actual validation

- Missing-implementation red test observed and preserved for both new modules.
- 13 new integration tests passed; with 6 unchanged inference tests, **19 passed**.
- Separate CLI smoke run stopped after 48 updates, then completed exactly 2,202
  remaining updates. Independent array review: `TECHNICAL_RAW_PIPELINE_AUDIT_PASS`.
- Initial combined test collection lacked an existing calibration module in the
  local mini-checkout. Copying that unchanged dependency resolved collection;
  no test or algorithm was relaxed. The failure and final pass logs are retained.
- The smoke archive's outcome estimates are engineering fixtures, not Q3 evidence.
  Repeated tests replay the same technical streams and add no independent sample.
- Full repository CI and cross-version tests must be read separately after push.

## Candidate-scale storage and computation, dry calculation only

For 160x160, R=1: 51,200 prefixes and 102,400 branches, 6,400,000 unique updates.
Saving all padded states in this layout yields 6,553,600 state slots, including
fork-start duplication, and **37,172,019,200 bytes** of raw arrays before NPZ
compression, JSON metadata, or filesystem overhead. Compression and runtime are
NOT predicted by the small smoke test. Production storage location, quota,
retention, concurrency and execution approval remain unresolved. This harness
implements neither multi-host locking nor a production scheduler.

## Run the technical test only

```sh
python -m scripts.q3_native_runner_20261019 init --out NEW_RUN
python -m scripts.q3_native_runner_20261019 run --out NEW_RUN --max-updates 48
python -m scripts.q3_native_runner_20261019 run --out NEW_RUN
python -m scripts.q3_native_runner_20261019 collect --out NEW_RUN > SUMMARY.json
python -m scripts.audit_q3_native_pipeline_20261019 --root NEW_RUN --summary SUMMARY.json --out NEW_AUDIT.json
pytest -q tests/test_q3_native_runner_20261019.py tests/test_q3_joint_inference_20261019.py
```

The 160x160 statistical method checks remain distribution-conditional. No margin
endorsement, independent scientific/method approval, final registered protocol or
approved production resource allocation is supplied here. The #585 distinction
between method review and biological execution authorization stays intact. Actual
recovery of flowers following pollinator return is not an endpoint of this smoke
run. Main is not modified; the single-paper scientific hypothesis is not declared
proved by successful engineering tests.
