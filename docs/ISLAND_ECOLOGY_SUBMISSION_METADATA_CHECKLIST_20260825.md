# Submission metadata checklist — shared gate with Journal of Ecology fallback provenance

Updated: 2026-09-06

The active first-submission route is now **Oikos Research Paper**. This file is retained because the metadata builder originated on the Journal of Ecology route and remains part of the regression-tested provenance. The current journal-specific checklist is `docs/CHAPTER2_OIKOS_SUBMISSION_CHECKLIST_20260831.md`.

Scientific status: **the scientific and manuscript-integration gates are closed.**

Author-supplied metadata and declarations are the active blocker. The completed response-geometry, parameter-robustness and conditional-WHY diagnostics remain frozen, and the current world-saturation/Izu-continuity manuscript state is recorded separately in the active Oikos manifest and submission-closure audit.

The final submission builder is intentionally blocked until all required identity metadata, confirmations and declarations are supplied.

## Completed scientific and manuscript work

The historical reassessment chain remains provenance: response geometry was mapped, pseudo-precise design frequencies were demoted, local-support semantics were corrected, external coverage was demoted from validation, and the conditional-WHY diagnostics were frozen. Subsequent work expanded the empirical confrontation without reopening those frozen claims, reached the geography-first world stopping rule, and justified Izu by measurement continuity rather than convenience or positive fit.

No additional simulation, world expansion or Chapter 3 phenotype result is required for the current Chapter 2 submission.

## Author metadata required now

Populate `data/design/island_ecology_submission_metadata_template.json` with:

1. final author order and affiliations;
2. corresponding-author selection, email, postal address and required ORCID;
3. coauthor ORCIDs if supplied;
4. Significance prior-work context;
5. acknowledgements, explicitly `None` if applicable;
6. funding, explicitly `None` if applicable;
7. inclusion / EDI statement;
8. conflict-of-interest statement;
9. author review of the prefilled ethics statement, followed by `ethics_statement_confirmed: true` only if accurate;
10. explicit submission declarations.

Author contributions / CRediT roles are not an initial-submission blocker on the active Oikos preflight and may remain unset until revision.

These values must still be supplied explicitly rather than inferred.

## Builders and closure audit

Identity-bearing metadata files can be validated with:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

The non-identity scientific/renderer/package preflight is:

```bash
python scripts/audit_chapter2_submission_closure.py --check
```

The final bundle command is:

```bash
python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

It will raise an error until all required metadata and declarations are supplied. The closure audit additionally fails if a future scientific, renderer or required-file regression appears, so such regressions cannot be mislabeled as author blockers.

## Double-anonymous boundary

When submission readiness is restored, title-page and author information remain separate from the anonymous manuscript and reviewer archive.
