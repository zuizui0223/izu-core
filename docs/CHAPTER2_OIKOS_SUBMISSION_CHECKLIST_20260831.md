# Chapter 2 Oikos submission checklist

Updated: 2026-09-08

## Active route

- Journal: **Oikos**
- Article type: **Research Paper**
- Scientific tier: **Tier B — hierarchical response architecture with bounded empirical recurrence**
- Journal-facing story: **Mechanistic prediction → Real-world compositional exposure → Izu biological consequence**
- Expanded story: **simulation separates richness-sensitive coarse regime placement from state × composition branch identity → Wanshan–Yongxing and Ogasawara establish source-native partner turnover/rewiring beyond a decisive richness contrast → Izu links contemporary functional community structure to corrected plant matching and shows weaker, branched downstream floral and pollen responses**
- Identifiability role: **claim boundary / robustness only; not a coequal study objective**
- Fallback: **Journal of Ecology Research Article**

Narrative contract:

`docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md`

The earlier four-act contract is retained only as provenance:

`docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md`

The scientific and manuscript-integration gates are closed. No additional simulation, world projection or Chapter 3 empirical result is required for the active Chapter 2 submission route.

The external step remains bounded: empirical systems are not assigned to synthetic regime labels, Wanshan–Yongxing and Ogasawara are not pooled as a universal island effect, and the 25-entry audit is not presented as validation coverage.

## Oikos initial-submission requirements implemented

- double-anonymous manuscript rendering;
- separate identity-bearing title page;
- main text rendered to **RTF**, an Oikos-supported upload format;
- single-column, double-spaced RTF main text;
- continuous line numbering and page numbering encoded in the RTF;
- Introduction forced to begin on page two;
- abstract capped at 300 words by the active manuscript contract;
- submission renderer uses the three-result journal-facing chain rather than dissertation-internal or old four-act routing;
- dedicated Significance statement;
- Data Availability / data-archiving statement;
- accepted-stage public repository fixed to **Dryad Digital Repository**; the anonymous review ZIP remains the first-submission reviewer surface;
- conflict-of-interest and ethics statement surfaces;
- explicit author confirmation of the prefilled ethics statement is fail-closed in metadata validation;
- reviewer-ready frozen data, code and audit materials in the anonymous review archive;
- figures regenerated fail-closed against frozen scientific results before the realized-richness overlay;
- Supporting information rendered as a separate RTF file;
- specific Appendix/Fig. S references are blocked from the blinded main text; the Oshima sensitivity is referred to only as **Supporting information**;
- no dissertation-internal Chapter 1/2/3 routing in the blinded manuscript or rendered Supporting information.

The active submission manifest is:

`data/design/chapter2_oikos_submission_manifest_20260831.json`

The active metadata template is:

`data/design/island_ecology_submission_metadata_template.json`

The machine-readable submission-closure preflight is:

`data/results/chapter2_submission_closure_audit_20260906.json`

It is regenerated/checked by:

`python scripts/audit_chapter2_submission_closure.py --check`

The closure preflight checks the scientific gate, active source/manifest paths, blinded manuscript RTF controls and Supporting Information renderer before classifying remaining blockers. In the blank author template, the expected state is **non-metadata preflight ready, submission not ready, and only author-supplied metadata/confirmations remaining**.

## Scientific claim ceiling retained at submission

The submission must continue to state that:

### Result 1 — mechanistic prediction

- the model defines response possibilities and mechanism, not natural prevalence;
- partner loss/arrival coefficients are fixed-surface diagnostics, not field-causal estimates;
- exact realized-richness matching makes the ensemble mean all-positive in **6/6** prespecified matching seeds;
- nevertheless **51–65/96** individual communities remain mixed-sign;
- under that hard control, community-realization share remains **50.04–55.92%**, state × community nonadditivity **42.72–48.51%**, and starting-position additive share only **0.94–2.21%**;
- therefore realized richness helps position the coarse mean regime, while branch identity remains contingent on starting state evaluated against realized community composition;
- the earlier **53/96** equal-initial-richness result is an initial-state diagnostic only and must not be used to claim that realized richness is unnecessary;
- local filtering and autonomous assurance remain downstream modifiers, not substitutes for the richness/composition hierarchy.

### Result 2 — real-world compositional exposure

- Wanshan–Yongxing matched plants show partner turnover **0.9796 [0.9443, 1.0000]** while pollinator-richness LRR is **−0.1054 [−1.3218, +0.2877]**;
- Ogasawara Anijima context shows partner turnover **0.6817 [0.4975, 0.9653]** while pollinator-richness LRR is **−0.3146 [−0.8755, +0.4055]**;
- these support the bounded statement that substantial composition change/rewiring can occur without a correspondingly decisive richness contrast;
- the two contexts are not exchangeable replication, a pooled coefficient, or causal evidence for geological island origin or anole invasion;
- the broader 42-entry/37-label world inventory remains descriptive context rather than an independent prevalence sample.

### Historical claim boundary

- the audited literature remains outcome-rich but process-poor: direct response outcomes occur in 21/25 entries but partner arrival/replacement in only 2/25;
- 0/25 audited research entries meet the full outcome-independent historical transition contract, so formal held-out prediction remains `not_evaluable`;
- geography-first expansion and the small-island supplement remain supporting robustness/provenance, not the paper's primary objective;
- this boundary prevents the contemporary empirical results from being rewritten as a matched historical causal transition.

### Result 3 — Izu biological consequence

- contemporary pollinator functional diversity predicts corrected trait matching with leave-one-island sign stability: **+1.9426** in Izu5 and **+2.0590** in post-Oshima4;
- matching-to-pollen propagation is positive on average (**+0.0353**, **+0.0342**) but island-fragile;
- all 8/8 shared plant targets have lower corrected matching post-Oshima, but floral tubes split **3 shorter / 4 longer / 1 unchanged** and pollen responses split **4 lower / 4 higher**;
- the historical signed-position raw association may remain as a boundary analysis, but null-corrected beyond-composition sorting is unsupported and the prespecified Oshima-source bridge is unsupported;
- FDQ does not establish causal matching change, matching does not establish causal pollen change, and present-day Izu associations do not identify historical *Bombus* loss;
- Chapter 3 phenotype is not Chapter 2 validation.

## Author-supplied information still required

The public repository choice is no longer an author blocker: **Dryad Digital Repository** is fixed for accepted-stage public data/code archiving under the active Oikos route.

Populate the metadata template with one consolidated block containing:

1. final ordered author list and each author's affiliations;
2. corresponding-author selection, email, postal address and **ORCID**;
3. coauthor ORCIDs if supplied;
4. a short **Significance prior-work context**;
5. acknowledgements, explicitly using `None` where applicable;
6. funding, explicitly using `None` where applicable;
7. inclusion / EDI statement;
8. conflict-of-interest statement;
9. confirmation that the prefilled ethics statement accurately reflects the manuscript's lack of new field sampling, specimen collection or experimental work requiring new approvals — set `ethics_statement_confirmed` to `true` only after that review;
10. explicit submission-declaration booleans.

**CRediT / author-contribution roles are not an initial-submission blocker.** Oikos requires CRediT for revised submissions; if no contribution statement is supplied now, the submission statements explicitly defer CRediT to revision.

These values are intentionally not inferred from repository history.

## Final build

When the author-supplied fields are complete:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json

python scripts/audit_chapter2_submission_closure.py --check

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

Until the author-supplied fields, ethics confirmation and declarations are complete, the builder remains fail-closed by design. Any future non-metadata error reopens packaging/renderer work rather than being mislabeled as an author blocker.
