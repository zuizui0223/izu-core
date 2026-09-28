# Chapter 2 NEE initial-submission checklist

Updated: 2026-09-15

Status: **AUTHOR-CONTROLLED FIELDS PENDING**

This checklist separates information required for the initial editorial submission from items that can remain pending until later publication stages. It does not freeze authorship, author order, corresponding-author status, funding, competing interests or declarations.

Current journal sources:

- Nature Ecology & Evolution submission guidelines: https://www.nature.com/natecolevol/submission-guidelines
- Preparing your material: https://www.nature.com/natecolevol/submission-guidelines/preparing-your-submission
- Article format: https://www.nature.com/natecolevol/content

## Initial-submission blockers

1. **Final author list and order**
   - Supply every author exactly as they should appear.
   - Confirm that every listed author approves the list and order and knows the manuscript is being submitted.

2. **Affiliation for every author**
   - Nature Ecology & Evolution requires names and affiliations of all co-authors in the manuscript unless double-anonymized review is chosen, in which case author identity/contact information belongs in the cover letter.
   - For ZHANG RUIQI only, the repository already has externally supported reusable identity fields, but they may be prefilled only if ZHANG RUIQI is confirmed as an author:
     - Division of Forest and Biomaterials Science, Graduate School of Agriculture, Kyoto University, Kitashirakawa Oiwake-cho, Sakyo-ku, Kyoto 606-8502, Japan.
     - institutional email: zhang.ruiqi.77h@st.kyoto-u.ac.jp
   - Source: `docs/CHAPTER2_AUTHOR_METADATA_PROVENANCE_20260912.md`.

3. **Corresponding-author designation and contact**
   - Identify the corresponding author(s) and the email to be used for editorial correspondence.
   - Do not infer this from first-author position or repository ownership.

4. **Author contributions**
   - Provide a contribution statement for each author. Do not infer CRediT roles from commits or conversation history.

5. **Competing interests**
   - Provide the statement required for submission, including an explicit declaration if there are no competing interests.

6. **Funding and acknowledgements**
   - Declare funding if the work falls within the scope of a grant.
   - Add acknowledgements only after authors confirm them.

7. **Cover-letter declarations**
   - Related manuscripts by any author that are under consideration or in press elsewhere: confirm `none` or list them.
   - Prior discussions with a Nature Ecology & Evolution editor about this work: confirm `none` or describe them.
   - Reviewer suggestions/exclusions are optional.

8. **Peer-review identity mode**
   - Confirm standard or double-anonymized peer review before generating the final upload files, because this changes where author identities and affiliations appear.

## Not initial-submission blockers under the current guidance

- Corresponding-author ORCID linkage: requested before final acceptance, not required to start editorial submission.
- Permanent archived code/data release DOI: retain as a prepublication task; the repository-only code-availability wording must be replaced before publication.

## Already technically closed

- Active target: Nature Ecology & Evolution Article.
- Abstract <= 200 words: guarded by pytest.
- Main text <= 3,500 words excluding Abstract, Methods, references and figure legends: guarded by pytest.
- Four main display items: guarded by pytest.
- Results/Methods topical subheadings and Discussion without subheadings: guarded by pytest.
- Natural `D1` versus synthetic `k`/`k_eff` distinction is stated in Methods before the natural-coordinate formula.
- Source-complementarity is disclosed: England is load-bearing for sampled synchrony dispersion and Martinique for joint-interior occupancy.
- A prospectively frozen four-candidate source-robustness challenge closed without opening any new natural coordinates or adding a source.
- Candidate hunting is closed.
- **AI/LLM-use disclosure is present in Methods.** It identifies OpenAI ChatGPT as an assistive tool for code drafting/review, workflow and source-provenance organization, and language editing; states that LLM output was not treated as empirical evidence or source authority; retains human responsibility for design, analysis, interpretation and the final manuscript; and does not list an LLM as an author.

## Minimal author reply needed to unlock finalization

Provide these fields in one message when ready:

```text
Authors in final order:
1. FULL NAME — affiliation
2. FULL NAME — affiliation
...

Corresponding author(s):
Email(s):

All authors approve list/order/submission: yes / no

Author contributions:
- Author 1: ...
- Author 2: ...

Competing interests: none / [statement]
Funding: none / [statement]
Acknowledgements: none / [statement]
Related manuscripts under consideration/in press: none / [details]
Prior discussion with NEE editor: none / [details]
Peer-review mode: standard / double-anonymized
```

ORCID(s) can be supplied now if convenient but need not block initial submission.
