# Chapter 2 author-metadata handoff

Updated: 2026-09-11

## Current state

The Chapter 2 scientific gate, manuscript routing, renderer/tests and non-metadata submission preflight are closed. Field E3/E4 is optional future validation and is not a completion gate.

The remaining submission blockers are author-supplied metadata and confirmations only. Do not infer or auto-fill these fields from names, affiliations, memory, acknowledgements in other documents or repository history.

## Supply this block once

Copy, fill and return the block below exactly once. Use `None` where the correct explicit answer is none.

```yaml
authors:
  - name: ""
    affiliations:
      - ""
    email: ""
    postal_address: ""
    orcid: ""
    corresponding_author: true
  # add coauthors in final submission order as needed

significance_prior_work_context: ""
acknowledgements: "None"
funding: "None"
inclusion_statement: ""
conflict_of_interest: "None"

ethics_statement_confirmed: false

submission_declarations:
  not_published_or_under_consideration_elsewhere: false
  all_authors_approve_submission: false
  all_entitled_authors_included: false
  necessary_acknowledgements_made: false
  legal_and_policy_requirements_met: false
  third_party_data_reuse_is_permitted: false
```

## Meaning of the confirmations

Set `ethics_statement_confirmed: true` only after an author has checked that the prefilled statement is accurate for this manuscript:

> Not applicable to new data collection in this manuscript. The study reports simulations, a source-audited synthesis of published literature, and secondary analysis of published plant–pollinator data; it includes no new field sampling, specimen collection or experimental work requiring new approvals, licences or permissions.

Set each submission declaration to `true` only when the authors can explicitly confirm it. The bundle builder is intentionally fail-closed and must not treat missing confirmation as implicit approval.

## What happens after this block is supplied

1. Populate `data/design/island_ecology_submission_metadata_template.json` without changing the scientific claim ceiling.
2. Run the metadata validator.
3. Run `python scripts/audit_chapter2_submission_closure.py --check`.
4. Build `dist/chapter2_oikos_submission_bundle.zip`.
5. Verify that `MANUSCRIPT.rtf` remains blinded and that identity-bearing information appears only on the title-page/metadata surfaces.

No new simulation, world-island search, Izu same-block analysis or Chapter 3 result is required before this transition.
