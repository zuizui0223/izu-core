# Chapter 2 Oikos author-metadata handoff — 2026-09-12

Status: **scientific and non-identity submission gates are closed; this form contains the remaining author-supplied inputs only.**

Use this form once. The completed answers can be copied directly into `data/design/island_ecology_submission_metadata_template.json` and then validated with `scripts/build_island_ecology_submission_metadata.py`.

Do not put these identity-bearing fields into the anonymous manuscript or anonymous reviewer archive.

## 1. Final ordered author list

For each author, provide:

```text
Author 1
full_name:
affiliations:
- affiliation 1
- affiliation 2 (if any)
orcid: optional unless corresponding author

Author 2
full_name:
affiliations:
- affiliation 1
orcid: optional
```

The order entered here is the final submission order.

## 2. Corresponding author

```text
corresponding_author_number: 1-based number from the ordered list above
email:
postal_address:
orcid: mandatory for Oikos submission
```

## 3. Relation to previous work / significance context

Supply a short explicit statement describing how this manuscript builds on:

- relevant prior work by any submitting author/coauthor that is cited in the manuscript; and
- relevant published work by the wider field.

Do not infer this from names or citation lists after the fact.

```text
significance_prior_work_context:
```

## 4. Acknowledgements

Enter final text, or exactly `None`.

```text
acknowledgements:
```

## 5. Funding

Enter final text, or exactly `None`.

```text
funding:
```

## 6. Inclusion / EDI statement

Enter the final explicit statement required for the active Oikos submission metadata.

```text
inclusion_statement:
```

## 7. Conflict of interest

Enter the final explicit statement, including an explicit no-conflict statement if applicable.

```text
conflict_of_interest:
```

## 8. Ethics statement confirmation

Current prefilled statement:

> Not applicable to new data collection in this manuscript. The study reports simulations, a source-audited synthesis of published literature, and secondary analysis of published plant–pollinator data; it includes no new field sampling, specimen collection or experimental work requiring new approvals, licences or permissions.

After author review, answer only:

```text
ethics_statement_confirmed: true / false
```

If `false`, provide corrected wording instead of changing the flag to true.

## 9. Submission declarations

Each item must be explicitly confirmed `true` by the authors; none may be inferred.

```text
not_published_or_under_consideration_elsewhere: true / false
all_authors_approve_submission: true / false
all_entitled_authors_included: true / false
necessary_acknowledgements_made: true / false
legal_and_policy_requirements_met: true / false
third_party_data_reuse_is_permitted: true / false
```

## Optional at initial submission

These are not current blockers:

```text
coauthor_orcids:
author_contributions_credit_roles:
```

## What happens after this form is completed

1. Populate `data/design/island_ecology_submission_metadata_template.json` exactly from author-supplied answers.
2. Run metadata validation.
3. Generate title page, cover letter, significance statement and submission statements.
4. Run the submission-closure audit.
5. Build the final submission bundle while preserving the double-anonymous boundary.

No new simulation, empirical expansion, NEE field work or Ecology Letters theory work is required to complete the current Oikos submission.
