# Chapter 2 SI S1–S33 original-source pointer triage (2026-10-15)

**Status: read-only reference inventory, not evidence that all native raw archives were recovered or deposited.** Exact historical baseline: `main c1b08577dd2a2432ce71df001df45a90ad0f0d74`; current SI Git blob `fdecc89abaee3479ae5eef3f476d5ba937505690`. See the [machine-readable 33-section pointer inventory](chapter2_si33_source_pointer_triage_20261015.json), the [original six-core preflight](CHAPTER2_ZENODO_UNPUBLISHED_DRAFT_PREFLIGHT_20261015.md), and the [two-source Q3/Q4 addendum](CHAPTER2_SINGLE_PAPER_RAW_SCOPE_ADDENDUM_20261015.md).

## What was actually measured

A deterministic literal-token scan parsed the merged [Supporting Information S1–S33](../CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md) by exact `## S1.` … `## S33.` headings. It separately retained literal machine-file tokens (including `.json`, `.zip`, `.tar`, `.npz`, `.py`), `EVIDENCE/` reviewer-package entries, named archive tokens, and directly written repository paths. All 33 sections were included; **21** contain a literal machine-file token and **12** do not: **S1, S2, S3, S4, S6, S7, S8, S15, S21, S22, S23, S32**.

**This is not a 21/33 source-completeness score.** `EVIDENCE/...` usually names a compact reviewer-package readout, not the original full native archive; an SI section without a literal extension may still have complete source receipts through shared materials. S32, for example, supplies original source hashes in prose without an explicit `.zip` filename. The scan cannot independently prove archive existence, exact source-to-section sufficiency, right-to-redistribute, full-raw retrieval, or any cross-host deposit. Do not silently promote a candidate connection to confirmed raw source admission.

## All 33 SI section records

