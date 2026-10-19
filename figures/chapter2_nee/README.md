# Chapter 2 — rendered, source-locked scientific figures

Four SVG figures are rendered from existing admitted results. **Figure 1 (Q1) and Figure 3 (event order and repeatability) are not yet rendered.** Four rendered plots are not a complete publication package, and no new ecological simulation was run.

| Main display | Vector figure | Numeric source | Inference status |
| --- | --- | --- | --- |
| Figure 2 | [Baseline pollen regime × further activity decline](figure_02_baseline_pollen.svg) | [384-path audit](../../docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json) | Exploratory, founder bootstrap with 12 founders |
| Figure 4 | [High-I closure and survival](figure_04_access_survival.svg) | [160×160 confirmed contrasts](../../docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json) | Registered, two separate adjusted 97.5% intervals |
| Figure 5 | [Conditional duration of I polymorphism](figure_05_variation_duration.svg) | [Saved-variation readback](../../docs/audits/CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json) | Retrospective readback of *same* 160×160 cohort |
| Figure 6 | [Late bounded environmental transfer](figure_06_late_transfer.svg) | [Conditional transfer tables](../../docs/audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json) | Descriptive, nested 64 cohorts / 32 donors |

Every SVG embeds a JSON metadata element with source identity and numerical values, plus source-value attributes on plotted marks. Run **pytest -q tests/test_chapter2_paper_figures_20261019.py** to compare the figure marks with the maintained numeric-source JSON files. This checks plot/source consistency, not a new independent biological replay. Plots are static editable vector drafts; changing source results must trigger replotting and renewed visual review.

**Interpretation boundaries.** In Figure 2, different baseline effectiveness regimes also create different histories and changes in absolute pollen service. In Figure 4, genetic closure at B8 and the B4.5/B8 survival interaction do not identify genetic mediation. In Figure 5, the longer B4.5 polymorphic duration includes time gained by avoiding extinction. In Figure 6, extinction remains in all-start occupancy denominators, but common-context performance is survivor-conditioned. Neither a population-wide recovery-probability clock, mutation-enabled irreversibility nor empirical island filtering is demonstrated by these figures.

The figure numbers follow the [single working NEE Article](../../docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md). Submission remains pending final figure artwork, full references/Methods, author checks and durable raw-data archiving.
