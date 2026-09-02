# Chapter 2 Oikos submission checklist

Updated: 2026-09-02

## Active route

- Journal: **Oikos**
- Article type: **Research Paper**
- Scientific tier: **Tier B — mechanistically resolved synthetic response geometry with bounded empirical confrontation**
- Journal-facing story: **Theory → Global confrontation → Identifiability → Izu mechanistic-resolution zoom**
- Expanded story: **simulation builds the relational response theory → the response vocabulary is carried into global island ecology → the source audit exposes an outcome-rich/process-poor process-measurement bottleneck → Izu increases resolution to separate composition-level matching from beyond-composition sorting**
- Fallback: **Journal of Ecology Research Article**

Narrative contract:

`docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md`

The scientific and manuscript-integration gates are closed. No additional simulation, world projection or Chapter 3 empirical result is required for the active Chapter 2 submission route.

The global step must remain bounded: the **response vocabulary** is projected/carried into the empirical island literature, but empirical systems are not assigned to synthetic regime labels and the 25-entry audit is not presented as validation coverage.

## Oikos initial-submission requirements implemented

- double-anonymous manuscript rendering;
- separate identity-bearing title page;
- main text rendered to **RTF**, an Oikos-supported upload format;
- single-column, double-spaced RTF main text;
- continuous line numbering and page numbering encoded in the RTF;
- Introduction forced to begin on page two;
- abstract capped at 300 words by the active manuscript contract;
- submission renderer replaces the old five-question labels with the four-act journal-facing funnel;
- dedicated Significance statement;
- Data Availability / data-archiving statement;
- accepted-stage public repository fixed to **Dryad Digital Repository**; the anonymous review ZIP remains the first-submission reviewer surface;
- conflict-of-interest and ethics statement surfaces;
- reviewer-ready frozen data, code and audit materials in the anonymous review archive;
- figures regenerated fail-closed against frozen scientific results before the relational Oikos overlay;
- Supporting information rendered as a separate RTF file;
- specific Appendix/Fig. S references are blocked from the blinded main text; the Oshima sensitivity is referred to only as **Supporting information**;
- no dissertation-internal Chapter 1/2/3 routing in the blinded manuscript or rendered Supporting information.

The active submission manifest is:

`data/design/chapter2_oikos_submission_manifest_20260831.json`

The active metadata template is:

`data/design/island_ecology_submission_metadata_template.json`

## Scientific claim ceiling retained at submission

The submission must continue to state that:

- the model defines conditional response possibilities, not natural prevalence;
- partner loss/arrival coefficients are fixed-surface diagnostics, not field-causal estimates;
- response direction is relational rather than intrinsic: starting state matters through its relation to the community actually realized;
- the exact baseline variance shares are finite-ensemble diagnostics, not stable population magnitudes;
- realized community remains the largest additive component across the prespecified seed and structural-horizon sensitivities, while starting state alone remains weak and state × community nonadditivity remains consequential;
- mixed geometry persists at zero trait adjustment and under equal initial pollinator richness; the latter supports only that richness reduction is not necessary for mixed geometry;
- global island systems establish the empirical necessity of a richer response vocabulary, not fitted synthetic-regime projection or validation coverage;
- the audited literature is outcome-rich but process-poor: direct response outcomes occur in 21/25 entries but partner arrival/replacement in only 2/25;
- 0/25 audited research entries meet the full outcome-independent external-prediction contract, so formal held-out prediction is `not_evaluable`;
- Izu raw matching is structured at the source-state/background-community-composition level;
- null-corrected beyond-composition sorting is unsupported;
- the prespecified Oshima-source bridge is unsupported;
- Chapter 3 phenotype is not Chapter 2 validation.

## Author-supplied information still required

The public repository choice is no longer an author blocker: **Dryad Digital Repository** is fixed for accepted-stage public data/code archiving under the active Oikos route.

Populate the metadata template with one consolidated block containing:

1. final ordered author list and each author's affiliations;
2. corresponding-author email, postal address and **ORCID** — Oikos requires the corresponding author to provide an ORCID at submission;
3. coauthor ORCIDs if supplied (encouraged, not required by this preflight);
4. a short **Significance prior-work context** explaining how this manuscript builds on relevant work by the submitting authors/coauthors cited in the paper and on other published work;
5. acknowledgements and funding, explicitly using `None` where applicable;
6. inclusion / EDI statement;
7. conflict-of-interest statement;
8. confirmation that the prefilled ethics statement accurately reflects the manuscript's lack of new field sampling, specimen collection or experimental work requiring new approvals;
9. explicit submission-declaration booleans.

**CRediT / author-contribution roles are not an initial-submission blocker.** Oikos requires CRediT for revised submissions; if no contribution statement is supplied now, the submission statements explicitly defer CRediT to revision.

These values are intentionally not inferred from repository history.

## Final build

When the author-supplied fields are complete:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json

python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Expected bundle:

`dist/chapter2_oikos_submission_bundle.zip`

The upload-facing bundle contains:

- `MANUSCRIPT.rtf` — blinded, double-spaced, continuous line/page numbers, Introduction on page two;
- `SUPPORTING_INFORMATION.rtf`;
- `TITLE_PAGE.rtf`;
- `COVER_LETTER.rtf`;
- `SIGNIFICANCE_STATEMENT.rtf`;
- `SUBMISSION_STATEMENTS.rtf`;
- deterministic figures and figure-input provenance;
- the anonymous reviewer data/code archive;
- the active Oikos manifest and frozen scientific audit files.

Until the author-supplied fields and declarations are complete, the builder remains fail-closed by design.
