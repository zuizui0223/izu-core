# DOI handoff for the five-result Article

Prepared 21 October 2026. Status: metadata and source crosswalk prepared; no external deposit, reserved DOI or publication is asserted. This handoff extends the historical [unpublished preflight](chapter2_zenodo_unpublished_preflight_20261015.json), whose six core packages do not cover every result in the current manuscript.

## Proposed metadata

**Title:** Code and source data for “Founding constraints and the predictability of reproductive evolution in an island plant model”

**Description:** Model-generated outputs, analysis code and provenance for a finite diploid study of reproductive assurance, floral investment and visitor matching under pollinator limitation. Separate experiments address fixed-assurance investment responses, assurance-by-environment contrasts, trait-specific predictability, registered persistence and target-allele retention, and exploratory transfers. Cohorts have different designs and inference units and must not be pooled as independently sampled natural islands. Negative and inconclusive results, frozen protocols, raw audit records and figure-source mappings accompany the manuscript. No new statistical analysis was performed for this editorial revision.

**Keywords:** reproductive assurance; floral investment; island colonization; pollinator limitation; finite populations; evolutionary predictability.

**Pending author decisions:** ordered creators and affiliations/ORCIDs; corresponding/depositor account; code and data licenses; version label; public-access or embargo choice; rights and author approval. No license or authorship is inferred from the repository owner.

## Source crosswalk

| Manuscript component | Authoritative inventory / receipt | Deposit requirement |
|---|---|---|
| R1–R2 original and fresh-founder intervention comparisons | [original manuscript](../CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md), [fresh-founder results](../CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md), [historical archive inventory](../CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md) | Preserve source campaigns and fresh-founder outputs separately, plus protocols and code revisions |
| R3 matched A/I repeatability | [matched report](../CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.md), [receipt](../audits/CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json) | Include the receipt and the underlying archived repeated-history sources; do not substitute the crossed cohort |
| R3 crossed founder/history prediction | [results](../CHAPTER2_FOUNDER_PREDICTABILITY_RESULTS_20261021.md), [matrix receipt](../audits/CHAPTER2_FOUNDER_PREDICTABILITY_MATRIX_20261021.json), [prediction receipt](../audits/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json) | Include existing matrix, protocol, code, source hashes and held-out prediction outputs; raw source is the confirmation cohort |
| R4 registered confirmation | [completion ledger](../CHAPTER2_CONFIRM160_COMPLETION_LEDGER_20261019.md), [asset SHA256 inventory](../audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json), [independent audit](../audits/CHAPTER2_CONFIRM160_INDEPENDENT_RAW_AUDIT_20261019.json) | Copy exact inventoried assets, protocols and receipts; a draft release may contain additional files and is not itself the admission manifest |
| R5 bounded transfer | [results](../CHAPTER2_READAPTATION_RESULTS_20261019.md), [release readback](../audits/CHAPTER2_READAPTATION_RELEASE_READBACK_20261019.json), [independent audit](../audits/CHAPTER2_READAPTATION_INDEPENDENT_AUDIT_20261019.json) | Include donor bindings, original run outputs, strict-comparison failure and declared tolerance audit; preserve nested replication |
| Extended evidence | [extended evidence](../CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md), [coverage index](../CHAPTER2_REPOSITORY_SYNTHESIS_COVERAGE_20261019.md) | Reconcile all linked pollen-factorial, finite-density, variation-clock, hitchhiking and secondary-colonization sources before asserting complete deposit |
| Manuscript and artwork | [figure map](../CHAPTER2_FIVE_RESULTS_FIGURE_MAP_20261021.md), current article extract and figures/chapter2_nee_five_results | Record final merged commit; include six SVGs, assembly code, references and source map |

## Existing archive gap

[Issue #436](https://github.com/zuizui0223/izu-core/issues/436) tracks four historical independent cohorts comprising 521 original ZIP artifacts. Same-provider draft GitHub releases and an incomplete historical external backup do not satisfy a complete public DOI archive. The [previous handoff](../CHAPTER2_PRIVATE_EXTERNAL_BACKUP_DEPOSIT_HANDOFF_20261013.md) retains the unresolved original-file gap; this revision neither recreates that file nor bypasses its transfer restriction. Current confirmation, prediction, transfer and supplementary sources must additionally be covered by the final deposit inventory.

## Release procedure

1. Pin the merged manuscript/code commit after both PRs pass their required checks; preserve the analysis-producing commits listed by each receipt as well.
2. Resolve creator, license, version and access fields. Decide whether linked software and dataset records are preferable to one combined record.
3. Build an exact file inventory with byte lengths and SHA256 values from the admitted source receipts, checking every supplementary source. Reconcile missing and extra files before upload; do not infer completeness from release asset counts.
4. Upload to an authenticated unpublished archive draft using the provider's current file/size rules. This preparation has not created such a draft.
5. Re-download every uploaded original file and compare hashes. Preserve failures and record complete/partial status independently for each cohort.
6. After author approval, publish the record(s), retain version-specific and concept DOI relationships, and replace manuscript availability placeholders with resolvable identifiers.

Until those steps finish, manuscript availability must say that GitHub source/provenance is available where accessible and external archival deposition is pending. It must not state that all raw outputs are deposited or that a DOI has been assigned.
