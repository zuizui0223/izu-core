# Chapter 2: original-mutation genomic response order promoted to main Figure 3

**2026-10-16, source-backed editorial change only.** This follows [the full original Q3 320-path annual diploid-genome admission](CHAPTER2_Q3_ORIGINAL320_NATIVE_GENOME_ADMISSION_20261016.md) (merged PR #563; source Actions [38823339694](https://github.com/zuizui0223/izu-core/actions/runs/38823339694)). A new biological simulation, a changed response threshold or a new test of population-scale drift is **not** part of this change.

## What reviewers now see

| Manuscript role | Original source-pinned PDF | Cohort and interpretation |
|---|---|---|
| **Main Figure 3** | `docs/atom_comparison_20261011/resolution_figures_20261011/atom_abm.pdf`, SHA-256 `51c65d51b242834a51bab1a9f84b87c6dcfcb8e5ad30d875b6620b391ccb2997` | **Original-birth-mutation** finite versus 257-node genotype-density in all ten original contexts, with six-category 32-history finite stacks and separate terminal I/A means. All 320 finite cases retain occupancy to update 200. At the predeclared 0.05 threshold (20 sustained censuses, 5-step tie), the two matched low-supply contexts show deterministic **A-first** but original finite A-first only **3/32** and **2/32**, with A-only **15/32** and **7/32**. |
| **Supplementary Figure S3** | Previous main Figure 3, source-regenerated using unchanged code/data at `outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf` | Panel A is a **different zero-mutation 128-independent-history** far/near bridge; panels B/C are a **different one-locus, two-fixed-environment/eight-repeat history diagnostic**. Neither experiment contributes to the 3/32 or 2/32 denominator. |
| **Supplementary Figure S1** | `trait_pollen_snapshot400.pdf`, unchanged | Fixed-plant pollen-deficit versus viable-offspring static assay, not evolutionary order. |
| **Supplementary Figure S2** | `crossing_by100.svg`, unchanged | Separately frozen synthetic visitor-tempo profile cohort; not an independent replicate of main Figure 3. |

The existing main Figure 4 remains a distinct demographic-capacity experiment with its original source/evidence rank. The other Q3 result in the article (703/2,304 before fixation; 315/1,238 favourable expected parental-weighting transitions) is from **yet another original fixed-access cohort**, not an identified explanation of the main Figure 3 mismatch. Thus the paper does not imply a single serial causal pathway from Q1 to Q4.

## Source and figure-change contract

1. `Figure3.pdf` is now the *original unchanged atom/ABM comparison PDF*, with its original 2026-10-11 SHA bound by `ATOM_ABM_FINAL_READOUT_20261011.json` and the unchanged `atom_materials()` numerical/source audit.
2. `SupplementaryFigureS3.pdf` is now the previous main-figure source, **regenerated without changing its plotting code or input data**. The old reviewer-PDF SHA-256 was `97db4780e69436e55de52b58b5c34607f1d76e3381b0a142af2181188b238e84`, while the new source-regenerated PDF SHA-256 is `3bafd179aeb1fbea9b68d3fdbb7288f7a78030f996b0e8f84e3396b868d0b9b8b`. Their rendered 145-dpi **2248×870 images were identical at every pixel**; extracted `pdftotext -layout` outputs also matched byte-for-byte. The PDF wrapper bytes need not be equal because renderer metadata can change. The two source experiments remain distinct and are not pooled for a genetic drift or variance fraction.
3. The **historical S1–S33 Supporting Information** stays exactly pinned to Git blob `fdecc89abaee3479ae5eef3f476d5ba937505690`. Figure-role statements are updated **only in the anonymous derived review-bundle text**, which must reject an altered historical SI blob. All original source-pointer inventory and historical audit notes remain preserved.
4. Original manuscript **143-word abstract**, source **4,994-word main text** (after new Figure 3 citation), and one unsubmitted Ecology Letters-format Letter. No new biological effect size or source-priority claim is introduced. The actual anonymous reviewer-word count must be checked independently in CI.
5. Reviewer-package membership remains **four main figures and three supplementary figures**; no extra untracked graphic file is inserted. Previous figure-source intake reports described the source's *historical role* as the then Figure 3; they remain useful provenance but are superseded for **current display numbering** by this document.

## Actual 2026-10-16 reviewed delivery verification

The [successful scientific/package Actions run 38828554768](https://github.com/zuizui0223/izu-core/actions/runs/38828554768), original artifact `12016501642`, produced a **157-member ZIP** with four main and three supplementary figures, a **143-word abstract** and **4,997-word anonymized main text**. Outer artifact ZIP SHA-256 `9868c4d358229cc2dd14a74a1fcbbaf0b8e4deba25d2177f21598bb2ddbd9d7e`; inner reviewer ZIP SHA-256 `ae2a91be1cb878724d3d8a4dd469a7a1602694f683215318ccab6ee828fcc918`. Both ZIPs passed full CRC checks. The actual main `Figure3.pdf` is byte-exact to the original pinned atom/ABM source (28,988 bytes, SHA-256 `51c65d51b242834a51bab1a9f84b87c6dcfcb8e5ad30d875b6620b391ccb2997`). The regenerated supporting `SupplementaryFigureS3.pdf` is **pixel-exact** to the previous main Figure3 under matched 145-dpi rendering, notwithstanding PDF metadata hash changes. New main/supplementary captions, the anonymized SI figure-role transformation and the historical source SI immutability were verified in the reviewer archive. No new biological result or external DOI is asserted.

## Scientific claim ceiling and external deposit

Original full 389,730,774-byte atom/ABM source ZIP with 774 members and 320 × 201 native finite diploid genomic censuses has been re-read and its original labels/checkpoints verified. Its preservation remains on GitHub: **not an independent cross-host DOI deposit**. The deterministic genotype-density operator is **not equal by definition to the finite ABM's mathematical stochastic expectation**; the difference between 3/32 and A-first density does not uniquely partition drift from stochastic genetic transmission and demographic feedback. A-first depends on threshold: source-matched density event order changes at 0.025 and 0.1.

External source coverage across the single Letter, author/license/version/access approval, durable external DOI and independent download remain **open in [Issue #436](https://github.com/zuizui0223/izu-core/issues/436)**. This document is no submission or deposit receipt.

**GO:** source-matched editorial Figure 3/S3 swap after exact-head scientific gate, CI and reviewer PDF visual inspection. **NO-GO:** treating these as independent ecological islands, a new experimental confirmation, an identified genetic drift share, or a deposited/public DOI.
