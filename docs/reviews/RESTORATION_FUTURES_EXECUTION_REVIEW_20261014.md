# Q3 conditional futures: independent execution implementation review

Date: 2026-10-14. PR: #514. Protocol base: `d7c18a6dc1ea547955aef75fbec0c53cf6fe950b`. Repaired implementation supplied for review: `dd4abe0500d73b8e4bf804437c47a9253e853c41`.

## Decision and boundary

**PASS for the repaired execution implementation at the exact file hashes below. No remaining Critical or Important implementation finding was identified in this review.** This permits preparing the frozen execution manifest for its final identity review. It does not certify a manifest that has not yet been created, successful GitHub admission, native fixtures, completed trajectories, or a scientific result.

The review used the coordinator-designated authoritative local staging copy of the GitHub branch. The reviewer did not independently fetch GitHub, write to GitHub, run any native population update, or create any scientific future. The local test runtime was Python 3.10.11; the production Python 3.11.14 / NumPy 2.2.6 identity remains a GitHub admission requirement. Runtime identities were mocked only in isolated tests of authorization logic, never for a production run.

## Scope and repaired findings

The review covered the fixed protocol, authorization receipt, execution ledger, producer, independent replay/readout implementation, contract, targeted tests, and dedicated workflow. The original archived producer and frozen native state/population/RNG interfaces were inspected to check the continuation adapter. The original review raised five Important findings; all five were repaired before activation:

1. The NumPy runtime identity now reads the correct `np.__version__` string attribute. The complete authorization function also passed an isolated test with mocked GitHub, Git-parent, and runtime inputs.
2. Manifest admission requires the complete prescribed file-hash inventory and valid digests; frozen protocol, preflight, archive, source-input and human-authorization identities; approved scope and limits; and a reviewed-parent commit. The activation commit may change only the execution-manifest path. Checkout fetch depth 2 supports the parent and diff checks. The final manifest must still bind the committed review report and be checked before its one-file activation push.
3. Packaging, file hashing, archive-member readback and final archive hashing now use bounded chunks with deadline checks. Readout preparation also checks the global deadline. The 238-minute internal deadline reserves margin below the conservative eight worker-hour ceiling. The complete publication receipt follows archive verification and final guards.
4. The coordinator retrieves every result in the completed batch before dispatching any replacement job. A completed exception therefore reaches the abort path before another batch replacement can start. Conservative durable reservations still precede scientific production plus its one replay.
5. The separate verifier now rereads all 3,904 saved pair receipts and independently checks primary means, original-slot denominators, simultaneous intervals, classifications, all-survivor gating, and global/block survival totals. It also checks per-case event counts, already-completed events, conditional means, and the three no-trigger original records. It does not import the producer's summary, classification, or event helpers. Publication is gated on this independent readout receipt.

## Verification performed without native updates

- The repaired focused test suite passed: **33 tests**, covering contract/readout adversarial cases, raw layout corruption, reservation accounting, manifest inventory/identity failures, exact runtime attributes, and deadline interruption during packaging.
- Exact mean preservation was checked directly on all **61 actual original trigger states**, using only saved arrays. All passed.
- An additional reviewer probe ran the full authorization function with locally constructed files, real file hashes, and mocked external/runtime interfaces. It passed. This does not replace checking the final real manifest or GitHub run state.
- An additional end-to-end raw-only aggregate probe wrote **3,904 synthetic pair receipts**, combined them with the three real no-trigger raw histories, and passed the independent readout verifier. Deliberately changing a published event count was rejected.
- A small complete stored archive passed the revised streamed packaging and SHA readback path. The focused tests separately exercised interruption during streaming.

These checks were performed with bytecode and pytest cache writes disabled and reviewer outputs confined to the review scratch directory. The synthetic receipt probe did not simulate populations, instantiate native RNG streams, or consume native operator calls.

## Scientific and operational invariants checked

The producer and independent replay both reconstruct the original five saved state fields, original Config, matched VisitorState, and empty immigration. They continue at absolute years `trigger,...,199` and save terminal census 200. The artificial restoration is applied once, keeps individual expressed I means and M/A loci unchanged, and consumes no random draw. The saved support and all original-array identities are checked.

