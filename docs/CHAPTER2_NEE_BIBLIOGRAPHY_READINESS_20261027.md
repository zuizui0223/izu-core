# Chapter 2 NEE Article — bibliography and source-manuscript readiness (2026-10-27)

**Status:** editorial source-integrity gate, not proof of final journal submission, original publisher-level validation of every reference, external DOI deposit or author approval. The single source-of-truth manuscript is [the completed R1–R5 Article](CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md).

## What was actually checked and repaired

1. The merged [primary-literature novelty audit](CHAPTER2_PRIMARY_LITERATURE_NOVELTY_AUDIT_20261027.md) distinguishes known island establishment, floral shift, genetic erosion and rescue theory from the **registered, model-specific founder-relative high-I allele-support policy contrast**. It does not claim systematic-search coverage or priority over every publication.
2. The previously retained NEE reference list had **29 DOI-bearing entries**, but six author-year pairs had no matching prose citation: *Bodbyl Roels & Kelly (2011)*, *Lande & Schemske (1985)*, *Lande & Porcher (2015)*, *Teixido & Aizen (2019)*, *Opedal (2019)*, and the **Acoca-Pidolle (2025) preprint**. The latter did not appear as an uncited surname because two other Acoca-Pidolle years were already cited.
3. All six were incorporated only into context-appropriate **Introduction or Discussion** sentences; original reference identities and DOI tokens were not deleted or altered. The 2025 preprint remains labelled **preprint**, not an accepted/peer-reviewed article or demonstrated universal irreversibility.
4. The technical [citation integrity test](../tests/test_chapter2_nee_citation_integrity_20261027.py) now fails if any of the **29** DOI-bearing entries is duplicated or lacks an author–year occurrence in the manuscript preceding References. This verifies editorial *citation presence*, **not** DOI resolution or all fields of all publisher metadata.
5. Independent publisher/PubMed lookups specifically confirmed titles/authors/journal/DOI identities for *Bodbyl Roels & Kelly (2011)* `10.1111/j.1558-5646.2011.01326.x`, *Lande & Schemske (1985)* `10.1111/j.1558-5646.1985.tb04077.x`, *Lande & Porcher (2015)* `10.1534/genetics.115.176693`, *Teixido & Aizen (2019)* `10.1093/aob/mcz014`, and *Opedal (2019)* `10.1111/nph.15403`. The Acoca-Pidolle preprint DOI `10.32942/X2R93P` is recorded on the author's ORCID and public preprint listing; it is not re-labelled as peer-reviewed.

## Active article invariants after this purely editorial revision

| Item | Gate | Meaning |
|---|---|---|
| Title | *Recurrent reproductive assurance and contingent floral evolution in an island plant model* | Explicit synthetic-model scope |
| Abstract | **174** whitespace-delimited words | Same abstract as the updated original review and editor enquiry |
| Main source | **3,498** whitespace-delimited words including source-only Discussion subheads | Below the repo's 3,500-word NEE Article limit; journal-composed output strips seven Discussion headings |
| Main figures | Exactly **6** Figure 1–6 legends, unchanged | Existing figures remain draft, not final print-certified artwork |
| R1–R5 Results | **Byte-identical** to the source-recovery working copy | No registered, negative or exploratory outcome changed |
| Registered R4 | genetic +8.328125 percentage points (B8), survival interaction +92.707031 points (B8 × B4.5) | **Separate original endpoints**, not estimated causal mediation |
| Prospective R2 | HOLD / NO DISPATCH; 384-cohort primary decision `both_inconclusive` | No biological run added |
| External archival DOI | **Not deposited / not verified** | GitHub draft releases/old archive receipts do not constitute independent repository deposits |

## Remaining production and external-input conditions

- **Reference metadata:** the precise final author list, punctuation, publisher bibliographic fields (volume, issue, first/last pages, early-online status) and journal citation style need an independent complete reference-manager or publisher check. The current author–year Markdown bibliography remains labelled *preliminary*, and final NEE formatting is not done.
- **Manuscript:** the source-only seven Discussion navigation headings must be removed through the audited formatter, not by changing the original scientific prose. Full source-relative Markdown links need journal-safe handling; compile the manuscript/Methods/supplement, visually inspect all six final figures and confirm citations in the final export.
- **Data/code:** verify the R1–R5 minimal raw deposit dataset and four original demographic source cohorts, complete rights/licence metadata, submit an approved external archive with independent download/hash readback, and add real data/code availability statements when materialized. Do not invent a DOI.
- **Author/legal:** order, affiliations, corresponding author/ORCID, roles, conflicts, funding, permissions, final submission/related-manuscript declarations and all-author signoff are still outstanding.
- **No new science:** neither citations nor this readiness note claim general island causality, universal selection-to-fixation fractions, actual pollen-restoration irreversibility, or confirmed initial selfing advantage.

**Decision:** The one-paper literature and citation correspondence are now source-checkable. This alone does **not** turn `submission_ready` true; the remaining blocking steps are production, archive/access, bibliography field QA and author-controlled approvals.
