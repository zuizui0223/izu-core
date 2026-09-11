# Chapter 2 submission-closure audit

Updated: 2026-09-11

## Decision

**The scientific gate is closed on the mechanism-mainline paper.** The active scientific sequence is conditional response geometry → exact realized-richness control → finite-community/system-size determinant ordering → downstream modifiers, with world/Izu evidence retained as a bounded empirical claim ceiling.

Field E3/E4 is not required for current-paper completion. No additional simulation, world-island expansion, Izu same-block field result or Chapter 3 phenotype result is required to make the current mechanism manuscript scientifically complete.

The machine-readable audit is `data/results/chapter2_submission_closure_audit_20260906.json` and is regenerated/checked by:

```bash
python scripts/audit_chapter2_submission_closure.py --check
```

## What the audit checks

Before classifying anything as an author blocker, the audit verifies that:

1. the frozen scientific gate is complete;
2. the active manuscript is `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`;
3. the active narrative lock is `docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`;
4. the Oikos manifest preserves the mechanism-mainline claim ceiling and `field_e3_e4_required_for_current_paper=false`;
5. the blinded manuscript and Supporting Information render to valid RTF;
6. the submission package still preserves the frozen 0/25 historical full-contract boundary.

The current frozen preflight records schema `1.1`, date `2026-09-11`, scientific state `synthetic_conditional_response_geometry_with_regime_dependent_determinant_ordering`, `mechanism_mainline_locked=true`, and `field_e3_e4_required=false`.

## Scientific boundary

The closure audit does not change scientific results. It freezes these boundaries:

- exact realized-richness matching: ensemble mean all-positive in 6/6 matching seeds while 51–65/96 individual realizations remain mixed;
- active-adjustment system-size audit: starting-position median share 2.55% → 55.84%, community-realization median share 72.98% → 12.72%, with starting position larger in 6/6 seeds from `k=4` onward;
- deterministic mean-field: branch heterogeneity disappears asymptotically when finite realized composition is averaged away;
- numerical crossover: model-specific, not a natural threshold;
- formal empirical audit: 25 entries / 21 exact labels, full contracts 0/25, formal external prediction `not_evaluable`;
- broader world and Izu analyses: Supporting Information/provenance and biological plausibility, not required validation;
- Chapter 3 phenotype: independently owned, not Chapter 2 validation;
- prospective Izu E3/E4: optional future validation programme.

## Remaining author-supplied inputs

The blank metadata template intentionally remains fail-closed. Required human inputs are:

1. final ordered author list and affiliations;
2. corresponding-author selection, email, postal address and ORCID;
3. Significance prior-work context;
4. acknowledgements;
5. funding;
6. inclusion / EDI statement;
7. conflict-of-interest statement;
8. explicit confirmation of the prefilled ethics statement via `ethics_statement_confirmed=true`;
9. explicit submission declarations.

Coauthor ORCIDs and CRediT roles are not initial-submission blockers. Dryad is fixed as the accepted-stage public repository.

## Next transition

After the author metadata block is supplied, run:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json

python scripts/audit_chapter2_submission_closure.py --check

python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Any future scientific, renderer or packaging regression reopens that specific surface. It must not be mislabeled as a reason to reopen field E3/E4.
