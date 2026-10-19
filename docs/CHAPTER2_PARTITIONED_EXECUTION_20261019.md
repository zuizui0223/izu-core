# Partitioned execution without duplicate scientific replication

**19 October 2026. Technical integration only, not a Q3 confirmation.**
Single Article: #590. Working PR: #597. Source parent:
`b65df91c48d89df9753853027bcb4a5d0ad6483f`.
The original native runner, biology, inference, frozen pilots and candidate
production/SESOI/seed contracts are unchanged.

## What works now

The new `scripts/q3_partitioned_runner_20261019.py` partitions the EXISTING
3-by-3 technical cohort into independent local directories. A complete
founder-by-visitor crossing stays together: two A-policy histories and both
budget futures remain paired. Worker shards have disjoint files and locks;
they never write to another worker's checkpoints. All shards retain the same
source/runtime/native experiment contract and the original technical seeds.
The 160-by-160 candidate can only be inspected by the arithmetic layout
command; it cannot be executed through this module.

A content-hashed partition manifest fixes every assignment before execution.
A worker seals its complete inventory with file and payload hashes. A repeated
completed worker verifies that seal and performs ZERO further updates. Missing
or additional tasks, changed code/runtime, changed assignments, corrupt files,
unreviewed locks and symbolic links cause rejection rather than partial
analysis. Lock files are not silently cleared after a process failure.

Collection holds all worker/native locks, checks every expected task, copies
sealed bytes into a private staging directory and validates native ancestry
and both endpoint matrices before publishing the complete directory. A copy
failure publishes no partial result. Repeated collection verifies the previous
receipt/summary and returns the same result. Changes after completion are not
silently accepted. This is a cooperative LOCAL-filesystem procedure; it is not
a multi-host/object-store lease system or an adversarial signed archive.
Atomic visibility on this filesystem does not certify survival of a machine
power loss. Storage permissions, quotas and backups require separate deployment
review.

## Executed checks

A source-pinned CLI smoke run stopped shard0 after 48 updates, then ran three
separate worker processes concurrently (submitted in reverse shard order).
They completed 2,202 remaining updates. The 9 technical crossings therefore
made exactly 2,250 unique native updates, 18 history tasks and 36 future tasks.
This is a replay of the same engineering cohort, not a new scientific sample.

All 54 task payloads and metadata matched a separate continuous serial run,
including all five PlantState arrays and every one of the 13 named RNG states.
The combined archive contains 2,304 genotype censuses, including duplicated
fork starts. These are saved censuses, NOT 2,304 independent biological paths.

The previously source-pinned independent raw reviewer, importing neither the
runner nor biology nor inference, rechecked all arrays, 36 fork matches,
allele-origin consistency, absorbing extinction and both endpoint matrices.
It returned `TECHNICAL_RAW_PIPELINE_AUDIT_PASS`. This is independent array and
arithmetic validation, not an independently coded biological model.

Tests: **11 new partition tests + 19 existing native/inference tests = 30 passed
locally.** A missing-implementation failure preceded implementation. An initial
successful test emitted Python's threaded-fork warning; the process test was
changed to explicit `spawn` and all 30 tests rerun without that warning.
Tests intentionally inject incomplete shards, bad hashes, foreign files,
changed manifests, stale locks, modified summaries, insufficient space and a
copy failure. None permits a partial final analysis. Completed-worker reruns
and repeated collection perform zero new biological updates.

## Candidate-scale arithmetic, not execution

A proposed 160-by-160 layout split 32 ways assigns 800 crossings per shard:

| Quantity | Per shard | Full candidate |
|---|---:|---:|
| Policy history tasks | 1,600 | 51,200 |
| Future budget tasks | 3,200 | 102,400 |
| Unique native updates | 200,000 | 6,400,000 |
| Raw padded state-array bytes | 1,161,625,600 | 37,172,019,200 |

This excludes metadata, compression and filesystem overhead. The current
safe collector copies worker artifacts into a separate directory; retaining
both worker and aggregate arrays would represent 74,344,038,400 raw bytes
before overhead (not an actual compressed disk-size prediction). No storage
reservation, cloud allocation, production source sampling or runtime estimate
has been made. A production archive may use a separately validated streaming
collector rather than blindly duplicating storage.

## Reproduce only the technical cohort

```sh
python -m scripts.q3_partitioned_runner_20261019 init --root NEW_WORK --shards 3
python -m scripts.q3_partitioned_runner_20261019 worker --root NEW_WORK --shard 0 --max-updates 48
# The three commands below can be started as separate local processes.
python -m scripts.q3_partitioned_runner_20261019 worker --root NEW_WORK --shard 2
python -m scripts.q3_partitioned_runner_20261019 worker --root NEW_WORK --shard 1
python -m scripts.q3_partitioned_runner_20261019 worker --root NEW_WORK --shard 0
python -m scripts.q3_partitioned_runner_20261019 collect --root NEW_WORK --destination NEW_COMPLETE
python -m scripts.audit_q3_native_pipeline_20261019 --root NEW_COMPLETE --summary NEW_COMPLETE/SUMMARY.json --out NEW_AUDIT.json
python -m scripts.q3_partitioned_runner_20261019 layout --axis-count 160 --shards 32
pytest -q tests/test_q3_partitioned_runner_20261019.py tests/test_q3_native_runner_20261019.py tests/test_q3_joint_inference_20261019.py
```

The new receipt records the local run and source identities. Remote CI must be
read at its own exact post-push head. No native scientific result, margin,
method approval, final registered design, biological execution authorization
or main-branch merge follows from passing these engineering tests. The
unresolved work is the final study/deployment approval, not further reinterpretation
of this technical cohort as evidence for the hypothesis.
