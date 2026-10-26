# NEE Article source-locked formatting preview (2026-10-23)

> **2026-10-26 current-form update:** This document records the October 23 renderer handoff. Merged [PR #643](https://github.com/zuizui0223/izu-core/pull/643) changed the current R1–R5 Article's title to **“Recurrent reproductive assurance and contingent floral evolution in an island plant model,”** and its 182-word abstract and A/M/I prose were source-checked. The [current formatter](../scripts/format_chapter2_nee_article_20261023.py) still strips seven source-only Discussion headings and the Introduction heading while preserving all prose. On the merged source, the editing master has **3,411 whitespace-delimited body words including editorial navigation headings**; the expected journal-formatted body has **3,351**. Older counts/phrasing below are dated snapshots, not a second active journal draft. External DOI, approved bibliography and final layout remain open.

**Status: technical author-review preview only. Not journal-approved, not an actual submission, and not a deposited DOI.** This is a formatting derivative of the single [completed-evidence Article master](CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md) as merged through [PR #622](https://github.com/zuizui0223/izu-core/pull/622). The master stays canonical and the source-registered G/S, exploratory joint-access and original figure values are unchanged.

## Official Article requirements verified

[NEE Content Types — Article](https://www.nature.com/natecolevol/content), checked 2026-10-23:

- Main text up to **3,500 words** excluding abstract/Methods/references/figure legends.
- Unreferenced abstract up to **200 words**.
- Up to **6** main figures/tables and up to 10 Extended Data items.
- **Introduction without heading** (approximately 500 referenced words).
- **Results and Online Methods use topical subheadings; Discussion must have no subheadings**.
- References guideline around 50, not a scientific reference-validation result.
- Article content-type page does **not** specify the 10-word title limit found under the separate Brief Communication category.

The current scientific master has a 182-word abstract, approximately 503-word Introduction, five R1–R5 Results and six main figure legends; the source master retained seven Discussion **editorial navigation** subheadings and an explicit Introduction heading, both unsuitable for a direct Article upload. Its bibliography remains labelled **preliminary**. Neither a passing word-count test nor this derivative means the paper is scientifically accepted or ready to submit.

## Exact production and falsifiable conditions

Read-only [rendering script](../scripts/format_chapter2_nee_article_20261023.py) creates `NEE_ARTICLE_AUTHOR_PREVIEW.md` and a source-commit/SHA-256 `FORMAT_PROOF.json`:

```bash
python -m pytest -q tests/test_chapter2_nee_article_format_20261023.py
python -m scripts.format_chapter2_nee_article_20261023 \
  --root . --source-commit "$(git rev-parse HEAD)" \
  --out outputs/chapter2_nee_format/NEE_ARTICLE_AUTHOR_PREVIEW.md \
  --report outputs/chapter2_nee_format/FORMAT_PROOF.json
```

Allowed transformations are deliberately limited to (1) removing the original **internal editorial title-page note**, (2) removing the Introduction label only, (3) removing seven Discussion navigation subheadings **while keeping the paragraphs in their exact original order**, and (4) normalizing three section headings to **Online Methods**, **Figure legends**, and **References**. The source Results and all numerical statements are byte-preserved. Original source-link paths remain relative to the full GitHub tree; the Markdown derivative is **not itself a link-complete journal manuscript package**.

The source-formatted preview is admitted only when the original title, five Results, explicit post-outcome/registered claim distinction, six numbered figure legends, no invented published DOI, original source-hashed manuscript and numerical figure roster all pass. No new model runs, effect estimates, p-values or inferential populations are created.

## Scientific framing for NEE

The registered primary claims remain **two**: G (founder-relative high-I support closure at B8, +8.328125 percentage points; source-conditional adjusted marginal 97.5% interval +6.693910 to +9.962340) and S (policy×budget survival interaction, +92.707031 pp; corresponding interval +92.049592 to +93.364471). The more ecologically nontrivial **resource-dependent net alive-and-accessible contrast** is **post-outcome**: −8.328125 pp under B8 and +35.56640625 pp under B4.5, between-budget difference +43.89453125 pp, read out from the original source-sealed 160×160 policy contrasts. Crossed-axis sensitivity intervals from [PR #622 original-summary readback](CHAPTER2_CROSSED_ACCESS_SIGN_REVERSAL_20261023.md) are conditional descriptions **not registered confirmation**.

Do not write that (i) A measures the observed selfing rate, (ii) founder identity causally predicts every floral change, (iii) 25,600 crossed cells are independent natural islands, (iv) all I prediction residual is genetic drift, (v) retention of a founder-target allele proves future adaptation or ancestral floral restoration, (vi) two resource budgets establish a unique universal tipping point, or (vii) the current raw archives have a published external DOI.

## Explicit external/author submission blockers

- Full bibliography has not been independently checked citation-by-citation and harmonized to NEE final style.
- Ordered authors, author contributions, competing interests, ethics/permits if applicable, funding, software/data licences and all-author approval are not declared.
- [R1–R5 data/code handoff](deposit/CHAPTER2_FIVE_RESULTS_DOI_HANDOFF_20261021.md) and [Issue #621](https://github.com/zuizui0223/izu-core/issues/621) still require complete authorized external raw-source deposition with DOI and independent readback. An internal GitHub review ZIP is **not** a published DOI dataset.
- Current SVG figure source checks do not replace author review of journal-size text and all source files to submit.
- No formal NEE submission/presubmission enquiry has been performed or scheduled by this formatting operation.

**Decision:** prepare a source-locked manuscript *layout* now without weakening scientific source fidelity; do not silently relabel an author-review artifact as a ready-to-submit or published Article.
