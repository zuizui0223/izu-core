# Journal of Ecology submission metadata checklist

Updated: 2026-08-25

Scientific status: **Chapter 2 complete and frozen for submission.**

This checklist contains only author/submission metadata. It must not reopen H1–H5, rerun simulations, add external systems, or reconnect external research programmes.

## Already complete

- Research Article title and running title
- numbered abstract under 350 words with final **Synthesis** point
- anonymous main manuscript
- Supporting Information
- Fig. 1–4 and Fig. S1 routing
- Table 1–3 and Table S1–S3 routing
- H2 analytical sign decomposition
- frozen numerical-result guards
- 13-system source and protected-boundary guards
- anonymized reviewer archive builder
- Data/code statement for peer review
- cover-letter scientific content
- CI on Python 3.10, 3.11 and 3.12

## Author-supplied metadata still required

Populate `data/design/island_ecology_submission_metadata_template.json` with the final agreed values below. Do not infer them from Git history, account names, other manuscripts or institutional context.

1. **Final author list and order**
   - full name exactly as it should appear
   - affiliation(s) for each author
   - ORCID for each author if used

2. **Corresponding author**
   - author index
   - institutional email
   - postal address

3. **Authorship and disclosure text**
   - acknowledgements, or explicit `None`
   - funding, or explicit `None`
   - author-contribution statement using full author names
   - inclusion statement required by the submission workflow
   - conflict-of-interest statement

4. **Submission declarations**
   - not published / not under consideration elsewhere
   - all authors approve the submitted version
   - all entitled authors are included
   - necessary acknowledgements are made
   - relevant legal/policy requirements are met
   - third-party data reuse is permitted

## Builder

Run:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

The builder fails closed while any required author metadata is unresolved. Once the metadata is complete it writes:

- `dist/ISLAND_ECOLOGY_TITLE_PAGE.md`
- `dist/ISLAND_ECOLOGY_COVER_LETTER.md`

The anonymous manuscript and reviewer archive remain unchanged.

## Journal-specific boundary

Journal of Ecology uses double-anonymous review. Author-identifying information belongs in the separate title-page file and must not be copied into the main manuscript, Supporting Information or reviewer archive. The title page carries manuscript title, author names and institutional addresses, acknowledgements, author contributions, data availability and conflict-of-interest information. The submission workflow also requests an inclusion statement.
