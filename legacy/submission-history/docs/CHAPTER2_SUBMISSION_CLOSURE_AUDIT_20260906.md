# Chapter 2 submission-closure audit

Updated: 2026-09-12

## Decision

**The scientific gate is closed on the mechanism-mainline paper.** The active scientific sequence is conditional response geometry → exact realized-richness control → finite-community/system-size determinant ordering → downstream modifiers → source-audited metadata/secondary-data confrontation → bounded empirical claim ceiling.

Chapter 2 is complete without new focal field data. Field E3/E4 is not required for current-paper completion. No additional simulation, world-island expansion, Izu same-block field result, NEE Stage-1 result or Chapter 3 phenotype result is required to make the current mechanism manuscript scientifically complete.

The machine-readable completion contract is `data/design/chapter2_simulation_metadata_completion_lock_20260912.json`. The claim-by-claim evidence map is `docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md`.

The machine-readable submission audit is `data/results/chapter2_submission_closure_audit_20260906.json` and is regenerated/checked by:

```bash
python scripts/audit_chapter2_submission_closure.py --check
```

## What the audit checks

Before classifying anything as an author blocker, the audit verifies that:

1. the frozen scientific gate is complete;
2. the active manuscript is `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`;
3. the active narrative lock is `docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`;
4. the no-new-focal-data completion lock remains `chapter2_complete_without_new_focal_data`;
5. the Oikos manifest preserves the mechanism-mainline claim ceiling and `field_e3_e4_required_for_current_paper=false`;
6. the active manuscript contains the source-audited metadata confrontation, including the formal `21/25`, `2/25`, `0/25` boundary plus the source-native Wanshan–Yongxing/Ogasawara and existing-Izu stress tests;
7. the blinded manuscript and Supporting Information render to valid RTF;
8. the submission package preserves the distinction between metadata confrontation and full natural validation.

## Scientific boundary

The closure audit does not change scientific results. It freezes these boundaries:

- exact realized-richness matching: ensemble mean all-positive in 6/6 matching seeds while 51–65/96 individual realizations remain mixed;
- active-adjustment system-size audit: starting-position median share 2.55% → 55.84%, community-realization median share 72.98% → 12.72%, with starting position larger in 6/6 seeds from `k=4` onward;
- deterministic mean-field: branch heterogeneity disappears asymptotically when finite realized composition is averaged away;
- numerical crossover: model-specific, not a natural threshold;
- formal empirical audit: 25 entries / 21 exact labels, comparable plant responses 21/25, direct partner arrival/replacement 2/25, full contracts 0/25, formal external prediction `not_evaluable`;
- source-native external confrontation: large partner turnover in Wanshan–Yongxing and Anijima can coexist with richness log-response intervals spanning zero; these are matched-plant contrasts, not replicated causal island effects;
- existing Izu confrontation: functional exposure → corrected matching is robust, matching → pollen is weaker and not leave-one-island sign stable, the historical signed-position projection fails null correction, and the Oshima bridge is not independently causal;
- metadata/secondary data therefore establish biological plausibility, adversarial stress tests and identifiability limits, **not full validation of the synthetic mechanism**;
- Chapter 3 phenotype: independently owned, not Chapter 2 validation;
- prospective Izu E3/E4: **post-Chapter-2 transport/falsification**, not a current completion gate.

## Figure / manuscript endpoint

The visual and inferential endpoint of the current manuscript is Figure 4:

```text
formal measurement ceiling
→ source-native composition ≠ richness contrasts
→ existing Izu support/failure
→ explicit synthetic-to-natural claim boundary
```

The future visitor → SVD → dependency → mature-seed chain is not the endpoint of Chapter 2. It may be used in a later prospective paper without reopening the present mechanism paper.

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

Any future scientific, renderer or packaging regression reopens that specific surface. It must not be mislabeled as a reason to reopen field E3/E4, NEE Stage 1 or additional world searching.
