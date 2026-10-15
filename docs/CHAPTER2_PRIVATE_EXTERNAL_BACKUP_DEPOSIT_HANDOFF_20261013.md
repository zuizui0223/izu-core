# Chapter 2 — private-source preservation and public deposit handoff (2026-10-13)

**Current state: original external readback integrity 520/521 across four independent demographic cohorts; scientific public DOI deposit remains OPEN.** This is a status update to the [2026-10-11 original-source preparation snapshot](CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md), not a retrospective rewrite of that snapshot. Its [machine-readable counterpart](../data/submission/chapter2_private_external_backup_deposit_handoff_20261013.json) records exact counts and receipt fingerprints.

## Source originals and externally authenticated private copies

| Original model cohort (64 separate synthetic visitor histories each) | Actions originals | Private external readback verified | Original ZIP bytes verified externally | Registered primary |
| --- | ---: | ---: | ---: | --- |
| Orthogonal matched-founder capacity | 130 | **130** | **227,238,776** | Inconclusive |
| Independent K × B | 130 | **130** | **226,003,482** | Inconclusive |
| Fixed B48 K confirmation | 131 | **130** | **224,423,683** | Supported **within frozen model**, not ecological field inference |
| Early/late selfed-seed viability (timed) | 130 | **130** | **225,311,380** | Inconclusive |
| **TOTAL** | **521** | **520** | **902,977,321** | Do not pool experiments as independent field systems |

The original ZIP aggregate is **903,095,464 bytes**. The one **118,143-byte** shortfall is exactly `chapter2-k48-future-shard-18.zip` (source ZIP SHA-256 `1b4c1450c387e24a844a97b25bcf01df20001ffe3afad64e2044e5d28cad3ff4`). Its original Actions byte stream and GitHub draft-release backup were previously verified, but its separate private Drive transfer was **stopped by a service safety check**. The private provider's block has not been and must not be circumvented. **Never call the fixed-B48 external backup complete.**

All 520 external-retrieved ZIPs have independent historical byte/SHA-256/size/CRC audit receipts preserved in a controlled private workspace, with zero reported mismatches. On 2026-10-13, their receipts were newly loaded and checked for counts, error fields, expected names and source-identification metadata. **The 520 ZIP byte-level checks were previously run, not rerun during creation of this status snapshot.** No private file URL, user identity or privileged path is published in this repo document.

| Private audit receipt basename | SHA-256 (entire JSON) | Prior verified original ZIPs |
| --- | --- | ---: |
| `chapter2_orthogonal_drive_readback_audit_20261012.json` | `1b2176d13e1e49aa0aead91f406b4677e2330ebb4602fc5de383aec987d97910` | 130 |
| `chapter2_kb_external_complete130_audit_20261012.json` | `fcdcb2ff77b72d0e8b235191f94422c05e4eae2b6ed82f300bc593f7ff4e3e69` | 130 |
| `chapter2_fixedB48_drive_restored_130_audit_20261012.json` | `be6d4d7b7aca216933a02801ac5d3e63f8f31cde70f6bb0ee942bc21636e8433` | 130 |
| `chapter2_timed_drive_readback_complete130_20261012.json` | `8b396c7ba456bafb910aea7c6b86ca3ccd9512751a20eb54642a74dfb7c0a091` | 130 |

For **timed**, later independent provenance work also reviewed **2,048 source-genome/parentage/future-sidecar identities**, **39,321,131 pedigree edges** and **229,376 futures**, and independently reproduced the preregistered main contrast (inconclusive). This statement is grounded in the [existing independent-validation issue record](https://github.com/zuizui0223/izu-core/issues/436#issuecomment-6120405691); these calculations were **not rerun** in this snapshot. Source workflow: [37944527799](https://github.com/zuizui0223/izu-core/actions/runs/37944527799), original SHA `e679e0ee190fa02e0a9d60876cd1a3e9987a4c79`.

## Preservation hierarchy and distinct projects

1. GitHub original Actions ZIPs and four **unpublished draft-release** exact-source archives already hold all 521 originals (same provider; not long-lived independent research DOI deposits). Original IDs, versioned tar hashes and reproduction commands are in the [source archive ledger](CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md). These copies must remain intact until an approved public deposit and independent readback verification are complete.
2. Separately hosted private copies have been byte-authenticated for 520/521 **unique originals**; transport containers, redundant copies and JSON audit receipts **do not add new biological observations**.
3. The unified paper also refers to **50 evolution campaign Actions ZIPs** (4,096 confirmation +8,448 assurance-generality cases; metadata-original sum 518,129,082 bytes) and **one separate local tempo archive** (268,940,123 bytes, SHA-256 `034e735d244228c1f4974897a76d16acef10767a81d5dd82f5f5204f48cf0738`). They are **not** among the 521 demographic Actions ZIPs and must be prepared/declared as separate components in any journal-wide deposit.
4. The four demographic experiments have **64 visitor-history inference clusters each**, not 521 empirical populations or 903 MB of statistically independent replicates. No source-level archival success establishes natural-island causation, genetic mediation or a fitness rescue law.

## Remaining release gates (do not infer or prefill without authorization)

- [ ] Resolve the single fixed-B48 external missing ZIP using an **authorized route**; do not bypass the provider's safety block. Alternatively retain its independently verified GitHub draft-release source with the incomplete external-preservation status explicitly reported.
- [ ] Confirm the approved deposit host/account, creators **and author order**, code/data **licenses**, access/embargo, final dataset version and attribution.
- [ ] Deposit unchanged original ZIPs and machine-readable inventories to a durable, independently administered versioned repository; obtain and verify persistent identifier/DOI after approval.
- [ ] Re-download **the deposited release** and verify all original ZIP hashes, pedigree/source linkage, accepted outcomes and immutable history-paired estimands against frozen originals; separately verify evolution campaign ZIPs and tempo archive.
- [ ] Only after success, update manuscript Data Availability, `REPRODUCE.md` and [Issue #436](https://github.com/zuizui0223/izu-core/issues/436). Do **not** close the issue while DOI/public validation is unfinished.

**No external repository release, DOI minting, new simulation, change to registered result/verdict, manuscript publication, or sharing-permission change was performed by this documentation update.**

## 2026-10-14 addendum — original fixed-B48 shard 18 readback, not external backup

The only missing **private external-copy** item, `chapter2-k48-future-shard-18.zip`, was freshly re-downloaded **read-only from its original GitHub Actions artifact ID 11600619779 (run 37896872795)**. Its actual 118,143 bytes matched original SHA-256 `1b4c1450c387e24a844a97b25bcf01df20001ffe3afad64e2044e5d28cad3ff4`. Independent ZIP verification found **65 distinct entries**, zero CRC failures, **32/32 JSON-to-sidecar SHA-256 matches** and exactly 32 declared source cases; the internal manifest reports 1,792 future conditions (not newly recalculated biological outcomes). The reusable check is [the pinned source-only verifier](../scripts/verify_chapter2_k48_shard18_source_20261014.py), with four local corruption/control fixture tests; see [machine-readable receipt](audits/chapter2_k48_shard18_fresh_actions_readback_20261014.json).

**Status remains 520/521 private external copies.** This fresh source readback **did not** transfer the ZIP into the blocked external provider, bypass its earlier safety stop, publish a versioned external dataset, assign a DOI, independently replay biological trajectories, change registered outcomes or alter any existing raw archive. It proves source recoverability at the stated check, **not** completion of the external preservation/deposition gate. The 2026-10-13 snapshot above is retained unchanged for chronological provenance. Issue #436 remains open.
