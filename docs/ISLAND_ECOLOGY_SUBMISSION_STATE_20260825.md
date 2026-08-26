# Island ecology submission state

Updated: 2026-08-26

## Current state

The Chapter 2 science is **complete and frozen for submission**.

No new simulation, field dataset, external-system search, parameter retuning, or external research programme is required for the manuscript.

The reviewer-facing manuscript is now **editorial V3**, generated deterministically from the frozen V2 manuscript source by `scripts/build_island_ecology_manuscript_v3.py`. V3 sharpens the Introduction gap and integrates the already-frozen H2 analytical sign decomposition into the Abstract, Methods, Results, Discussion and Conclusion. This editorial rendering does not rerun or alter the scientific analysis.

The V3 submission route has passed repository CI on Python 3.10, 3.11 and 3.12. The Supporting Information, H2 analytical sign decomposition, figure/table routing, source-audited external-system matrix, claim-boundary tests, anonymous review archive and final submission bundle routing are complete.

## Manuscript routing

- reviewer-facing artifact: `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md`;
- frozen source: `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`;
- deterministic builder: `scripts/build_island_ecology_manuscript_v3.py`.

The V3 artifact is materialized by the manuscript/review/bundle builders; the V2 source remains the committed prose provenance boundary.

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

The bundle contains editorial V3, the final title page and cover letter outside a nested **anonymous** review archive. Packaging materializes the validated editorial prose but does not rerun or modify the scientific analysis.

## Publication-stage item

A final immutable public code/data archive with persistent DOI is required before final publication, not before the scientific manuscript can be considered complete.
