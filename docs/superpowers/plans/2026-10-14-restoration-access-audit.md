# Existing restoration intervention: access audit

> **For agentic workers:** Use superpowers:executing-plans to implement this plan inline; use a fresh independent reviewer before delivery.

**Goal:** Determine what constraints the existing 64-pair investment-variation restoration actually removed, using only archived records.

**Architecture:** A standalone read-only audit admits hash-pinned ZIP inputs, pairs all 64 original/restored genomes, reconstructs annual support and moments, and checks existing signed pathwise accounting. It writes a case table and machine-readable summary; a companion note answers Q3 without changing the frozen primary.

**Tech Stack:** Python >=3.10, standard library, NumPy, pytest.

**Spec:** Active user goal and the source-pinned `CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md` at `688bcdf563d4150e6f3618e27967469cbbaa341e`.

## Global constraints

- Exactly 64 paired histories, 32 per original block; retain 61 triggers and 3 unchanged slots.
- No biological simulator invocation, new histories, resampling family, threshold tuning, or horizon extension.
- Preserve original primary and its `unresolved` decision; no equivalence or unique causal fraction.
- Keep original standing M/I and mutating A distinct. Report allele-copy and expressed variance separately.
- Hash/source/inventory mismatches fail before derived results are written. Missing fields remain an explicit identification limit.
- New paths only; other chats own F1 analyses, 4096-condition parent control, and manuscript integration.

## Review focus

- No-trigger slots have only a saved terminal restored state; do not mistake this for a 201-census restored trajectory.
- Zero expressed variance is compatible with positive allelic variance and segregation potential.
- Allelic lower bound permits but does not guarantee a sustained population-mean event.
- A first event before intervention does not measure post-intervention rescue; keep original and post-trigger occurrence separate.
- Extinction, missing years, duplicate cases, and false terminal values cannot silently disappear from the denominator.

## Tasks

1. Admit original input/cohort ZIPs and restored/accounting bundles by SHA-256; verify each of 64 raw pairs and source event definition. Record immutable provenance.
2. Add `scripts/audit_restoration_access_20261014.py` and `tests/test_restoration_access_20261014.py`. Test heterogeneous alleles with equal expressed means, fixation versus directional exclusion, sustained-event timing, no-trigger handling, and malformed records. Reconstruct each trajectory directly from saved arrays, verify moments and intervention, and reconcile the existing accounting.
3. Run the audit against the admitted archives. Save `data/results/restoration_access_cases_20261014.csv` and `data/results/restoration_access_audit_20261014.json`. Independently recompute headline counts and verify every table row from raw inputs; document results and limitations in `docs/CHAPTER2_RESTORATION_ACCESS_AUDIT_20261014.md`.
4. Review, test, publish a single GitHub PR against current main, and inspect remote head, changed paths, and relevant CI. Do not merge.

## Execution record

- Other-chat check: PR #511 owns assurance parent control; PRs #508–510 own F1 access/context audits. No overlap with the new paths here.
- Restored bundle contains original64 and restored64 genomes, receipts, frozen biology, and the registered protocol. Its ZIP SHA-256 matches the published receipt.
- Source snapshot: `688bcdf563d4150e6f3618e27967469cbbaa341e`. Raw bundle SHA-256: `90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6`.
- Source admission complete: all four ZIP hashes and every selected original NPZ against the full original cohort match. Source event definition is original initial I minus 0.05, sustained 20 censuses.
- Ten focused tests pass. All 64 case records, 61 triggers, 3 unchanged slots and 7,740 saved restored updates pass direct raw checks. Frozen primary remains unresolved.
- Fresh independent reviewer reconstructed all 64 × 32 CSV fields and 7,740 annual terms with no blocking code or scientific findings. Portable independent verifier and hash-bound receipt accompany the result.
- No scope changes or biological simulations; dedicated new paths are published against main, outside the other chats' branches. CI is a delivery check, not a substitute for raw-data admission.