| Section | Current merged SI heading | Literal file tokens | Up to two illustrative literal tokens | Context-matched original candidate (not a verified full coverage map) |
| --- | --- | ---: | --- | --- |
| S1 | Preregistered primary evolutionary study and four-setting result | 0 | — | — |
| S2 | Original relative pollen availability and finite horizon | 0 | — | — |
| S3 | Assigned expression-order and finite demographic study | 0 | — | — |
| S4 | Original evolved-genome source checks and demographic nulls | 0 | — | — |
| S5 | Separately frozen visitor-tempo supplement | 3 | `EVIDENCE/TEMPO_AUDIT_SUMMARY.json`, `EVIDENCE/TEMPO_RESULTS.json.gz` | izu_core_functional_loss_tempo_full_20261011.zip |
| S6 | Data accessibility and source provenance | 0 | — | — |
| S7 | Original-mutation numerical admission and matched finite-population realization | 0 | — | completed_atom_abm_20261011.zip |
| S8 | Conditional access boundaries and preparation-policy consequences | 0 | — | — |
| S9 | Controlled-expression test of preparation-policy persistence contrasts | 2 | `../data/results/persistence_mechanism_20261012/original_readout.json.gz`, `../data/results/persistence_mechanism_20261012/readout.json` | — |
| S10 | Initial-mean versus lifelong-expression contributions | 2 | `EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz`, `EVIDENCE/INITIAL_MEAN_READOUT.json` | — |
| S11 | Full-genome finite-response accounting | 1 | `EVIDENCE/GENOME_RESPONSE_READOUT.json` | — |
| S12 | Final occupancy versus cumulative persistence | 8 | `EVIDENCE/DURATION_READOUT.json`, `EVIDENCE/KERNEL_CHANNEL_ARRAYS_MANIFEST.json` | — |
| S13 | Matched finite–density investment-gap accounting and original archive recovery | 4 | `EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json`, `EVIDENCE/OPERATOR_GAP_READOUT.json` | — |
| S14 | Fixed-access ecological order boundary and absorbing states | 3 | `EVIDENCE/DIRECTIONAL_ACCESS_READOUT.json`, `EVIDENCE/ECOLOGICAL_ORDER_READOUT.json` | ecological_order_actual_github_38312090996.zip |
| S15 | Conditional future-state sufficiency | 0 | — | — |
| S16 | Controlled future parental weighting after initial-mean equalization | 1 | `EVIDENCE/FUTURE_PARENT_READOUT.json` | — |
| S17 | Mean-preserving restoration of investment allele variation | 1 | `data/results/investment_variation_restoration_readout_20261013.json` | — |
| S18 | What initial state can identify about realized order | 3 | `EVIDENCE/INITIAL_CLOCK_IDENTIFIABILITY.json`, `EVIDENCE/INITIAL_CLOCK_INDEPENDENT_REVIEW.json` | — |
| S19 | Expected-response onset does not determine realized sequence | 2 | `EVIDENCE/RESPONSE_ONSET_INDEPENDENT_REVIEW.json`, `EVIDENCE/RESPONSE_ONSET_READOUT.json` | — |
| S20 | Hidden genetic access changes realized order at matched initial phenotypes | 1 | `EVIDENCE/GENETIC_ACCESS_FROZEN_EXPLORATORY_READOUT.json` | — |
| S21 | What the existing64-pair variation restoration actually restores | 0 | — | — |
| S22 | Assurance expression in within-class future parent weights | 0 | — | — |
| S23 | Registered conditional futures from the original investment-fixation states | 0 | — | — |
| S24 | Why restored mean investment and threshold events need not agree | 5 | `EVIDENCE/Q3_EVENT_FRESH_RAW_REVIEW.json`, `EVIDENCE/Q3_EVENT_PROVENANCE.json` | — |
| S25 | Retrospective association in unrestricted preparation histories | 4 | `EVIDENCE/NATURAL_ORDER_INDEPENDENT_REVIEW.json`, `EVIDENCE/NATURAL_ORDER_PUBLIC_READBACK.json` | — |
| S26 | Registered distribution-policy contrasts and limits of maintenance identification | 3 | `EVIDENCE/Q3_TRIANGLE_CAMPAIGN_MANIFEST.json`, `EVIDENCE/Q3_TRIANGLE_INDEPENDENT_VERIFICATION.json` | — |
| S27 | Archived response-threshold sensitivity | 1 | `data/results/genetic_access_pilot_20261014/ARCHIVE_THRESHOLD_SENSITIVITY_INTAKE_20261014.json` | — |
| S28 | Approved attained-mean control of unrestricted natural histories | 4 | `EVIDENCE/NATURAL_ORDER_MEAN_INDEPENDENT_ADMISSION.json`, `EVIDENCE/NATURAL_ORDER_MEAN_PUBLIC_READBACK.json` | — |
| S29 | Original-I-constrained F1 genetic access versus conditional reproductive returns | 4 | `EVIDENCE/Q2_S29_FOUR_SIGN_MENDELIAN_F1.json`, `EVIDENCE/Q2_S29_ORIGINAL_I_M0_M6_F1.json` | — |
| S30 | Separately frozen investment-mutation renewal: unresolved ecological order reversal | 2 | `STANDING_ACCESS_CASES.json.gz`, `STANDING_ACCESS_READOUT.json` | — |
| S31 | Original-birth accounting of nonresponse after renewed standing support | 2 | `NONRESPONSE_CASES.json.gz`, `NONRESPONSE_READOUT.json` | — |
| S32 | Original-genome checkpoint diagnosis of the far-side assurance contrast | 0 | — | — |
| S33 | Independent 32-history prehistory-by-evolvability persistence under synthetic stress | 3 | `../data/design/chapter2_island_demographic_independent32_20261008.json`, `../data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json` | izu_core_island_demographic_stress_20261008.zip |

The **four candidate family hints** in the rightmost column are narrow: S5 visitor-tempo archive, S7 original mutation finite-ABM candidate, S14 the Q3 original 2,304-history pedigree archive, and S33 the independent Q4 32-history archive. S5/S7 are preflight *family-label correspondences*; S14/S33 are explicitly linked by the merged Q3/Q4 source addendum. None is independently re-downloaded or assigned a DOI in this audit. Original field/effect denominators across these archives must **not** be pooled.

