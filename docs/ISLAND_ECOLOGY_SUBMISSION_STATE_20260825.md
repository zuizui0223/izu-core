# Island ecology submission state

Updated: 2026-08-25

## Current state

The Chapter 2 science is **complete and frozen for submission**.

No new simulation, field dataset, external-system search, parameter retuning, or external research programme is required for the manuscript.

The current submission package has already passed repository CI on Python 3.10, 3.11 and 3.12. The anonymous manuscript, Supporting Information, H2 analytical sign decomposition, figure/table routing, source-audited external-system matrix, claim-boundary tests and anonymous review archive builder are complete.

## Remaining gate

Only **author-supplied submission metadata** remain unresolved.

Required input:

- final ordered author list;
- affiliation(s) for each author;
- corresponding-author email and postal address;
- ORCID(s), if used;
- acknowledgements and funding, including explicit `None` when absent;
- author-contribution statement;
- inclusion statement;
- conflict-of-interest statement;
- explicit submission declarations.

These values must not be inferred from Git history, account identity, another manuscript, or institutional context.

## Fail-closed workflow

Populate:

`data/design/island_ecology_submission_metadata_template.json`

Then run:

```bash
python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

If required metadata remain unresolved, the builder stops without creating an identity-bearing submission package.

When all metadata are supplied, it produces:

`dist/island_ecology_jecology_submission_bundle.zip`

The bundle contains the final title page and cover letter outside a nested **anonymous** review archive. The scientific manuscript is not modified by the packaging step.

## Publication-stage item

A final immutable public code/data archive with persistent DOI is required before final publication, not before the scientific manuscript can be considered complete.
