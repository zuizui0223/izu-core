# Q3 original-mutation 3/32, 2/32 — independent native source re-download gate (2026-10-16)

**State: FULL ORIGINAL ARCHIVE SOURCE RE-DOWNLOAD AND 990-EVENT RECALCULATION VERIFIED; NO NEW MODEL SIMULATIONS OR EXTERNAL DOI.**

This audits the scientific source for the one *Ecology Letters* Letter's separate Q3 original-mutation result. The existing source-run [38120835221](https://github.com/zuizui0223/izu-core/actions/runs/38120835221) completed **30 genotype-density numerical files at grid sizes 65/129/257** across 10 contexts and **320 finite ABM histories** (32 replicates in 10 contexts). The original result is stated in [the preserved numerical verdict](../atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md) and source readouts in `data/results/atom_cell_completed_20261011`.

## Original archived release and paper's claims

- The original complete archive `completed_atom_abm_20261011.zip` was previously preserved in **public GitHub Release** [atom-cell-inputs-20261011](https://github.com/zuizui0223/izu-core/releases/tag/atom-cell-inputs-20261011). Its recorded size is **389,730,774 bytes**, SHA-256 `7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918`.
- Preserved root inventory `data/results/atom_cell_completed_20261011/COMPLETED_ATOM_ABM_PRESERVATION_20261011.json` records **774 original ZIP members**, including a 773-file SHA-256/length ledger, 320 individual finite-path `.npz` and receipts, 30 original deterministic `.npz` and receipts, underlying source and output tables.
- Historical source-matched independent verifier `docs/atom_comparison_20261011/verify_matched_atom_abm.py` recovered **990 event classifications and 40 checkpoints** from the old archived trajectory arrays, as separately recorded in `matched_comparison_independent_verification.json`. These are historical checks, not a newly executed independent original-byte audit.

**Distinct event comparison:** under supply=0.125 and matched pollinator function, the original deterministic 257-cell model classified both the main and confirmation founders as assurance-first at **ΔI, ΔA=0.05 sustained 20 censuses**, but original finite ABM classified only **3/32** and **2/32** history replicates as assurance-first; **15/32** and **7/32** were assurance-only. All 32 paths remained occupied through update 200 in each of the two contexts. At a smaller 0.025 change threshold, the original deterministic categories are no longer assurance-first in both contexts; the observation does not imply a universal response order.

The original finite and genotype-density algorithms are **not assumed mathematical stochastic-expectation equivalents**. This is not a pure drift coefficient, and there is no natural-island abundance/pollination inference. The two contexts represent different original founder states; they are not 64 independent field populations.

## Completed original-byte readback (new 2026-10-16 result)

The original [read-only Actions run 38825943134](https://github.com/zuizui0223/izu-core/actions/runs/38825943134) completed successfully. Its SHA-pinned independent [small readout artifact 12014702656](https://github.com/zuizui0223/izu-core/actions/runs/38825943134/artifacts/12014702656) has outer artifact SHA-256 `00fea6477ab6ce66bebdf8b510e02080c4c1d38390029e95d79d22044d569457` and inner readout SHA-256 `565baa5d2633c1967d22fafe60661ba0a809f50a60e25fc4399e343133a84200`. The complete selected results and limits are committed in [the permanent source receipt](chapter2_atom_original_raw_reverification_receipt_20261016.json).

- **Original 389,730,774-byte ZIP:** exact original SHA-256 and length matched the publicly documented 2026-10-11 Release asset.
- **Original ZIP:** CRC readback succeeded; **774/774** unique members present, with **773/773** per-file original SHA-256 and uncompressed lengths matching the source preservation manifest.
- **Original matching 320 finite ABM paths and 10 finest-grid density traces:** loaded from original native NPZ arrays; **990/990** original event category tests across thresholds 0.025/0.05/0.1 and **40/40** original checkpoint rows exactly reproduced.
- **Original focal two contexts:** Main A-first density / finite **3/32 A-first +15/32 A-only**; Confirmation A-first density / finite **2/32 A-first +7/32 A-only**; all 32 paths occupied at t200 in both contexts. Other eight contexts and their original null/other event categories were also retained and verified.

This establishes **actual native original mean/census array authentication and reproduced Q3 response classifications**, beyond an earlier metadata-only preservation status. It does **not independently derive each historical trait value from every stored parent/genotype edge**, isolate the drift share, make density the ABM stochastic expectation, add independent founder/visitor environments, prove universality across ecological systems, or create an independent long-term DOI archive.

## Independent re-admission now implemented

The [source verifier](../../scripts/verify_chapter2_atom_original_raw_20261016.py) and [fast guard tests](../../tests/test_chapter2_atom_original_raw_20261016.py) are designed to:

1. Re-download the exact **389,730,774-byte original unchanged GitHub release asset** in the dedicated read-only CI workflow; refuse any SHA mismatch before analysing numerical data.
2. Check original archive CRC, 774 unique entry names and **773 per-entry SHA-256/byte lengths** against the committed historical preservation manifest, including its original run ID and original source commit.
3. Extract all **320 original per-replicate native mean/census traces**, read all **10 admitted finest-grid original native density traces** and reclassify 20-census sustained events at thresholds 0.025/0.05/0.1 without calling the original producer's event code.
4. Check **990 event labels** (10 × [32 finite + 1 density] × 3 thresholds), **40 population/trait checkpoints** (10 contexts ×4 times), original t200 occupancy, and original 3/32 and 2/32 counts without re-running Model 3 evolution.
5. Retain the native original `means`/`population` trace arrays' scientific scope. The comparison **does not rederive every old phenotype summary independently from all underlying original diploid parent/genome arrays** and is not a historical causal or natural-island mediation estimate.

The workflow [`chapter2-atom-original-readback-20261016.yml`](../../.github/workflows/chapter2-atom-original-readback-20261016.yml) has a narrow source-file activation trigger on its exact research branch, and will upload **only the small audit JSON** as a 90-day Actions artifact; it does not upload or publish the 390-MB original ZIP, mutate biological inputs or create a new archive version. Original source remains accessible at the unchanged GitHub release URL. This original provider is **not an independently administered DOI repository**.

**Failure condition:** If original data cannot be retrieved, if any source file hash differs, or if reclassified cases disagree with registered source, report which gate failed and preserve the original discordance; do not change the historical original SHA, replace the source with new simulations, search favorable thresholds, or claim source completeness.

**Paper and DOI bounds:** This Q3 archive is **not the same cohort** as the newly promoted main Figure 3A zero-mutation 128-history bridge, and not the one-locus 64-case panels B/C. External DOI issue [#436](https://github.com/zuizui0223/izu-core/issues/436) remains open pending author/coauthor order, code/data license, complete S1–S33 raw coverage, account/access and independent cross-host source re-download.
