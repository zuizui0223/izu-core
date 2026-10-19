# Q3 execution on GitHub Actions

19 October 2026. User-requested remote execution of the existing bounded
3x3 technical cohort in PR #597; not a 160x160 confirmation.

## Job graph

Existing `.github/workflows/ci.yml` triggers and full pytest matrix remain
unchanged. Added jobs run only for same-repository PR #597:

1. `q3-prepare`: check artifact transport, initialize the pinned three-shard
   technical contract, and compile the 160x160 planning manifest without
   consuming biological production seeds.
2. `q3-worker (0/1/2)`: three isolated ubuntu-24.04 runners. Each downloads
   the same plan artifact by its exact artifact ID, checks source/run
   identity, advances its own three crossings by 48 updates, resumes them
   to completion, verifies a repeat performs zero updates, and uploads a
   sealed shard. Both policies and budgets remain in the same crossing.
3. `q3-collect`: downloads the three sealed artifacts, verifies exact
   filenames, source/run identity, checksums and native per-shard receipts,
   and only then invokes the unchanged native collector and independent
   raw-array reviewer. Missing or failed shards prevent this job from
   publishing a verified result.

Python's exact patch release is resolved once by the prepare job and passed
to the workers and collector; numpy 2.2.6 and scipy 1.15.3 are fixed across
all runners. Checkouts use the PR head SHA and do not persist credentials.
New jobs have contents:read/actions:read, a 20-minute per-job ceiling, and
no secrets or repository write permissions. The matrix has at most three
parallel workers. No new workflow trigger, grant, or whitelist change.

## Evidence and archive boundaries

This is the SAME previously tested technical cohort: 18 prefixes, 36
terminal branches, 2,250 unique native updates and 2,304 saved genotype
censuses. Those numbers are engineering evidence, not new independent
scientific replicates. Production seeds are not consumed, no final method
or margin is approved, and original Model3 operators, runners, data and
160x160 gates are unchanged.

Artifacts have distinct plan, per-shard-ready, diagnostics and final
verified names tied to the workflow batch. Ready files cannot overwrite
one another. Failure diagnostics retain local checkpoints when available;
an abrupt runner termination can still prevent a final upload. The
artifact retention request is 14 days (subject to repository limits), NOT
an indefinite scientific deposition or a reservation for the estimated
160x160 archive. Re-run the whole workflow for a new immutable batch.

Cross-runner files are transferred by
`scripts/q3_actions_artifacts_20261019.py`, with strict filename inventory,
SHA256 checks and source/run identity. ZIP members are written only after
validation, never extracted with unrestricted extractall. This is integrity
checking of first-party Actions artifacts, not an adversarial digital
signature. Runtime mismatch, absent shards, duplicate paths or stale
contracts stop processing rather than silently produce partial analysis.

## Local validation before publication

The initial new-test import failed before implementation. Six transfer
and workflow tests then passed. A separate end-to-end rehearsal restored
one plan into three independent directories, packed every sealed shard,
restored all into a fourth directory, and re-derived the final result:
54 files, 2,304 saved censuses, 36 fork matches, 2,250 updates,
TECHNICAL_RAW_PIPELINE_AUDIT_PASS, confirmation seeds consumed 0.

Actual Actions job status and artifact IDs must be taken from the new
remote run. This document does not claim that local success is remote
success or that full repository CI equals scientific confirmation.