## Ten known archive candidates, exactly as preserved in earlier files

The following values are **copied source receipts** from the unmodified six-core preflight and two/additional candidate sources. Byte sizes and SHA-256 strings are historical recorded values, **not re-computed payload hashes in this PR**.

| # | Original container filename | Recorded bytes | Recorded SHA-256 | Inventory stage |
| --- | --- | ---: | --- | --- |
| 1 | `chapter2-orthogonal-130-original-shard-artifacts.tar` | 227,543,040 | `03e1292511219ea4ee64499d35ac0e5a5f824f1ee0fd420ecd7ca97f4f9ebf65` | six_core_preflight |
| 2 | `chapter2-kb-130-original-shard-artifacts.tar` | 226,304,000 | `7d367a9e4a9f4f60f25dbee2ccabc84ef0969f5d9b0096c7df07380314dcfff9` | six_core_preflight |
| 3 | `chapter2-fixedB48-all-original-131-artifacts.tar` | 224,860,160 | `3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c` | six_core_preflight |
| 4 | `chapter2-timed-130-original-shard-artifacts.tar` | 225,617,920 | `b5ab3a99eeaf36da399290508a64fa022cacc734aa1d794cab3b8443707309aa` | six_core_preflight |
| 5 | `chapter2_public_archive_20261006.zip` | 518,372,739 | `0596de11afea2f9f0b5a781f6d0ddd1fa7ea772f048ec0ccfc06e9ecbbf60695` | six_core_preflight |
| 6 | `izu_core_functional_loss_tempo_full_20261011.zip` | 268,940,123 | `034e735d244228c1f4974897a76d16acef10767a81d5dd82f5f5204f48cf0738` | six_core_preflight |
| 7 | `model3_replenishment_evolution_20261005.zip` | 763,914,318 | `37bd0bd312734715392add19f424696121fbe88517dfa784d8e702173ec71b6c` | prior_additional_candidate |
| 8 | `completed_atom_abm_20261011.zip` | 389,730,774 | `7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918` | prior_additional_candidate |
| 9 | `ecological_order_actual_github_38312090996.zip` | 251,663,558 | `819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a` | new_addendum_candidate |
| 10 | `izu_core_island_demographic_stress_20261008.zip` | 335,015 | `cd9f998e38ec51e747c4495dbe94b1fe1168d48d31ef54a438250bfa0ace5a21` | new_addendum_candidate |

Six core + two earlier candidates + two later Q3/Q4 candidates = **ten documented candidate containers**. That count is **not** the number of independent ecological samples or enough to claim complete S1–S33 raw source coverage. The private fixed-B48 **520/521** provider transfer safety stop still applies; a GitHub source clone does not bypass the private transfer/access constraint. DOI/Zenodo source/version/creators/licenses/embargo remain unapproved and unset.

## Next actions and boundaries

1. **Source-family coverage:** for each of S1–S33, resolve original experiment ID, inference unit, exact original raw archive hash and internal member receipt. Reconcile shared trajectories (e.g. S30–S31) before counting a new independent raw family. Start with the 12 sections lacking literal machine-file references, then manually inspect the 21 that do have them.
2. **External source rights:** document public/private location, ownership, access/licensing permissions and availability. A reviewer JSON member or a public GitHub Release is not equivalent to an independently hosted DOI dataset.
3. **Archive admission:** after legitimate author/depositor approval, re-read selected full original raw containers and inner member hashes, then independently verify a second-host durable version. Preserve original failure/negative results and the provider safety stop; do not invent missing receipts.

The parent [Data Availability issue #436](https://github.com/zuizui0223/izu-core/issues/436) remains open. This audit adds **no** reproductive simulations, original data modifications, source transfers, Zenodo draft, external DOI or completed registration of the whole SI universe.
