# Chapter 2 NEE author-metadata handoff

Updated: 2026-09-15

## Current state

Chapter 2 science, the frozen NEE route, the post-promotion source-robustness challenge, manuscript v0.4, figures, reference provenance, presubmission bundle tooling and canonical CI are closed on `main`.

The remaining initial-submission work is author-controlled metadata and confirmations only. Do **not** infer final authorship, author order, corresponding-author status, funding, competing interests, related-manuscript disclosures, prior editor discussions or submission approval from repository ownership or earlier drafts.

Current Nature Ecology & Evolution initial-submission guidance requires a manuscript and cover letter. Author names/affiliations belong in the manuscript unless double-anonymized peer review is chosen, in which case author affiliation/contact information is supplied in the cover letter. The cover letter must disclose related manuscripts and prior discussions with a Nature Ecology & Evolution editor. Nature Portfolio also requires competing-interest disclosure during submission. Corresponding-author ORCID linkage is requested before final acceptance rather than being an initial-submission blocker.

Policy sources:
- https://www.nature.com/natecolevol/submission-guidelines/preparing-your-submission
- https://www.nature.com/natecolevol/submission-guidelines/dapr
- https://www.nature.com/natecolevol/submission-guidelines
- https://www.nature.com/nature/editorial-policies/competing-interests

A source-locked record supports one reusable identity candidate in `docs/CHAPTER2_AUTHOR_METADATA_PROVENANCE_20260912.md`: ZHANG RUIQI's name, Kyoto University affiliation, institutional address and institutional email. It does **not** establish final inclusion/order, corresponding-author status or ORCID for this paper.

## Supply this block once

Confirm or edit the block below. Add coauthors in final submission order. Use the literal string `None` where the correct explicit answer is none.

```yaml
peer_review_model: ""  # choose: single-anonymized | double-anonymized

authors:
  - name: "ZHANG RUIQI"  # source-locked identity candidate; confirm inclusion/order
    affiliations:
      - "Division of Forest and Biomaterials Science, Graduate School of Agriculture, Kyoto University, Kitashirakawa Oiwake-cho, Sakyo-ku, Kyoto 606-8502, Japan"
    email: "zhang.ruiqi.77h@st.kyoto-u.ac.jp"
    postal_address: "Kitashirakawa Oiwake-cho, Sakyo-ku, Kyoto 606-8502, Japan"
    corresponding_author: null  # true/false
    orcid: ""  # optional for initial submission; do not infer
  # add coauthors in final submission order as needed

related_manuscripts_under_consideration_or_in_press: ""
prior_discussions_with_nee_editor: ""
acknowledgements: "None"
funding_statement: "None"
competing_interests: ""

ethics_statement_confirmed: false

llm_use_statement: ""
llm_use_statement_confirmed: false

submission_declarations:
  not_published_or_under_consideration_elsewhere_except_disclosed_related_work: false
  all_authors_approve_submission: false
  all_entitled_authors_included: false
  necessary_acknowledgements_made: false
  legal_and_policy_requirements_met: false
  third_party_data_reuse_is_permitted: false
```

## Meaning of the confirmations

`peer_review_model` is an author choice. If `double-anonymized` is selected, identity-bearing author information must be removed from the review manuscript and retained in the cover-letter/submission-system surfaces.

Exactly one author must have `corresponding_author: true`. Do not infer this from first-author position or repository ownership.

For the cover letter:
- set `related_manuscripts_under_consideration_or_in_press` to `None` or describe the related work;
- set `prior_discussions_with_nee_editor` to `None` or identify the editor/discussion.

Set `competing_interests` explicitly. `None` is acceptable only if the authors can truthfully declare no competing interests.

Set `ethics_statement_confirmed: true` only after an author has checked this manuscript-specific statement:

> This manuscript reports simulations, source-audited synthesis of published literature and secondary analysis of public plant–pollinator datasets. It contains no new research involving human participants, live vertebrate animals or newly collected specimens requiring new ethical approval.

Nature Ecology & Evolution states that use of LLMs should be documented in the Methods (or another suitable section). Because this project has used LLM-assisted workflow/writing support, the final wording must be author-reviewed rather than silently omitted. A conservative starting point is:

> OpenAI ChatGPT was used to assist with language editing, code/workflow review and manuscript organization. All scientific decisions, analyses, source verification and final text were reviewed and approved by the authors.

Edit this sentence to match the actual use before setting `llm_use_statement_confirmed: true`.

Set each submission declaration to `true` only after explicit author confirmation. Missing confirmation is not implicit approval.

## What happens after this block is supplied

1. Populate `data/design/chapter2_nee_initial_submission_metadata.json`.
2. Run `python scripts/validate_chapter2_nee_initial_submission_metadata.py`.
3. Insert the confirmed author/affiliation surface according to the chosen peer-review model.
4. Insert the confirmed competing-interest, funding, ethics and LLM-use wording where required.
5. Rebuild `dist/chapter2_nee_presubmission_bundle.zip` and relabel it initial-submission-ready only after the validator passes.

ORCID linkage and a permanent archive DOI remain prepublication tasks; neither is used to block initial editorial submission under the current journal guidance.
