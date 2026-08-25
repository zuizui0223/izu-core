# Title page template — Journal of Ecology

## Current status

The scientific manuscript is complete. This file is a human-readable title-page template only.

Final author-identifying values must be supplied explicitly in:

`data/design/island_ecology_submission_metadata_template.json`

Then generate the final title page with:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Do **not** infer author names/order, affiliations, email addresses, ORCIDs, acknowledgements, funding, contributions or declarations from Git history, account names, other manuscripts or institutional context.

## Title

**One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification**

## Authors

`[AUTHOR 1 FULL NAME]`  
`[AUTHOR 2 FULL NAME, if applicable]`  
`[additional authors in agreed order]`

## Affiliations

1. `[AFFILIATION 1: department/institute, university/organization, city, country]`
2. `[AFFILIATION 2, if applicable]`

Use numbered author–affiliation links in the formatted submission file.

## Corresponding author

`[FULL NAME]`  
`[institutional email]`  
`[postal address]`

## ORCID

- `[AUTHOR]: [ORCID, if supplied]`

## Running title

**State-dependent island pollination responses**

## Article type

Research Article

## Keywords

agent-based model; ecological networks; functional traits; island biogeography; plant–pollinator interactions; reproductive assurance; resilience; response heterogeneity

## Author contributions

`[explicit author-supplied contribution statement using full names]`

## Inclusion statement

`[explicit author-supplied statement for the Journal of Ecology submission workflow]`

## Conflict of interest

`[explicit declaration]`

## Acknowledgements

`[funding, field/logistical support and non-author contributions, or explicit None]`

## Funding

`[funding statement, or explicit None]`

## Data availability

Use the submission-stage statement in `data/design/island_ecology_submission_metadata_template.json`. Replace it with the immutable archive DOI before final publication.

## Anonymous-review rule

This title page is a **separate submission file** and must not be appended to the double-anonymous review manuscript. The reviewer-facing manuscript and review archive must omit author names, affiliations, email addresses, acknowledgements and author-identifying public repository links.
