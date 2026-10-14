# Chapter 2 Q1→Q2 factorial: lossless original-case shard packing gate

**2026-10-13. PRE-EXECUTION TECHNICAL DELIVERY ONLY; no original 200-update pilot trajectory is produced or published.** This is a prerequisite between the PR #500 original full-genome producer and the PR #501 six-source external re-download/independent original-model verifier. It is **not** approval to run the source producer, not a data deposit, and not evidence for a new evolution law.

## Concrete file-format mismatch closed

The frozen original Model 3 pilot producer, `scripts/prepare_chapter2_clock_pilot_archive_20261013.py`, intentionally writes a **directory** of one NPZ per trajectory and `_COMPLETION.json`. That is a safe immutable source staging layout, but `scripts/review_chapter2_clock_external_archives_20261013.py` expects each of six externally re-downloaded sources to be a **flat ZIP with 256 NPZ members plus `_COMPLETION.json` (257 exactly)**. A release ZIP manually assembled without exact source-case completeness, provenance hashes and reproducible member rules would undermine the independent raw archive gate.

The new `scripts/package_chapter2_clock_pilot_shard_20261013.py` is a **read-only packager of already completed biology** (aside from emitting a *new* ZIP/receipt). It never imports any biological operator or executes any Model 3 update. It verifies the original registered source 1,536-case inventory and six 256-case shards before any output, then for the selected shard:

- Requires exactly 256 existing original case NPZs and the producer's original `_COMPLETION.json`; rejects missing/extra files, directory traversal, symlinks, duplicate case IDs, incomplete cases or unsupported source/runtime/biology.
- Requires all stored per-case original SHA256 and byte lengths to agree with the current **real source body**, plus the frozen original source/registry/protocol, original 200-update horizon and each original A/I 20-census, ±5-tie six-class event label.
- Records all member SHA256 and produces an archive with deterministic sorted basename order, timestamp 1980-01-01 and ordinary regular-file permission bits; preserves each **original NPZ byte stream unchanged** (`ZIP_STORED`, as the NPZ payload is already compressed).
- Reopens its actual ZIP and checks all 257 original member bodies, hashes and ZIP CRC. Records full SHA256/byte length and original case hashes in an exclusive, immutable packaging receipt. Refuses replacing existing ZIP/receipt.
- Marks output **`SOURCE_ZIP_BYTES_VERIFIED_NOT_ARCHIVED_OR_INDEPENDENTLY_REPLAYED`**. External release URLs, mirror, DOI, independent re-download and scientific readiness intentionally remain absent/false.

## Execute only after six scientific 256-case shards actually exist

```bash
python scripts/package_chapter2_clock_pilot_shard_20261013.py \
  --registry data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json \
  --shard main_c0 \
  --source <ORIGINAL_256_CASE_DIRECTORY> \
  --out <NEW_ORIGINAL_RELEASE_ZIP> \
  --receipt <NEW_SOURCE_PACKAGING_RECEIPT_JSON>
```

Repeat once for every registered `main_c0/main_c3/main_c4/confirmation_c0/confirmation_c3/confirmation_c4` shard; do **not** create substitute simulated cases or use original older 2,304 histories. The six created ZIPs must be deposited with a reviewer-approved dataset title/license/access plan and a genuinely separate authorized mirror; **two copies on the same service do not demonstrate independent custody**. Then obtain each *actual* release and mirror copy independently, SHA-check both, use PR #501's source-only native 200-step verifier on the full 1,536 cases, and run PR #502's preregistered exploratory report only after six receipts and complete 128 paired stream clusters have been admitted.

## Explicit evidence limits and archival blockers

This script can package a forged test directory that **claims** 256 cases if a hostile writer also fabricates mutually agreeing completion hashes. It is intentionally *not* an independent source replay verifier: PR #501 is responsible for authenticating the actual source/archive and replaying every genotype, mating, inheritance, parental source return and mutation. The accompanying isolated unit tests use **mock data that are not even genuine NPZs** to prove byte-level packing and failure handling; none are biological outcomes.

The existing repository's four older demographic-cohort backup inventory (520/521 ZIPs separately verified) concerns **different experiments**. That receipt cannot satisfy any of the present 1,536-case pilot's external release/mirror/DOI gates; one prior provider service safety rejection must not be bypassed. [The source-preservation handoff on main](https://github.com/zuizui0223/izu-core/blob/main/docs/CHAPTER2_PRIVATE_EXTERNAL_BACKUP_DEPOSIT_HANDOFF_20261013.md) records those separate historical limits. This packaging plan does not identify or authorize a particular new external provider.

Current mandatory HOLDs:

1. **Independent pilot source-run approval is absent.** Original full Model3 producer stays disabled (`APPROVAL_GIT_BLOB=None`) despite green technical CI.
2. **New 200-update biological data do not yet exist.** Six real 256-case input directories, raw ZIPs and mirrors are missing.
3. **External custody and publication are not approved.** Deposit provider, author order, license, access/embargo and version/DOI are pending. GitHub draft releases alone would be same-provider backups, not independent long-term data preservation.
4. **Original-source independent replay is prospective.** PR #501's raw source verifier cannot be labelled successful on actual pilot data until externally published source+mirror ZIPs are obtained and all six case receipts and parentage match.

Original supported/rejected Q1–Q4 findings are not changed; no validated two-stage A-access versus I-response clock, real ecological threshold or order-mediated Q4 demographic rescue is claimed.

### Tests and replay boundary

The local packaging tests cover deterministic two-package equivalence, all 257 original member bytes, CRC, source/registry mismatch, missing/extra cases, typoed onset labels, unsupported NumPy/technical data, symlinks and no-overwrite. The genuine original-source reader import test is intentionally **skipped** in a detached scratchpad lacking the full GitHub repository, and MUST pass under the exact checked-out branch's GitHub CI before this code is technically admitted.
