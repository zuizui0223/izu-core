# Chapter 2 submission-closure audit

Updated: 2026-09-06

## Decision

**Chapter 2 is closed on the scientific, manuscript, renderer and non-identity packaging surfaces.**

The remaining path to an actual Oikos submission is now restricted to author-supplied identity, declarations and confirmations. No additional simulation, world-island expansion, Izu analysis or Chapter 3 phenotype result is required to make the current Chapter 2 submission scientifically complete.

The machine-readable audit is:

`data/results/chapter2_submission_closure_audit_20260906.json`

and is regenerated/checked by:

```bash
python scripts/audit_chapter2_submission_closure.py --check
```

## What the audit checks before calling something an author blocker

The audit does not merely inspect empty metadata fields. It first verifies that:

1. the frozen Chapter 2 scientific gate is complete;
2. the active manuscript used by the bundle is `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`;
3. all static submission surfaces required by the bundle exist;
4. the active Oikos manifest still preserves the 0/25 full-contract ceiling and the post-saturation Izu measurement-continuity rule;
5. the blinded main manuscript can render to RTF with double spacing, continuous line numbering, page numbering and the required page break before Introduction;
6. the Supporting Information can render independently to RTF.

Only after those checks pass are remaining validation failures classified as author-supplied metadata/confirmation blockers.

Current result:

- scientific gate complete: **yes**;
- non-metadata submission preflight ready: **yes**;
- non-metadata submission errors: **0**;
- submission ready: **no**;
- blocker class: **author-supplied metadata and confirmations only**.

## Current blank-template validation state

The blank metadata template intentionally produces **14 concrete validation errors**. These are grouped into nine practical human-input categories because some related fields are supplied together.

The required categories are:

1. final ordered author list and affiliations;
2. corresponding-author selection, email, postal address and ORCID;
3. Significance prior-work context;
4. acknowledgements;
5. funding;
6. inclusion / EDI statement;
7. conflict-of-interest statement;
8. explicit author confirmation of the prefilled ethics statement;
9. explicit submission declarations.

Coauthor ORCIDs and CRediT roles are not initial-submission blockers under the current preflight. Dryad is already fixed as the accepted-stage public repository.

## Fail-closed correction made in this audit

Before this audit, the checklist required an author to review the prefilled ethics statement, but the metadata validator did not enforce that review. The bundle could therefore have proceeded once the other fields were supplied even if nobody had explicitly confirmed the ethics wording.

This is now fixed with:

`ethics_statement_confirmed`

The field defaults to `null` and must be set to `true` only after an author has checked that the statement accurately describes the submitted manuscript. The metadata and bundle builders now fail closed until that confirmation is present.

## Scientific boundary remains unchanged

This submission audit does not alter any scientific denominator, result or chapter interpretation.

The active boundaries remain:

- descriptive world breadth: **42 research entries / 37 exact geographic labels**;
- frozen formal identifiability universe: **25 entries / 21 exact labels**;
- full outcome-independent contracts: **0/25**;
- formal external prediction: **`not_evaluable`**;
- large-island geography-first expansion: preregistered saturation reached after two consecutive zero-novelty tranches;
- mandatory small-island supplement: partial transition chronology recovered, no full contract;
- Izu: selected after world saturation by measurement continuity and falsification capacity, not proximity, representativeness or positive model fit;
- Chapter 3 *Campanula microdonta* phenotype: independently owned downstream realization, not Chapter 2 validation.

## Next transition

No further repository-side scientific work is required before metadata completion. The next transition is a single consolidated author-metadata block. After that block is supplied, run:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json

python scripts/audit_chapter2_submission_closure.py --check

python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

The final bundle remains fail-closed: if a future scientific, renderer or packaging regression appears, the closure audit will stop classifying the state as author-metadata-only.
