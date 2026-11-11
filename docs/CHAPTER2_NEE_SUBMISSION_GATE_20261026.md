# Chapter 2 Nature Ecology & Evolution submission gate (2026-10-26)

**Merged-source checkpoint (2026-10-26):** [PR #642](https://github.com/zuizui0223/izu-core/pull/642) and [PR #643](https://github.com/zuizui0223/izu-core/pull/643) have been merged into main at commits `62e21fc6081aef99c45db45781eda0a1ef6d0e07` and `b82e529ecb9bc0dfebfd73e1b73bf164b2bb4b4c`, respectively, after their exact PR-head CI and Chapter 2 scientific gates reported success. This verifies the review branches, not an independent NEE editorial assessment. The current master title, paper abstract and R1–R5 Results were merged without modifying any frozen biological producer, registered G/S values or original R2 `both_inconclusive` adjudication. The **journal-ready / submission / DOI** status stays **false / none / none**.

**Scope:** editorial/repository verification only. This file records completed and blocked submission prerequisites; no submitted manuscript, Nature Ecology & Evolution (NEE) editorial decision, raw archive upload, author approval, or DOI is claimed. The single scientific Article remains the [completed-evidence editing master](CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md), with [five-result evidence / original nulls](CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md).

## 1. Current paper and boundary of the new front-facing storyline

Working title (model-bounded, not guaranteed final):
**Recurrent reproductive assurance and contingent floral evolution in an island plant model**

This is a **finite diploid simulation study**, not a direct historical estimate of island-floral evolution. It distinguishes reproductive assurance capacity A, visitor functional matching M, and allocation investment I. The central inference remains the *registered* separation of genetic target access and resource-dependent persistence; distinct A/M/I repeatability and prediction estimates are **exploratory, separate cohorts**. A is not equivalent to SC/realized selfing; M is not literal flower colour/architecture, and I is not physical flower size. No demonstrated four-stage causal mediation, quantified pure drift share, or irreversible genetic evolutionary trap.

| Checked component | Status and evidence |
|---|---|
| Core original Q1–Q4 and R1–R5 | Unchanged numeric/registered results; [five-result Article](CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md) and [original source recovery tests](../tests/test_chapter2_r1_r5_source_recovery_20261022.py) |
| New introduction/R3/Discussion emphasis | Functional recurrence versus conditional flower evolution with honest A/M/I qualifications; source-matched editor draft, not new registered discovery |
| R3 A repeatability | Exploratory, across all 12 setting × start cells A far-endpoint within-context variance < I; among four central starts, exact-four-repeat A 66–111/128 versus I 7–20/128. Many invariant near/far A contrasts are zero. [Source audit](CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.md) |
| A fixation direction | Separate 160 × 160 B8 cohort, high available A=.75 allele fixation 25,307/25,600 evolving versus 5,145/25,600 fixed expression; source audit shows non-neutral directional component without independent selection/fixation shares. [#617 source](CHAPTER2_A_DIRECTION_VS_FIXATION_EVIDENCE_20261022.md) |
| M versus I history prediction | Known-source leave-cell-out squared prediction-error reduction +40.146% (M change) versus +0.359% (I change); no inference about new founders, colour/shape, or chance percentage. [Prediction audit](CHAPTER2_FOUNDER_PREDICTABILITY_RESULTS_20261021.md) |
| Registered policy effects | B8 high-I target support loss +8.328125 pp; B4.5/B8 survival policy × resource +92.707031 pp, separate primary endpoints. [Raw-admitted results](CHAPTER2_CONFIRM160_RESULTS_20261019.md) |

## 2. Exact Chapter 1 and prior-art treatment

[Chapter 1 in the `island` repository](https://github.com/zuizui0223/island/pull/319) remains a Draft submission PR. The current public repository does not establish publication, a publicly citable manuscript DOI, or a submitted version. **Do not place Ch1 as a published or in-press reference.** Introduce the ecological tension with actual published research, notably:

- Grossenbacher et al. (2017), *New Phytologist*. doi:10.1111/nph.14534 — relative prevalence of self-compatibility on islands.
- Hetherington-Rauth & Johnson (2020), *American Naturalist* 196:87–100, doi:10.1086/709018 — no universal island flower-size reduction across the studied taxa.
- Ciarle (2026), *Oikos* e11782, doi:10.1002/oik.11782 — *Coprosma* leaf/stature analyses distinguish biased colonization and in situ evolution. This is a caution against treating extant island trait composition as historical floral evolution, **not** a test of our A/M/I pollination mechanisms.

Ch1 may be described as a **related in-preparation macroecological analysis** in a transparent editorial cover letter, if appropriate and approved by the author(s), while explaining overlap and non-overlap; do not misrepresent it as submitted. If an actual public DOI/status subsequently exists, verify it before citing. Ch1 and Ch2 use different data streams, questions and inferential estimands.

## 3. NEE Article format: checked versus still open

Official [Nature Ecology & Evolution Article requirements](https://www.nature.com/natecolevol/content): main text ≤3,500 words, abstract ≤200 words, ≤6 display items; Introduction without a heading in the composed version, topical Results and Methods subheadings, **no Discussion subheadings**, reference guideline ~50. The edited source Article satisfies **174 abstract whitespace-delimited words** and **3,411 Introduction-through-Discussion whitespace-delimited words (including source navigation headings)** on this branch. The seven Discussion navigation headings are **retained in the source master** to preserve the audited renderer's explicit source-to-output contract; the final composed Article **removes** them without changing Discussion prose. Likewise, the Markdown `## Introduction` marker is removed only in the journal-formatted export. Six proposed main display figures already exist as source-linked drafts; final vector/image, captions and export QA are **not** thereby certified.

**Still open beyond raw DOI:** final integrated Figure 1–6 visual QA and print/export layout; executable Methods and associated source manifest accuracy; references and declarations, author order/approval, affiliations, contributions, funding, conflicts; reviewer-accessible reproducibility; data and code availability URLs; final journal-specific package and author signoff. These are required checks, not grounds to mislabel the work submission-ready.

### 2026-10-27 citation-source audit — completed editorial preflight, not final references

The [bibliography/source readiness audit](CHAPTER2_NEE_BIBLIOGRAPHY_READINESS_20261027.md) reconciles all **29** retained DOI-bearing manuscript bibliography entries with an author–year citation preceding References. Five previously unused published sources and a 2025 **preprint** were cited without changing the R1–R5 Results or numerical figures. The current editing master remains **174 abstract / 3,498 main source words including seven editorial Discussion headings**. The [new source-only check](../tests/test_chapter2_nee_citation_integrity_20261027.py) covers unique DOI tokens, citation presence and unchanged five-result evidence. Full DOI metadata and NEE reference-format review still require journal production QA and author approval; this does not resolve the raw-data/archive and permission gates.

## 4. DOI deposit is a real remaining blocker (not a fictitious link)

For a Nature Portfolio empirical/model Article, a transparent minimum-dataset **Data availability** statement and reviewers' access are required; code-central research needs **Code availability** details and a citable version when possible. [Nature Portfolio reporting policy](https://www.nature.com/ncomms/editorial-policies/reporting-standards).

Current code, raw results and historical original-source receipts remain in GitHub Actions/draft Releases and local/saved archives. This is **not** an external long-term DOI deposit. Existing [raw-archive issue #436](https://github.com/zuizui0223/izu-core/issues/436) covers four original demographic cohorts (521 Actions artifact ZIPs, in four separate protected tar archives); it does not by itself establish a complete **current** R1–R5 manuscript deposit. The source-tracked [deposit-readiness inventory](CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md) is an earlier-version checkpoint, not proof of bytes uploaded to an independent repository.

**Deposit gate, to be executed only with actual archive access and contributor/license clearance:**

1. Define the *current R1–R5 minimum sufficient dataset* (original source/model commits, frozen protocols, registered primary outcomes and nulls, independent fresh-founder experiments, 160 × 160 raw receipts/source genomes, conditional transfer evidence, published figures, read-only reproducible scripts). Keep original biological run and nested design identities; don't require unexplained inclusion of all historical exploratory analyses.
2. Inventory the original **bytes**, archive members, internal hashes/CRCs, exact SHA-256 receipts and independent-source axes. Retrieve verified archives from original storage; a JSON inventory or DOI placeholder is not a download.
3. Obtain rights/licensing, author-approved uploader/ORCID metadata, repository choice, publication/embargo decision and external account authorization. Prefer a versioned DOI-minting repository with sufficient total size and independent governance (e.g. institutional repository/Zenodo/Dryad, subject to their actual limits and permissions).
4. Upload approved bytes; **re-download from the external host** and independently verify raw/archive hashes, complete membership, critical JSON readouts and executable reproducibility. Record the resulting exact DOI/version/URL and access/license in the Article, `REPRODUCE.md`, and source-deposit receipt.
5. Only then mark the relevant data-deposit gate resolved; do not close #436 unless all **four** demographic cohorts specified there are independently preserved and verified.

**No account authorization, external upload or external DOI has been completed by this document.**

## 5. Freeze unrelated experiment expansion

The remaining R2 prospective founder × visitor × nested-repeat genetic-access programme is **HOLD**, independent from publication of this bounded Article. Earlier 384-carrier prospective primary outcomes remain `both_inconclusive`. Current static identifiability exercises and planning PRs do not enable production biological workers. Reopen only in response to a separately approved scientific design or explicit editorial/reviewer request. No silent resampling to turn an inconclusive result positive.

## Current decision

- **Editorial structure:** A/M/I framing integrated while maintaining R4 registered inferential centre.
- **Scientific claim priority:** R1–R5 as originally admitted; exploratory predictability not promoted to proof of drift, natural island histories or species-level convergence.
- **Journal-ready:** **false** until the full data/code, figure/method, authorship and package gates are met.
- **Submission / DOI:** neither is claimed to exist.
