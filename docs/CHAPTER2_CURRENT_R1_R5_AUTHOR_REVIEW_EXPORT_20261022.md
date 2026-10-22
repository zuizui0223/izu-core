# Chapter 2 current R1–R5 author-review source package (2026-10-22)

**Author-review only; not journal-submission ready, not a DOI deposit.**

The [completed R1–R5 evidence recovery](CHAPTER2_R1_R5_SOURCE_RECOVERY_AUDIT_20261022.md) was merged via [PR #618](https://github.com/zuizui0223/izu-core/pull/618), and the [A direction versus fixation audit](CHAPTER2_A_DIRECTION_VS_FIXATION_EVIDENCE_20261022.md) was merged via [PR #617](https://github.com/zuizui0223/izu-core/pull/617). Those mergers kept original scientific results, canonical Model3 implementation and all six main figures unchanged.

## Reason for this new source package

Historical [PR #615](https://github.com/zuizui0223/izu-core/pull/615) generated a valid author-review ZIP **for an earlier manuscript title and the earlier `figures/chapter2_nee` plot layout**. PR #614 had already updated the active article to the five-result title and `figures/chapter2_nee_five_results`. The old PR #615 package therefore **cannot be presented as the latest manuscript**, even though its then-source hashes verified. This new source-locked export leaves the historical ZIP and PR branch intact and fixes the artifact identity.

The current editing master is:

`docs/CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md`

Title: **Founding constraints and the predictability of reproductive evolution in an island plant model**.

The six numbered main SVGs from `figures/chapter2_nee_five_results` are:

1. Founder-to-future framework (`figure_01_framework.svg`)
2. Investment decline with fixed assurance (`figure_02_independent_decline.svg`)
3. Assurance × investment environment contrast (`figure_03_assurance_interaction.svg`)
4. Endpoint repeatability and predictor skill (`figure_04_predictability.svg`)
5. B8 genetic support and B4.5 population persistence (`figure_05_persistence_options.svg`)
6. Conditional transfer and distinct outcomes (`figure_06_transfer.svg`)

The package also includes the completed-evidence supplement, R1–R5 recovery audit, retained extended evidence, figure map, founder-predictability readout, A direction/fixation audit, original registered G/S compact result, prior-art and coding limitations, and publication-preparation checklist. Every source is recorded by SHA-256 in `MANIFEST.json`, alongside the original Git commit. Relative citation links in the Markdown require the full GitHub repository tree.

## Reproduction and acceptance

```bash
python -m pytest -q tests/test_chapter2_five_result_author_review_20261022.py \
  tests/test_chapter2_r1_r5_source_recovery_20261022.py \
  tests/test_chapter2_paper_figures_20261019.py
python -m scripts.build_chapter2_five_result_author_review_20261022 \
  --root . --source-commit "$(git rev-parse HEAD)" \
  --out outputs/chapter2_r1_r5_author_review/R1_R5_CURRENT_AUTHOR_REVIEW.zip
(cd outputs/chapter2_r1_r5_author_review && sha256sum -c R1_R5_CURRENT_AUTHOR_REVIEW.zip.sha256)
```

The independent Actions job `current-r1-r5-author-review` checks all current numbered figures, all source manifest members, registered G/S endpoints, and the absence of old title or unexecuted Results. It uploads `chapter2-r1-r5-author-review-<run ID>` only upon success; the job never runs a biological population update. Original source assets are read and copied verbatim, never overwritten.

## Scientific and submission limits

The included G (+8.328125 percentage points) and S (+92.70703125 pp) remain **separate preregistered comparisons**. R1 independent founder fixed-A readback, R2 interaction qualification, R3 retrospective repeatability and prediction, R4 post-outcome joint-state analysis and R5 transfer/pedigree evidence retain their original evidence levels. These experiments are not jointly one natural island colonization lineage, and do not identify causal genetic mediation, permanent ancestral irreversibility, speciation rates, or a general mainland recolonization advantage.

The main figures remain **draft** vector artwork. Final print-size checks, complete Methods/SI, author declarations, journal-specific references and external source archive/DOI readback still require confirmation. No submissions or deposits have been made by this package.