Each triggered case has exactly 64 registered fresh pair seeds and two arms with separate mutable named generator objects initialized identically within a pair. The independent replay reconstructs the seed and state separately from the original archive, checks all saved state fields and parentage, and rejects I-support drift. Shared use of the intended frozen biological kernel is explicit; this is independent path reconstruction, not an independently implemented biological model.

The primary uses all 64 original-slot weights with three exact policy zeros. Any terminal extinction invalidates all three primary mean inferences. Neither dropping pairs, replacing seeds, extending sample size, nor substituting an unconditional or pooled-survivor estimand is allowed. The checked interval formula and operational classifications match the frozen fixed-state, coupling-specific, paired-survivor conditional target. No silent endpoint substitution was found.

The workflow activates only on a push touching the separate execution manifest on the named branch. It has no manual-dispatch trigger and rejects rerun attempts and prior workflow runs. At most two child workers are used. Call reservations cover production and one replay before dispatch, including conservative reservation consumption on failure; four synthetic fixture calls are separately reserved. Disk admission accounts for raw output and archive copies, and failure artifacts are preserved with a technical HOLD rather than a selected scientific result.

## Conditions still required for execution and scientific completion

1. Review the exact final manifest, its required file hashes, the committed review report hash, the reviewed parent, unchanged approved limits, and the single-file activation diff before the activation push.
2. GitHub must pass the exact production runtime gate, source/state admission, and four bounded synthetic native fixtures. These native fixtures have deliberately not been run locally.
3. All 7,808 trajectories and their one independent replay must finish within the approved aggregate call/time/disk ceilings. Any technical failure must remain HOLD; run history and reservations must not be discarded to obtain another attempt.
4. Scientific interpretation requires complete artifact retrieval, archive hash/readback evidence, full independent replay and readout receipts, final resource receipts, and review of the resulting decisions. This implementation review supplies none of those as an already-observed scientific outcome.

## Exact reviewed file identities

The review report's own hash is intentionally omitted to avoid a self-reference. The final execution manifest must hash the committed report separately.

| File | SHA256 |
| --- | --- |
| `scripts/q3_futures_contract_20261014.py` | `8ad0a13b7d5484fa0fffe02d19726f54748a5250469e0c3837c552ea8525409a` |
| `scripts/run_q3_futures_20261014.py` | `477b65756e18744d9ddc590672d520935dff810a44fe2b1f4f1b80a864c554e3` |
| `scripts/verify_q3_futures_paths_20261014.py` | `7843882f58363c179474f31b4bfead482cc05610bcfac862a6bc2c79b982c27b` |
| `tests/test_q3_futures_contract_20261014.py` | `ea919a5d7a33058ca4f4c16aa8ea3acf8ef9c1cd96da18183e8cebae41969a9e` |
| `tests/test_q3_futures_replay_20261014.py` | `b85e32c4c44f674bef2bdc026c7bb1b36d5daef4fbf9da3e43da458d8e58e3cd` |
| `tests/test_q3_futures_execution_gate_20261014.py` | `f99bc1e2a47da1d91b26b184365d9a58ade55103fbfed441e460d80af804d236` |
| `.github/workflows/q3-restoration-futures-20261014.yml` | `92e0dacafc16e4e845986fd1fff59ccdd3b0c55b94b20286d991d0584dd4d940` |
| `docs/CHAPTER2_RESTORATION_CONDITIONAL_FUTURES_20261014.md` | `e549464de272e5a792b45e61ea68f14af02ddf46ed1287a2a81249d0791f48e9` |
| `data/designs/restoration_futures_preflight_20261014.json` | `165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b` |
| `data/designs/q3_futures_authorization_20261014.json` | `297aa3267a07dfc2fd14fe75f9f553b71447bd35d8288464d844ef91146fb9f8` |
| `docs/superpowers/plans/2026-10-14-q3-futures-execution.md` | `3f02abe88714d61a0fa8cf7580356f5655e703cfe80c5ff112e992a4dc2f84a1` |
